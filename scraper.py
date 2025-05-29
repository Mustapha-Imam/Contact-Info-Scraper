import re
import csv
import time
import random
import argparse
import requests
import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from config import USER_AGENTS, PROXIES, DELAY

# Configure logging
logging.basicConfig(
    filename='scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Regex patterns
EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
PHONE_REGEX = r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{2,4}[-.\s]?\d{3,5}\b'

def get_random_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive'
    }

def scrape_url(url):
    """Scrape emails, phone numbers, and title from URL"""
    result = {
        'url': url,
        'domain': urlparse(url).netloc,
        'title': '',
        'emails': set(),
        'phones': set(),
        'status': 'success',
        'error': None
    }

    try:
        # Rotate proxies and headers
        proxy = random.choice(PROXIES) if PROXIES else None
        headers = get_random_headers()

        response = requests.get(
            url,
            headers=headers,
            proxies=proxy,
            timeout=15,
            allow_redirects=True
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        result['title'] = soup.title.string.strip() if soup.title else ''

        # Extract from both visible text and meta tags
        page_text = soup.get_text()
        meta_text = " ".join([meta.get('content', '') for meta in soup.find_all('meta')])

        # Combine sources for better coverage
        combined_text = page_text + " " + meta_text

        # Find emails and phones
        result['emails'] = set(re.findall(EMAIL_REGEX, combined_text, re.IGNORECASE))
        result['phones'] = set(re.findall(PHONE_REGEX, combined_text))

    except requests.exceptions.RequestException as e:
        result['status'] = 'failed'
        result['error'] = str(e)
        logging.error(f"Request failed for {url}: {str(e)}")
    except Exception as e:
        result['status'] = 'error'
        result['error'] = str(e)
        logging.exception(f"Unexpected error with {url}")

    return result

def main():
    parser = argparse.ArgumentParser(description='Professional Web Scraper')
    parser.add_argument('-i', '--input', default='urls.txt', help='Input file with URLs')
    parser.add_argument('-o', '--output', default='results.csv', help='Output CSV file')
    parser.add_argument('-d', '--delay', type=float, default=DELAY, help='Delay between requests')
    args = parser.parse_args()

    # Read URLs
    try:
        with open(args.input, 'r') as f:
            urls = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Input file '{args.input}' not found")
        return

    # Scrape with progress
    results = []
    print(f"Scraping {len(urls)} URLs...\n")
    for i, url in enumerate(urls):
        print(f"Processing ({i+1}/{len(urls)}): {url}")
        result = scrape_url(url)
        results.append(result)
        time.sleep(args.delay + random.uniform(-0.5, 0.5))  # Randomized delay

    # Export results
    with open(args.output, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['url', 'domain', 'title', 'emails', 'phones', 'status', 'error']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for res in results:
            res['emails'] = '; '.join(res['emails'])
            res['phones'] = '; '.join(res['phones'])
            writer.writerow(res)

    print(f"\nScraping completed. Results saved to {args.output}")

if __name__ == '__main__':
    main()
