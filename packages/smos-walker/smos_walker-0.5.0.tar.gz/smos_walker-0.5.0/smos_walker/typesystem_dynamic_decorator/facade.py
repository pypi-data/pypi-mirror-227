from smos_walker.constants import DataBlockType
from smos_walker.core.exception import SmosWalkerException
from smos_walker.core.node import BaseNode
from smos_walker.typesystem_dynamic_decorator.dynamic_decorator import (
    DynamicIndexerNodeVisitor,
)


def dynamically_decorate_tree(
    statically_decorated_tree: BaseNode, datablock: DataBlockType
) -> DynamicIndexerNodeVisitor:
    """Dynamically decorates a statically-decorated typesystem tree **IN-PLACE**

    Takes the resulting tree from the static decoration part and dynamically decorate it
    with the help of a concrete datablock complying to the typesystem described in the XML schema.

    Warning:
        The tree is mutated **IN-PLACE**, this is **NOT** a pure function.

    Args:
        statically_decorated_tree: The statically-decorated tree resulting from
            the `typesystem_static_decorator` component.
        datablock: A whole datablock (`.DBL` file) that complies with the same XML schema
            used to generate the typesystem tree.

    Raises:
        SmosWalkerException: When the provided `datablock` is `None`.

    Returns:
        The visitor used to dynamically analyze the tree.
    """
    if datablock is None:
        raise SmosWalkerException("DataBlock could not be read.")

    visitor = DynamicIndexerNodeVisitor(datablock)
    statically_decorated_tree.accept(visitor)

    return visitor
