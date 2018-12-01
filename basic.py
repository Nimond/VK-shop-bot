import requests
from bs4 import BeautifulSoup

names = {"лапша": ["лапши", "лапшички"],
        }
class product_info:
    def __init__(self, cost, stars, name, url, photo):
        self.cost = cost
        self.stars = stars
        self.name = name
        self.url = 'https://deldelhi.ru' + url
        self.photo = photo


def get_products(s):
    pr = []
    
    for key in names:
        if s in names[key]:
            s = key
            break

    r = requests.get("https://deldelhi.ru/search/", params={'query':s})
    soup = BeautifulSoup(r.text, 'html.parser')
    products = soup.find(attrs={'class':'thumbs product-list'})
    if products == None:
        return "no"

    products = products.find_all('li')

    if len(products) != 0:
        print("found "+str(len(products))+" products")
        for product in products:
            print("lol")
            name = product.find('a')['title']
            cost = product.find(attrs = {'class': 'price nowrap'}).text
            stars = product.find(attrs = {'class': 'rating nowrap'})
            photo = 'https://deldelhi.ru' + product.find(attrs = {'class': 'badge-wrapper'}).find('img')['src']


            if stars != None:
                full = stars.find_all(attrs = {'class': 'icon16 star'})
                half = stars.find_all(attrs = {'class': 'icon16 star-half'})
                stars = len(full)+len(half)*0.5
            url = product.find('a')['href']

            temp = product_info(cost, stars, name, url, photo)
            pr.append(temp)
            print('lel')

    return pr
