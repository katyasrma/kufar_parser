import base64
import statistics

import requests
from bs4 import BeautifulSoup


class Kufar():
    def __init__(self, kufar_url):
        self.kufar_url = kufar_url

    def get_page_url(self, number_page):
        """This function returns url by page number"""
        part_code = '{' + f'"t":"abs","f":true,"p":{number_page}' + '}'
        cursor_code = base64.b64encode(part_code.encode('ascii'))
        url = self.kufar_url[:(self.kufar_url.find('cursor=')) + 7] + str(cursor_code)[2:-1]
        return url

    def parse(self):
        """This function returns the average price for a product category"""
        number_page = 1
        price_list = []
        while requests.get(self.get_page_url(number_page), allow_redirects=False).status_code == 200:
            page = requests.get(self.kufar_url)
            soup = BeautifulSoup(page.text, "html.parser")
            all_notebooks_price = soup.findAll('p', class_='styles_price__x_wGw')

            for data in all_notebooks_price:
                if data.text != 'Договорная':
                    price_list.append(float(data.text.rstrip(' р.').replace(' ', '')))
            number_page += 1
        aver = statistics.mean(price_list)
        return aver


obj = Kufar(kufar_url='https://www.kufar.by/l/mikrokompyutery?cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6MX0%3D')
obj.parse()
