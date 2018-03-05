import logging
import requests
from bs4 import BeautifulSoup
from urlparse import urlparse, parse_qs


logger = logging.getLogger('recsys.scripts.scraper')


class MissingDataException(Exception):
    pass


def doi_from_url(url):
    qs = parse_qs(urlparse(url).query)
    return qs['doi'][0] if 'doi' in qs and qs['doi'] else None


def cid_from_url(url):
    qs = parse_qs(urlparse(url).query)
    return qs['cid'][0] if 'cid' in qs and qs['cid'] else None


class Citation():
    def init_from_div(self, div):
        self.title = div.h3.a.string.strip()
        self.url = div.h3.a.attrs['href']
        self.doi = doi_from_url(self.url)
        self.citation_only = False

        info = div.find(class_="pubinfo")
        if info:
            authors = info.find(class_="authors")
            if authors:
                self.authors = [a.strip() for a in authors.string[len('by '):].strip().split(', ')]

            venue = info.find(class_="pubvenue")
            if venue:
                self.venue = venue.string[len('- '):]

            year = info.find(class_="pubyear")
            if year:
                self.year = year.string[len(', '):]

        abstract = div.find(class_="pubabstract")
        if abstract:
            self.abstract = abstract.string.strip()

    def __init__(self, tr, from_element="tr"):
        """Take a BeautifulSoup Tag for a tr in the citation list table."""
        if from_element == "div":
            self.init_from_div(tr)
            return

        td = tr.find_all('td')[1]
        attrs = td.a.attrs

        self.title = td.a.string
        self.url = attrs['href']
        self.cid = cid_from_url(self.url)
        self.citation_only = 'class' in attrs and 'citation_only' in attrs['class']

        # hoping that contents[2] will always be the author/year string
        author_year = td.contents[2].string.split() if len(td.contents) > 2 else []

        # [u'-', u'Baumeister,', u'Leary', u'-', u'1995']
        if author_year and author_year[0] == '-':
            next_dash = author_year.index('-', 1) if '-' in author_year[1:] else len(author_year)

            self.author = ' '.join(author_year[1:next_dash])
            self.year = author_year[next_dash + 1] if next_dash + 1 < len(author_year) else None

        context = td.select('p.citationContext')
        if context:
            self.context = context[0].string.strip()


class CoCitations():
    def __init__(self, doi):
        url = "http://citeseerx.ist.psu.edu/viewdoc/similar"
        payload = {
            "doi": doi,
            "type": "cc"
        }

        response = requests.get(url, params=payload)

        if response.status_code != 200:
            logger.error('ERROR code {} for {}'.format(response.status_code, doi))
            raise MissingDataException("CoCitations {} {}".format(response.status_code, doi))

        soup = BeautifulSoup(response.content, "html.parser")

        self.co_citations = []

        table = soup.find(class_="refs")

        for tr in table.find_all('tr'):
            score = tr.find(class_="title")
            if not score:
                continue

            url = tr.a.attrs['href']
            citation_only = ('showciting' in url)

            self.co_citations.append({
                "score": int(score.text.strip()),
                "cid": cid_from_url(url),
                "citation_only": citation_only,
            })


class Record():
    def add_citations(self, divs):
        for div in divs:
            self.citations.append(Citation(div, 'div'))

    def fetch_cid_info(self, cid):
        self.cid = cid
        
        url = "http://citeseerx.ist.psu.edu/showciting"
        payload = {"cid": cid}

        response = requests.get(url, params=payload)

        if response.status_code != 200:
            logger.error('ERROR code {} for {}'.format(response.status_code, cid))
            raise MissingDataException("Record {} {}".format(response.status_code, cid))

        soup = BeautifulSoup(response.content, "html.parser")

        title = soup.h2.string.strip()
        if len(title) >= 6 and title[-1] == ")" and title[-6] == "(":
            self.year = title[-5:-1]
            title = title[:-6].strip()
        self.title = title

        authors = soup.find(id="docAuthors")
        if authors:
            self.authors = authors.string.strip()[len("by "):].split(", ")

        venue = soup.find(id="docVenue")
        if venue:
            self.venue = venue.find_all('td')[1].string

        self.citations = []
        divs = soup.find_all('div', class_='result')
        self.add_citations(divs)

        next_page = soup.find(id="pager")
        while next_page.a:
            next_url = next_page.a.attrs['href']
            qs = parse_qs(urlparse(next_url).query)

            payload = {
                "cid": cid,
                "sort": "cite",
                "start": qs['start'][0]
            }
            response = requests.get(url, payload)

            if response.status_code != 200:
                logger.error('ERROR code {} for {}'.format(response.status_code, next_url))

            soup = BeautifulSoup(response.content, "html.parser")
            divs = soup.find_all('div', class_='result')
            self.add_citations(divs)
            next_page = soup.find(id="pager")

    def __init__(self, identifier, identifier_key="doi", citation_only=False, skip_citations=False):
        """Fetch a record.

        identifier_key can be "doi" or "cid"
        identifier is the actual doi or cid identification number
        """
        logger.debug("Scraping for {} {}".format(identifier_key, identifier))

        if identifier_key == 'cid' and citation_only:
            self.fetch_cid_info(identifier)
            return

        url = "http://citeseerx.ist.psu.edu/viewdoc/versions"
        payload = {identifier_key: identifier}

        response = requests.get(url, params=payload)

        if response.status_code != 200:
            logger.error('ERROR code {} for {}'.format(response.status_code, identifier))
            raise MissingDataException("Record {} {}".format(response.status_code, identifier))

        soup = BeautifulSoup(response.content, "html.parser")

        self.doi = doi_from_url(response.url)
        self.pdf_url = "http://citeseerx.ist.psu.edu/viewdoc/download?doi={}&rep=rep1&type=pdf".format(self.doi)
        self.authors = []

        for tr in soup.find_all('tr'):
            if tr.td:
                datum = tr.td.string.lower()

                if datum == "title":
                    self.title = tr.find_all('td')[1].string
                elif datum == "abstract":
                    self.abstract = tr.find_all('td')[1].string
                elif datum == "year":
                    self.year = tr.find_all('td')[1].string
                elif datum == "venue":
                    self.venue = tr.find_all('td')[1].string
                elif datum == "author name":
                    self.authors.append(tr.find_all('td')[1].string.strip())

        if not skip_citations:
            self.citations = self.get_citations(self.doi)

    def get_citations(self, doi):
        url = "http://citeseerx.ist.psu.edu/viewdoc/citations"
        payload = {'doi': doi}

        response = requests.get(url, params=payload)

        if response.status_code != 200:
            logger.error('ERROR code {} for {}'.format(response.status_code, doi))
            raise MissingDataException("Citations {} {}".format(response.status_code, doi))

        soup = BeautifulSoup(response.content, "html.parser")

        citations = []

        citation_table = soup.find(id="citations").table
        if citation_table is not None:
            for tr in citation_table.find_all('tr'):
                c = Citation(tr)
                citations.append(c)

        return citations

    def toJSON(self):
        obj = self.__dict__
        if 'citations' in obj:
            obj['citations'] = [c.__dict__ for c in obj['citations']]
        return obj
