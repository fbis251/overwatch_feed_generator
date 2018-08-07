#!/usr/bin/env python
import json
import sys

from bs4 import BeautifulSoup

# Constants
DEFAULT_AUTHOR = "Overwatch PC Team"
DEFAULT_URL = "https://playoverwatch.com/en-us/game/patch-notes/pc/"

# Error Constants
EXIT_ERROR_PATCH_PARSE = 'Error while parsing patch versions'
EXIT_ERROR_PATCH_POST_NOT_FOUND = 'Error while finding post contents by ID'


# Provides information about patches including the version and the ID of the post element that
# contains the patch details
class Patch:
    title = ''
    element_id = ''

    def __init__(self, title, element_id):
        self.title = title
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

    version_element_id = ''
    version_element = patch.select_one('a')
    if version_element is not None:
        version_element_id = version_element.get('href')
        if version_element_id.startswith('#'):
            version_element_id = version_element_id[1:]

    if not (title == "" and version_element_id == ""):
        patches.append(Patch(title=title, element_id=version_element_id))
    else:
        sys.exit(EXIT_ERROR_PATCH_PARSE)

posts = []
for patch in patches:
    patch_id = patch.element_id
    patch_info = soup.find('div', {'id': patch_id})
    if patch_info is None:
        sys.exit(EXIT_ERROR_PATCH_POST_NOT_FOUND)
    title = patch.title
    author = DEFAULT_AUTHOR
    date = ''
    description = ''
    url = DEFAULT_URL

    if patch_id is not None:
        # Append patch ID anchor to the base URL
        url = url + '#' + patch_id

    # Try to get the date for a post that contains it
    header_list = patch_info.select('h1')
    post_title = ''
    if len(header_list) > 0:
        post_title = header_list[0].get_text(strip=True)
        # Dates are usually separated from titles via an emdash
        split = post_title.split(" \u2013 ")
        if len(split) == 2:
            date = split[len(split) - 1]
        else:
            # emdash wasn't used in title split, try to use regular hyphen
            split = post_title.split(" - ")
            if len(split) == 2:
                date = split[len(split) - 1]

    # Date is still blank, try to determine it from the post title
    if date == '':
        header_list = patch_info.select('h2.HeadingBanner-header')
        post_header_date = header_list[0].get_text(strip=True)
        if post_header_date != "":
            # MAKE SURE THE HEADER DATE IS NOT IN ALL CAPS FOR CONSISTENCY WITH OTHER DATES
            post_header_date = post_header_date.capitalize()
        date = post_header_date

    # Get the patch info DIV contents (innerHTML) as the post body
    description = patch_info.decode_contents()

    posts.append({
        'title': title,
        'author': author,
        'date': date,
        'url': url,
        'description': description
    })

print(json.dumps(posts, indent=True))
