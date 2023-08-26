"""Catalog of Visitors that do visit the decorated typesystem tree.
"""
# An example visitor class
# (the to_dict methods were already implemented at node level)
from typing import Callable
from smos_walker.config import SmosWalkerConfig
from smos_walker.constants import PathType

from smos_walker.core.node import (
    ArrayFixedNode,
    ArrayVariableNode,
    BaseNode,
    LeafNode,
    NodeDimension,
    NodeVisitor,
    StructNode,
    ConcreteNodeType,
    render_base_node_dynamic_offset,
)
from smos_walker.util import indent_string, merge_dicts


class DictExportNodeVisitor(NodeVisitor):
    """Export all known information about a node (both static and dynamic)"""

    def visit_leaf(self, node: LeafNode):
        return merge_dicts(render_base_node_dynamic_offset(node), node.to_dict())

    def visit_struct(self, node: StructNode):
        return merge_dicts(
            render_base_node_dynamic_offset(node),
            node.to_dict(),
            {
                "~children": [child.accept(self) for child in node.children],
            },
            # {
            #     "~children": [child.to_dict() for child in node.children],
            # },
        )

    def visit_array_fixed(self, node: ArrayFixedNode):
        return merge_dicts(
            render_base_node_dynamic_offset(node),
            node.to_dict(),
            {
                "~child": node.child.accept(self),
            },
            # {
            #     "~child": node.child.to_dict(),
            # },
        )

    def visit_array_variable(self, node: ArrayVariableNode):
        return merge_dicts(
            render_base_node_dynamic_offset(node),
            {
                "dynamic_size": node.dynamic_size
            },  # Like dynamic_offset, this list can be very long.
            node.to_dict(),
            {
                "~child": node.child.accept(self),
            },
            # {
            #     "~child": node.child.to_dict(),
            # },
        )


class ShallowDictExportNodeVisitor(NodeVisitor):
    """Plain Visitor using the native dict representation methods of Nodes."""

    def visit_leaf(self, node: LeafNode):
        return node.to_dict()

    def visit_struct(self, node: StructNode):
        return node.to_dict()

    def visit_array_fixed(self, node: ArrayFixedNode):
        return node.to_dict()

    def visit_array_variable(self, node: ArrayVariableNode):
        return node.to_dict()


