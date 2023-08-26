from smos_walker.typesystem_parser.core import RawNode, render_typesystem_parsed_tree
from smos_walker.xml_reader.facade import read_xml


def render_typesystem_parsed_tree_from_xml(
    xsd_path: str, xml_schema_path: str
) -> RawNode:
    """Generates the most basic tree from the XML schema, with the only addition being the developed typesystem.

    Args:
        xsd_path: Path pointing towards the XSD file, also known as "binx.xsd".
        xml_schema_path: Path pointing towards an XML schema file.

    Returns:
        A basic tree constituted of dicts, with the explicited typesystem.
    """
    data = read_xml(xsd_path, xml_schema_path)
    tree = render_typesystem_parsed_tree(data, data)
    return tree
