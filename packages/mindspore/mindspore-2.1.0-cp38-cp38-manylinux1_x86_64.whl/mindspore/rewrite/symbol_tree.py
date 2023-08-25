# Copyright 2022 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""SymbolTree class define of Rewrite according to forward function of a network."""
import stat
from typing import Optional, Union, Tuple, Any
import os
import sys
import ast
import importlib.util
import types
import time
import astunparse

from mindspore.nn import Cell
from mindspore import log as logger
from mindspore.rewrite.ast_creator_register import ast_creator_registry
from .node import Node, TreeNode
from .api.node_type import NodeType
from .ast_helpers import AstModifier, AstReplacer, StrChecker, AstFinder, CheckPropertyIsUsed
from .api.scoped_value import ScopedValue, ValueType
from .symbol_tree_dumper import SymbolTreeDumper
from .topological_manager import TopoManager
from .namer import TargetNamer, NodeNamer, ClassNamer
from .common.observer import Observer
from .common.observable import Observable
from .common.event import Event


class Position:
    """
    Position indicates a source code position in one network.

    Rewrite recommend using class method `create()` of position rather than constructor of Position.

    Args:
        symbol_tree (SymbolTree): A handler of SymbolTree indicated position in which SymbolTree.
        node (Node): A handler of Node indicated position is around which Node.
        before_node (bool): A bool indicated position is before or after the 'node'.
    """

    def __init__(self, symbol_tree, node, before_node: bool):
        self.symbol_tree = symbol_tree
        self.node = node
        self.before_node = before_node

    @classmethod
    def create(cls, symbol_tree, node, before_node):
        """
        Class method of Position. Return None when symbol_tree or node is None.

        Args:
            symbol_tree: A handler of SymbolTree indicated position in which SymbolTree.
            node: A handler of Node indicated position is around which Node.
            before_node (bool): A bool indicated position is before or after the 'node'.

        Returns:
            A Position.
        """
        if symbol_tree is None or node is None:
            return None
        return Position(symbol_tree, node, before_node)


class FieldFinder(AstFinder):
    """
    Check whether field exist in specific scope.

    Args:
        scope (ast.AST): An instance of ast node as search scope.
    """
    def __init__(self, scope: ast.AST):
        super().__init__(scope)
        self._result = False
        self._field_name = ""

    def visit_Attribute(self, node: ast.Attribute) -> Any:
        """Visit a node of type ast.Attribute."""
        value = node.value
        if not isinstance(value, ast.Name):
            return super(FieldFinder, self).generic_visit(node)
        if value.id != "self":
            return super(FieldFinder, self).generic_visit(node)
        if node.attr == self._field_name:
            self._result = True
        return super(FieldFinder, self).generic_visit(node)

    def check(self, field) -> bool:
        """
        Check whether `field` exist in scope.

        Args:
            field (str): A string indicates target field name.

        Returns:
            A bool indicate whether `field` exist in scope.
        """
        self._result = False
        self._field_name = field
        self.visit(self._scope)
        return self._result


class IfFixer(ast.NodeTransformer):
    """
    Fix ast.If if body is empty while orelse is not empty.
    """

    def visit_If(self, node: ast.If) -> Any:
        """Visit a node of type ast.If."""
        if not node.body and node.orelse:
            node.body.append(ast.Pass())
        return super().generic_visit(node)

    def fix(self, node):
        """
        Fix ast.If node in `node` if whose body is empty while whose orelse is not empty.

        Args:
            node (ast.AST): An ast node to be fixed.
        """
        self.generic_visit(node)


