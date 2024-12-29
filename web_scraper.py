import requests
from bs4 import BeautifulSoup
import time
import os
import csv
import json
import pandas as pd
from urllib.parse import urljoin

class WebScraper:
    def __init__(self, base_url, max_depth=2, delay=1, keywords=None, output_format="json"):
        self.base_url = base_url
        self.max_depth = max_depth
        self.delay = delay
        self.keywords = [kw.strip().lower() for kw in keywords] if keywords else []
        self.output_format = output_format
        self.visited_links = set()
        self.results = []

    def is_relevant(self, text):
        """Check if a given text contains any of the user-specified keywords."""
        if not self.keywords:
            return True
        return any(keyword in text.lower() for keyword in self.keywords)

    def fetch_page(self, url, depth):
        """Fetch a webpage, parse its content, and find links for crawling."""
        if url in self.visited_links or depth > self.max_depth:
            return

        try:
            print(f"Fetching: {url}")
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                print(f"Error: Received status code {response.status_code} for {url}")
                return

            soup = BeautifulSoup(response.content, "html.parser")
            self.visited_links.add(url)

            # Extract and filter relevant content
            page_data = {"url": url, "title": soup.title.string if soup.title else "No Title"}
            if self.is_relevant(page_data["title"]):
                self.results.append(page_data)

            # Find and crawl links
            for link in soup.find_all("a", href=True):
                next_link = urljoin(url, link["href"])
                if next_link.startswith(self.base_url):
                    self.fetch_page(next_link, depth + 1)

            # Pause to avoid overwhelming the server
            time.sleep(self.delay)
        except requests.RequestException as e:
            print(f"Request failed: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def save_results(self):
        """Save the scraping results in the specified output format."""
        os.makedirs("output", exist_ok=True)
        if self.output_format == "json":
            with open("output/scraped_data.json", "w", encoding="utf-8") as json_file:
                json.dump(self.results, json_file, indent=4)
            print("Results saved to output/scraped_data.json")
        elif self.output_format == "csv":
            keys = self.results[0].keys()
            with open("output/scraped_data.csv", "w", newline="", encoding="utf-8") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=keys)
                writer.writeheader()
                writer.writerows(self.results)
            print("Results saved to output/scraped_data.csv")
        elif self.output_format == "excel":
            df = pd.DataFrame(self.results)
            df.to_excel("output/scraped_data.xlsx", index=False)
            print("Results saved to output/scraped_data.xlsx")
        else:
            print(f"Unsupported output format: {self.output_format}")

    def run(self):
        """Start the web scraping process."""
        print("Starting web scraping...")
        self.fetch_page(self.base_url, depth=1)
        if self.results:
            self.save_results()
        else:
            print("No relevant data found.")

if __name__ == "__main__":
    # Example usage
    base_url = input("Enter the base URL: ")
    max_depth = int(input("Enter maximum crawling depth (e.g., 2): "))
    delay = int(input("Enter delay between requests in seconds (e.g., 1): "))
    keywords = input("Enter keywords for filtering (comma-separated, optional): ").split(",")
    output_format = input("Enter output format (json/csv/excel): ").strip().lower()

    scraper = WebScraper(base_url, max_depth, delay, keywords, output_format)
    scraper.run()
