import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, Mock
from news_aggregator import NewsAggregator, Article

@patch("news_aggregator.requests.get")
def test_fetch_news_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "articles": [
            {
                "title": "Title 1",
                "url": "http://example.com/1",
                "description": "Desc 1",
                "urlToImage": "http://example.com/img1.jpg",
                "author": "Author 1",
                "publishedAt": "2023-01-01T12:00:00Z",
                "source": {"name": "Source 1"}
            },
            {
                "title": "Title 2",
                "url": "http://example.com/2",
                "description": "Desc 2",
                "urlToImage": "http://example.com/img2.jpg",
                "author": "Author 2",
                "publishedAt": "2023-01-02T12:00:00Z",
                "source": {"name": "Source 2"}
            }
        ]
    }
    mock_get.return_value = mock_response

    aggregator = NewsAggregator(api_key="fakekey")
    aggregator.fetch_news("technology")
    articles = aggregator.get_articles()

    assert len(articles) == 2
    assert articles[0].title == "Title 1"
    assert articles[1].source == "Source 2"

@patch("news_aggregator.requests.get")
def test_fetch_news_failure(mock_get):
    mock_response = Mock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response

    aggregator = NewsAggregator(api_key="fakekey")
    aggregator.fetch_news("technology")
    articles = aggregator.get_articles()

    assert articles == []

@patch("news_aggregator.requests.get")
def test_fetch_news_exception(mock_get):
    mock_get.side_effect = Exception("Network error")

    aggregator = NewsAggregator(api_key="fakekey")
    aggregator.fetch_news("technology")
    articles = aggregator.get_articles()

    assert articles == []

def test_clean_articles_removes_duplicates():
    aggregator = NewsAggregator(api_key="fakekey")
    article1 = Article(title="Title", url="http://example.com")
    article2 = Article(title="Title Duplicate", url="http://example.com")
    article3 = Article(title="Title 2", url="http://example2.com")
    aggregator.articles = [article1, article2, article3]
    aggregator._clean_articles()
    assert len(aggregator.articles) == 2
    urls = [a.url for a in aggregator.articles]
    assert "http://example.com" in urls
    assert "http://example2.com" in urls
