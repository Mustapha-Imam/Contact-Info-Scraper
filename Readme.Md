# Professional Web Scraper

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Requests](https://img.shields.io/badge/Requests-2.26+-green)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup4-4.10+-orange)

A production-ready web scraper that extracts contact information (emails/phones) and page metadata from websites with robust error handling and anti-blocking measures.

## Features

- Contact Extraction: Regex-based email and phone number detection
- Anti-Blocking Measures:
  - Rotating user agents
  - Randomized request delays
  - Proxy support
  - Respectful crawling delays
- Error Handling:
  - Comprehensive logging
  - Connection timeout handling
  - HTTP status checks
- CSV Export: Structured output with domain metadata
- Configurable: Easy-to-modify settings via config.py

## Usage

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Add target URLs to `urls.txt` (one per line)

3. Run scraper:
```bash
python scraper.py --input urls.txt --output results.csv --delay 2.0
```

## Sample Output
| url                | domain       | title          | emails                     | phones           | status  |
|--------------------|--------------|----------------|----------------------------|------------------|---------|
| https://example.com| example.com  | Example Domain | contact@example.com        | +1-555-123-4567  | success |

## Customization
Modify `config.py` to:
- Add more user agents
- Configure proxy servers
- Adjust default delay

## Ethical Considerations
- Includes 2.5+ second delay between requests by default
- Respects robots.txt (manual implementation guidance included)
- User agent rotation prevents server overload
