import requests
from bs4 import BeautifulSoup
import os

url = os.getenv('url')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

def construct_local_url(input_text, number_images):
    """
    Constructs the local URL based on the input text and number of images.
    """
    if input_text.startswith('/more'):
        input_text = input_text.replace('/more', '')
        try:
            num = int(input_text[0]) * number_images
            input_text = input_text[2:]
            local_url = url + f'index.php?page=post&s=list&tags={input_text}&pid={num}'
        except:
            local_url = url + f'index.php?page=post&s=list&tags={input_text}&pid=0'
    else:
        local_url = url + f'index.php?page=post&s=list&tags={input_text}&pid=0'
    return local_url

def extract_links(counter, response):
    """
    Extracts the links from the response HTML based on the counter.
    """
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []

    a_tags = soup.find_all('a')

    for a in a_tags:
        href = a.get('href')
        if 's=view' in href:
            absolute_url = requests.compat.urljoin(url, href)
            links.append(absolute_url)
            counter -= 1
        if counter == 0:
            break
    return links

def extract_image_urls(links):
    """
    Extracts the image URLs from the given links.
    """
    images = [img['src'].split('?', 1)[0] for link in links for img in BeautifulSoup(requests.get(link, headers=headers).text, 'html.parser').find_all('img', id='image')]
    return images
