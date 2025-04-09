import json
import requests
from bs4 import BeautifulSoup
import re

# Function to scrape details from the assessment URL
def scrape_assessment_details(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Initialize the variables for each field
        job_levels = "N/A"
        languages = "N/A"
        assessment_length = "N/A"
        
        # Check for the "Job levels" field
        job_levels_tag = soup.find('strong', string='Job levels')
        if job_levels_tag:
            job_levels = job_levels_tag.find_next('p').text.strip()
        
        # Check for the "Languages" field
        languages_tag = soup.find('strong', string='Languages')
        if languages_tag:
            languages = languages_tag.find_next('p').text.strip()

        # Check for the "Assessment length" field
        length_tag = soup.find('strong', string='Assessment length')
        if length_tag:
            # Extract the length text and search for a time pattern
            length_text = length_tag.find_next('p').text.strip()
            # Use regex to find numeric values for time (in minutes)
            time_match = re.search(r'(\d+)\s*(minutes|min|mins)?', length_text)
            if time_match:
                assessment_length = int(time_match.group(1))  # Extract the number of minutes
        
        return assessment_length, languages, job_levels

    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return "N/A", "N/A", "N/A"

# Main function to load data, scrape details, and save back
def scrape_and_enhance_assessments(input_file='shl_assessments.json', output_file='shl_assessments.json'):
    try:
        # Load the existing assessments data
        with open(input_file, 'r') as f:
            assessments = json.load(f)
        
        updated_assessments = []
        
        # Loop over each assessment and scrape additional details
        for assessment in assessments:
            url = assessment['url']
            assessment_length, languages, job_levels = scrape_assessment_details(url)
            
            # Add the scraped details to the assessment data
            assessment['assessment_length'] = assessment_length
            assessment['languages'] = languages
            assessment['job_levels'] = job_levels
            
            updated_assessments.append(assessment)
        
        # Save the updated assessments back to the file
        with open(output_file, 'w') as f:
            json.dump(updated_assessments, f, indent=4)
        
        print(f"✅ Scraped and saved details for {len(updated_assessments)} assessments.")
    
    except Exception as e:
        print(f"Error processing assessments: {e}")

# Run the scraper
if __name__ == "__main__":
    scrape_and_enhance_assessments()
