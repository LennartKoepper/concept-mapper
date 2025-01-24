from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib import request


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False

    if isinstance(element, Comment):
        return False

    return True


def text_from_html(body):
    """returns the visible text from the given html body without tags"""

    soup = BeautifulSoup(body, 'html.parser')

    # find all strings on website
    texts = soup.find_all(string=True)

    # filter unvisible strings
    visible_texts = filter(tag_visible, texts)

    # remove excessive whitespace and join the texts
    return u' '.join(t.strip() for t in visible_texts)


def scrape_visible_text(url: str) -> str:
    """scrapes the visible text from the website with the given url"""
    return text_from_html(request.urlopen(url).read())
