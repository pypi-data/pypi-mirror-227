from smos_walker.core.node import BaseNode
from smos_walker.typesystem_parser.facade import render_typesystem_parsed_tree_from_xml
from smos_walker.typesystem_static_decorator.enhanced_tree_converter import (
    statically_decorate_tree,
)


def get_statically_decorated_tree(typesystem_parsed_tree: any) -> BaseNode:
    """Statically decorates a typesystem-developed raw tree. Uses the dedicated `BaseNode` data structure.

    Takes the resulting tree from the typesystem parsing component and statically decorate it.

    Note:
        The return tree is a new data structure. It should be leaving the passed argument unaltered.

    Args:
        typesystem_parsed_tree: The typesystem-parsed tree resulting from the `typeystem_parser` component.

    Returns:
        A statically decorated tree
    """
    return statically_decorate_tree(typesystem_parsed_tree)


def load_statically_decorated_tree(xsd_path: str, xml_schema_path: str) -> BaseNode:
    """User-friendly way to load statically-decorated tree. It includes the usage of the typesystem parser.

    Args:
        xsd_path: Path pointing towards the XSD file, also known as "binx.xsd".
        xml_schema_path: Path pointing towards an XML schema file.

    Returns:
        A statically decorated tree
    """
    typesystem_parsed_tree = render_typesystem_parsed_tree_from_xml(
        xsd_path, xml_schema_path
    )
    return get_statically_decorated_tree(typesystem_parsed_tree)
