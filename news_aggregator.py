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

    # Fetch the news articles from the API using api_key
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

    # Remove duplicates by URL
    def _clean_articles(self):
        unique = {}
        for article in self.articles:
            if article.url not in unique:
                unique[article.url] = article
        self.articles = list(unique.values())

    def get_articles(self):
        return self.articles

    # Convert list of articles object into suitable dataframe
    def get_refined_data(self, data):
        rows = []
        for a in data:
            try:
                row = {
                    "title": getattr(a, "title", ""),
                    "author": getattr(a, "author", "Unknown"),
                    "source": {"name": getattr(a, "source", "Unknown")},
                    "publishedAt": getattr(a, "published_date", None),
                    "content": getattr(a, "content", "")
                }
                rows.append(row)
            except Exception as e:
                print(f"Error processing article: {e}")
        return pd.DataFrame(rows)



