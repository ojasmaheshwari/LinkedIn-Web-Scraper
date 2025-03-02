# LinkedIn Web Scraper

A Python-based web scraper for extracting data from LinkedIn profiles. This tool automates the process of gathering professional information using Selenium.

## Features
- Extracts profile details such as name, bio, experience and education.
- Uses Selenium for browser automation.
- Supports authentication via LinkedIn credentials.
- Saves scraped data in CSV format.

## Prerequisites
Ensure you have the following installed:
- Python 3.x
- Google Chrome
- ChromeDriver (matching your Chrome version)
- Selenium

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/ojasmaheshwari/LinkedIn-Web-Scraper.git
   cd LinkedIn-Web-Scraper
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
1. Run the script:
   ```sh
   python main.py
   ```
   or run all code inside `main.ipynb` file

## Disclaimer
This tool is for educational purposes only. Scraping LinkedIn data may violate LinkedIn's terms of service. Use responsibly.

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Requirement it does not satisfy
- Scraping socials
    - I could not scrape socials simply because I could not find where the socials were present in a user's LinkedIn page. If you let me know where the socials are present, I can scrape that data easily too.

## Development Process and My Thoughts
Web scraping is actually pretty straightforward. While you can't just extract an information in one find command, you have to keep digging down and use multiple find queries to get to your data.
Initially I thought of not using Selenium and just using requests module so I won't have to simulate a browser. But there were some obvious problems. The main problem being that I just could not get dynamically created html which was 
handled by javascript. So I had to use Selenium. The rest of the process was straightforward once I understood how web scraping was actually done. It is just a little tedious but straight-forward process.
