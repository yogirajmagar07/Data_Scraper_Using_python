
# Data Scraper Using Python

This repository contains a Python script that scrapes data from the HP RERA website. It uses Selenium for web automation, BeautifulSoup for parsing HTML, and Pandas for data manipulation.

## Prerequisites

Ensure you have Python 3.6+ installed on your system. You can download Python from [python.org](https://www.python.org/).

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yogirajmagar07/Data_Scraper_Using_python.git
    cd Data_Scraper_Using_python
    ```

2. Create a virtual environment and activate it (optional but recommended):

    ```sh
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On Unix or MacOS
    source venv/bin/activate
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Make sure you have Google Chrome installed on your machine.
2. Run the `extract.py` script:

    ```sh
    python extract.py
    ```

3. The script will scrape data from the HP RERA website, process it, and save it to `extract.csv`.

## File Descriptions

- `requirements.txt`: Lists all the dependencies required to run the script.
- `extract.py`: The main script that performs the web scraping, data extraction, and data cleaning.

## Sample Output

The output of the script will be saved in a file named `extracted_data.csv` in the same directory as the script. The CSV file will contain the following columns:

- GSTIN No.
- PAN No.
- Name
- Permanent Address

## Contributing

Feel free to open issues or submit pull requests if you find any bugs or have suggestions for improvements.

