# Event Information Scraper

This project is a Python-based web scraper designed to extract event information from a specified website. It utilizes Selenium for web automation and is structured to be scalable and reusable.

## Project Structure

```
event-info-scraper
├── src
│   ├── __init__.py
│   ├── main.py
│   ├── scraper
│   │   ├── __init__.py
│   │   ├── events_scraper.py
│   │   └── utils.py
│   └── config
│       └── __init__.py
│       └── settings.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd event-info-scraper
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the scraper, execute the following command:
```
python src/main.py
```

## Configuration

You can modify the configuration settings in `src/config/settings.py` to adjust the base URL, region mappings, and other constants as needed.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.