from glob import glob
from typing import Optional

import pandas as pd

from script_manager.handlers.directories import DirectoryHandler


class CSVHandler:
    """
    A class for handling CSV files and data.
    """

    @staticmethod
    def find_csv_file(
        csv_file_name: str,
        csv_directory: Optional[str] = None,
    ) -> str:
        """
        Find the CSV file in the specified directory.

        Args:
            csv_file_name (str): The name of the CSV file.
            csv_directory (str, optional): Directory to search for CSV files.
                If not provided, it will be retrieved from the environment
                variable DOWNLOADS_DIRECTORY.

        Returns:
            str: The path to the CSV file.
        """
        csv_file = ""
        csv_directory = csv_directory or DirectoryHandler().downloads_dir
        for file in glob(f"{csv_directory}/*{csv_file_name}*.csv"):
            csv_file = file
        return csv_file

    @staticmethod
    def extract_csv(csv_file_path: str) -> pd.DataFrame:
        """
        Extract data from the CSV file.

        Args:
            csv_file_path (str): The path to the CSV file.

        Returns:
            pd.DataFrame: The extracted data as a pandas.DataFrame.
        """
        return pd.read_csv(csv_file_path)

    @staticmethod
    def update_csv_entry(
        index,
        prop: str,
        csv_file_path: str,
        csv_data: pd.DataFrame,
        skipped: bool = False,
        value: Optional[str] = None,
    ) -> None:
        """
        Update a CSV entry.

        Args:
            index: Index of the CSV entry.
            prop (str): Property to update (e.g., "Status").
            csv_file_path (str): Path to the CSV file.
            csv_data (pd.DataFrame): DataFrame containing CSV data.
            skipped (bool, optional): Whether the update was skipped.
            value (str, optional): Value to update the property.

        Returns:
            None
        """
        status = "Skipped" if skipped else value or "Updated"
        csv_data.loc[index, prop] = status
        csv_data.to_csv(csv_file_path, index=False)

    @staticmethod
    def save_to_csv(
        data: list | pd.DataFrame,
        csv_file_name: str,
        csv_directory: Optional[str] = None,
    ) -> str:
        """
        Save data to a CSV file.

        Args:
            data (list | pandas.DataFrame): Data to save to the CSV.
            csv_file_name (str): Name of the CSV file.
            csv_directory (str (optional)): The location to save the csv to.
                Defaults to the environment variable [DOWNLOADS_DIRECTORY]

        Returns:
            str: The created csv file's path.
        """
        csv_directory = csv_directory or DirectoryHandler().downloads_dir
        data = pd.DataFrame(data) if isinstance(data, list) else data
        csv_file_path = rf"{csv_directory}\{csv_file_name}.csv"
        data.to_csv(csv_file_path, index=False)
        return csv_file_path