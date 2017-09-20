#!/usr/bin/env python
from bs4 import BeautifulSoup
import json

DEFAULT_AUTHOR = "Overwatch PC Team"
DEFAULT_URL = "https://playoverwatch.com/en-us/game/patch-notes/pc/"

class NewsPost:
    title = ""
    author = ""
    date = ""
    url = ""
    description = ""

    def __init__(self, title, author, url, description):
        self.title = title
        self.author = author
        self.url = url
        self.description = description

        # Dates are separated from titles via an emdash
        split = title.split(" \u2013 ")
        if len(split) == 2:
            self.date = split[len(split) - 1]
        else:
            # emdash wasn't used in title split, try to use regular hyphen
            split = title.split(" - ")
            if len(split) == 2:
                self.date = split[len(split) - 1]

soup = BeautifulSoup(open('posts.html'), 'html.parser')
posts = []
for patch_info in soup.find_all("div", attrs={"class": "patch-notes-body"}):
    title = ""
    author = DEFAULT_AUTHOR
    description = ""
    url = DEFAULT_URL

    patch_id = patch_info.get('id')
    if patch_id is not None:
        # Append patch ID anchor to the base URL
        url = url + '#' + patch_id

    titleList = patch_info.select('h1')
    if len(titleList) > 0:
        title = titleList[0].get_text(strip=True)

    content_number = 0
    for contents in patch_info.contents:
        content_number += 1
        if content_number < 2:
            # Skip the first two children since they're just the <h1> for the title and a \n
            continue
        description += str(contents)

    post = NewsPost(title, author, url, description)
    json_entry = {}
    json_entry['title'] = post.title
    json_entry['author'] = post.author
    json_entry['date'] = post.date
    json_entry['url'] = post.url
    json_entry['description'] = post.description
    posts.append(json_entry)

print(json.dumps(posts))
