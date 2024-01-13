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
    try:
        global flipkart
        name1 = name.replace(" ","+")   #iphone x  -> iphone+x
        flipkart=f'https://www.flipkart.com/search?q={name1}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off'
        res = requests.get(f'https://www.flipkart.com/search?q={name1}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off',headers=headers)

        soup = BeautifulSoup(res.text,'html.parser')
        flipkart_name = soup.select('._4rR01T')[0].getText().strip()  ### New Class For Product Name
        flipkart_name = flipkart_name.upper()
        if name.upper() in flipkart_name:
            flipkart_price = soup.select('._1_WHN1')[0].getText().strip()  ### New Class For Product Price
            flipkart_name = soup.select('._4rR01T')[0].getText().strip()

            return f"{flipkart_name}\nPrise : {flipkart_price}\n"
        else:

            flipkart_price='           Product Not Found'
        return flipkart_price
    except:

        flipkart_price= '           Product Not Found'
    return flipkart_price


def ebay(name):
    global ebay_url
    ebay_url = f'https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw={name}&_sacat=0'
    res = requests.get(ebay_url, headers=headers)
    try:
        global ebay
        name1 = name.replace(" ","+")
        ebay=f'https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw={name1}&_sacat=0'
        res = requests.get(f'https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw={name1}&_sacat=0',headers=headers)

        soup = BeautifulSoup(res.text,'html.parser')
        length = soup.select('.s-item__price')
        ebay_page_length=int(len(length))
        for i in range (0,ebay_page_length):
            info = soup.select('.SECONDARY_INFO')[i].getText().strip()
            info = info.upper()
            if info=='BRAND NEW':
                ebay_name = soup.select('.s-item__title')[i].getText().strip()
                name=name.upper()
                ebay_name=ebay_name.upper()
                if name in ebay_name[:25]:
                    ebay_price = soup.select('.s-item__price')[i].getText().strip()
                    ebay_name = soup.select('.s-item__title')[i].getText().strip()

                    ebay_price = ebay_price.replace("INR","₹")

                    ebay_price=ebay_price[0:14]
                    break
                    return f"{ebay_name}\nPrise : {ebay_price}\n"

                else:
                    i+=1
                    i=int(i)
                    if i==ebay_page_length:

                        ebay_price = '           Product Not Found'
                        break

        return f"{ebay_name}\nPrise : {ebay_price}\n"
    except:

        ebay_price = '           Product Not Found'
    return ebay_price


def croma(name):
    global croma_url
    croma_url = f'https://www.croma.com/search/?text={name}'
    res = requests.get(croma_url, headers=headers)
    try:
        global croma
        name1 = name.replace(" ","+")
        croma=f'https://www.croma.com/search/?text={name1}'
        res = requests.get(f'https://www.croma.com/search/?text={name1}',headers=headers)

        soup = BeautifulSoup(res.text,'html.parser')
        croma_name = soup.select('h3')

        croma_page_length = int( len(croma_name))
        for i in range (0,croma_page_length):
            name = name.upper()
            croma_name = soup.select('h3')[i].getText().strip().upper()
            if name in croma_name.upper()[:25]:
                croma_name = soup.select('h3')[i].getText().strip().upper()
                croma_price = soup.select('.pdpPrice')[i].getText().strip()

                break
            else:
                i+=1
                i=int(i)
                if i==croma_page_length:

                    croma_price = '           Product Not Found'
                    break

        return f"{croma_name}\nPrise : {croma_price}\n"
    except:

        croma_price = '           Product Not Found'
    return croma_price

def amazon(name):
    global amazon_url
    amazon_url = f'https://www.amazon.in/{name.replace(" ", "-")}/s?k={name.replace(" ", "+")}'
    res = requests.get(amazon_url, headers=headers)
    try:
        global amazon
        name1 = name.replace(" ","-")
        name2 = name.replace(" ","+")
        amazon=f'https://www.amazon.in/{name1}/s?k={name2}'
        res = requests.get(f'https://www.amazon.in/{name1}/s?k={name2}',headers=headers)

        soup = BeautifulSoup(res.text,'html.parser')
        amazon_page = soup.select('.a-color-base.a-text-normal')
        amazon_page_length = int(len(amazon_page))
        for i in range(0,amazon_page_length):
            name = name.upper()
            amazon_name = soup.select('.a-color-base.a-text-normal')[i].getText().strip().upper()
            if name in amazon_name[0:20]:
                amazon_name = soup.select('.a-color-base.a-text-normal')[i].getText().strip().upper()
                amazon_price = soup.select('.a-price-whole')[i].getText().strip().upper()

                break
            else:
                i+=1
                i=int(i)
                if i==amazon_page_length:

                    amazon_price = '           Product Not Found'
                    break
        return f"{amezon_name}\nPrise : {amezon_price}\n"
    except:

        amazon_price = '           Product Not Found'
    return amazon_price


def olx(name):
    global olx_url
    olx_url = f'https://www.olx.in/items/q-{name.replace(" ", "-")}?isSearchCall=true'
    res = requests.get(olx_url, headers=headers)
    try:
        global olx
        name1 = name.replace(" ","-")
        olx=f'https://www.olx.in/items/q-{name1}?isSearchCall=true'
        res = requests.get(f'https://www.olx.in/items/q-{name1}?isSearchCall=true',headers=headers)

        soup = BeautifulSoup(res.text,'html.parser')
        olx_name = soup.select('._2tW1I')
        olx_page_length = len(olx_name)
        for i in range(0,olx_page_length):
            olx_name = soup.select('._2tW1I')[i].getText().strip()
            name = name.upper()
            olx_name = olx_name.upper()
            if name in olx_name:
                olx_price = soup.select('._89yzn')[i].getText().strip()
                olx_name = soup.select('._2tW1I')[i].getText().strip()
                olx_loc = soup.select('.tjgMj')[i].getText().strip()
                try:
                    label = soup.select('._2Vp0i span')[i].getText().strip()
                except:
                    label = "OLD"

                break
            else:
                i+=1
                i=int(i)
                if i==olx_page_length:

                    olx_price = '           Product Not Found'
                    break
        return f"{olx_name}\nPrise : {olx_price}\n"
    except:

        olx_price = '           Product Not Found'
    return olx_price


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
