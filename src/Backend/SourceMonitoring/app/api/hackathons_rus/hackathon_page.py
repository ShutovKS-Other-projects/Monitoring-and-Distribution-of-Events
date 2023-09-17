import requests
from bs4 import BeautifulSoup


def get_url(response: requests.Response) -> str:
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    html_segment = soup.find_all('div', class_='t-feed__post-popup__container t-container t-popup__container t-popup__container-static')[0]
    return html_segment.find('meta', itemprop='mainEntityOfPage')['content']


def get_image_url(response: requests.Response) -> str:
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    html_segment = soup.find_all('div', class_='t-feed__post-popup__container t-container t-popup__container t-popup__container-static')[0]
    return html_segment.find('img', itemprop='image')['src']


def get_name(response: requests.Response) -> str:
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    html_segment = soup.find_all('div', class_='t-feed__post-popup__container t-container t-popup__container t-popup__container-static')[0]
    return html_segment.find('h1', itemprop='name').text.strip()


def get_type_participation(response: requests.Response) -> str:
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    html_segment = soup.find_all('div', class_='t-feed__post-popup__container t-container t-popup__container t-popup__container-static')[0]
    tag_elements = soup.find_all('span', class_='t-uptitle t-uptitle_xs')
    tag_texts = [tag.text for tag in tag_elements]
    type_participation = None
    for tag_text in tag_texts:
        if tag_text == 'online':
            type_participation = 'online'
        elif tag_text == 'offline':
            if type_participation is None:
                type_participation = 'offline'
            else:
                type_participation += '/offline'
    return type_participation


def get_description(response: requests.Response) -> str:
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    html_segment = soup.find_all('div', class_='t-feed__post-popup__container t-container t-popup__container t-popup__container-static')[0]
    feed_text = html_segment.find('div', id='feed-text')
    description = feed_text.text
    trigger = feed_text.find('strong').text
    split_text = description.split(trigger)
    return split_text[0].strip() if len(split_text) > 1 else ""


def get_registration_end_date(response: requests.Response) -> str:
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    html_segment = soup.find('div', class_='t-feed__post-popup__container t-container t-popup__container t-popup__container-static')
    ol_element = html_segment.find('ol')
    if ol_element:
        list_items = ol_element.find_all('li')
        for item in list_items:
            if 'Регистрация до' in item.text:
                registration_end_date = item.text
                break
    return registration_end_date


def get_info_from_hackathon_page(response: requests.Response):
    url = get_url(response)
    image_url = get_image_url(response)
    name = get_name(response)
    type_participation = get_type_participation(response)
    description = get_description(response)
    registration_end_date = get_registration_end_date(response)
    return dict(
        url=url,
        name=name,
        image_url=image_url,
        description=description,
        type_participation=type_participation,
        registration_end_date=registration_end_date)
