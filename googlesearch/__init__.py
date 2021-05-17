from requests import get
from bs4 import BeautifulSoup

usr_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/61.0.3163.100 Safari/537.36'}

def escape_search_term(search_term):
    return search_term.replace(' ', '+')

def search(term, num_results=10, lang="en"):

    def fetch_results(search_term, number_results, language_code):
        escaped_search_term = escape_search_term(search_term)
        google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, number_results+1, language_code)
        response = get(google_url, headers=usr_agent)
        response.raise_for_status()
        return response.text

    def parse_results(raw_html):
        soup = BeautifulSoup(raw_html, 'html.parser')
        result_block = soup.find_all('div', attrs={'class': 'g'})
        for result in result_block:
            link = result.find('a', href=True)
            title = result.find('h3')
            if link and title:
                yield link['href']

    html = fetch_results(term, num_results, lang)
    return list(parse_results(html))

def check_result(term, lang="de"):

    def fetch_result(search_term, language_code):
        escaped_search_term = escape_search_term(search_term)

        google_url = 'https://www.google.com/search?q=%22{}%22&hl={}&oq=%22{}%22'.format(escaped_search_term, language_code, escaped_search_term)
        response = get(google_url, headers=usr_agent)
        response.raise_for_status()
        return response.text
    
    def parse_result(raw_html):
        soup = BeautifulSoup(raw_html, 'html.parser')
        result_block = soup.find(id='topstuff')
        return result_block

    def check_result(parsed_result):
        return len(parsed_result) == 0
    
    html = fetch_result(term, lang)
    return check_result(parse_result(html))
