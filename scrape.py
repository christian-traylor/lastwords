import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
import warnings

base_url = "https://www.tdcj.texas.gov/death_row/dr_executed_offenders.html"
warnings.filterwarnings("ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning)

def get_html(url):
    response = requests.get(url, verify=False)  #TODO: We need to have a .pem file so we can use verify=True
    response.raise_for_status()
    return response.text

def get_inmate_links_and_date(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'class': 'tdcj_table indent'})
    links_and_dates = []
    for row in table.find_all('tr')[1:]:
        inmate_links = []
        inmate_information_link = row.find_all('td')[1].find('a')['href']
        last_statement_link = row.find_all('td')[2].find('a')['href']
        date_executed = row.find_all('td')[7].text
        inmate_links.extend([f"https://www.tdcj.texas.gov/death_row/{inmate_information_link}", 
                             f"https://www.tdcj.texas.gov/death_row/{last_statement_link}", date_executed])
        links_and_dates.append(inmate_links)
    return links_and_dates

def clean_text(text):
    return text.replace('\u2032', "'").replace('\u2033', '"').strip()

def get_last_statement(html):
    soup = BeautifulSoup(html, 'html.parser')
    last_statement_tag = soup.find('p', text='Last Statement:')
    if last_statement_tag:
        last_statement = clean_text(last_statement_tag.find_next_sibling('p').get_text(strip=True))
        if last_statement in ("No statement was made.", "This inmate declined to make a last statement."):
            return 'N/A'
        return last_statement
    return 'N/A'

def get_inmate_information(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'class': 'table_deathrow indent'})
    inmate_info = {}
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) > 2:
            key = cells[1].text.strip()
            value = clean_text(cells[2].text.strip())
            inmate_info[key] = value
        elif len(cells) == 2:
            key = cells[0].text.strip()
            value = clean_text(cells[1].text.strip())
            inmate_info[key] = value
    return inmate_info

def save_data(links_and_dates):
    entry = 588
    inmate_data = {}
    
    for (inmate_information_link, last_statement_link, date_executed) in tqdm(links_and_dates):
        try:
            inmate_information_html = get_html(inmate_information_link)
        except Exception as e:
            print(e)
        try:
            last_statement_html = get_html(last_statement_link)
        except Exception as e:
            print(e)
        try:
            last_statement = get_last_statement(last_statement_html)
        except Exception as e:
            print(e)
        try:
            inmate_information = get_inmate_information(inmate_information_html)
        except Exception as e:
            print(e)

        inmate_data[entry] = {}
        inmate_data[entry]['last_statement'] = last_statement
        inmate_data[entry]['inmate_information'] = inmate_information
        inmate_data[entry]['date_executed'] = date_executed

        entry -= 1

        if entry == 233:  # Last inmate with data in HTML table
            break

    file_path = 'data.json'

    with open(file_path, 'w') as file:
        json.dump(inmate_data, file, indent=4)


def main():
    html = get_html(base_url)
    links_and_dates = get_inmate_links_and_date(html)
    save_data(links_and_dates)

if __name__ == "__main__":
    main()