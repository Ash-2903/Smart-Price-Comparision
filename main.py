from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
import webbrowser

app = Flask(__name__)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

flipkart_url = ''
ebay_url = ''
croma_url = ''
amazon_url = ''
olx_url = ''


def flipkart(name=""):
    global flipkart_url
    flipkart_url = f'https://www.flipkart.com/search?q={name}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off'
    res = requests.get(flipkart_url, headers=headers)
    # Your existing flipkart function code


def ebay(name):
    global ebay_url
    ebay_url = f'https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw={name}&_sacat=0'
    res = requests.get(ebay_url, headers=headers)
    # Your existing ebay function code


def croma(name):
    global croma_url
    croma_url = f'https://www.croma.com/search/?text={name}'
    res = requests.get(croma_url, headers=headers)
    # Your existing croma function code


def amazon(name):
    global amazon_url
    amazon_url = f'https://www.amazon.in/{name.replace(" ", "-")}/s?k={name.replace(" ", "+")}'
    res = requests.get(amazon_url, headers=headers)
    # Your existing amazon function code


def olx(name):
    global olx_url
    olx_url = f'https://www.olx.in/items/q-{name.replace(" ", "-")}?isSearchCall=true'
    res = requests.get(olx_url, headers=headers)
    # Your existing olx function code


def urls():
    return f"{flipkart_url}\n\n\n{ebay_url}\n\n\n{croma_url}\n\n\n{amazon_url}\n\n\n{olx_url}"


def open_urls():
    webbrowser.open_new(flipkart_url)
    webbrowser.open_new(ebay_url)
    webbrowser.open_new(croma_url)
    webbrowser.open_new(amazon_url)
    webbrowser.open_new(olx_url)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    product_name = request.form['product_name']

    flipkart(product_name)
    ebay(product_name)
    croma(product_name)
    amazon(product_name)
    olx(product_name)
    t6 = urls()

    return render_template('index.html', t6=t6)


if __name__ == '__main__':
    app.run(debug=True)
