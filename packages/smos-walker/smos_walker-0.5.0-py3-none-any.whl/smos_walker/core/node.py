from functools import cached_property
import json
import math
from typing import Type, TypeAlias, TypedDict

from smos_walker.constants import PrimitiveTypeTagNameMapping
from smos_walker.util import merge_dicts


class Visitor:
    def __str__(self):
        return self.__class__.__name__


RecursiveListOfIntegers = int | list["RecursiveListOfIntegers"]

ConcreteNodeType: TypeAlias = (
    Type["LeafNode"]
    | Type["StructNode"]
    | Type["ArrayFixedNode"]
    | Type["ArrayVariableNode"]
)


class NodeVisitor(Visitor):  # Interface
    """Generic interface for the visitor pattern, used for tree exploration"""

    def visit_leaf(self, node: "LeafNode"):
        pass

    def visit_struct(self, node: "StructNode"):
        pass

    def visit_array_fixed(self, node: "ArrayFixedNode"):
        pass

    def visit_array_variable(self, node: "ArrayVariableNode"):
        pass


class NodeDimension(TypedDict):
    """A Node's dimension is composed of an optional name and a mandatory size."""

    name: str | None
    size: int


class BaseNode:
    """Base Node: The abstract base node that all others inherit from.

    A convention followed in this class hierarchy is to prefix by `dynamic` attributes that can only
    determined with a concrete instance of a datablock.
    It means that they cannot be determined solely from the type system XML schema.

    Attributes:
        name: Mandatory node's name (static)
        label: Optional label over the node (static)
        block_byte_size: Computed at compile time, if possible (static)

        dynamic_dimensionality: Dimensionality: number of integers required to uniquely identify the node
        dynamic_coverage: Accumulated size obtained during each of the node's visit when reading the binary data block
        dynamic_offset: Dynamic offset while reading. The array is of dimension `dynamic_dimensionality`
    """

    def __init__(self, name: str, label: str | None = None) -> None:
        """
        Args:
            name: Mandatory node's name
            label: Optional label over the node
        """

        # Static attributes
        # -----------------
        self.name: str = name
        self.label: str | None = label

        # Dynamic attributes
        # ------------------
        self.dynamic_dimensionality: int | None = None
        self.dynamic_coverage: int | None = None
        self.dynamic_offset: RecursiveListOfIntegers | None = None

        # Optional attributes
        # -------------------
        self.path: str | None = None

    def __repr__(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.__repr__()

    @cached_property
    def static(self) -> bool:
        """True if the node's children block size is known in advance (static)

        To be overriden by subclasses
        """
        return self.block_byte_size is not None

    @cached_property
    def block_byte_size(self) -> int | None:
        return None

    @property
    def numpifiable(self) -> bool:
        return (
            self.static
            # pylint: disable=no-member
            or (isinstance(self, ArrayVariableNode) and self.quasi_static)
            # If children are numpifiable, the node is numpifiable
            # or isinstance(self, StructNode)
            # and all(child.numpifiable for child in self.children)
        )

    def to_dict(self):
        return shallow_render_base_node(self)

    def accept(self, visitor: NodeVisitor):
        pass  # To be implemented by subclasses


class LeafNode(BaseNode):
    """Leaf Node: the final concrete data described by the type system.

    It is analoguous to primitive types in programming languages.

    It satisfies the following properties:

    - it is always `static`
    - it has no children (as its name indicated, like a leaf on a tree)

    Attributes:
        primitive_type: A string representing the primitive of the node.
            No type checking is performed ; an unexpected value will engender a runtime error.
    """

    def __init__(
        self,
        name: str,
        primitive_type: str,
    ) -> None:
        super().__init__(name)
        self.primitive_type: str = primitive_type

    @cached_property
    def block_byte_size(self):
        return PrimitiveTypeTagNameMapping[self.primitive_type]["byte_count"]

    def to_dict(self):
        return merge_dicts(
            shallow_render_base_node(self),
            {
                "_class": self.__class__.__name__,
                "primitive_type": self.primitive_type,
            },
        )

    def accept(self, visitor: NodeVisitor):
        return visitor.visit_leaf(self)


class StructNode(BaseNode):
    """Struct Node: the abstract data structure containing the others.

    It is analoguous to structures in programming languages such as C.

    More specifically, structures are closely related to the type system.
    Indeed, the "structure" and "type" concepts are merged into one in this parser.
    In the original XML schema files, `useType` tags often have an only `struct` tag child.
    However, it can also contains one  `ArrayFixed` or one `ArrayVariable`.
    If that is the case, the array node child is wrapped into a list containing itself,
    to simulate a structure node having it as a child.

    It satisfies the following properties:

    - It has a list of children. They can be of all type deriving `BaseNode`.
    - It is static when all its children are static
    - When static, it can be mapped to a Numpy's `dtype`

    Attributes:
        type_name: The name of the type containing the structure.
        children: Members of the structure.
    """

    def __init__(
        self,
        name: str,
        type_name: str,
        children: list[BaseNode],
    ) -> None:
        super().__init__(name)
        self.type_name: str = type_name
        self.children: list[BaseNode] = children

        if isinstance(self.children, (ArrayFixedNode, ArrayVariableNode)):
            # During initial conception, it has been - wrongly - assumed that struct tags
            # always were a direct child of useType tags, hence the merging between the
            # two concepts. A StructNode is actually more a "UseTypeNode".
            # Since Arrays can also be children of useType tags, the fix was to wrap them
            # into a struct node.
            self.children = [self.children]

    @cached_property
    def block_byte_size(self):
        if all(child.static for child in self.children):
            return sum(child.block_byte_size for child in self.children)
        return None

    def to_dict(self):
        return merge_dicts(
            shallow_render_base_node(self), shallow_render_struct_node(self)
        )

    def accept(self, visitor: NodeVisitor):
        return visitor.visit_struct(self)

    def yield_children(self):
        for child in self.children:
            yield child


class ArrayFixedNode(BaseNode):
    """Array Fixed Node: the nicest array node.

    It is analoguous to static arrays in programming languages such as C.

    It satisfies the following properties:

    - It has one or more dimensions. Their naming is optional.
    - It is static when its unique child is static.
    - When static, it can be mapped to a Numpy's `dtype`
    - It has one child, that can be a leaf or a struct

    Property known to be wrong
    - If the child is a struct, it has to be static. => It can contain other arrayvariables

    To prove these, the `PredicateNodeVisitor` could be used.

    Attributes:
        dimensions: The name of the type containing the structure.
        cardinality: Total number of children accross all dimensions.
        child: The type of data contained in the array.
    """

    def __init__(
        self,
        name: str,
        dimensions: list[NodeDimension],  # multiple dimensions allowed [label, dim]
        child: LeafNode | StructNode,
    ) -> None:
        super().__init__(name)
        self.dimensions: list[NodeDimension] = dimensions
        self.cardinality: int = math.prod(
            dimension["size"] for dimension in self.dimensions
        )
        self.child: LeafNode | StructNode = child

    @cached_property
    def block_byte_size(self):
        if self.child.static:
            return self.cardinality * (self.child.block_byte_size)
        return None

    def to_dict(self):
        return merge_dicts(
            shallow_render_base_node(self), shallow_render_array_fixed_node(self)
        )

    def accept(self, visitor: NodeVisitor):
        return visitor.visit_array_fixed(self)


class ArrayVariableNode(BaseNode):
    """Array Variable Node: the one that did create the need for this project in the first place.

    It is analoguous to dynamically allocated arrays in programming languages such as C.

    It satisfies the following properties:

    - It has only one variable dimension
    - It is never static, as its total size cannot be determined without an instance of a datablock providing its length
    - When quasi-static, it can be mapped to a Numpy's `dtype`
    - The only dimension is always named
    - Children are always Struct (uncertain, as ArrayFixed node can reference LeafNodes directly)
    - `size_ref` is always a Leaf (very likely, as it stores a scalar describing the dimension)

    Properties to be proved formally:

    - The most nested ArrayVariable in a schema hierarchy is quasi-static.

    Warning:
        Currently, the `child` attribute can only be a `StructNode`,
        but this is likely to be a `StructNode | LeafNode`, though not encountered yet.

    To prove these, the `PredicateNodeVisitor` could be used.

    Attributes:
        size_ref: A leaf node describing the array length. It can only be determined as runtime.
            The size_ref is the _header_ of an array variable. Related to the `dimensions` attribute of an `ArrayFixed`.
        dynamic_size: Like `BaseNode`'s `dynamic_coverage` and `dynamic_offset`,
            this attribute can be multi-dimensional and can only be read at runtime.
                For example, for an arrayvariable 2 in an arrayvariable 1,
                multiple arrayvariables 2 will be present at runtime and this variable will contain a list of integers.
        child: The type of data contained in the array.
    """

    def __init__(
        self,
        name: str,
        child: StructNode,
        size_ref: LeafNode,
    ) -> None:
        super().__init__(name)
        self.size_ref: LeafNode = size_ref
        self.child: StructNode = child

        # Actual length, read dynamically
        self.dynamic_size: RecursiveListOfIntegers | None = None

    @property
    def quasi_static(self):
        if not self.child:
            return None  # information not available yet
        return self.child.static

    def to_dict(self):
        return merge_dicts(
            shallow_render_base_node(self),
            shallow_render_array_variable_node(self),
        )

    def accept(self, visitor: NodeVisitor):
        return visitor.visit_array_variable(self)


def shallow_render_base_node(node: BaseNode):
    return merge_dicts(
        {
            "name": node.name,
            "static": node.static,
            "block_byte_size": node.block_byte_size,
        },
        ({} if node.label is None else {"label": node.label}),
        (
            {}
            if node.dynamic_dimensionality is None
            else {"dynamic_dimensionality": node.dynamic_dimensionality}
        ),
        (
            {}
            if node.dynamic_coverage is None
            else {"dynamic_coverage": node.dynamic_coverage}
        ),
    )


def render_base_node_dynamic_offset(node: BaseNode):
    return (
        {} if node.dynamic_offset is None else {"dynamic_offset": node.dynamic_offset}
    )


def shallow_render_array_variable_node(node: ArrayVariableNode):
    return {
        "_class": node.__class__.__name__,
        "size_ref": node.size_ref.to_dict(),
        "quasi_static": node.quasi_static,
    }


def shallow_render_array_fixed_node(node: ArrayFixedNode):
    return {
        "_class": node.__class__.__name__,
        "dimensions": node.dimensions,
        "cardinality": node.cardinality,
    }


def shallow_render_struct_node(node: StructNode):
    return {
        "_class": node.__class__.__name__,
        "type_name": node.type_name,
    }
