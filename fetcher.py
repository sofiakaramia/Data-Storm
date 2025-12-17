import requests

class WeatherDataError(Exception):
    """Custom exception for errors during weather data fetching."""
    pass

class WeatherDataFetcher:
    """
    Module for fetching current weather data from the OpenWeatherMap API.

    Uses the 'requests' library for making HTTP requests.
    """
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, api_key: str):
        """
        Initializes the WeatherDataFetcher object.

        Args:
            api_key: The unique API key for OpenWeatherMap.
        """
        if not api_key or not isinstance(api_key, str):
            raise ValueError("API Key must be a non-empty string.")
        self._api_key = api_key

    def fetch_current_weather(self, city: str) -> dict:
        """
        Retrieves current weather data (temperature, humidity, pressure) for the specified city.

        Args:
            city: The name of the city to retrieve data for.

        Returns:
            A dictionary containing key weather indicators (temp, humidity, pressure).

        Raises:
            WeatherDataError: If an error occurred during the API request (e.g., 404, 401).
            ValueError: If the city name is invalid.

        Examples:
            >>> fetcher = WeatherDataFetcher("YOUR_API_KEY")
            >>> weather_data = fetcher.fetch_current_weather("Kyiv")
            >>> print(weather_data['temp'])
            # 20.5
        """
        if not city or not isinstance(city, str):
            raise ValueError("City name must be a non-empty string.")

        params = {
            'q': city,
            'appid': self._api_key,
            'units': 'metric'
        }

        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status() 
            
            data = response.json()
            
            if 'main' not in data:
                raise WeatherDataError("API response is missing 'main' weather data.")

            weather_info = {
                'city': city,
                'temp': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure']
            }
            return weather_info

        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            if status_code == 404:
                raise WeatherDataError(f"City '{city}' not found (Error 404).")
            elif status_code == 401:
                raise WeatherDataError("Invalid API Key (Error 401).")
            else:
                raise WeatherDataError(f"API request failed with status code {status_code}: {e}")
        except requests.exceptions.RequestException as e:

            raise WeatherDataError(f"A connection error occurred: {e}")
        except Exception as e:
            raise WeatherDataError(f"An unexpected error occurred: {e}")
