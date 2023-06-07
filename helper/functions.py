import requests
from bs4 import BeautifulSoup
import time

url = os.getenv('url')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

def get_local_url(input_text, number_images):
    if input_text.startswith('/more'):
        input_text = input_text.replace('/more', '')
        num = int(input_text[0]) * number_images
        input_text = input_text[2:]
        local_url = url + f'index.php?page=post&s=list&tags={input_text}&pid={num}'
    else:
        local_url = url + f'index.php?page=post&s=list&tags={input_text}&pid=0'
    return local_url

def get_links(counter, response):
    soup = BeautifulSoup(response.text, 'html.parser')
    links = ""

    a_tags = soup.find_all('a')

    for a in a_tags:
        href = a.get('href')
        if 's=view' in href:
            absolute_url = requests.compat.urljoin(url, href)
            links += absolute_url
            links += '\n'
            counter -= 1
        if counter == 0:
            break
    return links

def get_image_urls(links):
    images = []
    for i in links.splitlines():
        img_response = requests.get(i, headers=headers)
        if img_response.status_code == 200:
            img_soup = BeautifulSoup(img_response.text, 'html.parser')
            img_tags = img_soup.find_all('img', id='image')
            for img in img_tags:
                img_src = img['src'].split('?', 1)[0]
                images.append(img_src)
    return images
