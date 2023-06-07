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
            page_id = int(input_text[0]) 
            input_text = input_text[2:]
            local_url = url + f'index.php?page=post&s=list&tags={input_text}&pid={page_id*number_images}'
        except:
            local_url = url + f'index.php?page=post&s=list&tags={input_text}&pid=0'
            page_id = 0
    else:
        local_url = url + f'index.php?page=post&s=list&tags={input_text}&pid=0'
        page_id = 0
    return local_url, input_text, page_id

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

def extract_image_urls(links, score_threshold):
    """
    Extracts the image URLs from the given links, filtering out images below the score threshold.
    """
    images = []
    for link in links:
        img_response = requests.get(link, headers=headers)
        if img_response.status_code == 200:
            img_soup = BeautifulSoup(img_response.text, 'html.parser')
            img_tags = img_soup.find_all('img', id='image')
            for img in img_tags:
                img_src = img['src'].split('?', 1)[0]
                score = int(img_soup.find('span', id='psc' + img['src'].split('?')[-1]).text)
                if score >= score_threshold:
                    images.append(img_src)
    return images

def trending_list():
    tags_url = url + 'index.php?page=toptags'
    response = requests.get(tags_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', class_='server-assigns')
    rows = table.find_all('tr')
    
    tags = ""  # String to store the tags
    
    for row in rows[2:]:
        rank = row.find_all('td')[0].text.strip()[1:]
        tag = row.find_all('td')[1].text.strip()
        tags += rank + '. ' + '/tag_' + tag + "\n"  # Add the tag to the tags string with a new line
    
    return tags  # Return the string of tags
