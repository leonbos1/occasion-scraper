import requests
from bs4 import BeautifulSoup

url = "https://www.autoscout24.nl/lst/Alfa%20Romeo?cy=NL&pricefrom=0&ustate=N%2CU&page=1"

response = requests.get(url)
print(f"Status: {response.status_code}")

soup = BeautifulSoup(response.text, "html.parser")

# Find all articles
articles = soup.find_all("article")
print(f"\nFound {len(articles)} articles")

if len(articles) > 0:
    print("\n=== FIRST ARTICLE ===")
    first_article = articles[0]
    print(f"Article attributes: {first_article.attrs}")
    
    # Find all links in the article
    links = first_article.find_all("a")
    print(f"\nFound {len(links)} links in first article")
    
    for i, link in enumerate(links[:3]):  # Show first 3 links
        print(f"\n--- Link {i+1} ---")
        print(f"Classes: {link.get('class')}")
        print(f"Href: {link.get('href')}")
        print(f"Text: {link.text.strip()[:50]}")
