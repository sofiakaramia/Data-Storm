import pandas as pd
import json
from typing import list, dict, Union

class WeatherAnalysisError(Exception):
    """Custom exception for errors during weather data analysis."""
    pass

class WeatherAnalyzer:
    """
    Module for cleaning, processing, and performing statistical analysis on weather data.

    Utilizes the pandas library for efficient data manipulation.
    """
    
    def __init__(self):
        """Initializes the WeatherAnalyzer."""
        pass
    
    def data_to_dataframe(self, data_list: List[Dict[str, Union[str, float]]]) -> pd.DataFrame:
        """
        Converts a list of weather dictionaries into a pandas DataFrame.
        
        Args:
            data_list: A list of dictionaries with weather data. 
                       Expected keys: 'temp', 'humidity', 'pressure', 'city'.

        Returns:
            A pandas DataFrame ready for analysis.

        Raises:
            WeatherAnalysisError: If the input data list is empty or invalid.
        """
        if not data_list or not isinstance(data_list, list):
            raise WeatherAnalysisError("Input data list cannot be empty or non-list.")

        try:
            df = pd.DataFrame(data_list)
            required_cols = ['temp', 'humidity', 'pressure']
            
            for col in required_cols:
                df[col] = pd.to_numeric(df[col], errors='coerce')

            return df
        except Exception as e:
            raise WeatherAnalysisError(f"Error converting data to DataFrame: {e}")

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Performs data cleaning, handling missing values (NaN) and basic anomalies.

        Args:
            df: The pandas DataFrame containing weather data.

        Returns:
            The cleaned pandas DataFrame.
        """
        df_cleaned = df.dropna(subset=['temp', 'humidity', 'pressure'])

        df_cleaned = df_cleaned[
            (df_cleaned['humidity'] >= 0) & (df_cleaned['humidity'] <= 100)
        ]
        df_cleaned = df_cleaned[df_cleaned['pressure'] > 0]

        return df_cleaned

    def get_summary_statistics(self, df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        """
        Calculates summary statistics (mean, min, max) for key weather indicators.

        Args:
            df: The cleaned pandas DataFrame.

        Returns:
            A nested dictionary containing statistics for 'temp', 'humidity', and 'pressure'.

        Raises:
            WeatherAnalysisError: If the DataFrame is empty.
        """
        if df.empty:
            raise WeatherAnalysisError("Cannot calculate statistics: DataFrame is empty after cleaning.")

        stats = {}
        for col in ['temp', 'humidity', 'pressure']:
            stats[col] = {
                'mean': df[col].mean(),
                'min': df[col].min(),
                'max': df[col].max()
            }
            
        for col in stats:
            stats[col] = {k: round(v, 2) for k, v in stats[col].items()}
            
        return stats
    
    def save_summary_to_json(self, stats: Dict[str, Dict[str, float]], filepath: str):
        """
        Saves the summary statistics dictionary to a JSON file (Demonstration of data output).

        Args:
            stats: The summary statistics dictionary returned by get_summary_statistics.
            filepath: The full path to the output JSON file.

        Raises:
            WeatherAnalysisError: If there is an error during file writing.
        """
        if not stats:
            raise WeatherAnalysisError("Statistics data is empty, cannot save.")
            
        try:
            with open(filepath, 'w') as f:
                json.dump(stats, f, indent=4)
        except Exception as e:
            raise WeatherAnalysisError(f"Error saving statistics to file: {e}")
            
    def convert_celsius_to_kelvin(self, temp_c: float) -> float:
        """
        Converts temperature from Celsius to Kelvin.
        
        Args:
            temp_c: Temperature in Celsius.
            
        Returns:
            Temperature in Kelvin.
        """
        if not isinstance(temp_c, (int, float)):
             raise ValueError("Input temperature must be a number.")
        return temp_c + 273.15
