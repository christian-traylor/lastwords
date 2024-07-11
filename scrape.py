import requests
from bs4 import BeautifulSoup

base_url = "https://www.tdcj.texas.gov/death_row/dr_executed_offenders.html"

def get_html(url):
    response = requests.get(url, verify=False)  #TODO: We need to have a .pem file so we can use verify=True
    response.raise_for_status()
    return response.text

def get_inmate_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'class': 'tdcj_table indent'})
    links = []
    for row in table.find_all('tr')[1:]:
        link = row.find_all('td')[2].find('a')['href']
        links.append(f"https://www.tdcj.texas.gov/death_row/{link}")
    return links

def get_last_statement(html):
    soup = BeautifulSoup(html, 'html.parser')
    last_statement_tag = soup.find('p', text='Last Statement:')
    if last_statement_tag:
        # The last statement should be the next sibling <p> tag
        last_statement = last_statement_tag.find_next_sibling('p').get_text(strip=True)
        return last_statement
    return 'N/A'

def main():
    html = get_html(base_url)
    inmate_links = get_inmate_links(html)
    
    for link in inmate_links:
        inmate_html = get_html(link)
        last_statement = get_last_statement(inmate_html)
        print(f"Last Statement: {last_statement}\n")

if __name__ == "__main__":
    main()