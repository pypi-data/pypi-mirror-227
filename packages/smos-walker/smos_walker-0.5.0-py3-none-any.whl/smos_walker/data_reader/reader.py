"""Shamelessly taken from the SMOS-Toolbox

Source:
https://github.com/ARGANS/SMOS-Toolbox-for-L1-metrics/blob/pil_dev/pkg/src/l1metrics/utils.py
"""

import zipfile
import os
import numpy as np

from smos_walker.core.exception import SmosWalkerException


# HeaDeR file # Txt
def get_earth_explorer_hdr_raw_content(path):
    if ".zip" in str(path) and zipfile.is_zipfile(path):
        # Using 7zip could help speeding up this step
        with zipfile.ZipFile(path) as zfile:
            for filename in zfile.namelist():
                if ".HDR" in filename:
                    with zfile.open(filename) as file:
                        content = file.read()
                    break
    elif os.path.isdir(path):
        for filename in next(os.walk(path))[2]:
            if ".HDR" in filename:
                with open(os.path.join(path, filename), "rb") as file:
                    content = file.read()
                break
    elif not os.path.exists(path):
        raise SmosWalkerException(
            "The directory or file does not exist at the location provided"
        )
    else:
        raise SmosWalkerException(
            "The function expects either a path to a HDR/DBL directory, or a path to the zip file of such directory."
        )
    return content.decode("ASCII")


# DataBLock file # Binary
def get_earth_explorer_dbl_raw_content(path):
    np_rawdata = None
    if ".zip" in str(path) and zipfile.is_zipfile(path):
        # Using 7zip could help speeding up this step
        with zipfile.ZipFile(path) as zfile:
            for filename in zfile.namelist():
                if ".DBL" in filename:
                    np_rawdata = np.frombuffer(
                        zfile.read(filename), dtype=np.uint8, count=-1
                    )
                    break
    elif os.path.isdir(path):
        for filename in next(os.walk(path))[2]:
            if ".DBL" in filename:
                with open(os.path.join(path, filename), "rb") as file:
                    np_rawdata = np.fromfile(file, dtype=np.uint8, count=-1)
                break
    elif not os.path.exists(path):
        raise SmosWalkerException(
            "The directory or file does not exist at the location provided"
        )
    else:
        raise SmosWalkerException(
            "The function expects either a path to a HDR/DBL directory, or a path to the zip file of such directory."
        )
    return np_rawdata
