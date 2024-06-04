import requests
from bs4 import BeautifulSoup

API_KEY = "sk-ant-api03-AABBCC"
API_URL = "https://api.anthropic.com/v1/complete"

def chat_with_claude(prompt):
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY,
        "anthropic-version": "2023-06-01"
    }
    data = {
        "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
        "model": "claude-v1",
        "max_tokens_to_sample": 100
    }
    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["completion"]
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while scraping the website: {e}")
        return None

def analyze_website(soup):
    if soup:
        # Extract relevant information from the parsed HTML
        title = soup.title.text if soup.title else "N/A"
        headings = [h.text for h in soup.find_all(["h1", "h2", "h3"])]
        paragraphs = [p.text for p in soup.find_all("p")]
        
        # Prepare the prompt for Claude
        prompt = f"Please analyze the following website information:\n\nTitle: {title}\n\nHeadings:\n{chr(10).join(headings)}\n\nParagraphs:\n{chr(10).join(paragraphs)}\n\nProvide a summary and key insights from the website."
        
        # Get analysis from Claude
        analysis = chat_with_claude(prompt)
        
        # Write the scraped output and analysis to a file
        with open("output.txt", "w") as file:
            file.write(f"Title: {title}\n\n")
            file.write("Headings:\n")
            file.write("\n".join(headings))
            file.write("\n\nParagraphs:\n")
            file.write("\n".join(paragraphs))
            file.write("\n\nAnalysis from Claude:\n")
            file.write(analysis)
        
        print("Scraped output and analysis written to output.txt")
    else:
        print("Failed to scrape the website.")

def main():
    url = input("Enter the URL of the website to scrape: ")
    soup = scrape_website(url)
    analyze_website(soup)

if __name__ == "__main__":
    main()