class SymbolTree(Observer, Observable):
    """
    A symbol-tree usually corresponding to forward method of a network.

    Rewrite recommend using SymbolTreeBuilder to instantiate an instance of SymbolTree rather than invoking constructor
    of SymbolTree directly.

    Args:
        origin_network (Cell): A handler to original network instance.
        module_ast (ast.Module): An instance of ast.AST represents ast node of original network.
    """

    def __init__(self, origin_network: Cell, module_ast: ast.Module):
        super().__init__()
        Observable.__init__(self)
        origin_network_key = "handler"
        # init unique-namers
        self._target_namer = TargetNamer()
        self._node_name_namer = NodeNamer()
        # name or node would use as name of field, so name of origin network handler field should be added into \
        # _node_name_namer.
        self._node_name_namer.add_name(origin_network_key)
        self._topo_mgr = TopoManager(self)
        self._topo_mgr.reg_observer(self)

        self._nodes: {str, Node} = {}
        # parameters of forward method
        self._inputs: [Node] = []
        self._ori_cls_name = type(origin_network).__name__
        self._opt_cls_name = ClassNamer.instance().get_name(self._ori_cls_name)
        self._origin_network = origin_network
        self._module_ast: ast.Module = module_ast
        self._class_ast: Optional[ast.ClassDef] = None
        self._root_ast: Optional[ast.FunctionDef] = None
        self._init_func_ast: Optional[ast.FunctionDef] = None
        self._deleted_field = {}
        self._deleted_node = []
        self._external_func_ast = []
        self._father_class_ast = []

        # head node is always point to the first node(in source code order) of SymbolTree
        self._head = None
        # tail node is always point to the last node(in source code order) of SymbolTree
        self._tail = None
        self._return: Optional[Node] = None

        self._modified = False
        self._node_visitor = None

        self._tmp_file_limits = 20
        self._tmp_files = []
        self._saved_file_name = "./network_define.py"
        # used to insert "sys.path.append(xxx)"
        self._net_file_paths = []

    def __del__(self):
        for tmp_file in self._tmp_files:
            tmp_file.close()

    @staticmethod
    def _find_consumers_and_providers(nodes: [Node]):
        """
        Find consumers and providers for all nodes according to their targets and arguments.
        """
        consumers: {ScopedValue: [Node]} = {}
        providers: {ScopedValue: Node} = {}
        for node in nodes:
            for arg in node.get_args():
                if consumers.get(arg):
                    consumers[arg].append(node)
                else:
                    consumers[arg] = [node]
            for _, arg in node.get_kwargs():
                if consumers.get(arg):
                    consumers[arg].append(node)
                else:
                    consumers[arg] = [node]
            for target in node.get_targets():
                if providers.get(target) is not None:
                    raise RuntimeError(f"Target({target}) of node duplicated")
                providers[target] = node
        return consumers, providers

    @staticmethod
    def _find_all_class_in_symboltree(stree: 'SymbolTree', seen_class: {type, str}, allow_class_name: [], replacers):
        """Find all non-duplicated class name of SymbolTree recursively."""
        replacer = AstReplacer(stree.get_class_ast())
        replacers.append(replacer)
        for node in stree.nodes():
            if not isinstance(node, TreeNode):
                continue
            if node.symbol_tree.get_class_ast() is None:
                continue
            sub_stree: SymbolTree = node.symbol_tree
            SymbolTree._find_all_class_in_symboltree(sub_stree, seen_class, allow_class_name, replacers)
            # all modified ast.ClassDef should export to code
            if sub_stree._modified:
                allow_class_name.append(sub_stree._class_ast.name)
                continue
            # all un-modified ast.ClassDef only keep one instance
            seen_cls_name = seen_class.get(type(sub_stree.get_origin_network()))
            if seen_cls_name is not None:
                replacer.replace_all(sub_stree._class_ast.name, seen_cls_name)
            else:
                seen_class[type(sub_stree.get_origin_network())] = sub_stree.get_class_ast().name
                allow_class_name.append(sub_stree.get_class_ast().name)

    def finish_build(self):
        """Add Event.TopologicalChangeEvent event when build is finished."""
        self.add_event(Event.TopologicalChangeEvent)

    def create_assign_node(self, targets, func_name, args, kwargs):
        """
        Create a ast.Assign type node.

        Args:
            targets (list): _description_
            func_name (_type_): _description_
            args (_type_): _description_
            kwargs (_type_): _description_

        Returns:
            _type_: _description_
        """
        # create targets
        ast_targets = [ast_creator_registry.get("Name")(targets)]
        # create call
        ast_func = ast_creator_registry.get("Attribute")(func_name)
        ast_args = ast_creator_registry.get("Args")(args)
        ast_kwargs = ast_creator_registry.get("KwArgs")(kwargs) if kwargs else []
        ast_value = ast_creator_registry.get("Call")(func=ast_func, args=ast_args, keywords=ast_kwargs)
        # create assign
        ast_node = ast_creator_registry.get("Assign")(targets=ast_targets, value=ast_value)
        return ast_node

    def inner_create_call_function(self, node_name, ast_node, func_name, func, targets, args, kwargs):
        '''
        Instantiate an instance of node whose type is `CallFunction`.

        Args:
            node_name (str): Name of node.
            func_name (str): Name of function.
            ast_node ([ast.AST, optional]): An instance of ast.AST represents corresponding node in ast.
            targets (list[ScopedValue]): A list of instance of `ScopedValue`. See detail in docstring of Node class.
            func ([ScopedValue, optional]): An instance of `ScopedValue`. See detail in docstring of Node class.
            args (list[ScopedValue]): A list of instance of `ScopedValue`. See detail in docstring of Node class.
            kwargs (dict{str: ScopedValue}): A list of instance of `ScopedValue`. See detail in docstring of `Node`
                class.
        '''
        logger.info(f"func name: {func_name}; func: {func}; targets: {targets}; args: {args}; kwargs: {kwargs}")
        node = Node(NodeType.CallFunction, ast_node, targets, func_name, args, kwargs, node_name, func)
        node.set_belong_symbol_tree(self)
        return node

    def get_ori_cls_name(self) -> str:
        """
        Get class name of original network.

        Returns:
            A str represents class name of original network.
        """
        return self._ori_cls_name

    def get_opt_cls_name(self) -> str:
        """
        Get class name of rewritten network.

        Returns:
            A str represents class name of rewritten network.
        """
        return self._opt_cls_name

    def get_module_ast(self):
        """
        Getter of `_module_ast`.

        Returns:
            An instance of ast.AST represents ast node of corresponding module.
        """
        return self._module_ast

    def set_module_ast(self, ast_node: ast.Module):
        """
        Setter of _module_ast.

        Args:
            ast_node (ast.Module): An instance of ast.Module represents ast node of module of corresponding network
                                   class.
        """
        self._module_ast = ast_node

    def get_ast_root(self):
        """
        Getter of `_root_ast`.

        Returns:
            An instance of ast.AST represents ast node of corresponding forward method.
        """
        return self._root_ast

    def set_ast_root(self, ast_node: ast.FunctionDef):
        """
        Setter of _root_ast.

        Args:
            ast_node (ast.FunctionDef): An instance of ast.FunctionDef represents ast node of forward method of
                                        corresponding network class.
        """
        self._root_ast = ast_node

    def get_class_ast(self):
        """
        Getter of `_class_ast`.

        Returns:
            An instance of ast.ClassDef represents ast node of corresponding network class.
        """
        return self._class_ast

    def set_class_ast(self, ast_node: ast.ClassDef):
        """
        Setter of `_init_func_ast`.

        Args:
            ast_node (ast.ClassDef): An instance of ast.ClassDef represents ast node of corresponding network class.
        """
        self._class_ast = ast_node

    def get_init_func_ast(self):
        """
        Getter of _init_func_ast.

        Returns:
            An instance of ast.FunctionDef represents ast node of init method of corresponding network class.
        """
        return self._init_func_ast

    def set_init_func_ast(self, ast_node: ast.FunctionDef):
        """
        Setter of _init_func_ast.

        Args:
            ast_node (ast.FunctionDef): An instance of ast.FunctionDef represents ast node of init method of
                                        corresponding network class.
        """
        self._init_func_ast = ast_node

    def get_inputs(self):
        return self._inputs

    def get_head_node(self):
        """
        Getter of `_head` which represents the beginning node while iterating SymbolTree nodes.

        Returns:
            An instance of node.
        """
        return self._head

    def get_origin_network(self):
        """
        Getter of `_origin_network`.

        Returns:
            An instance of Cell which represents original network.
        """
        return self._origin_network

    def get_nodes_dict(self):
        """Get dict of nodes"""
        return self._nodes

    def get_father_class_ast(self):
        """Get _father_class_ast"""
        return self._father_class_ast

    def append_net_file_path(self, file_path):
        """Append a file_path into _net_file_paths"""
        if file_path not in self._net_file_paths:
            self._net_file_paths.append(file_path)

    def get_net_file_path(self):
        """Get _net_file_paths"""
        return self._net_file_paths

    def nodes(self):
        """
        Get generator of nodes of current `SymbolTree`.

        Returns:
            A generator for iterating Nodes of `SymbolTree`.
        """
        # Put nodes in the list to avoid iteration stops caused by node topology being modified
        nodes = []
        node = self._head
        while node is not None:
            nodes.append(node)
            node = node.get_next()
        return iter(nodes)

    def get_node(self, node_name: str) -> Optional[Node]:
        """
        Get node of current symbol_tree by `node_name`.

        Args:
            node_name (str): A str represents name of node as key of query.

        Returns:
            An instance of Node if found else None.
        """

        return self._nodes.get(node_name)

    def get_node_inputs(self, node_or_name: Union[Node, str]) -> [Node]:
        """
        Getter of inputs in topological relation of current 'node_or_name'.

        Args:
            node_or_name (Union[Node, str]): An instance of node or a str represents name of node.

        Returns:
            A list of instances of Node as input nodes if 'node_or_name' belong to current SymbolTree. An empty list if
            'node_or_name' not belong to current SymbolTree.
        """

        real_node: Optional[Node] = self._get_real_node(node_or_name)
        if real_node is None:
            logger.info("Node(%s) is not belong to current SymbolTree", node_or_name)
            return []
        return node_or_name.get_inputs()

    def get_node_users(self, node_or_name: Union[Node, str]) -> [Tuple[Node, int]]:
        """
        Getter of outputs in topological relation of current 'node_or_name'.

        Args:
            node_or_name (Union[Node, str]): An instance of node or a str represents name of node.

        Returns:
            A list of instances of Node as output nodes if 'node_or_name' belong to current SymbolTree. An empty list if
            'node_or_name' not belong to current SymbolTree.
        """

        real_node: Optional[Node] = self._get_real_node(node_or_name)
        if real_node is None:
            logger.info("Node(%s) is not belong to current SymbolTree", node_or_name)
            return []
        if real_node.get_node_type() == NodeType.Output:
            return []
        return TopoManager.get_node_users(real_node)

    def before(self, node_or_name: Union[Node, str]) -> Position:
        """
        Get insert position before 'node_or_name' in source code list.
        Consider using symbol_tree, node and before/after as position for sub-tree feature.

        Note:
            Topological order is not determined here which is determined by arguments of node and updated by
            TopologicalManager automatically.

        Args:
            node_or_name (Union[Node, str]): An instance of node or a str represents name of node.

        Returns:
            A Position represents an insert point.

        Raises:
            AssertError: If 'node_or_name' is not a Node or a str
            RuntimeError: If 'node_or_name' is not belong to this SymbolTree or any sub-SymbolTree of current
                SymbolTree.
        """

        node = self._get_real_node(node_or_name)
        if node is None:
            raise RuntimeError("Node is not belong to current SymbolTree: ", node_or_name)
        return Position.create(node.get_belong_symbol_tree(), node, True)

    def after(self, node_or_name: Union[Node, str]) -> Position:
        """
        Get insert position after 'node_or_name' in source code list.
        Consider using symbol_tree, node and before/after as position for sub-tree feature.

        Note:
            Topological order is not determined here which is determined by arguments of node and updated by
            TopologicalManager automatically.

        Args:
            node_or_name (Union[Node, str]): An instance of node or a str represents name of node.

        Returns:
            A Position represents an insert point.

        Raises:
            AssertError: If 'node_or_name' is not a Node or a str
            RuntimeError: If 'node_or_name' is not belong to this SymbolTree or any sub-SymbolTree of current
                SymbolTree.
        """
        node = self._get_real_node(node_or_name)
        if node is None:
            raise RuntimeError("Node is not belong to current SymbolTree: ", node_or_name)
        return Position.create(node.get_belong_symbol_tree(), node, False)

    def insert_node(self, position: Optional[Position], node: Node, insert_to_ast: bool = True) -> Node:
        """
        Insert a node into SymbolTree.
        Note:
            Name of node will be unique while inserting node into SymbolTree.

            ValueType.CustomObjValue type arguments will be converted to ValueType.NamingValue and custom object will
            be saved in global_vars dict while inserting node into SymbolTree.

            Targets of node will be unique while inserting node into SymbolTree.

            A field instantiation statement will be added into "init" function of network class using node name as field
            name when `insert_to_ast` is True while inserting node into SymbolTree.

            An assign statement represents invoking to this node will be added into forward function of network class
            corresponding to field-instantiation-statement when `insert_to_ast` is True while inserting node into
            SymbolTree.

            Topological relation is updated and inputs of corresponding node is updated.

        Args:
            position (Position): A Position indicates an insert position point.
            node (Node): An instance of node to be inserted in.
            insert_to_ast (bool): A bool indicates whether to update corresponding ast node at same time, default is
                True.

        Returns:
            An instance of node which has been inserted into SymbolTree.

        Raises:
            ValueError: Node in the SymbolTree is inserted into SymbolTree again.
            RuntimeError: If 'position' is not in current SymbolTree.
            RuntimeError: If corresponding ast node is not an ast.Assign when 'insert_to_ast' is True.
        """
        if node in self.nodes():
            raise ValueError(f"Node in the SymbolTree cannot be inserted into SymbolTree again: {node.get_name()}")
        if position is not None and hasattr(position.node, "container"):
            cellcontainer = getattr(position.node, "container")
            index = cellcontainer.node_list.index(position.node)
            index = index if position.before_node else index + 1
            cellcontainer.insert(index, node)
            return node
        # if position in current SymbolTree
        if position is not None and position.symbol_tree is not self:
            raise RuntimeError("Position is not in current SymbolTree:", position)
        if position is not None and position.node.get_node_type() == NodeType.Input:
            valid = True
            if position.before_node:
                valid = False
            if position.node.get_next() is not None and position.node.get_next().get_node_type() == NodeType.Input:
                valid = False
            if not valid:
                raise RuntimeError("Can not insert a node before or between parameters:", position)
        # unique node name while insert node into symbol_tree
        node_name = self._node_name_namer.get_name(node)
        node.set_name(node_name)
        # save target name, which is used to provide unique target
        if node.get_targets():
            for target in node.get_targets():
                self._target_namer.add_name(str(target))
        self._handle_custom_obj_in_normalized_args(node)
        self._insert_node(position, node)
        if isinstance(node, TreeNode):
            node.symbol_tree.reg_observer(self)
        if self._node_visitor:
            self._node_visitor.append_node(node)
        # update init-function-ast and construct-function-ast
        if insert_to_ast:
            self._insert_to_ast_while_insert_node(node, position)
        return node

    def append_node(self, node: Node, append_to_ast: bool = True) -> Node:
        """
        Append a node to SymbolTree.

        Args:
            node (Node): An instance of node to be appended.
            append_to_ast (bool): A bool indicates whether to update corresponding ast node at same time, default is
                True.

        Returns:
            An instance of node which has been appended to SymbolTree.
        """
        return self.insert_node(Position.create(self, self._tail, False), node, append_to_ast)

    def append_origin_field(self, node: Node) -> Node:
        """
        Append an original field node to SymbolTree. An original field node represents a node created from existing
        statement in forward method, from existing ast node in ast of forward method, so ast node do not need to update
        while these nodes appending to SymbolTree.
        This method is called while building SymbolTree usually.

        Args:
            node (Node): An instance of node to be appended.

        Returns:
            An instance of node which has been appended to SymbolTree.
        """
        if node.get_node_type() == NodeType.Output:
            self._return = node
        elif node.get_node_type() == NodeType.Input:
            self._inputs.append(node)
        elif node.get_node_type() == NodeType.Tree:
            # add father_class_ast into main tree, used when get_code
            for father_ast in node.symbol_tree.get_father_class_ast():
                if father_ast not in self._father_class_ast:
                    self._father_class_ast.append(father_ast)
            # add subtree's net path into main tree
            for file_path in node.symbol_tree.get_net_file_path():
                if file_path not in self._net_file_paths:
                    self.append_net_file_path(file_path)
        return self.append_node(node, False)

    def append_input_node(self, ast_node, param_name: str, default: Optional[ScopedValue] = None):
        """
        Append an input node to SymbolTree corresponding to parameter of forward method of network class.
        This method is called while building SymbolTree usually.

        Args:
            ast_node (ast.AST): A ast Node corresponding to current parameter.
            param_name (str): A str represents name of parameter of forward method of network class.
            default (ScopedValue, optional): A ScopedValue represents default value of parameter. Default is None which
                means parameter has no default value.

        Returns:
            An instance of input node which has been appended to SymbolTree.
        """
        if param_name == "self":
            return
        for input_node in self._inputs:
            targets = input_node.get_targets()
            if len(targets) != 1:
                raise RuntimeError("targets should have 1 elements")
            target: ScopedValue = targets[0]
            if target.type != ValueType.NamingValue:
                raise RuntimeError("target.type should equal to ValueType.NamingValue")
            if target.scope != "":
                raise RuntimeError("target.scope should be empty")
            exist_param = target.value
            if exist_param == param_name:
                raise RuntimeError("input duplicated:", param_name)
        input_node = Node.create_input_node(ast_node, param_name, default, name=f"input_{param_name}")
        self.append_origin_field(input_node)

    def try_append_python_node(self, ast_scope: ast.AST, ast_node: ast.AST) -> Optional[Node]:
        """
        Try appending a python node to SymbolTree if 'ast_node' is not None and 'ast_node' is not Empty if 'ast_node' is
        a list or a dict.
        This method is called while building SymbolTree usually.

        Args:
            ast_scope (ast.AST): A ast node represents ast node of scope of node.
            ast_node (ast.AST): A ast node represents ast node.

        Returns:
            An instance of python node if a new node has been appended to SymbolTree else None.
        """
        if ast_node is None:
            return None
        if isinstance(ast_node, (list, dict)) and not ast_node:
            return None
        return self.append_python_node(ast_scope, ast_node)

    def append_python_node(self, ast_scope: ast.AST, ast_node: ast.AST) -> Node:
        """
        Append a python node to SymbolTree.
        This method is called while building SymbolTree usually.

        Args:
            ast_scope (ast.AST): A ast node represents ast node of scope of node.
            ast_node (ast.AST): A ast node represents ast node.

        Returns:
            An instance of python node which has been appended to SymbolTree.
        """
        logger.info("Ignoring unsupported node (%s) (%s).", type(ast_node).__name__, type(ast_scope).__name__)
        node_name = self._node_name_namer.get_name(type(ast_node).__name__)
        node = Node.create_python_node(ast_node, node_name)
        self._insert_node(Position.create(self, self._tail, False), node)
        return node

    def set_output(self, return_value: str, index: int) -> Node:
        """
        Update return value of return of forward method of network class.

        Args:
            return_value (str): A str represents new return value.
            index (int): A int indicates which return value to be updated.

        Returns:
            An instance of node represents return node after updated.
        """
        if self._return is None:
            raise RuntimeError("SymbolTree has no output")
        self.set_node_arg(self._return, index, return_value)
        return self._return

    def erase_node(self, node_or_name: Union[Node, str]) -> Node:
        """
        Erase a node from SymbolTree.
        Note:
            If node is depended on by other node, RuntimeError will raise.

            Topological relation is updated.

        Args:
            node_or_name (Union[Node, str]): An instance of node or a str represents name of node.

        Returns:
            An instance of node which has been erased from SymbolTree.

        Raises:
            RuntimeError: If 'node_or_name' is not in current SymbolTree.
            RuntimeError: If erase corresponding ast node failed.
        """

        node = self._get_real_node(node_or_name)
        if node is None:
            raise RuntimeError("Node is not belong to current SymbolTree: ", node_or_name)
        if hasattr(node, "container"):
            cellcontainer = getattr(node, "container")
            cellcontainer.erase(node)
            return node
        ret = AstModifier.erase_ast_from_function(self._root_ast, node.get_ast())
        if not ret:
            raise RuntimeError("node not in function ast tree.")
        self._topo_mgr.on_erase_node(node)
        for key, value in self._nodes.items():
            if id(value) == id(node):
                self._nodes.pop(key)
                value.isolate()
                break
        self._deleted_node.append(node.get_name())
        return node

    def replace(self, old_node: Node, new_nodes: [Node]) -> Node:
        """
        Replace an old_node with a node list.

        Args:
            old_node (Node): Node to be replaced.
            new_nodes (list[Node]): Node list to replace in.

        Returns:
            Last node in new_nodes list.

        Raises:
            RuntimeError: If 'old_node' is isolated.
            RuntimeError: If 'old_node' is not belong to current SymbolTree.
        """

        if hasattr(old_node, "container"):
            self._replace_container_node(old_node, new_nodes)
            return new_nodes[0]
        real_old_node = self._get_real_node(old_node)
        if real_old_node is None:
            raise RuntimeError("Old node is not belong to current SymbolTree:", old_node)
        # get position
        next_node: Node = old_node.get_next()
        prev_node: Node = old_node.get_prev()
        if prev_node is None and next_node is None:
            raise RuntimeError("Try replacing a isolated node: ", old_node)
        if prev_node is None:
            position = self.before(next_node)
        else:
            position = self.after(prev_node)
        for node in new_nodes:
            self.insert_node(position, node, True)
            position = self.after(node)
        self.erase_node(old_node)
        return new_nodes[-1]

    def set_node_arg(self, node: Union[Node, str], index: int, arg: Union[ScopedValue, str]):
        """
        Set argument of 'node'.

        Args:
            node (Union[Node, str]): Node to be modified. Can be a node or name of node.
            index (int): Indicate which input being modified.
            arg (Union[ScopedValue, str]): New argument to been set.

        Raises:
            RuntimeError: If 'node' is not belong to current SymbolTree.
        """

        real_node = self._get_real_node(node)
        if real_node is None:
            raise RuntimeError("Node is not belong to current SymbolTree: ", node)

        new_arg, old_arg = node.set_arg(arg, index)
        self._topo_mgr.on_update_arg(node, index, old_arg, new_arg)

    def set_node_arg_by_node(self, dst_node: Union[Node, str], arg_idx: int, src_node: Union[Node, str],
                             out_idx: Optional[int] = None):
        """
        Set argument of 'dst_node' by another Node.

        Args:
            dst_node (Node): Node to be modified. Can be a node or name of node.
            arg_idx (int): Indicate which input being modified.
            src_node (Node): Node as new input. Can be a node or name of node.
            out_idx ([int, optional]): Indicate which output of 'src_node' as new input of 'dst_node'. Default is None
                which means use first output of 'node_to_link' as new input.

        Raises:
            RuntimeError: If 'dst_node' is not belong to current SymbolTree.
            RuntimeError: If 'src_node' is not belong to current SymbolTree.
            RuntimeError: If 'out_idx' is out of range.
            RuntimeError: If 'src_node' has multi-outputs while 'out_idx' is None or 'out_idx' is not offered.
        """

        real_dst_node = self._get_real_node(dst_node)
        if real_dst_node is None:
            raise RuntimeError("dst_node is not belong to current SymbolTree: ", dst_node)
        real_src_node = self._get_real_node(src_node)
        if real_src_node is None:
            raise RuntimeError("src_node is not belong to current SymbolTree: ", src_node)

        targets = real_src_node.get_targets()
        if out_idx is None:
            if len(targets) != 1:
                raise RuntimeError("node should has one output when out_idx is not provided")
            out_idx = 0
        if out_idx >= len(targets):
            raise RuntimeError("out_idx out of range: ", out_idx)
        new_arg = targets[out_idx]
        real_dst_node.set_arg(new_arg, arg_idx)
        self._topo_mgr.on_update_arg_by_node(real_dst_node, arg_idx, real_src_node, out_idx)

    def unique_name(self, name: str):
        """Get a unique name in the symboltree"""
        return self._target_namer.get_name(name)

    def set_node_target(self, node: Union[Node, str], index: int, target: Union[ScopedValue, str]):
        """
        Set target of `node` .

        Args:
            node (Union[Node, str]): Node to be modified. Can be a node or name of node.
            index (int): Indicate which target being modified.
            arg (Union[ScopedValue, str]): New target to been set.

        Raises:
            ValueError: If `node` is not belong to current SymbolTree.
            ValueError: If index of `node` 's target is greater than number of targets.
        """

        real_node = self._get_real_node(node)
        if real_node is None:
            raise ValueError("Node is not belong to current SymbolTree: ", node)
        if isinstance(target, str):
            target = ScopedValue.create_naming_value(target)
        targets = node.get_targets()
        if index >= len(targets):
            raise ValueError(f"Index of node's target should be less than {len(targets)}, but got {index}")
        old_target = targets[index]
        targets[index] = target
        node.set_targets(targets)
        self._topo_mgr.on_update_target(node, index, old_target, target)

    def print_node_tabulate(self):
        print(self._topo_mgr.dump())

    def dump(self):
        """Dump graph."""
        dump_st = SymbolTreeDumper(self)
        dump_st.dump()

    def update_module_ast(self):
        for node in self._external_func_ast:
            self._module_ast.body.append(node)
        # Put father asts in front of first ClassDef
        index = [type(body) for body in self._module_ast.body].index(ast.ClassDef)
        for node in reversed(self._father_class_ast):
            self._module_ast.body.insert(index, node)

    def get_code(self) -> str:
        """
        Get source code of modified network.

        Returns:
            A str represents source code of modified network.
        """
        self._remove_unused_import()
        if self._init_func_ast:
            self._remove_unused_field()
        self._remove_duplicated_import()
        self.update_module_ast()
        ast.fix_missing_locations(self._module_ast)
        # Find all ast.ClassDef which can be export to code
        # Replace duplicated ast.ClassDef reference in main-ClassDef
        seen_class: {type, str} = {}
        allow_class_name = [self._class_ast.name]
        replacers = []
        SymbolTree._find_all_class_in_symboltree(self, seen_class, allow_class_name, replacers)
        # Add all non-ClassDef body to gencode_module
        # Add all ClassDef in allow_class_name to gencode_module
        # Use gencode_module to generate code
        bodies = []
        for body in self._module_ast.body:
            if not isinstance(body, ast.ClassDef):
                bodies.append(body)
                continue
            if body.name in allow_class_name:
                bodies.append(body)
        gencode_module = ast.Module(body=bodies)
        if_fixer = IfFixer()
        if_fixer.fix(gencode_module)
        code = astunparse.unparse(gencode_module)
        # Restore main-ClassDef
        for replacer in replacers:
            replacer.undo_all()
        return code

    def get_network(self):
        """
        Get modified network.

        Returns:
            A network object.
        """
        cls = self._get_cls_through_file()
        new_net = cls(self._origin_network)
        self._merge_origin_property(new_net)
        return new_net

    def set_saved_file_name(self, file_name: str):
        if file_name.endswith(".py"):
            self._saved_file_name = file_name
        else:
            self._saved_file_name = file_name + ".py"

    def get_saved_file_name(self):
        return self._saved_file_name

    def save_network_to_file(self):
        abs_path = os.path.abspath(self._saved_file_name)
        if os.path.isfile(abs_path):
            os.remove(abs_path)
        with os.fdopen(os.open(self._saved_file_name, os.O_WRONLY | os.O_CREAT, stat.S_IRWXU), 'wb') as f:
            source = self.get_code()
            f.write(source.encode('utf-8'))
            f.flush()

    def _insert_to_ast_while_insert_node(self, node: Node, position: Optional[Position]):
        """ insert_to_ast_while_insert_node. """
        node.set_func(ScopedValue.create_naming_value(node.get_name(), "self"))
        node_ast = node.get_ast()
        if not isinstance(node_ast, ast.Assign):
            raise RuntimeError("Only support insert cell op now")
        if isinstance(node, TreeNode):
            setattr(self._origin_network, node.get_name(), node.get_instance())
            args_call = AstModifier.create_call(ScopedValue(ValueType.NamingValue, "", "getattr"),
                                                [ScopedValue(ValueType.NamingValue, "", "obj"),
                                                 ScopedValue(ValueType.StringValue, "", node.get_name())])
            value = ast.Call(func=ast.Name(node.symbol_tree.get_opt_cls_name(), ast.Store(), lineno=0,
                                           col_offset=0), args=[args_call], keywords=[], lineno=0, col_offset=0)

            ast_target = ast.Name("self." + node.get_name(), ast.Store(), lineno=0, col_offset=0)
            assign = ast.Assign(targets=[ast_target], value=value, lineno=0, col_offset=0)
            AstModifier.insert_assign_ast_to_function(self._init_func_ast, assign)

            AstModifier.insert_assign_ast_to_function(self._root_ast, node_ast,
                                                      None if position is None else position.node.get_ast(),
                                                      position.before_node)
            sub_stree: SymbolTree = node.symbol_tree
            from .symbol_tree_builder import SymbolTreeBuilder
            SymbolTreeBuilder.merge_module_of_subtree(self, sub_stree)
        else:
            AstModifier.insert_assign_to_function(self._init_func_ast,
                                                  targets=[ScopedValue(ValueType.NamingValue, "self", node.get_name())],
                                                  expr=ScopedValue(ValueType.NamingValue, "", "getattr"),
                                                  args=[ScopedValue(ValueType.NamingValue, "", "obj"),
                                                        ScopedValue(ValueType.StringValue, "", node.get_name())])
            AstModifier.insert_assign_ast_to_function(self._root_ast, node_ast,
                                                      None if position is None else position.node.get_ast(),
                                                      position.before_node)
        setattr(self._origin_network, node.get_name(), node.get_instance())

    def _remove_unused_import(self):
        """remove unused import in self._module_ast"""
        str_checker = StrChecker(self._module_ast)
        for i in range(len(self._module_ast.body) - 1, -1, -1):
            body = self._module_ast.body[i]
            if not isinstance(body, (ast.Import, ast.ImportFrom)):
                continue
            if isinstance(body, ast.Import):
                continue
            if isinstance(body, ast.ImportFrom) and body.module == "cell":
                self._module_ast.body.remove(body)
                continue
            for alias in body.names:
                name = alias.asname if alias.asname else alias.name
                if not str_checker.check(name):
                    if len(body.names) == 1:
                        self._module_ast.body.remove(body)
                        i += 1
                    else:
                        body.names.remove(alias)

    def _replace_container_node(self, old_node, new_nodes):
        cellcontainer = getattr(old_node, "container")
        index = cellcontainer.node_list.index(old_node)
        for n in reversed(new_nodes):
            cellcontainer.insert(index, n)
        index = cellcontainer.node_list.index(old_node)
        cellcontainer.erase(old_node)

    def _filter_out_to_delete_field(self, to_delete_field):
        """filter out used field from `to_delete_field`"""
        for func_def in self._class_ast.body:
            if not isinstance(func_def, ast.FunctionDef):
                continue
            if func_def.name != "__init__":
                to_delete_to_delete_keys = []
                property_checker = CheckPropertyIsUsed(func_def)
                for key, _ in self._deleted_field.items():
                    if property_checker.check("self", key):
                        to_delete_to_delete_keys.append(key)
                        property_checker = CheckPropertyIsUsed(func_def)
                for key in to_delete_to_delete_keys:
                    self._deleted_field.pop(key)
            else:
                for body in func_def.body:
                    if not isinstance(body, ast.If):
                        continue
                    test = body.test
                    field_finder = FieldFinder(test)
                    to_delete_to_delete_keys = []
                    for key, _ in self._deleted_field.items():
                        if field_finder.check(key):
                            to_delete_to_delete_keys.append(key)
                    for key in to_delete_to_delete_keys:
                        self._deleted_field.pop(key)

    def _remove_unused_field(self):
        """remove unused field in __init__ function"""
        multi_targets = []
        self._deleted_field = {}
        for index, body in enumerate(self._init_func_ast.body):
            if not isinstance(body, ast.Assign):
                continue
            targets = body.targets
            for target in targets:
                if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) \
                        and target.value.id == "self":
                    self._deleted_field[target.attr] = index
                    if len(targets) > 1:
                        multi_targets.append(index)
        self._filter_out_to_delete_field(self._deleted_field)
        for i in range(len(self._init_func_ast.body) - 1, -1, -1):
            if i in self._deleted_field.values():
                if i in multi_targets:
                    raise RuntimeError("Can not erase field ast node in __init__ function because of multi-targets")
                AstModifier.erase_ast_from_function(self._init_func_ast, self._init_func_ast.body[i])
        ast.fix_missing_locations(self._init_func_ast)

    def _remove_duplicated_import(self):
        """Remove duplicated import of 'net'."""
        imports = []
        for body in self._module_ast.body:
            if isinstance(body, (ast.ImportFrom, ast.Import)):
                import_str = astunparse.unparse(body)
                if import_str not in imports:
                    imports.append(import_str)
                else:
                    self._module_ast.body.remove(body)

    def _get_real_node(self, node_or_name: Union[Node, str]) -> Optional[Node]:
        if isinstance(node_or_name, str):
            return self.get_node(node_or_name)
        return node_or_name

    def _insert_tree(self, position: Position, root: Node, insert_to_ast: bool = True) -> Node:
        """
        Insert a node-tree into SymbolTree.
        Note:
            Inputs of intra sub-tree nodes need to be welly set.

            Inputs of inter sub-tree nodes will be updated by Rewrite automatically.

        Args:
            position (Position): A Position indicates an insert position point.
            root (Node): An instance of node as root of node-tree to be inserted in.
            insert_to_ast (bool): A bool indicates whether to update corresponding ast node at same time, default is
                True.

        Returns:
            An instance of node as root node of node-tree which has been inserted into SymbolTree.

        Raises:
            RuntimeError: If 'position' is not in current SymbolTree.
        """

        # if position not in current SymbolTree
        if position.symbol_tree is not self:
            raise RuntimeError("Position is not in current SymbolTree: ", position)

        queue: [Node] = [root]
        todos: [] = []
        inputs_list: [] = []
        while queue:
            cur_node = queue.pop(0)
            if cur_node in todos:
                continue
            todos.append(cur_node)
            node_inputs = cur_node.get_inputs()
            inputs_list.append(node_inputs)
            for node_input in node_inputs:
                if node_input is not None:
                    queue.append(node_input)
        todos.reverse()
        inputs_list.reverse()
        for index, todo in enumerate(todos):
            self.insert_node(position, todo, insert_to_ast)
            position = self.after(todo)
            # relink input of node
            original_inputs = inputs_list[index]
            for arg_idx, original_input in enumerate(original_inputs):
                if original_input is not None:
                    self.set_node_arg_by_node(todo, arg_idx, original_input)
        return root

    def _add_node2nodes(self, node: Node):
        """
        Add `node` to `_nodes` dict.

        Args:
            node (Node): A Node to be added into `_nodes`.

        Raises:
            RuntimeError: If name of the node is duplicated.
        """
        node_name = node.get_name()
        if self._nodes.get(node_name) is not None:
            raise RuntimeError("generated duplicated node name", node_name, self._nodes.get(node_name),
                               node)
        self._nodes[node_name] = node

    def _insert_node(self, position: Optional[Position], node: Node):
        """
        Insert a node into SymbolTree.
        1. Add `node` to `_nodes`.
        2. Insert `node` to node list(source code order).
        3. Update topological relation and update inputs of `node`.

        Args:
            position ([Position, optional]): Indicates node insert position. Position is None when inserting first node
                of SymbolTree.
            node (Node): A Node to be inserted into SymbolTree.

        Raises:
            RuntimeError: Position is None when _nodes of SymbolTree is not Empty. It means position can not be None
                unless inserting first node.
        """
        if position is None:
            if self._nodes:
                raise RuntimeError("self._nodes should be empty")
            self._head = node
        else:
            if position.before_node:
                position.node.insert_before(node)
            else:
                position.node.insert_after(node)
        self._tail = node
        self._add_node2nodes(node)
        self._topo_mgr.on_insert_node(node)
        node.set_belong_symbol_tree(self)

    def _handle_custom_obj_in_normalized_args(self, node: Node):
        """
        Convert CustomObjValue type argument to NamingValue type argument by storing custom object in global_vars dict.

        Args:
            node (Node): A Node whose arguments and keyword arguments to be handled.
        """
        result: {str, ScopedValue} = {}
        for arg, value in node.get_normalized_args().items():
            if not isinstance(value, ScopedValue):
                raise TypeError("value should be ScopedValue, got: ", type(value))
            if value.type == ValueType.CustomObjValue:
                field = self._node_name_namer.get_name(f"var_{type(value.value).__name__}")
                setattr(self._origin_network, field, value.value)
                init_targets = [ScopedValue.create_naming_value(field, "self")]
                AstModifier.append_global_vars_expr_to_init(self._init_func_ast, init_targets, field)
                result[arg] = init_targets[0]
            else:
                result[arg] = value
        node.set_normalized_args(result)

    def _get_cls_through_file(self):
        """
        Load rewritten network class of current SymbolTree.
        1. Get source code of current SymbolTree.
        2. Saving source code to a tempfile.
        3. Import rewritten network class using "__import__" function.

        Returns:
            A class handle.
        """
        self._update_container()
        file_path = os.getcwd()
        file_path = os.path.join(file_path, "rewritten_network")
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        file_name = "{0}_{1}.py".format(self._opt_cls_name, id(self))
        network_file = os.path.join(file_path, file_name)
        with os.fdopen(os.open(network_file, os.O_WRONLY | os.O_CREAT, stat.S_IRWXU), 'wb') as f:
            source = self.get_code()
            f.write(source.encode('utf-8'))
            f.flush()
            os.fsync(f)
        tmp_module_path, tmp_module_file = os.path.split(network_file)
        tmp_module_name = tmp_module_file[:-3]
        sys.path.append(tmp_module_path)
        tmp_module = None

        i = 0
        while not tmp_module:
            spec = importlib.util.spec_from_file_location(tmp_module_name, network_file)
            if spec:
                tmp_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(tmp_module)
            else:
                logger.warning(f"load module {tmp_module_name} failed, retrying.")
                if i > 10:
                    break
                time.sleep(0.5)
                i += 1
        if not tmp_module:
            logger.error(f"load module {tmp_module_name} failed.")
        # Save new module to sys.modules to support inspect.getsource().
        sys.modules[tmp_module_name] = tmp_module
        network_cls = getattr(tmp_module, self._opt_cls_name)
        if network_cls is None:
            raise RuntimeError("Can not find network class:", self._opt_cls_name)
        return network_cls

    def _on_change(self, event: Event):
        self._modified = True
        self.changed(event)

    def _update_container(self):
        """Update instance of node in container."""
        for node in self.nodes():
            index = 0
            if node.get_node_type() == NodeType.CellContainer:
                for n in node.node_list:
                    if not n.valid:
                        continue
                    if n.get_node_type() == NodeType.Tree:
                        obj = n.symbol_tree.get_network()
                        node.get_instance()[index] = obj
                    else:
                        node.get_instance()[index] = n.get_instance()
                    index += 1

    def _cal_difference_set(self, input, other):
        """Calculate different set of two sets."""
        set1 = set(input)
        set2 = set(other)
        return set1 - set2

    def _merge_origin_property(self, new_net):
        """Merge property of two network."""
        tmp = self._cal_difference_set(dir(self._origin_network), dir(new_net))
        new_attr_names = self._cal_difference_set(tmp, self._deleted_field.keys())
        for name in new_attr_names:
            setattr(new_net, name, getattr(self._origin_network, name))
        # merger cells
        cells = self._cal_difference_set(self._origin_network.name_cells().keys(), new_net.name_cells().keys())
        cells = self._cal_difference_set(cells, self._deleted_node)
        for c in cells:
            new_net.insert_child_to_cell(c, self._origin_network.name_cells()[c])
        # merge primitives
        primitives = self._cal_difference_set(self._origin_network._primitives.keys(), new_net._primitives.keys())
        for p in primitives:
            new_net._primitives[p] = self._origin_network._primitives[p]

    def _create_call_function(self, func, targets, args, kwargs):
        """
        Create a Node object and generate the execution code to insert into the source code.
        The source code calls the 'func' function with 'args' and' kwargs' as parameters.

        Args:
            func (FunctionType) - The function to be called.
            targets (list [str]) - indicates the output name. As the output of the node in the source code.
            args (ParamType) - parameter name of the node. Used as a parameter to a code statement in source
                code. The default value is None, which means there is no parameter input in the cell.
            kwargs ({str: ParamType}) - The key type must be str, and the value type must be ParamType. The
                input parameter name used to describe the formal parameter with a keyword. Enter the name in the source
                code as the 'kwargs' in the statement expression. The default value is None, which means there is no
                'kwargs' input.

        Returns:
            An instance of `Node`.
        """
        if not isinstance(func, types.FunctionType):
            raise TypeError("The 'func' parameter must be a Function, but got ", type(func))

        _package = func.__globals__['__package__']
        func_name = ".".join([_package, func.__name__]) if _package else func.__name__

        ast_assign = self.create_assign_node(targets, func_name, args, kwargs)
        scope_targets = [ScopedValue.create_naming_value(targets[0])]
        scope_func = ScopedValue.create_naming_value(func_name, "")
        call_args = list()
        for arg in args:
            if isinstance(arg, Node):
                call_args.append(ScopedValue.create_variable_value(arg.get_targets()[0].value))
            else:
                call_args.append(ScopedValue.create_variable_value(arg))
        call_kwargs = {}
        for k, v in kwargs.items():
            call_kwargs[k] = ScopedValue.create_variable_value(v)
        node = self.inner_create_call_function(func_name, ast_assign, scope_func, func, scope_targets, call_args,
                                               call_kwargs)
        return node