class HumanReadableNodeVisitor(NodeVisitor):
    """Renders a human-readable text-representation of a node.

    Various flags to control displayed data
    """

    def __init__(
        self,
        *,
        indent_pattern: str = "    ",
        write_dimension_name_flag: bool = False,
        write_dynamic_attributes: bool = False,
        write_primitive_type: bool = False,
        write_path: bool = True,
        write_static: bool = False,
        write_numpifiable: bool = False,
        write_block_byte_size=False,
        ignore_static_nodes: bool = False,
        ignore_non_dimensional_nodes: bool = False,
    ):
        """Constructor

        Args:
            indent_pattern: Indentation string.
            write_dimension_name_flag: Write the names of dimensions for Array Fixed.
            write_dynamic_attributes: Write dynamic attributes. Relevant only for dynamically decorated trees.
                See `render_dynamic_attributes`.
            write_primitive_type: Write the primitive type names for Leaf Nodes (eg `unsignedInteger-32`).
                Disabling it declutters the final output.
            write_path: Write the typesystem path pointing to the node.
                Useful for copypasting node reference for later querying.
            write_static: Write information about the staticity / quasi-staticity of a node.
            write_numpifiable: Write the node's `numpifiable` attribute.
                It means the data represented by the node can be viewed with numpy,
                given that enough coordinates are provided (matching the node's dimensionality)
            ignore_static_nodes: Ignore static nodes. Recommended for printing highest-level
                recommended numpifiable nodes, and decluttering the final output.
            ignore_non_dimensional_nodes: Ignore nodes with `dimensionality = None`.
                These nodes were bypassed during the dynamic decoration (phase 3)
        """
        self.lines: list[str] = []
        self.indentation = 0
        self.indent_pattern = indent_pattern
        self.write_dimension_name_flag = write_dimension_name_flag
        self.write_dynamic_attributes = write_dynamic_attributes
        self.write_primitive_type = write_primitive_type
        self.write_block_byte_size = write_block_byte_size

        self.write_path = write_path
        self.write_static = write_static
        self.write_numpifiable = write_numpifiable

        self.ignore_static_nodes = ignore_static_nodes
        self.ignore_non_dimensional_nodes = ignore_non_dimensional_nodes

    def write(self, line):
        self.lines.append(
            indent_string(self.indentation, line, indent_pattern=self.indent_pattern)
        )

    def write_node(self, node, string):
        self.write(
            f"{string} {self.render_numpifiable(node)} {self.render_static(node)} {self.render_block_byte_size(node)} "
            f"{self.render_dynamic_attributes(node)} {self.render_path(node)}"
        )

    def __str__(self):
        return "\n".join(self.lines)

    def nest(self):
        self.indentation += 1

    def unnest(self):
        self.indentation -= 1

    def guard(self, node: BaseNode):
        return (
            self.ignore_non_dimensional_nodes and node.dynamic_dimensionality is None
        ) or (self.ignore_static_nodes and node.static)

    def visit_leaf(self, node: LeafNode):
        if self.guard(node):
            return
        self.write_node(node, f"{render_leaf_node(node, self.write_primitive_type)}")

    def visit_struct(self, node: StructNode):
        if self.guard(node):
            return
        if node.name:
            self.write_node(node, f"{node.name}")
            self.nest()

        for child in node.children:
            child.accept(self)

        if node.name:
            self.unnest()

    def visit_array_fixed(self, node: ArrayFixedNode):
        if self.guard(node):
            return
        rendered_sizes = render_dimensions(
            node.dimensions, write_dimension=self.write_dimension_name_flag
        )
        self.write_node(node, f"{node.name}[{rendered_sizes}]")
        self.nest()
        node.child.accept(self)
        self.unnest()

    def visit_array_variable(self, node: ArrayVariableNode):
        if self.guard(node):
            return
        self.write_node(node, f"{node.name}[{render_leaf_node(node.size_ref)}]")
        self.nest()
        node.child.accept(self)
        self.unnest()

    def render_dynamic_attributes(self, node: BaseNode):
        if not self.write_dynamic_attributes:
            return ""
        return render_dynamic_attributes(node)

    def render_path(self, node: BaseNode):
        if not self.write_path or node.path is None:
            return ""
        return render_path(node.path)

    def render_block_byte_size(self, node: BaseNode):
        if not self.write_block_byte_size or node.path is None:
            return ""
        return f"<size={node.block_byte_size}>"

    def render_static(self, node: BaseNode):
        if not self.write_static:
            return ""

        string = "<static>" if node.static else "<non-static>"
        if isinstance(node, ArrayVariableNode):
            string += " "
            string += "<quasistatic>" if node.quasi_static else "<non-quasistatic>"
        return string

    def render_numpifiable(self, node: BaseNode):
        if not self.write_numpifiable:
            return ""
        return "<numpifiable>" if node.numpifiable else "<not-numpifiable>"


class AbstractPredicateNodeVisitor(NodeVisitor):
    """Base predicate node visitor. Needs to be extended."""

    def __init__(self, predicate: Callable[[BaseNode], bool]):
        self.predicate = predicate

    def visit_leaf(self, node: LeafNode):
        return self.predicate(node)


class UniversalPredicateNodeVisitor(AbstractPredicateNodeVisitor):
    """Verify that all nodes in the tree do match a particular condition"""

    def visit_struct(self, node: StructNode):
        return self.predicate(node) and all(
            child.accept(self) for child in node.children
        )

    def visit_array_fixed(self, node: ArrayFixedNode):
        return self.predicate(node) and node.child.accept(self)

    def visit_array_variable(self, node: ArrayVariableNode):
        return self.predicate(node) and node.child.accept(self)


class ExistentialPredicateNodeVisitor(AbstractPredicateNodeVisitor):
    """Verify existence of a node in the tree that do match a particular condition"""

    def visit_struct(self, node: StructNode):
        return self.predicate(node) or any(
            child.accept(self) for child in node.children
        )

    def visit_array_fixed(self, node: ArrayFixedNode):
        return self.predicate(node) or node.child.accept(self)

    def visit_array_variable(self, node: ArrayVariableNode):
        return self.predicate(node) or node.child.accept(self)


class MaxArrayVariableDepthCounterNodeVisitor(NodeVisitor):
    def __init__(self):
        self.depth: int = 0
        self.max_depth: int = 0

    def nest(self):
        self.depth += 1
        self.max_depth = max(self.depth, self.max_depth)

    def unnest(self):
        self.depth -= 1

    def visit_struct(self, node: StructNode):
        for child in node.children:
            child.accept(self)

    def visit_array_fixed(self, node: ArrayFixedNode):
        node.child.accept(self)

    def visit_array_variable(self, node: ArrayVariableNode):
        self.nest()
        node.child.accept(self)
        self.unnest()


