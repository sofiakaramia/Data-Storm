# Data Storm: Weather Data Processing & Visualization Package

**Спеціальні мови програмування** **Розрахункова робота** **Виконали:** Рудницька С.О. та Підлипна М.Т.

---

## Overview

**Data Storm** is a modular Python package developed for fetching, cleaning, analyzing, and processing atmospheric data from the OpenWeatherMap API. It is structured using the Object-Oriented Programming (OOP) paradigm to ensure clear separation of concerns, high stability, and extensibility.

## Key Features

* **API Data Retrieval (`fetcher.py`):** Securely fetches current weather data (Temperature, Humidity, Pressure) from a public API using the `requests` library.
* **Robust Error Handling:** Implements comprehensive input validation (`ValueError`) and custom exceptions (`WeatherDataError`, `WeatherAnalysisError`) to handle network issues, API key failures, and non-existent queries.
* **Data Processing (`analyzer.py`):** Utilizes the `pandas` library for efficient data manipulation, including conversion to `DataFrame`, handling missing values (NaN), and basic anomaly detection (e.g., non-physical humidity levels).
* **Statistical Analysis:** Provides core analytical functions to calculate summary statistics (Mean, Minimum, Maximum) for all key weather indicators.
* **Data Output:** Functionality to save processed summary statistics to a JSON file.

## Project Architecture & Structure

The project adheres strictly to the Python packaging standard (src-layout) and OOP principles, with clear functional separation between modules.

### Logical Modules

| Module | Core Class | Responsibility |
| :--- | :--- | :--- |
| `fetcher.py` | `WeatherDataFetcher` | Communicates with the external OpenWeatherMap API to retrieve raw data and handle connection errors. |
| `analyzer.py` | `WeatherAnalyzer` | Transforms raw data into a `pandas.DataFrame`, cleans anomalies, performs statistical calculations, and handles data export. |

### Directory Structure

```text
DataStorm/
├── LICENSE
├── README.md
├── setup.cfg
├── pyproject.toml
├── data_storm_demo.ipynb
└── src/
    └── data_storm/
        ├── __init__.py
        ├── fetcher.py
        └── analyzer.py
