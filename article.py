import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse

class Article:
    def __init__(self, title, url, description=None, image_url=None, author=None, published_date=None, source=None, content=None):
        self.title = title
        self.url = url
        self.description = description or ""
        self.image_url = image_url
        self.author = author or "Unknown author"
        self.published_date = published_date or "Unknown date"
        self.source = source or "Unknown source"
        self.content = content or ""

    # Web scraping to extract from articles
    def scrape_details(self):
        try:
            res = requests.get(self.url, timeout=5)
            if res.status_code == 200:
                soup = BeautifulSoup(res.content, "html.parser")
                self.author = self._extract_author(soup) or self.author
                self.published_date = self._extract_pub_date(soup) or self.published_date
                self.source = self._extract_source(soup) or self.source
                self.content = self._extract_content(soup) or self.content
        except Exception:
            # Keep existing values if scraping fails
            pass

    # Extract author extra information from article
    def _extract_author(self, soup):
        author_meta_names = ['author', 'article:author', 'byline']
        for name in author_meta_names:
            meta = soup.find('meta', attrs={'name': name})
            if meta and meta.get('content'):
                return meta['content']
            meta = soup.find('meta', attrs={'property': name})
            if meta and meta.get('content'):
                return meta['content']
        author_tag = soup.find(attrs={'class': lambda x: x and 'author' in x.lower()})
        if not author_tag:
            author_tag = soup.find(attrs={'id': lambda x: x and 'author' in x.lower()})
        if author_tag:
            return author_tag.get_text(strip=True)
        # Additional check for BBC News author
        if "bbc.co.uk" in self.url or "bbc.com" in self.url:
            author_tag = soup.find('span', class_='byline__name')
            if author_tag:
                return author_tag.get_text(strip=True)
        return None

    # Extract publication extra information from article
    def _extract_pub_date(self, soup):
        pub_date_meta_props = ['article:published_time', 'datePublished', 'pubdate', 'timestamp']
        for prop in pub_date_meta_props:
            meta = soup.find('meta', attrs={'property': prop})
            if meta and meta.get('content'):
                return meta['content']
            meta = soup.find('meta', attrs={'name': prop})
            if meta and meta.get('content'):
                return meta['content']
        time_tag = soup.find('time')
        if time_tag and time_tag.get('datetime'):
            return time_tag['datetime']
        elif time_tag:
            return time_tag.get_text(strip=True)
        return None

    # Extract source extra information from article
    def _extract_source(self, soup):
        source_meta = soup.find('meta', attrs={'property':'og:site_name'})
        if source_meta and source_meta.get('content'):
            return source_meta['content']
        parsed_url = urlparse(self.url)
        hostname = parsed_url.hostname or "Unknown source"
        if hostname.startswith("www."):
            hostname = hostname[4:]
        return hostname

    # Extract content extra information from article
    def _extract_content(self, soup):
        paragraphs = soup.find_all('p')
        if paragraphs:
            return ' '.join([p.get_text() for p in paragraphs[:5]])
        return None

    def format_date(self):
        if self.published_date == "Unknown date":
            return self.published_date
        try:
            dt = datetime.fromisoformat(self.published_date.replace("Z", "+00:00"))
            return dt.strftime("%B %d, %Y, %H:%M %Z")
        except Exception:
            return self.published_date
