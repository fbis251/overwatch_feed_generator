#!/usr/bin/env python
import json
import sys

from bs4 import BeautifulSoup

# Constants
DEBUG = False
DEFAULT_AUTHOR = "Overwatch PC Team"
DEFAULT_URL = "https://playoverwatch.com/en-us/game/patch-notes/pc/"

# Error Constants
EXIT_ERROR_PATCH_PARSE = 'Error while parsing patch versions'
EXIT_ERROR_PATCH_POST_NOT_FOUND = 'Error while finding post contents by ID'


# Provides information about patches including the version and the ID of the post element that
# contains the patch details
class Patch:
    title = ''
    date = ''
    element_id = ''

    def __init__(self, title, date, element_id):
        self.title = title
        self.date = date
        self.element_id = element_id


# Begin parsing the patches page
soup = BeautifulSoup(open('posts.html'), 'html.parser')

# Remove some elements that will add unnecessary whitespace in the feed
for element in soup.select('svg.IconHeading-icon'):
    element.decompose()
for element in soup.select('img.HeroHeader-image-mobile'):
    element.decompose()

patches = []
# Get the list of patch versions and post ID's from the sidebar
for patch in soup.find_all("li", class_="PatchNotesSideNav-listItem"):
    title = ''
    title_element = patch.select_one('h3')
    if title_element is not None:
        title = title_element.get_text(strip=True)

    date = ''
    date_element = patch.select_one('p.u-float-right')
    if date_element is not None:
        date = date_element.get_text(strip=True)

    element_id = ''  # The ID of the element that contains this patch's update notes
    patch_element = patch.select_one('a')
    if patch_element is not None:
        element_id = patch_element.get('href')
        if element_id.startswith('#'):
            element_id = element_id[1:]

    if not (title == "" or date == "" or element_id == ""):
        if DEBUG:
            print("valid patch title: [{}], date: [{}], version_element_id: [{}]".format(title, date, element_id))
        patches.append(Patch(title=title, date=date, element_id=element_id))
    else:
        sys.exit(EXIT_ERROR_PATCH_PARSE)

posts = []
for patch in patches:
    if DEBUG:
        print(
            "parsing post for patch, title: [{}], date: [{}], version_element_id: [{}]".format(patch.title,
                                                                                               patch.date,
                                                                                               patch.element_id))

    patch_id = patch.element_id
    patch_div = soup.find('div', {'id': patch_id})
    if patch_div is None:
        print("patch not found, title: [{}], date: [{}], version_element_id: [{}]".format(patch.title,
                                                                                          patch.date,
                                                                                          patch.element_id),
              file=sys.stderr)
        sys.exit(EXIT_ERROR_PATCH_POST_NOT_FOUND)
    title = patch.title
    author = DEFAULT_AUTHOR
    date = patch.date
    description = patch_div.decode_contents()  # Get the patch info DIV contents (innerHTML) as the post body
    url = DEFAULT_URL + '#' + patch_id

    posts.append({
        'title': title,
        'author': author,
        'date': date,
        'url': url,
        'description': description
    })

print(json.dumps(posts, indent=True))
