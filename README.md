# Data Storm: Weather Data Processing & Visualization Package

**Special Programming Languages** **Calculative Work**  
**Authors:** Rudnytska S.O. and Pidlypna M.T.

---

## Overview

**Data Storm** is a modular Python package developed for fetching, cleaning, analyzing, and processing atmospheric data from the OpenWeatherMap API. It uses Object-Oriented Programming (OOP) principles to ensure a clear separation of concerns, high stability, and extensibility.

## Key Features

- **API Data Retrieval (`fetcher.py`)**: Fetches current weather data (Temperature, Humidity, Pressure) from a public API using the `requests` library.
- **Robust Error Handling**: Implements comprehensive input validation (`ValueError`) and custom exceptions (`WeatherDataError`, `WeatherAnalysisError`) to handle network issues, API key failures, and non-existent queries.
- **Data Processing (`analyzer.py`)**: Utilizes the `pandas` library for efficient data manipulation, including conversion to `DataFrame`, handling missing values (NaN), and basic anomaly detection (e.g., non-physical humidity levels).
- **Statistical Analysis**: Provides core analytical functions to calculate summary statistics (Mean, Minimum, Maximum) for all key weather indicators.
- **Data Output**: Saves processed summary statistics to a JSON file.

## Project Architecture & Structure

This project strictly follows the Python packaging standard (src-layout) and Object-Oriented Programming (OOP) principles with clear separation between modules.

### Logical Modules

| Module       | Core Class              | Responsibility                                                              |
|--------------|-------------------------|------------------------------------------------------------------------------|
| `fetcher.py` | `WeatherDataFetcher`     | Communicates with the external OpenWeatherMap API to retrieve raw data and handle connection errors. |
| `analyzer.py`| `WeatherAnalyzer`        | Transforms raw data into a `pandas.DataFrame`, cleans anomalies, performs statistical calculations, and handles data export. |

### Directory Structure

```text
DataStorm/
├── LICENSE
├── README.md
├── setup.cfg
├── pyproject.toml
├── data_storm_demo.ipynb
├── src/
│   ├── data_storm/
│   │   ├── __init__.py
│   │   ├── fetcher.py
│   │   └── analyzer.py
```
### Usage Example
## Loading and processing data
```
import sys
import os
import matplotlib.pyplot as plt
from typing import List, Dict 
import pandas as pd
import random

# Adding src to system path for module access
try:
    project_root = os.getcwd() 
    src_path = os.path.join(project_root, 'src')

    if src_path not in sys.path:
        sys.path.append(src_path)
        print(f"Path '{src_path}' successfully added to sys.path.")
except Exception as e:
    print(f"Error with path: {e}")

# Importing custom classes
from data_storm.fetcher import WeatherDataFetcher, WeatherDataError 
from data_storm.analyzer import WeatherAnalyzer, WeatherAnalysisError

API_KEY = "9bc0e55c27ecccae14d8b03cf3ec9ff0"  
city_name = "Lviv"

# Example function for mock historical data generation
def get_mock_historical_data(city: str, fetcher: WeatherDataFetcher) -> List[Dict]:
    """Simulates fetching varied weather data points over a time period."""
    try:
        base_data = fetcher.fetch_current_weather(city)
        print(f"    [MOCK] Base data point obtained from API.")
    except Exception:
        base_data = {'city': city, 'temp': 15.0, 'humidity': 70, 'pressure': 1010}
        print(f"    [MOCK] Using default base data.")

    data_list = []
    for i in range(10):
        point = base_data.copy()
        point['temp'] += random.uniform(-3, 3)
        point['humidity'] += random.randint(-8, 8)
        point['pressure'] += random.randint(-3, 3)
        data_list.append(point)
    
    data_list.append({'city': city, 'temp': None, 'humidity': 60, 'pressure': 1010})        
    data_list.append({'city': city, 'temp': 10.0, 'humidity': -5, 'pressure': 1015})         
    data_list.append({'city': city, 'temp': 500, 'humidity': 50, 'pressure': 'N/A'})        
    return data_list

# Running the fetcher and analyzer classes
try:
    fetcher = WeatherDataFetcher(API_KEY)
    analyzer = WeatherAnalyzer()

    print(f"--- 3. Full Pipeline (Fetch -> Clean -> Analyze) for {city_name} ---")

    raw_data = get_mock_historical_data(city_name, fetcher)
    print(f"   [A] Received {len(raw_data)} raw data points (with anomalies).")

    df = analyzer.data_to_dataframe(raw_data)
    df_cleaned = analyzer.clean_data(df)

    rows_initial = len(df)
    rows_cleaned = len(df_cleaned)
    rows_dropped = rows_initial - rows_cleaned
    print(f"   [B] Data cleaned. Removed {rows_dropped} rows (NaN/anomalies) out of {rows_initial}.")
    print("\n   [B] Cleaned data (first 5 rows):")
    print(df_cleaned[["temp", "humidity", "pressure"]].head().to_markdown(index=False))

    stats = analyzer.get_summary_statistics(df_cleaned)
    print("\n   [C] Summary statistics:")
    stats_df = pd.DataFrame(stats).T
    print(stats_df.to_markdown())

    OUTPUT_FILE = "weather_summary.json"
    analyzer.save_summary_to_json(stats, OUTPUT_FILE)
    print(f"\n   [D] Summary successfully saved to '{OUTPUT_FILE}'.")

except (WeatherDataError, WeatherAnalysisError, ValueError) as e:
    print(f"\nCRITICAL pipeline error: {e}")
```
## Vizualizing data
```
def plot_avg_temperature_by_year(temperature_df: pd.DataFrame) -> None:
    """Plots the average temperature per year using matplotlib with subplots and grid."""
    if temperature_df.empty:
        raise ValueError("temperature_df is empty, cannot plot.")
    
    avg_temp = temperature_df.mean(axis=1)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(avg_temp.index, avg_temp.values, marker="o", color="tab:red")

    ax.set_title("Average Temperature by Year (2007–2016)", fontsize=16)
    ax.set_xlabel("Year")
    ax.set_ylabel("Average Temperature (°C)")
    ax.grid(True)

    plt.tight_layout()
    plt.show()
```
## Running the demo
```
# Run temperature plot
temperature_df = build_temperature_df_from_cleaned(df_cleaned, start_year=2007)
plot_avg_temperature_by_year(temperature_df)

# Run humidity plot (Bar Chart)
humidity_df = build_monthly_humidity_from_cleaned(df_cleaned)
plot_monthly_humidity(humidity_df)

# Run pressure plot (Line Chart)
pressure_df = build_monthly_pressure_from_cleaned(df_cleaned)
plot_monthly_pressure(pressure_df)
```
