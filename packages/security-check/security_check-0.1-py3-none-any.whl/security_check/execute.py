import subprocess
import json
from bs4 import BeautifulSoup
import requests


def get_score(url):
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    element = soup.select_one('#severity-rating')
    nota = float(element.text)

    return nota


def run():
    return_terminal = subprocess.run(['safety', 'check', '--json'], capture_output=True, text=True)

    return_dict = json.loads(return_terminal.stdout)

    vulnerabilities = return_dict.get('vulnerabilities')

    for i in range(len(vulnerabilities)):
        try:
            score = get_score(vulnerabilities[i].get('more_info_url'))
            vulnerabilities[i]['score'] = score
        except:
            print(f'Warning - cant procces url {vulnerabilities[i].get("more_info_url")}')

    return_dict['vulnerabilities'] = vulnerabilities

    print(json.dumps(return_dict))
