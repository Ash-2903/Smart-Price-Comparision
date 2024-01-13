from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

flipkart = ''
ebay = ''
croma = ''
amazon = ''
olx = ''


def flipkart_search(name):
    try:
        global flipkart
        name1 = name.replace(" ", "+")
        flipkart = f'https://www.flipkart.com/search?q={name1}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off'
        res = requests.get(f'https://www.flipkart.com/search?q={name1}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off', headers=headers)

        soup = BeautifulSoup(res.text, 'html.parser')
        flipkart_name = soup.select('._4rR01T')[0].getText().strip().upper()
        if name.upper() in flipkart_name:
            flipkart_price = soup.select('._1_WHN1')[0].getText().strip()
            flipkart_name = soup.select('._4rR01T')[0].getText().strip()

            return f"{flipkart_name}\nPrice : {flipkart_price}\n"
        else:
            flipkart_price = 'Product Not Found'
        return flipkart_price
    except:
        flipkart_price = 'Product Not Found'
    return flipkart_price


def ebay_search(name):
    try:
        global ebay
        name1 = name.replace(" ", "+")
        ebay = f'https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw={name1}&_sacat=0'
        res = requests.get(f'https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw={name1}&_sacat=0', headers=headers)

        soup = BeautifulSoup(res.text, 'html.parser')
        length = soup.select('.s-item__price')
        ebay_page_length = int(len(length))

        for i in range(0, ebay_page_length):
            info = soup.select('.SECONDARY_INFO')[i].getText().strip().upper()
            info = info.upper()
            if info == 'BRAND NEW':
                ebay_name = soup.select('.s-item__title')[i].getText().strip()
                name = name.upper()
                ebay_name = ebay_name.upper()

                if name in ebay_name[:25]:
                    ebay_price = soup.select('.s-item__price')[i].getText().strip()
                    ebay_name = soup.select('.s-item__title')[i].getText().strip()

                    ebay_price = ebay_price.replace("INR", "₹")
                    ebay_price = ebay_price[0:14]
                    return f"{ebay_name}\nPrice : {ebay_price}\n"

                else:
                    i += 1
                    i = int(i)
                    if i == ebay_page_length:
                        ebay_price = 'Product Not Found'
                        break

        return f"{ebay_name}\nPrice : {ebay_price}\n"
    except:
        ebay_price = 'Product Not Found'
    return ebay_price


def croma_search(name):
    try:
        global croma
        name1 = name.replace(" ", "+")
        croma = f'https://www.croma.com/search/?text={name1}'
        res = requests.get(f'https://www.croma.com/search/?text={name1}', headers=headers)

        soup = BeautifulSoup(res.text, 'html.parser')
        croma_name = soup.select('h3')

        croma_page_length = int(len(croma_name))
        for i in range(0, croma_page_length):
            name = name.upper()
            croma_name = soup.select('h3')[i].getText().strip().upper()

            if name in croma_name.upper()[:25]:
                croma_name = soup.select('h3')[i].getText().strip().upper()
                croma_price = soup.select('.pdpPrice')[i].getText().strip()
                return f"{croma_name}\nPrice : {croma_price}\n"
            else:
                i += 1
                i = int(i)
                if i == croma_page_length:
                    croma_price = 'Product Not Found'
                    break

        return f"{croma_name}\nPrice : {croma_price}\n"
    except:
        croma_price = 'Product Not Found'
    return croma_price


def amazon_search(name):
    try:
        global amazon
        name1 = name.replace(" ", "-")
        name2 = name.replace(" ", "+")
        amazon = f'https://www.amazon.in/{name1}/s?k={name2}'
        res = requests.get(f'https://www.amazon.in/{name1}/s?k={name2}', headers=headers)

        soup = BeautifulSoup(res.text, 'html.parser')
        amazon_page = soup.select('.a-color-base.a-text-normal')
        amazon_page_length = int(len(amazon_page))

        for i in range(0, amazon_page_length):
            name = name.upper()
            amazon_name = soup.select('.a-color-base.a-text-normal')[i].getText().strip().upper()

            if name in amazon_name[0:20]:
                amazon_name = soup.select('.a-color-base.a-text-normal')[i].getText().strip().upper()
                amazon_price = soup.select('.a-price-whole')[i].getText().strip().upper()
                return f"{amazon_name}\nPrice : {amazon_price}\n"
            else:
                i += 1
                i = int(i)
                if i == amazon_page_length:
                    amazon_price = 'Product Not Found'
                    break

        return f"{amazon_name}\nPrice : {amazon_price}\n"
    except:
        amazon_price = 'Product Not Found'
    return amazon_price


def urls():
    global flipkart, ebay, croma, amazon, olx
    return f"{flipkart}\n\n\n{ebay}\n\n\n{croma}\n\n\n{amazon}\n\n\n{olx}"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product_name = request.form['product_name']
        t1 = flipkart_search(product_name)
        t2 = ebay_search(product_name)
        t3 = croma_search(product_name)
        t4 = amazon_search(product_name)

        return render_template('index.html', t1=t1, t2=t2, t3=t3, t4=t4, t5='', t6=urls())

    return render_template('index.html', t1='', t2='', t3='', t4='', t5='', t6='')


if __name__ == '_main_':
    app.run(debug=True)