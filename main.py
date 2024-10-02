import requests
from bs4 import BeautifulSoup
import pandas as pd

cookies = {
    'PHPSESSID': 'm9j1le3qi40q42oh9jf37lkm3d',
    'c_new_but_date2': '2024-12-31',
    '_gid': 'GA1.2.807989240.1727866836',
    '_gat_gtag_UA_58277_11': '1',
    '__gads': 'ID=7d88f6a2108946fc:T=1727866886:RT=1727866886:S=ALNI_MYSBbhqKS9zd9lEXsVk4TMtkoV_7g',
    '__gpi': 'UID=00000f1d1259451d:T=1727866886:RT=1727866886:S=ALNI_MYTAsV1nC-MeEqAMz45K2WRtvk3aw',
    '__eoi': 'ID=13c524b2c1f82e24:T=1727866886:RT=1727866886:S=AA-AfjbdQ0DLn3uNUTBVgm8fZNOB',
    'FCNEC': '%5B%5B%22AKsRol_PUAhYh8utnSVjHV2aSzIY0gjDIWT3kjYnSH8uAJ0gWL2rVoClAM2H1uA6YvYO86OOqtqQO3qYGSRPDw-BGWwe5UhYJfEEcDthTyaMZCB_uQ0mqwDFYF3aVqVWRcYcrXn7uXuIDOmlpvbp20Jkr0BV3gSvgA%3D%3D%22%5D%5D',
    '_ga_M5LCK2TTTF': 'GS1.1.1727866835.1.1.1727866910.52.0.179174947',
    '_ga': 'GA1.2.1880546333.1727866836',
    '_gat': '1',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en;q=0.9',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
}

def fetch_page(url, cookies, headers):
    """Fetches the page and returns the BeautifulSoup object."""
    try:
        response = requests.get(url, cookies=cookies, headers=headers)
        return BeautifulSoup(response.text, 'lxml')
    except requests.exceptions.RequestException as e:
        print(f'Error Fetching Page {e}')
        return None

def extract_companies_data(soup):
    """Extracts company names and links from the page."""
    companies_links = []
    
    cards = soup.find_all('div', {'class': 'col-md-6 col-sm-12 title-line-height'})
    if not cards:
        print("No Data")
    else:
        for card in cards:
            companies = card.find_all('a')
            for company in companies:
                companies_links.append('https://www.kinderdagverblijf-info.nl' + company['href'])
    
    return companies_links

def fetch_company_details(company_link, cookies, headers):
    """Fetches company details such as name, location, and phone number."""
    soup = fetch_page(company_link, cookies, headers)
    if soup:
        location = soup.find('div', {'class': 'font-medium text-info text-truncate'})
        phone = soup.find('ins')
        company_name = soup.find('h1', {'class': 'mb-md-0'})

        # Collect details in a dictionary
        return {
            'Company Name': company_name.text.strip() if company_name else 'N/A',
            'Location': location.text.strip() if location else 'N/A',
            'Phone': phone.text.strip() if phone else 'N/A'
        }
    return None

def save_to_csv(data, filename):
    """Saves the company data to a CSV file."""
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def main():
    url = 'https://www.kinderdagverblijf-info.nl/azindex.php'
    soup = fetch_page(url, cookies, headers)
    
    if soup:
        companies_links = extract_companies_data(soup)
        all_companies_data = []
        
        for company_link in companies_links:
            company_details = fetch_company_details(company_link, cookies, headers)
            if company_details:
                all_companies_data.append(company_details)
        
        # Save all data to CSV
        save_to_csv(all_companies_data, 'companies_data.csv')

# Run the main function
if __name__ == '__main__':
    main()