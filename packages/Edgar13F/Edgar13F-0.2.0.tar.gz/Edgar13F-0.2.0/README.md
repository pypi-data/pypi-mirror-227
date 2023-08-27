# Edgar13F Scraper

A Python package for scraping 13F filings from the SEC Edgar database.

## Installation

To install this package, clone this repository, navigate to its directory, and then use pip:
```bash
git clone https://github.com/jackabrown21/Edgar13F.git
cd Edgar13F
pip install .
```


Duplicate the `.env.example` file, rename it to `.env`, and replace the dummy values with your actual values.

## Usage

```python
from Edgar13F import SecEdgarScraper

companies = {
    "FiduciaryManagementInc": 764532, # "Company": CIK Number
    "SoutheasternAssetManagement": 807985,
    ...
}

base_file_path = 'data/csvs' # Folder of CSVs with the specific companies with this specific information: Form Type, Form Description, Filing Date, Accession Number
data_path = 'data/raw/' # Folder where you would like the XMLs to be downloaded to

scraper = SecEdgarScraper(companies, base_file_path, data_path)
scraper.scrape()
```
