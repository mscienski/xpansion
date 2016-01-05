import requests
import lxml.html
import random
import json
from cgi import parse_qs, escape

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
    if 'query' in json and 'pages' in json['query']:
        missing_no = len([miss for miss in json['query']['pages'].keys() if miss == '-1')
        total = len([tot for tot in json['query']['pages'].keys()])
        
        return total != missing_no
    
    return False


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

        if len(list_items):
            for item in list_items:
                formatted_item = item.text_content()
                formatted_entries.append(formatted_item)

    return formatted_entries

def choose_random_entry(entries):
    return random.choice(entries)

def app(environ, start_response):
    if environ['QUERY_STRING']:
        d = parse_qs(environ['QUERY_STRING'])
        query_text = d.get('text', [''])[0]
        if query_text:
            query_text = escape(query_text)
            metadata = get_article_meta(query_text)
            random_entry = None
            out_text = 'No expansion found for ' + query_text
            if has_articles(metadata):
                titles = get_titles(metadata)
                articles = get_articles(titles)
                entries = get_entries(articles)
                if len(entries):
                    random_entry = choose_random_entry(entries)

            start_response('200 OK', [
              ('Content-Type', 'application/json')
            ])

            if random_entry:
                out_text = query_text + ' could mean: ' + random_entry

            response = dict({
                'response_type': 'in_channel',
                'text': out_text
            })

            return json.dumps(response)

    start_response('412 Precondition Failed', [
        ('Content-Type', 'text/plain')
    ])

    return iter(['Need a text= query parameter'])
