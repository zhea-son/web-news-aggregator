import requests
from article import Article
import pandas as pd

class NewsSource:
    def fetch_news(self, category):
        raise NotImplementedError("Subclasses must implement fetch_news method")

class NewsAggregator(NewsSource):
    def __init__(self, api_key):
        self.api_key = api_key
        self.articles = []

    def fetch_news(self, category):
        url = f"https://newsapi.org/v2/everything?q={category}&apiKey={self.api_key}"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                articles_data = data.get("articles", [])
                self.articles = []
                for item in articles_data:
                    article = Article(
                        title=item.get("title"),
                        url=item.get("url"),
                        description=item.get("description"),
                        image_url=item.get("urlToImage"),
                        author=item.get("author"),
                        published_date=item.get("publishedAt"),
                        source=item.get("source", {}).get("name")
                    )
                    article.scrape_details()
                    self.articles.append(article)
                self._clean_articles()
            else:
                self.articles = []
        except Exception:
            self.articles = []

    def _clean_articles(self):
        # Remove duplicates by URL
        unique = {}
        for article in self.articles:
            if article.url not in unique:
                unique[article.url] = article
        self.articles = list(unique.values())

    def get_articles(self):
        return self.articles

    def get_refined_data(self):
        return pd.DataFrame([{
            'title': a.title,
            'url': a.url,
            'description': a.description,
            'image_url': a.image_url,
            'author': a.author,
            'publishedAt': a.published_date,
            'source': a.source
        } for a in self.articles])




