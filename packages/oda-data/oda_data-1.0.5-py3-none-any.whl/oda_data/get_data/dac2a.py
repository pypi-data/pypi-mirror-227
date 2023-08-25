from oda_data import config

from oda_data.get_data import common
from oda_data.logger import logger


def download_dac2a(small_version: bool = False) -> None:
    """Download the DAC1 file from OECD.Stat. Data for all years is downloaded at once.
    This function stores the raw data as a feather file in the raw data folder.

    Args:
        small_version: optionally save a smaller version of the file with only key
            columns (default is False)."""
    logger.info(f"Downloading DAC2A data... This may take a while.")
    common.download_single_table(
        bulk_url=config.TABLE2A_URL,
        raw_file_name="Table2a_Data.csv",
        output_file_name="table2a_raw",
        save_path=config.OdaPATHS.raw_data,
        config_file_path=config.OdaPATHS.settings / "dac2a_config.json",
        small_version=small_version,
    )
