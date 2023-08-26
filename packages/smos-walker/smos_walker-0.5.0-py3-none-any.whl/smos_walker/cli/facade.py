import logging
from typing import Literal
from smos_walker.api.tools import output_tree_to_json, output_tree_to_txt
from smos_walker.typesystem_dynamic_decorator.facade import dynamically_decorate_tree
from smos_walker.typesystem_parser.facade import (
    render_typesystem_parsed_tree_from_xml,
)
from smos_walker.typesystem_static_decorator.facade import (
    get_statically_decorated_tree,
)
from smos_walker.util import json_dumps


# Works for BaseNodes
CLI_OUTPUT_FORMATS = {
    "txt": output_tree_to_txt,
    "json": output_tree_to_json,
}

CLI_STEP_CHOICES = {
    1: "Dict-representation of the Type System, that has been prealably developed.",
    2: "Static Decoration of the Type System Tree",
    3: "Dynamic Decoration of the Type System Tree",
}


class CliStepChoice:
    TYPE_SYSTEM_PARSING = (
        "Dict-representation of the Type System, that has been prealably developed."
    )
    TYPE_SYSTEM_STATIC_DECORATION = "Static Decoration of the Type System Tree"
    TYPE_SYSTEM_DYNAMIC_DECORATION = "Dynamic Decoration of the Type System Tree"


def entrypoint(
    xsd_path: str,
    xml_schema_path: str,
    *,
    datablock_folder_path: str | None = None,
    output_format: Literal["txt", "json"] = "json",
    step: Literal[1, 2, 3] = 1
) -> str:
    """_summary_

    Args:
        xsd_path: Path pointing towards the XSD file, also known as "binx.xsd".
        xml_schema_path: Path pointing towards an XML schema file.
        datablock_folder_path: Required by step 3 (dynamic indexing). Defaults to None.
        output_format: Output format.
        step: Step

    Returns:
        String-representation of the working tree
    """
    parsed_typesystem_tree = render_typesystem_parsed_tree_from_xml(
        xsd_path, xml_schema_path
    )

    if step == 1:
        converter = json_dumps  # This is not a BaseNode, so Visitors cannot be applied
        return converter(parsed_typesystem_tree)

    decorated_tree = get_statically_decorated_tree(parsed_typesystem_tree)

    if step == 2:
        converter = CLI_OUTPUT_FORMATS[output_format]
        return converter(decorated_tree)

    if datablock_folder_path is None:
        logging.warning(
            "The binary datablock is required to dynamically decorate the type tree."
        )
        return None

    dynamically_decorate_tree(decorated_tree, datablock_folder_path)

    if step == 3:
        converter = CLI_OUTPUT_FORMATS[output_format]
        return converter(decorated_tree)

    logging.warning("No step after step 3.")
    return None
