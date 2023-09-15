import json
import requests

url = "https://feeds.tildacdn.com/api/getfeed/?feeduid=617755803461&recid=488758159&c=1694767429185&size=16&slice=1&sort%5Bdate%5D=desc&filters%5Bdate%5D%5B%3C%5D=now&getparts=true"


def get_links_to_hackathons(response: requests.Response):
    urls = []

    result = response.text
    json_text = json.loads(result)
    posts = json_text['posts']
    for post in posts:
        urls.append(post['url'])

    return urls
