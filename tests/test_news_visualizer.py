import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pandas as pd
from news_visualizer import NewsVisualizer

@pytest.fixture
def sample_data():
    return pd.DataFrame([
        {
            "author": "Author 1",
            "title": "Breaking News on Economy",
            "source": {"name": "Source A"},
            "content": "The market is going through a recession.",
            "publishedAt": "2024-09-01T08:30:00Z"
        },
        {
            "author": "Author 2",
            "title": "Tech Innovation Announced",
            "source": {"name": "Source B"},
            "content": "A breakthrough in quantum computing was made.",
            "publishedAt": "2024-09-02T15:00:00Z"
        },
        {
            "author": None,
            "title": "Health Sector Updates",
            "source": {"name": "Source C"},
            "content": "Vaccine developments continue to progress.",
            "publishedAt": "2024-09-03T11:00:00Z"
        }
    ])

def test_visualizer_initialization(sample_data):
    visualizer = NewsVisualizer(sample_data)
    assert isinstance(visualizer.data, pd.DataFrame)
    assert 'author' in visualizer.data.columns
    assert visualizer.data['author'].isnull().sum() == 0  # Should be filled with 'Unknown'

def test_plot_by_source(sample_data):
    visualizer = NewsVisualizer(sample_data)
    plot = visualizer.plot_by_source()
    assert plot is not None

def test_plot_top_authors(sample_data):
    visualizer = NewsVisualizer(sample_data)
    plot = visualizer.plot_top_authors()
    assert plot is not None

def test_plot_article_lengths(sample_data):
    visualizer = NewsVisualizer(sample_data)
    plot = visualizer.plot_article_lengths()
    assert plot is not None

def test_plot_over_time(sample_data):
    visualizer = NewsVisualizer(sample_data)
    plot = visualizer.plot_over_time()
    assert plot is not None

def test_plot_wordcloud(sample_data):
    visualizer = NewsVisualizer(sample_data)
    plot = visualizer.plot_wordcloud()
    assert plot is not None

# def test_plot_publication_times(sample_data):
#     visualizer = NewsVisualizer(sample_data)
#     plot = visualizer.plot_publication_times()
#     assert plot is not None

# def test_plot_sentiments(sample_data):
#     visualizer = NewsVisualizer(sample_data)
#     plot = visualizer.plot_sentiments()
#     assert plot is not None

# def test_plot_keywords(sample_data):
#     visualizer = NewsVisualizer(sample_data)
#     plot = visualizer.plot_keywords()
#     assert plot is not None

# def test_plot_sentiment_distribution(sample_data):
#     visualizer = NewsVisualizer(sample_data)
#     plot = visualizer.plot_sentiment_distribution()
#     assert plot is not None

# def test_analyze_content(sample_data):
#     visualizer = NewsVisualizer(sample_data)
#     fig = visualizer.analyze_content()
#     assert fig is not None
