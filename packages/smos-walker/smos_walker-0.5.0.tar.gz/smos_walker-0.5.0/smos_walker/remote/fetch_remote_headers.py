import argparse
import json
import logging
import os
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path, PurePosixPath
from typing import Callable
from zipfile import ZipFile

from tqdm import tqdm

from smos_walker.xml_reader.facade import extract_tag_content_from_hdr

logging.basicConfig()
logger = logging.getLogger("fetch_remote_headers")
logger.setLevel(logging.INFO)

SMOS_FTP_PASSWORD = "SMOS_FTP_PASSWORD"


def main():
    args = build_argument_parser().parse_args()

    config = Config(
        host=args.host,
        user=args.user,
        password=args.password,
        schema_type=args.schema_type,
        start_date=args.start_date,
        end_date=args.end_date,
        date_format=args.date_format,
        output_directory=args.output_directory,
    )

    logger.info(f"Fetch remote headers with {config=}")
    logger.info(f"Using the {SMOS_FTP_PASSWORD} env variable to fetch password")

    # Fallback on environment variable
    if config.password is None:
        config.password = os.getenv(SMOS_FTP_PASSWORD)

    steps = set(args.steps)
    logger.info(f"{steps=}")

    if "1" in steps:
        original_working_directory = os.getcwd()
        logger.info("Step 1: %s", fetch_remote_headers.__name__)
        fetch_remote_headers(config)
        os.chdir(original_working_directory)

    if "2" in steps:
        logger.info("Step 2: %s", extract_relevant_info_from_headers.__name__)
        extract_relevant_info_from_headers(config.output_directory, config.schema_type)

    logger.info("Finished")


@dataclass
class Config:
    host: str
    user: str
    password: str = field(repr=False)
    schema_type: str
    start_date: str
    end_date: str
    date_format: str
    output_directory: str


default_config = Config(
    host="ftp://smos-diss.eo.esa.int",
    user="yreyricord@argans.co.uk",
    password=None,
    schema_type="MIR_OSUDP2",
    start_date="20161223",
    end_date="20161224",
    date_format="%Y%m%d",
    output_directory=str(Path.cwd() / "generated"),
)


def build_argument_parser() -> argparse.ArgumentParser:

    # Default values in help
    # See https://stackoverflow.com/questions/12151306/argparse-way-to-include-default-values-in-help
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "--host",
        type=str,
        help="FTP Host",
        default=default_config.host,
    )
    parser.add_argument(
        "--user",
        type=str,
        help="FTP User",
        default=default_config.user,
    )
    parser.add_argument(
        "--password",
        type=str,
        help="FTP Password",
        required=False,
    )
    parser.add_argument(
        "--schema_type",
        type=str,
        help="Schema Type",
    )
    parser.add_argument(
        "--start_date",
        type=str,
        help="Start Date (default date format, overridable: see date_format)",
    )
    parser.add_argument(
        "--end_date",
        type=str,
        help="End Date (default date format, overridable: see date_format)",
    )
    parser.add_argument(
        "--date_format",
        type=str,
        help="Date Format",
        default=default_config.date_format,
    )
    parser.add_argument(
        "--output_directory",
        type=str,
        help="Output Directory",
        default=default_config.output_directory,
    )
    parser.add_argument(
        "--steps",
        nargs="+",
        help="Steps to execute",
        required=False,
        choices=["1", "2"],
        default=["1", "2"],
    )

    return parser


def dummy_consumer(hdr_path: Path):
    output_path = hdr_path.with_suffix(".json")
    with open(output_path, "w", encoding="utf-8") as text_file:
        content = json.dumps(str(output_path))
        text_file.write(str(content))


def relevant_info_consumer(hdr_path: Path):
    output_path = hdr_path.with_suffix(".json")
    with open(output_path, "w", encoding="utf-8") as text_file:
        tag_names = ["Long_at_ANX", "Ascending_Flag", "Ref_Filename"]
        result = {
            tag_name: extract_tag_content_from_hdr(hdr_path, tag_name)
            for tag_name in tag_names
        }
        content = json.dumps(result, indent=2)
        text_file.write(str(content))


def extract_relevant_info_from_headers(
    output_directory: str,
    schema_type: str,
    *,
    consumer: Callable[[Path], None] = relevant_info_consumer,
):
    base_path = Path(output_directory) / schema_type

    for path in base_path.rglob("*.HDR"):
        consumer(path)


def fetch_remote_headers(config: Config):
    host = config.host
    user = config.user
    password = config.password
    schema_type = config.schema_type
    start_date = config.start_date
    end_date = config.end_date
    date_format = config.date_format
    output_directory = config.output_directory

    # Change current working directory to the configured one.
    os.makedirs(output_directory, exist_ok=True)
    os.chdir(output_directory)
    logger.info("Working directory: %s", os.getcwd())

    start_date = datetime.strptime(start_date, date_format)
    end_date = datetime.strptime(end_date, date_format)
    desc = f"Iterating through days in [[{start_date.strftime(date_format)} ; {end_date.strftime(date_format)}]]"

    for current_date in tqdm(date_range(start_date, end_date), desc=desc):

        # Extract year, month, and day from current_date
        year = current_date.strftime("%Y")
        month = current_date.strftime("%m")
        day = current_date.strftime("%d")

        # Set remote directory path
        remote_dir_udp = str(
            PurePosixPath("/") / "SMOS" / "L2OS" / schema_type / year / month / day
        )

        # Create local directory if it doesn't exist
        local_dir_udp_month = Path(schema_type) / year / month
        local_dir_udp_day = local_dir_udp_month / day

        os.makedirs(local_dir_udp_day, exist_ok=True)

        # Change working directory
        os.chdir(local_dir_udp_month)

        logger.info(f"Starting download {remote_dir_udp} from {host} to {os.getcwd()}")

        command = f'lftp -u "{user}","{password}" {host} << EOF\nset ssl:verify-certificate no\nmirror {remote_dir_udp} ./;\nbye\nEOF'

        logger.info(f"{command=}")
        subprocess.run(command, shell=True, check=False)

        extract_header(day)

        os.chdir("../../..")


def extract_header(day: str):

    # Create a ZipFile Object and load sample.zip in it
    for filename in os.listdir(f"./{day}/"):

        # Check if the file is a zip file
        if not filename.endswith(".zip"):
            continue

        # Construct the full path to the zip file
        zip_path = os.path.join(f"./{day}/", filename)

        # Open the zip file
        with ZipFile(zip_path, "r") as zip_file:
            # Iterate over the files in the zip file
            for name in zip_file.namelist():
                # Check if the file is a HDR file
                if name.endswith(".HDR"):
                    # Extract the HDR file from the zip file
                    zip_file.extract(name, f"./{day}/")

        # Delete the zip file
        os.remove(zip_path)


def date_range(start_date: datetime, end_date: datetime, inclusive: bool = True):
    # Calculate the number of days between start_date and end_date
    day_count = (end_date - start_date).days
    if inclusive:
        day_count += 1
    logger.info(f"{day_count=}")

    # Iterate over dates between start_date and end_date, inclusive
    return ((start_date + timedelta(days=day_index)) for day_index in range(day_count))


if __name__ == "__main__":
    main()
