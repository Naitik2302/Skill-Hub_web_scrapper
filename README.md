# Web Scraper

A Python-based web scraping tool to extract data from websites, follow links up to a user-defined depth, and save the results in JSON, CSV, or Excel formats.

## Features
- Extracts page content and metadata from the given base URL.
- Crawls links recursively up to a user-specified depth.
- Filters content based on keywords provided by the user.
- Delays between requests to avoid overloading servers.
- Saves scraped data in JSON, CSV, or Excel format.
- Supports error handling for broken links and failed requests.

---

## Requirements
- Python 3.7 or higher
- Required Python libraries:
  - `requests`
  - `beautifulsoup4`
  - `pandas`

Install the dependencies with:
```bash
pip install requests beautifulsoup4 pandas
