import os
import csv
from scraping.web_scraping import WebScraping


def main():
    
    # Paths
    current_folder = os.path.dirname(__file__)
    csv_path = os.path.join(current_folder, 'pages.csv')
    pages_folder = os.path.join(current_folder, 'pages')
    
    # Start scraper
    scraper = WebScraping()
    
    # Load pages from csv file
    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            url = row[0]
            
            print(f"Scrapping page: {url}...")
            
            # Clean url for folder and file names
            url_clean = url
            clean_chars = [
                '/',
                ':',
                '.',
                '?',
                '&',
                '=',
                '%',
                '#',
                '+',
                ',',
                ' ',
                '\'',
                '\"'
            ]
            for char in clean_chars:
                url_clean = url_clean.replace(char, '_')
            page_folder = os.path.join(pages_folder, url_clean)
            
            # Create folder if it doesn't exist
            if not os.path.exists(page_folder):
                os.makedirs(page_folder)
            
            # Load page
            scraper.set_page(url)
            
            # Save html code
            html_path = os.path.join(page_folder, 'page.html')
            scraper.save_page(html_path)
            
            # Save screenshot
            screenshot_path = os.path.join(page_folder, 'screenshot.png')
            scraper.screenshot(screenshot_path)
            
            
if __name__ == "__main__":
    main()