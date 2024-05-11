import os
import csv
from scraping.web_scraping import WebScraping
from bs4 import BeautifulSoup


def main():
    
    # Paths
    current_folder = os.path.dirname(__file__)
    csv_path = os.path.join(current_folder, 'pages.csv')
    pages_folder = os.path.join(current_folder, 'pages')
    
    # Start scraper
    scraper = WebScraping(
        width=1920,
        height=2000,
    )
    
    # Load pages from csv file
    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            url = row[0]
            
            print(f"Scrapping page: {url}...")
            
            # Clean url for folder and file names
            url_clean = url.replace('https://', '')
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
            scraper.zoom(20)
            
            # Save html code
            html_path = os.path.join(page_folder, 'page.html')
            scraper.save_page(html_path)
            
            # Clean html code
            with open(html_path, 'r') as html_file:
                html_code = html_file.read()
                soup = BeautifulSoup(html_code, 'html.parser')
                
                # Remove unrequired tags
                tags_to_remove = [
                    "script",
                    "style",
                    "meta",
                    "noscript",
                    "link",
                    "iframe",
                    "form",
                    "input",
                    "select",
                    "option",
                    "textarea",
                    "label",
                    "fieldset",
                    "legend",
                    "object",
                    "embed",
                    "svg",
                    "canvas",
                    "map",
                    "area",
                    "audio",
                    "video",
                    "track",
                    "source",
                ]
                for script in soup(tags_to_remove):
                    script.extract()
                    
                # Remove unrequired attributes
                allowed_attributes = [
                    "href",
                    "src",
                    "alt",
                    "title",
                    "class",
                    "id",
                ]
                for tag in soup.find_all(True):
                    for attr in list(tag.attrs):
                        if attr not in allowed_attributes:
                            del tag[attr]
                    
                # Save clean html code
                clean_html_path = os.path.join(page_folder, 'clean_page.html')
                with open(clean_html_path, 'w') as clean_html_file:
                    clean_html_file.write(str(soup))
            
            # Save screenshot
            screenshot_path = os.path.join(page_folder, 'screenshot.png')
            scraper.screenshot(screenshot_path)
            
            
if __name__ == "__main__":
    main()