import requests
import json
import string
from bs4 import BeautifulSoup


url = 'https://www.cfcunderwriting.com/en-gb/'

def get_soup(url):
    """A function to convert a url using BeautifulSoup"""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup

soup = get_soup(url)

def find_list_resources(tag, attribute, soup):
    """ A function to list all the resources within a given tag"""
    resources = []
    for x in soup.find_all(tag):
        try:
            resources.append(x[attribute])
        except KeyError:
            pass
    return resources


def external_resources(soup):
    """A function write all external resources from a website
    into a json file created in current directory"""
    # create list of all tags within html
    tag_list = []
    for tag in soup.find_all(True):
        if tag.name in tag_list:
            pass
        else:
            tag_list.append(tag.name)
    # create list of all sources
    source_list = [
        source for tag in tag_list
        for source in find_list_resources(tag, "src", soup)
    ]
    # create list of external sources
    external_sources = [source for source in source_list if 'http' in source]
    # create json file in current directory
    with open("external_sources.json", "w") as j:
        json.dump(external_sources, j)
    return None

def enumerate_hyperlinks(soup):
    """A function to return a list of enumerated hyperlinks"""
    hyperlinks = [
        resource for resource in find_list_resources("a", "href", soup)
        if resource != '#' and resource != 'javascript:;'
    ]
    numbered_hyperlinks = [(number, link)
                       for number, link in enumerate(hyperlinks,1)]
    return numbered_hyperlinks


def loc_privacy_policy(soup):
    """A function to produce url of privacy policy using list of hyperlinks on
    index page"""
    for item in enumerate_hyperlinks(soup):
        if "privacy" in item[1]:
            new_url = url + item[1].strip('/en-gb')
    return new_url

new_soup = get_soup(loc_privacy_policy(soup))

def word_frequency(new_soup):
    """A function to write a word frequency json file for all visible words
    for a given url"""
    # use BeautifulSoup to produce list of all strings
    stripped = [text for text in new_soup.stripped_strings]
    # join all words for processing as string
    content = " "
    all_privacy_content = content.join(stripped)
       # remove unicode
    all_privacy_content = all_privacy_content.replace('\xa0', '')
    # remove punctuation and a case
    for punctuation in string.punctuation:
        all_privacy_content = all_privacy_content.replace(punctuation, '').lower()
    # remove numbers
    all_privacy_content = ''.join(word for word in all_privacy_content
                                  if not word.isdigit())
    # split out all words for counting
    separate_strings = all_privacy_content.split(' ')
    # count!
    frequencies = set()
    for word in separate_strings:
        frequencies.add((word, separate_strings.count(word)))
    frequencies = list(frequencies)
    # create json file in current directory
    with open("word_frequencies.json", "w") as j:
        json.dump(frequencies, j)
    return None


if __name__ == '__main__':
    url = 'https://www.cfcunderwriting.com/en-gb/'
    soup = get_soup(url)
    external_resources(soup)
    print("Created external resources JSON in current directory")
    print(enumerate_hyperlinks(soup))
    print(loc_privacy_policy(soup))
    new_soup = get_soup(loc_privacy_policy(soup))
    word_frequency(new_soup)
    print("Created word frequency JSON in current directory")
