ROOT='http://www.paulgraham.com/'
SEED_URL='http://www.paulgraham.com/articles.html'


from bs4 import BeautifulSoup
import requests


def get_soup(url):
    r = requests.get(url)
    r.encoding = 'utf-8'
    return BeautifulSoup(r.content, 'lxml')
    #return BeautifulSoup(requests.get(url).content, 'lxml')

def get_links(url=SEED_URL):
    soup = get_soup(url)
    links = []
    for link in soup.find_all('a'):
        if 'href' in link.attrs:
            href = link.get('href')
            href = href if '/' in href else ROOT + href
            links.append(href)
    return links

def text(url):
    soup = get_soup(url)
    if soup.find('font'):
        return soup.find('font').text.strip()

def write(links, filename):
    with open(filename, 'w', encoding='UTF-8') as f:
    #with open(filename, 'w') as f:
        print('link[0]', links[0])  # links[0]은 index.html 이라 뺀 것이구나
        for i,link in enumerate(links[1:21]):  # 너무 길어서 총 50개만 읽어들이도록 함
            print('[{}] {}'.format(i,link))
            content = text(link)
            if content:
                f.write(content)
                f.write('\n')



if __name__ == '__main__':
    links = get_links(url=SEED_URL)
    print(links)
    write(links, 'data\jhs\jhs.txt')
