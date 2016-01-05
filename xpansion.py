from requests import Request, Session
from bs4 import BeautifulSoup
soup = BeautifulSoup(html_doc, 'html.parser')

WIKIURI = 'http://en.wikipedia.org/w/api.php'

def app(environ, start_response):
      data = "Hello, World!\n"
      start_response("200 OK", [
          ("Content-Type", "text/plain"),
          ("Content-Length", str(len(data)))
      ])
      stuff = find_wiki_articles('pas')
      return iter(stuff)

def find_wiki_articles(term):
    payload = {
        'action': 'query',
        'titles': term
    }

    s = Session()
    req = Request('GET', WIKIURI,
        params=payload,
        headers=header
    )
    prepped = req.prepare()

    return prepped.headers
