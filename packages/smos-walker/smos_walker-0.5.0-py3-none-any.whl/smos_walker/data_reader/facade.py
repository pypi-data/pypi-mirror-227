from smos_walker.constants import DataBlockType
from smos_walker.data_reader.reader import (
    get_earth_explorer_dbl_raw_content,
    get_earth_explorer_hdr_raw_content,
)


def read_hdr(datablock_folder_path: str) -> str:
    return get_earth_explorer_hdr_raw_content(datablock_folder_path)


def read_dbl(datablock_folder_path: str) -> DataBlockType | None:
    """Reads a Data Block file. A Data Block file (`*.DBL`) is a binary file respecting a XML _binx_ schema.

    Args:
        datablock_folder_path: Path pointing towards the **folder** containing the datablock file (`*.DBL`)

    Returns:
        A data block (numpy array of `uint8`) if read was successful, `None` otherwise.
    """
    return get_earth_explorer_dbl_raw_content(datablock_folder_path)
