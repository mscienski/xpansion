import requests
import lxml.html
import random

WIKIARTICLEURI = 'http://en.wikipedia.org/wiki/'
WIKIAPIURI = 'http://en.wikipedia.org/w/api.php'

def get_article_meta(term):
    payload = {
        'action': 'query',
        'format': 'json',
        'titles': term.lower() + '|' + term.upper()
    }

    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'identity, deflate, compress, gzip',
        'user_agent': 'Xpansion/0.1 (https://github.com/mscienski/xpansion; mscienski@mscienski.com)'
    }

    resp = requests.get(WIKIAPIURI, params=payload, headers=headers)

    return resp.json()


def has_articles(json):
    return 'query' in json and 'pages' in json['query'] and not '-1' in json['query']['pages']


def get_titles(json):
    titles = []
    id_keys = [key for key in dict(json['query']['pages'])]
    for key in id_keys:
        titles.append(json['query']['pages'][key]['title'])

    return titles


def get_articles(titles):
    pages = []
    for title in titles:
        pages.append(requests.get(WIKIARTICLEURI + title).text)

    return pages


def get_entries(html_docs):
    formatted_entries = []
    for doc in html_docs:
        html = lxml.html.document_fromstring(doc)
        list_items = html.cssselect('#mw-content-text > ul li')

        for item in list_items:
            formatted_item = item.text_content()
            formatted_entries.append(formatted_item)

    return formatted_entries

def choose_random_entry(entries):
    return random.choice(entries)

def app(environ, start_response):
      metadata = get_article_meta('asp')
      random_entry = ''
      if has_articles(metadata):
          titles = get_titles(metadata)
          articles = get_articles(titles)
          entries = get_entries(articles)
          random_entry = choose_random_entry(entries)

      start_response("200 OK", [
          ("Content-Type", "text/html;charset=utf8")
      ])

      return iter(environ)

def test_func():
    metadata = get_article_meta('asp')
    if has_articles(metadata):
        titles = get_titles(metadata)
        articles = get_articles(titles)
        entries = get_entries(articles)
        random_entry = choose_random_entry(entries)

    print random_entry or None
