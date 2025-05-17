import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, Mock
from article import Article

def test_article_initialization():
    article = Article(
        title="Test Title",
        url="http://example.com",
        description="Test description",
        image_url="http://example.com/image.jpg",
        author="Test Author",
        published_date="2023-01-01T12:00:00Z",
        source="Test Source",
        content="Test content"
    )
    assert article.title == "Test Title"
    assert article.url == "http://example.com"
    assert article.description == "Test description"
    assert article.image_url == "http://example.com/image.jpg"
    assert article.author == "Test Author"
    assert article.published_date == "2023-01-01T12:00:00Z"
    assert article.source == "Test Source"
    assert article.content == "Test content"

@patch("article.requests.get")
def test_scrape_details_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = b"<html><head><meta name='author' content='Mock Author'></head><body><p>Paragraph 1</p><p>Paragraph 2</p></body></html>"
    mock_get.return_value = mock_response

    article = Article(title="Test", url="http://example.com")
    article.scrape_details()

    assert article.author == "Mock Author"
    assert article.content.startswith("Paragraph 1")

@patch("article.requests.get")
def test_scrape_details_failure(mock_get):
    mock_get.side_effect = Exception("Network error")

    article = Article(title="Test", url="http://example.com")
    article.scrape_details()

    # Should keep default values on exception
    assert article.author == "Unknown author"
    assert article.content == ""

def test_format_date_valid():
    article = Article(title="Test", url="http://example.com", published_date="2023-01-01T12:00:00Z")
    formatted = article.format_date()
    assert "January" in formatted

def test_format_date_invalid():
    article = Article(title="Test", url="http://example.com", published_date="invalid-date")
    formatted = article.format_date()
    assert formatted == "invalid-date"
