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
amazon_url = ''
olx_url = '' 



def flipkart(name=""):
    global flipkart_url
    try:
        flipkart_url = f'https://www.flipkart.com/search?q={name}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off'
        res = requests.get(flipkart_url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        flipkart_name = soup.select('._4rR01T')[0].getText().strip().upper()

        if name.upper() in flipkart_name:
            flipkart_price = soup.select('._1_WHN1')[0].getText().strip()
            flipkart_name = soup.select('._4rR01T')[0].getText().strip().upper()
            cxw8mj_element = soup.select_one('.CXW8mj')
            image_element = cxw8mj_element.select_one('img')
            image_url = image_element.get('src')
            global flipcart_img 
            flipcart_img = image_url
            return f"{flipkart_name}\nPrice: {flipkart_price}\n"
    
        # return 'Product Not Found'
    except:
         return 'Product Not Found'
    

ebay_n1 = ebay_n2 = ebay_n3 = ""
ebay_p1 = ebay_p2 = ebay_p3 = ""
ebay_i1 = ebayi2 = ebay_i3 = ""

def ebay(name):
    global ebay_url
    ebay_url = f'https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw={name}&_sacat=0'
    res = requests.get(ebay_url, headers=headers)

    soup = BeautifulSoup(res.text, 'html.parser')

    product_name = soup.find_all("div", class_="s-item__title")
    price = soup.find_all("span", class_="s-item__price")

    cxw8mj_element = soup.find_all('div', class_='s-item__image-section')

    product_url = soup.find_all("a", class_="s-item__link")
    ebay_results = []
    ebay1 = []
    ebay2 = []
    ebay3 = []
    ebay_n1 = product_name[1].text
    ebay_p1 = price[1].text
    ebay_i1 = cxw8mj_element[1].find('img')['src']
    ebay1 = [ebay_n1, ebay_p1, ebay_i1]
    ebay_n2 = product_name[2].text
    ebay_p2 = price[2].text
    ebay_i2 = cxw8mj_element[2].find('img')['src']
    ebay2 = [ebay_n2, ebay_p2, ebay_i2]
    ebay_n3 = product_name[3].text
    ebay_p3 = price[3].text
    ebay_i3 = cxw8mj_element[3].find('img')['src']
    ebay3 = [ebay_n3, ebay_p3, ebay_i3]
    

    ebay_results = [ebay1, ebay2, ebay3]

    return ebay_results 


def amazon(name):
    global amazon_url
    amazon_url = f'https://www.amazon.in/{name.replace(" ", "-")}/s?k={name.replace(" ", "+")}'
    res = requests.get(amazon_url, headers=headers)
    # Your existing amazon function code
    soup = BeautifulSoup(res.text, 'html.parser')
    amazon_name_elements = soup.select('.a-color-base.a-text-normal')
    amazon_page_length = len(amazon_name_elements)

    for i in range(0, amazon_page_length):
            name = name.upper()
            amazon_name = amazon_name_elements[i].getText().strip().upper()

            if name in amazon_name[0:20]:
                amazon_name = amazon_name_elements[i].getText().strip().upper()
                amazon_price = soup.select('.a-price-whole')[i].getText().strip().upper()
                return f"{amazon_name}\nPrice : {amazon_price}\n"
            
            return 'Product Not Found'

   
    
olx_n1 = olx_n2 = olx_n3 = ""
olx_p1 = olx_p2 = olx_p3 = ""
olx_i1 = olx_i2 = olx_i3 = ""
def olx(name):
    global olx_url
    olx_url = f'https://www.olx.in/items/q-{name.replace(" ", "-")}?isSearchCall=true'
    res = requests.get(olx_url, headers=headers)

    soup = BeautifulSoup(res.text, 'html.parser')
    product_name = soup.find_all("span", class_="_2poNJ")
    price = soup.find_all("span", class_="_2Ks63")
    image_element = soup.find_all('figure', class_='_3UrC5')

    olx_results = []
    olx1 = []
    olx2 = []
    olx3 = []
    olx_n1 = product_name[1].text
    olx_p1 = price[1].text
    olx_i1 = image_element[1].find('img')['src']
    olx1 = [olx_n1, olx_p1, olx_i1]
    olx_n2 = product_name[2].text
    olx_p2 = price[2].text
    olx_i2 = image_element[1].find('img')['src']
    olx2 = [olx_n2, olx_p2, olx_i2]
    olx_n3 = product_name[3].text
    olx_p3 = price[3].text
    olx_i3 = image_element[1].find('img')['src']
    olx3 = [olx_n3, olx_p3, olx_i3]

    olx_results = [olx1,olx2,olx3]

    # for i in range(1,4):
    #     olx_results += product_name[i].text + "\n" + price[i].text + "\n" + image_element[i].find('img')['src'] + "\n\n\n"

    return olx_results    

    



def urls():
    return f"{flipkart_url}\n\n\n{ebay_url}\n\n\n{amazon_url}\n\n\n{olx_url}"


def open_urls():
    webbrowser.open_new(flipkart_url)
    webbrowser.open_new(ebay_url)
    # webbrowser.open_new(croma_url)
    webbrowser.open_new(amazon_url)
    webbrowser.open_new(olx_url)

default_intro = "Discover unbeatable deals at PricePulse! Compare prices effortlessly, navigate the best bargains, and transform your shopping experience. Empower your purchases with smart choices and significant savings. Welcome to a world where every click counts! 💻💱💵"


@app.route('/')
def index():
    return render_template('index.html',default_intro = default_intro)


@app.route('/search', methods=['POST'])
def search():
    product_name = request.form['product_name']

    flipkart(product_name)
    ebay(product_name)
    # croma(product_name)
    amazon(product_name)
    olx(product_name)
    t6 = urls()

    t2=ebay(product_name)
    prod1 = t2[0]
    prod2 = t2[1]
    prod3 = t2[2]
    ebay_i1M = prod1[2]
    ebay_i2M = prod2[2]
    ebay_i3M = prod3[2]

    t5=olx(product_name)
    p1 = t5[0]
    p2 = t5[1]
    p3 = t5[2]
    olx_i1M = p1[2]
    olx_i2M = p2[2]
    olx_i3M = p3[2]

    print(p1[2]+ " " + p2[2] + " " + p3[2])

    return render_template('index.html', t6=t6,t1=flipkart(product_name),ebay1=prod1,ebay2 = prod2,ebay3 = prod3,ebay_i1M = ebay_i1M,ebay_i2M = ebay_i2M,ebay_i3M=ebay_i3M,t4=amazon(product_name), olx1 = p1, olx2 = p2, olx3 = p3, olx_i1M=olx_i1M, olx_i2M = olx_i2M, olx_i3M=olx_i3M, flipcart_img = flipcart_img )

if __name__ == '__main__':
    app.run(debug=True)

