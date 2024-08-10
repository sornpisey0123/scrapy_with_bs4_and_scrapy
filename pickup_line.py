import requests
from bs4 import BeautifulSoup
import json

# Define the URL
url = "https://www.womansday.com/relationships/dating-marriage/a41055149/best-pickup-lines/"

# Fetch the webpage
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Find all titles and pickup lines
pickup_lines_dict = {}
for title in soup.find_all("h2"):
    title_text = title.text.strip()
    pickup_lines = []
    
    # Find the next <ul> following the <h2> tag
    ul_tag = title.find_next("ul")
    
    # Check if <ul> exists and extract <li> tags if it does
    if ul_tag:
        for line in ul_tag.find_all("li"):
            pickup_lines.append(line.text.strip())
    
    # Add the title and corresponding pickup lines to the dictionary
    pickup_lines_dict[title_text] = pickup_lines

# Save the dictionary as a JSON file
with open("pickup_lines.json", "w") as json_file:
    json.dump(pickup_lines_dict, json_file, indent=4)

print("Pickup lines scraped and saved as pickup_lines.json")
