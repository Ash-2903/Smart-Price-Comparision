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
    try:
        flipkart_url = f'https://www.flipkart.com/search?q={name}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off'
        res = requests.get(flipkart_url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        flipkart_name = soup.select('._4rR01T')[0].getText().strip().upper()

        if name.upper() in flipkart_name:
            flipkart_price = soup.select('._1_WHN1')[0].getText().strip()
            flipkart_name = soup.select('._4rR01T')[0].getText().strip().upper()
            return f"{flipkart_name}\nPrice: {flipkart_price}\n"
    
        return 'Product Not Found'
    except:
         return 'Product Not Found'
    

def ebay(name):
    global ebay_url
    ebay_url = f'https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw={name}&_sacat=0'
    res = requests.get(ebay_url, headers=headers)

    soup = BeautifulSoup(res.text, 'html.parser')


    product_name = soup.find_all("div", class_="s-item__title")
    price = soup.find_all("span", class_="s-item__price")

    cxw8mj_element = soup.find_all('div', class_='s-item__image-section')

    product_url = soup.find_all("a", class_="s-item__link")
    ebay_results = ""
    for i in range(1,len(product_name)):
        ebay_results += product_name[i].text + "\n" + price[i].text + "\n" + cxw8mj_element[i].find('img')['src'] + "\n" + product_url[i].get('href') + "\n\n\n"
        if(i==3):
             break
    return ebay_results

    


def croma(name):
    global croma_url
    croma_url = f'https://www.croma.com/search/?text={name}'
    res = requests.get(croma_url, headers=headers)
    # Your existing croma function code
    soup = BeautifulSoup(res.text, 'html.parser')
    croma_name_elements = soup.select('h3')

    croma_page_length = len(croma_name_elements)

    for i in range(0, croma_page_length):
            name = name.upper()
            croma_name = croma_name_elements[i].getText().strip().upper()

            if name in croma_name[:25]:
                croma_name = croma_name_elements[i].getText().strip().upper()
                croma_price = soup.select('.pdpPrice')[i].getText().strip()
                return f"{croma_name}\nPrice : {croma_price}\n"
            
            return 'Product Not Found'

    


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

   
    

def olx(name):
    global olx_url
    olx_url = f'https://www.olx.in/items/q-{name.replace(" ", "-")}?isSearchCall=true'
    res = requests.get(olx_url, headers=headers)

    soup = BeautifulSoup(res.text, 'html.parser')
    product_name = soup.find_all("span", class_="_2poNJ")
    price = soup.find_all("span", class_="_2Ks63")
    image_element = soup.find_all('figure', class_='_3UrC5')

    olx_results = ""

    for i in range(1,4):
        olx_results += product_name[i].text + "\n" + price[i].text + "\n" + image_element[i].find('img')['src'] + "\n\n\n"

    return olx_results
        # print(product_name[i].text)
        # print(price[i].text)
        # print(image_element[i].find('img')['src'])
        # print("\n")
    # olx_name_elements = soup.select('._2tW1I')
    # olx_page_length = len(olx_name_elements)

    # for i in range(0, olx_page_length):
    #         name = name.upper()
    #         olx_name = olx_name_elements[i].getText().strip().upper()

    #         if name in olx_name:
    #             olx_price = soup.select('._89yzn')[i].getText().strip()
    #             olx_name = olx_name_elements[i].getText().strip()
    #             olx_loc = soup.select('.tjgMj')[i].getText().strip()
    #             try:
    #                 label = soup.select('._2Vp0i span')[i].getText().strip()
    #             except:
    #                 label = "OLD"

    #             return f"{olx_name}\nPrice : {olx_price}\nLocation : {olx_loc}\nLabel : {label}\n"
    #         return 'Product Not Found'
            

    
    



def urls():
    return f"{flipkart_url}\n\n\n{ebay_url}\n\n\n{croma_url}\n\n\n{amazon_url}\n\n\n{olx_url}"


def open_urls():
    webbrowser.open_new(flipkart_url)
    webbrowser.open_new(ebay_url)
    webbrowser.open_new(croma_url)
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
    croma(product_name)
    amazon(product_name)
    olx(product_name)
    t6 = urls()

    return render_template('index.html', t6=t6,t1=flipkart(product_name),t2=ebay(product_name),t3=croma(product_name),t4=amazon(product_name),t5=olx(product_name))

if __name__ == '__main__':
    app.run(debug=True)




# from flask import Flask, render_template, request, jsonify
# from bs4 import BeautifulSoup
# import requests
# import webbrowser
# from googletrans import Translator

# app = Flask(__name__)

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
# }

# flipkart_url = ''
# ebay_url = ''
# croma_url = ''
# amazon_url = ''
# olx_url = ''

# def flipkart(name=""):
#     global flipkart_url
#     try:
#         flipkart_url = f'https://www.flipkart.com/search?q={name}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off'
#         res = requests.get(flipkart_url, headers=headers)
#         soup = BeautifulSoup(res.text, 'html.parser')
#         flipkart_name = soup.select('._4rR01T')[0].getText().strip().upper()

#         if name.upper() in flipkart_name:
#             flipkart_price = soup.select('._1_WHN1')[0].getText().strip()
#             flipkart_name = soup.select('._4rR01T')[0].getText().strip().upper()
#             return f"{flipkart_name}\nPrice: {flipkart_price}\n"
#         return 'Product Not Found'
#     except:
#          return 'Product Not Found'

# def ebay(name):
#     global ebay_url
#     try:
#         ebay_url = f'https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw={name}&_sacat=0'
#         res = requests.get(ebay_url, headers=headers)
#         soup = BeautifulSoup(res.text, 'html.parser')
#         clearfix_elements = soup.select('.clearfix')

#         if len(clearfix_elements) >= 0:
#             for i in range(3):
#                 ebay_price_element = clearfix_elements[i].select_one('.s-item__price')
#                 ebay_title_element = clearfix_elements[i].select_one('.s-item__title')

#                 if ebay_price_element and ebay_title_element:
#                     ebay_price = ebay_price_element.getText().strip()
#                     ebay_title = ebay_title_element.getText().strip()

#                     ebay_price = ebay_price.replace("INR", "₹")
#                     ebay_price = ebay_price[0:14]

#                     return f"{ebay_title}\nPrice: {ebay_price}\n"
#         else:
#             return 'Product Not Found'
#     except:
#         return 'Product Not Found'

# def croma(name):
#     global croma_url
#     try:
#         croma_url = f'https://www.croma.com/search/?text={name}'
#         res = requests.get(croma_url, headers=headers)
#         soup = BeautifulSoup(res.text, 'html.parser')
#         croma_name_elements = soup.select('h3')
#         croma_page_length = len(croma_name_elements)

#         for i in range(0, croma_page_length):
#             name = name.upper()
#             croma_name = croma_name_elements[i].getText().strip().upper()

#             if name in croma_name[:25]:
#                 croma_name = croma_name_elements[i].getText().strip().upper()
#                 croma_price = soup.select('.pdpPrice')[i].getText().strip()
#                 return f"{croma_name}\nPrice : {croma_price}\n"
#         return 'Product Not Found'
#     except:
#         return 'Product Not Found'

# def amazon(name):
#     global amazon_url
#     try:
#         amazon_url = f'https://www.amazon.in/{name.replace(" ", "-")}/s?k={name.replace(" ", "+")}'
#         res = requests.get(amazon_url, headers=headers)
#         soup = BeautifulSoup(res.text, 'html.parser')
#         amazon_name_elements = soup.select('.a-color-base.a-text-normal')
#         amazon_page_length = len(amazon_name_elements)

#         for i in range(0, amazon_page_length):
#             name = name.upper()
#             amazon_name = amazon_name_elements[i].getText().strip().upper()

#             if name in amazon_name[0:20]:
#                 amazon_name = amazon_name_elements[i].getText().strip().upper()
#                 amazon_price = soup.select('.a-price-whole')[i].getText().strip().upper()
#                 return f"{amazon_name}\nPrice : {amazon_price}\n"
#         return 'Product Not Found'
#     except:
#         return 'Product Not Found'

# def olx(name):
#     global olx_url
#     try:
#         olx_url = f'https://www.olx.in/items/q-{name.replace(" ", "-")}?isSearchCall=true'
#         res = requests.get(olx_url, headers=headers)
#         soup = BeautifulSoup(res.text, 'html.parser')
#         olx_name_elements = soup.select('._2tW1I')
#         olx_page_length = len(olx_name_elements)

#         for i in range(0, olx_page_length):
#             name = name.upper()
#             olx_name = olx_name_elements[i].getText().strip().upper()

#             if name in olx_name:
#                 olx_price = soup.select('._89yzn')[i].getText().strip()
#                 olx_name = olx_name_elements[i].getText().strip()
#                 olx_loc = soup.select('.tjgMj')[i].getText().strip()
#                 try:
#                     label = soup.select('._2Vp0i span')[i].getText().strip()
#                 except:
#                     label = "OLD"

#                 return f"{olx_name}\nPrice : {olx_price}\nLocation : {olx_loc}\nLabel : {label}\n"
#         return 'Product Not Found'
#     except:
#         return 'Product Not Found'

# # def urls():
# #     return f"{flipkart_url}\n\n\n{ebay_url}\n\n\n{croma_url}\n\n\n{amazon_url}\n\n\n{olx_url}"
    

# def urls():
#     # Check if the URLs are defined before constructing the string
#     urls_list = [flipkart_url, ebay_url, croma_url, amazon_url, olx_url]
#     if any(url is None for url in urls_list):
#         return 'URLs are not available'
#     return f"{flipkart_url}\n\n\n{ebay_url}\n\n\n{croma_url}\n\n\n{amazon_url}\n\n\n{olx_url}"

# def open_urls():
#     webbrowser.open_new(flipkart_url)
#     webbrowser.open_new(ebay_url)
#     webbrowser.open_new(croma_url)
#     webbrowser.open_new(amazon_url)
#     webbrowser.open_new(olx_url)

# default_intro = "Discover unbeatable deals at PricePulse! Compare prices effortlessly, navigate the best bargains, and transform your shopping experience. Empower your purchases with smart choices and significant savings. Welcome to a world where every click counts! 💻💱💵"

# @app.route('/')
# def index():
#     return render_template('index.html', default_intro=default_intro)


# def translate_texts(text, lang):
#     translator = Translator()
#     detected_language = translator.detect(text).lang
#     print(f"Detected Language: {detected_language}")
#     print(f"Destination Language: {lang}")
#     translated_text = translator.translate(text, src=detected_language, dest=lang).text
#     return translated_text


# @app.route('/translate', methods=['POST'])
# def translate():
#     lang_code = request.form['lang_sel']
#     translated_text = translate_texts(default_intro, lang_code)
#     return render_template('index.html',default_intro=translated_text)



# @app.route('/search', methods=['POST'])
# def search():
#     product_name = request.form['product_name']

#     flipkart_data = flipkart(product_name)
#     ebay_data = ebay(product_name)
#     croma_data = croma(product_name)
#     amazon_data = amazon(product_name)
#     olx_data = olx(product_name)

#     t6 = urls()

#     return render_template('index.html', t6=t6, t1=flipkart_data, t2=ebay_data, t3=croma_data, t4=amazon_data, t5=olx_data)
# # def search():
# #     product_name = request.form['product_name']
# #     flipkart_data = flipkart(product_name)
# #     ebay_data = ebay(product_name)
# #     croma_data = croma(product_name)
# #     amazon_data = amazon(product_name)
# #     olx_data = olx(product_name)
# #     t6 = urls()
# #     return render_template('index.html', t6=t6, t1=flipkart_data, t2=ebay_data, t3=croma_data, t4=amazon_data, t5=olx_data)

# @app.route('/translate/search', methods=['POST'])
# def translate_search():
#     product_name = request.form['product_name']
#     flipkart_data = flipkart(product_name)
#     ebay_data = ebay(product_name)
#     croma_data = croma(product_name)
#     amazon_data = amazon(product_name)
#     olx_data = olx(product_name)
#     t6 = urls()
#     return render_template('index.html', t6=t6, t1=flipkart_data, t2=ebay_data, t3=croma_data, t4=amazon_data, t5=olx_data)



# if __name__ == '__main__':
#     app.run(debug=True)
