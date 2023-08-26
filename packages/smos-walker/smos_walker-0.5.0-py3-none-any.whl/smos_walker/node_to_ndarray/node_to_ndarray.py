from typing import TypedDict
import numpy as np
from smos_walker.constants import PrimitiveTypeTagNameMapping
from smos_walker.core.exception import SmosWalkerException
from smos_walker.core.node import (
    ArrayFixedNode,
    ArrayVariableNode,
    BaseNode,
    LeafNode,
    NodeVisitor,
    StructNode,
)


class TypeInfo(TypedDict):
    name: str
    type: type
    shape: tuple[int, ...]


def node_to_type_info(
    node: BaseNode,
) -> TypeInfo:
    return node.accept(StaticBlockSlicerNodeVisitor())


class StaticBlockSlicerNodeVisitor(NodeVisitor):
    def visit_leaf(self, node: LeafNode) -> TypeInfo:
        if not node.static:
            raise SmosWalkerException("The node should be static")
        return {
            "name": node.name,
            "type": PrimitiveTypeTagNameMapping[node.primitive_type]["np"],
            "shape": tuple(),
        }

    def visit_struct(self, node: StructNode) -> TypeInfo:
        if not node.static:
            raise SmosWalkerException("The node should be static")
        return {
            "name": node.name,
            "type": np.dtype(
                [
                    (
                        info["name"],
                        info["type"],
                        info["shape"],
                    )
                    for child in node.children
                    if (info := child.accept(self))
                ]
            ),
            "shape": tuple(),
        }

    def visit_array_fixed(self, node: ArrayFixedNode) -> TypeInfo:
        if not node.static:
            raise SmosWalkerException("The node should be static")
        return {
            **node.child.accept(self),
            # Structs that are a direct child of Array Fixed/Variable are anonymous, so use the Array's name
            "name": node.name,
            "shape": tuple(d["size"] for d in node.dimensions),
        }

    # For 0-dimensional array variable we can create the type from their dynamic_size
    def visit_array_variable(self, node: ArrayVariableNode) -> TypeInfo:
        if not node.quasi_static:
            raise SmosWalkerException("The node should be quasi static")

        return {
            **node.child.accept(self),
            # Structs that are a direct child of Array Fixed/Variable are anonymous, so use the Array's name
            "name": node.name,
            # Shape is the responsibility of the caller.
            # "shape": (node.dynamic_size,),
        }
