import requests
from bs4 import BeautifulSoup
import json
import csv
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class SHLScraper:
    def __init__(self):
        self.base_url = 'https://www.shl.com/solutions/products/product-catalog/'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (compatible; SHLScraper/1.0)"
        }

    def get_assessment_links(self):
        response = requests.get(self.base_url, headers=self.headers)
        if response.status_code != 200:
            print(f"Failed to fetch main page: {self.base_url}")
            return []

        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', href=True)
        assessment_links = [link['href'] for link in links if '/product-catalog/view/' in link['href']]
        return list(set(assessment_links))  # Deduplicate

    def parse_assessment_page(self, url):
        try:
            session = requests.Session()
            retries = Retry(
                total=3,
                backoff_factor=2,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=["GET"]
            )
            session.mount('https://', HTTPAdapter(max_retries=retries))

            response = session.get(url, headers=self.headers, timeout=15)
            if response.status_code != 200:
                print(f"[{response.status_code}] Skipping {url}")
                return None

            soup = BeautifulSoup(response.content, 'html.parser')
            assessment = {}

            # Title
            title_tag = soup.find('h1')
            assessment['name'] = title_tag.text.strip() if title_tag else 'N/A'
            assessment['url'] = url

            # Get Description
            desc_block = soup.find('div', class_='product-description')
            if desc_block:
                assessment['description'] = desc_block.get_text(strip=True)

            # Key Features: Difficulty, Time, etc.
            key_info_blocks = soup.select('div.product-detail')
            for block in key_info_blocks:
                label_tag = block.find('strong')
                if label_tag:
                    key = label_tag.get_text(strip=True).replace(":", "")
                    val = label_tag.next_sibling
                    if val is None:
                        val = block.get_text(strip=True).replace(label_tag.get_text(strip=True), "").strip()
                    else:
                        val = str(val).strip()
                    assessment[key] = val

            # Extract time and difficulty (if available)
            time_block = soup.find('div', class_='time-block')
            if time_block:
                assessment['time'] = time_block.get_text(strip=True)  # Assuming this contains time info.

            difficulty_block = soup.find('div', class_='difficulty-block')
            if difficulty_block:
                assessment['difficulty'] = difficulty_block.get_text(strip=True)  # Assuming this contains difficulty info.

            return assessment
        except Exception as e:
            print(f"Error parsing {url}: {e}")
            return None

    def scrape_all(self):
        print("Fetching assessment links...")
        links = self.get_assessment_links()
        if not links:
            print("No links found.")
            return []

        print(f"Found {len(links)} links. Starting to parse...\n")
        assessments = []
        for i, relative_link in enumerate(links):
            full_url = f"https://www.shl.com{relative_link}"
            print(f"[{i+1}/{len(links)}] Scraping: {full_url}")
            assessment = self.parse_assessment_page(full_url)
            if assessment:
                assessments.append(assessment)
            time.sleep(1)
        return assessments

    def save_to_json(self, data, filename='shl_assessments.json'):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def save_to_csv(self, data, filename='shl_assessments.csv'):
        if not data:
            return
        keys = set()
        for item in data:
            keys.update(item.keys())
        keys = list(keys)

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)

if __name__ == '__main__':
    scraper = SHLScraper()
    all_data = scraper.scrape_all()
    scraper.save_to_json(all_data)
    scraper.save_to_csv(all_data)
    print(f"\n✅ Done! Scraped and saved {len(all_data)} assessments.")
