import os
import string

import requests
from bs4 import BeautifulSoup

saved_files = []
def extract_articles(page, article_type):
    page = page + 1
    for i in range(1,page):
        d = f'Page_{str(i)}'
        try:
            if not os.path.exists(d):
                os.mkdir(d)
            if os.path.exists(d):
                os.chdir(d)
        except Exception as e:
            print(e)
        r = requests.get('https://www.nature.com/nature/articles?sort=PubDate&year=2020&page='+ str(i))
        r.raise_for_status() #

        soup = BeautifulSoup(r.text, 'html.parser')
        soup.prettify()
        articles = soup.find_all('article')
        for article in articles:
            type_span = article.find('span', {'data-test': 'article.type'})
            if type_span and type_span.text.strip().lower() == article_type.lower():
                link_tag = article.find('a', {'data-track-action': 'view article'})
                if link_tag and 'href' in link_tag.attrs:
                    article_url = 'https://www.nature.com' + link_tag['href']
                    filename = saved_articles_content(article_url)
                    if filename:
                        saved_files.append(filename)


        os.chdir('..')
    print(f'Saved articles: {saved_files}')
    print('Saved all articles.')

def saved_articles_content(article_url):
    response = requests.get(article_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the article title
    title_tag = soup.find('h1')
    if not title_tag:
        return None # Skip if there's no title

    title = title_tag.text.strip()
    # Clean up the filename
    filename = title.translate(str.maketrans('','', string.punctuation)).replace(' ', '_') + '.txt'

    # Extract the article content
    content = []
    for p in soup.find_all('p', {'class': 'article__teaser'}):
        content.append(p.text.strip())

    if not content:
        return None # Skip if there's no content

    # Join the content into a single string
    article_text = '\n'.join(content)

    # Save to a file
    with open(filename, 'wb') as file:
        file.write(article_text.encode('utf-8'))

    return filename

extract_articles(int(input()), input())