class SimpleQueryNodeVisitor(NodeVisitor):
    """Query node by attribute. Tries to find at least one matching attribute in the node's dict

    Return the first found node. name should be unique ideally.
    """

    def __str__(self):
        return super().__str__() + "|" + f"{self.query_dict=}"

    def __init__(self, query_dict: dict[str, str]):
        self.query_dict = query_dict

    def node_match(self, node):
        for attribute_name, value in self.query_dict.items():
            # See https://stackoverflow.com/questions/61517/python-dictionary-from-an-objects-fields
            if attribute_name in vars(node) and vars(node)[attribute_name] == value:
                return True
        return False

    def visit_leaf(self, node: LeafNode):
        return node if self.node_match(node) else None

    def visit_struct(self, node: StructNode):
        if self.node_match(node):
            return node
        for child in node.yield_children():
            found = child.accept(self)
            if found:
                return found
        return None

    def visit_array_fixed(self, node: ArrayFixedNode):
        return self.visit_array_common(node)

    def visit_array_variable(self, node: ArrayVariableNode):
        return self.visit_array_common(node)

    def visit_array_common(self, node: ArrayFixedNode | ArrayVariableNode):
        if self.node_match(node):
            return node
        found = node.child.accept(self)
        if found:
            return found
        return None


class DictIndexNodeVisitor(NodeVisitor):
    """Index all nodes by their name for easy index, and fill the `path` member of nodes IN PLACE

    Note:
        Modifies IN PLACE the hierarchy.

    Warning:
        - names should be unique for a given parent node.
        - the last visited node will have precedence over the other synonymous nodes in case of conflicts.
    """

    def __init__(self):
        self.path: list[str] = []
        self.mapping: dict[PathType, ConcreteNodeType] = {}

    def add_to_mapping(self, node: ConcreteNodeType):
        tuple_path = tuple(self.path)
        self.mapping[tuple_path] = node
        node.path = tuple_path

    def visit_leaf(self, node: LeafNode):

        self.path.append(node.name)
        self.add_to_mapping(node)
        self.path.pop()

    def visit_struct(self, node: StructNode):

        if node.name:
            self.path.append(
                node.name if node.name else SmosWalkerConfig.ANONYMOUS_STRUCT_IDENTIFIER
            )
            self.add_to_mapping(node)
            for child in node.children:
                child.accept(self)
            self.path.pop()
        else:
            for child in node.children:
                child.accept(self)

    def visit_array_fixed(self, node: ArrayFixedNode):

        self.path.append(node.name)

        self.add_to_mapping(node)

        node.child.accept(self)
        self.path.pop()

    def visit_array_variable(self, node: ArrayVariableNode):

        self.path.append(node.name)
        self.add_to_mapping(node)

        node.child.accept(self)
        self.path.pop()


def render_dimensions(
    dimensions: list[NodeDimension], write_dimension: bool = True, separator: str = ", "
) -> str:
    """Renders a string-representation of an ArrayFixed's dimensions.

    You can test this function using doctest:

    ```bash
    poetry run python -m doctest smos_walker/core/visitors.py
    ```

    Examples:
        >>> render_dimensions([{'name': 'model', 'size': 3}, {'name': 'pol', 'size': 8}])
        'model=3, pol=8'
        >>> render_dimensions([{'name': None, 'size': 2}])
        '2'

    Args:
        dimensions: List of dimensions
        write_dimension: When enabled, writes the dimension's name into the rendered string. Defaults to True.
        separator: Separator between the rendered dimensions. Defaults to ", ".

    Returns:
        Rendered dimensions
    """
    return separator.join(
        str(
            f"{dimension['name']}={dimension['size']}"
            if write_dimension and "name" in dimension and dimension["name"] is not None
            else dimension["size"]
        )
        for dimension in dimensions
    )


def render_leaf_node(node: LeafNode, write_primitive_type=False):
    if write_primitive_type:
        return (
            f"{node.name}: {node.primitive_type}" if node.name else node.primitive_type
        )
    return f"{node.name}" if node.name else "<unnamed>"


def render_dynamic_attributes(node: BaseNode):
    dyndim = f"<dyndim={node.dynamic_dimensionality}>"
    dyncov = f"<dyncov={node.dynamic_coverage}>" if node.dynamic_coverage else ""
    arrvarspecific = (
        render_dynamic_attributes_for_arrayvariable_node(node)
        if isinstance(node, ArrayVariableNode)
        else ""
    )

    return f"{dyndim} {arrvarspecific} {dyncov}"


def render_dynamic_attributes_for_arrayvariable_node(node: ArrayVariableNode):
    if node.dynamic_size is None:
        return "string"
    if isinstance(node.dynamic_size, int):
        return f"<dynsize={node.dynamic_size}>"
    return f"<dynsize=[{len(node.dynamic_size)}, ...]>"


def render_path(path: list[int | str]) -> str:
    return "/" + "/".join(str(p) for p in path)
