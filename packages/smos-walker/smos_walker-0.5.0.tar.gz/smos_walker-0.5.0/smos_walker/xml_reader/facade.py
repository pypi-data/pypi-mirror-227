import logging
from xml.etree.ElementTree import ParseError
import xmlschema
from lxml import etree

from smos_walker.config import SmosWalkerConfig
from smos_walker.core.exception import SmosWalkerException


def extract_xml_schema_filename_from_hdr_file(datablock_folder_path: str) -> str:
    """Extract the XML schema filename from a .HDR file

    EarthExplorer data consists in a folder containing two files:

    - a .DBL (Datablock) binary file, containing the actual data
    - a .HDR (Header) XML file, describing the related datablock

    The .HDR contains useful information such as the datablock expected length, as well as the
    name of the XML schema file describing the typesystem of the datablock. This information can be used
    to avoid having the client to give a fully qualified path to the XML file when creating a SmosWalker instance,
    and instead having them give a location to a folder containing all XML schemas instead. It also avoids information
    deduplication since the schema filename can be determined from the EarthExplorer folder itself, thus reducing the
    amount of parameters the client has to provide.

    Note:
        The datablock expected length could be used for validation when reading a DBL file with SmosWalker.

    Args:
        datablock_folder_path: Path to the folder containing the DBL and HDR files (EarthExplorer)

    Raises:
        SmosWalkerException: If HDR file was not found
        SmosWalkerException: If the Datablock_Schema was not found in the HDR parsed XML

    Returns:
        The name of the schema file describing the DBL
    """

    result_list = extract_tag_content_from_earthexplorer_hdr(
        datablock_folder_path, "Datablock_Schema"
    )

    if len(result_list) != 1:
        raise SmosWalkerException(
            f"Could not find a unique result for Datablock_Schema (found: {len(result_list)})"
        )

    return result_list[0]


def read_xml(xsd_path: str, xml_schema_path: str):
    """_summary_

    Args:
        xsd_path: Path pointing towards the XSD file, also known as "binx.xsd".
        xml_schema_path: Path pointing towards an XML schema file.

    Raises:
        SmosWalkerException: When the schema validation _itself_ failed
        SmosWalkerException: When the provided file (`xml_schema_path`) is not compliant with the given XSD (`xsd_path`)

    Returns:
        Result of the `xmlschema` usage
    """

    if SmosWalkerConfig.VERBOSE:
        logging.info(f"Loading XML schema: {xsd_path}")
    my_schema = xmlschema.XMLSchema(xsd_path, converter=xmlschema.JsonMLConverter)

    if SmosWalkerConfig.VERBOSE:
        logging.info(f"Validating file: {xml_schema_path}")

    try:
        valid = my_schema.is_valid(xml_schema_path)
    except ParseError as error:
        raise SmosWalkerException("Validation of the schema failed.") from error

    if not valid:
        raise SmosWalkerException(f"File {xml_schema_path=} is not valid. Exiting now.")

    if SmosWalkerConfig.VERBOSE:
        logging.info("Loading XML data to dict")
    data = my_schema.to_dict(xml_schema_path)

    return data


def extract_tag_content_from_earthexplorer_hdr(
    datablock_folder_path: str, tag_name: str
) -> list[str]:
    """Extract the tag content of all found tags matching the given tag name.

    Args:
        datablock_folder_path: Path to the folder containing the DBL and HDR files (EarthExplorer)
        tag_name: Case-sensitive tag name to find in the HDR

    Returns:
        List of all found tags content.
    """

    hdr_path = get_hdr_path_from_earthexplorer_folder(datablock_folder_path)

    return extract_tag_content_from_hdr(hdr_path, tag_name)


def build_xpath(tag_name: str) -> str:
    return "//*[contains(local-name(), '" + tag_name + "')]"


def extract_tag_content_from_hdr(hdr_path: str, tag_name: str) -> list[str]:
    nodes = query_xml(hdr_path, build_xpath(tag_name))

    return stringify_nodes(nodes)


def get_metadata_from_header(datablock_folder_path: str) -> list[list[str]]:
    tag_names_to_grep = [
        # Fixed Header
        "File_Name",
        "File_Description",
        "Notes",
        "Mission",
        "File_Class",
        "File_Type",
        "Validity_Start",
        "Validity_Stop",
        "System",
        "Creator",
        "Creator_Version",
        "Creation_Date",
        # Variable Header
        "Ref_Doc",
        "Long_at_ANX",
        "Ascending_Flag",
        "Polarisation_Flag",
        "Datablock_Size",  # Can be used for parser validation
    ]
    return [
        stringify_nodes(nodes)
        for nodes in query_xml(
            get_hdr_path_from_earthexplorer_folder(datablock_folder_path),
            (list(build_xpath(tag_name) for tag_name in tag_names_to_grep)),
        )
    ]


def stringify_nodes(nodes) -> list[str]:
    return ["".join(node.itertext()) for node in nodes]


def get_hdr_path_from_earthexplorer_folder(datablock_folder_path: str) -> str:
    return get_file_path_from_earthexplorer_folder(datablock_folder_path, "*.HDR")


def get_dbl_path_from_earthexplorer_folder(datablock_folder_path: str) -> str:
    return get_file_path_from_earthexplorer_folder(datablock_folder_path, "*.DBL")


def get_file_path_from_earthexplorer_folder(
    datablock_folder_path: str, glob_pattern: str
) -> str:
    # Try to get the unique file from the given folder and glob pattern
    file_glob = list(datablock_folder_path.glob(glob_pattern))

    if len(file_glob) != 1:
        raise SmosWalkerException(
            f"Expected a unique HDR file in given {datablock_folder_path=}. (found: {len(file_glob)})"
        )

    return file_glob[0]


def query_xml(xml_path: str, xpath: str | list[str]):
    tree = etree.parse(xml_path)
    if isinstance(xpath, str):
        return tree.getroot().xpath(xpath)
    else:
        return [tree.getroot().xpath(path) for path in xpath]
