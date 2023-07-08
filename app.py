import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Send a GET request to the main page
url = "https://thegarynullshow.podbean.com/page/3/"
response = requests.get(url)

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find the episode content section
episode_content = soup.find("div", class_="episode-content")

# Find all the show links within the episode content section
show_links = episode_content.find_all("a", class_="text-decoration-none")

# Extract the URLs of the individual show pages
base_url = "https://thegarynullshow.podbean.com"
show_urls = [urljoin(base_url, link["href"]) for link in show_links]

# Iterate through the show URLs
for show_url in show_urls:
    # Send a GET request to each show page
    response = requests.get(show_url)

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the specific content you want on each show page
    e_description = soup.find("p", class_="e-description")

    # Check if e_description exists
    if e_description:
        health_news = e_description.find("h1") or e_description.find("h2")
        if health_news:
            health_news = health_news.span.get_text(strip=True)
        else:
            health_news = "N/A"

        news_items = e_description.find_all(["h1", "h2", "ul"])

        # Print the extracted information for each show
        print("Show URL:", show_url)
        print("Health News:", health_news)
        print("News Items:")
        for item in news_items:
            print("·", item.span.get_text(strip=True))
        print("---")  # Separator between shows
    else:
        print("No description found for:", show_url)
        print("---")  # Separator between shows
