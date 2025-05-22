from typing import Counter
import pandas as pd
import plotly.express as px
import seaborn as sns
import plotly.graph_objects as go
from wordcloud import WordCloud
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from dateutil import parser
import re

nltk.download('punkt')
nltk.download('stopwords')

class NewsVisualizer:
    def __init__(self, data):
        self.data = data

        # Convert 'author' column to string type to handle None values properly
        self.data['author'] = self.data['author'].astype('object').where(self.data['author'].notnull(), None)
        self.data['author'] = self.data['author'].fillna('Unknown')
        self.data['title'] = self.data['title'].fillna('')
        self.data['source'] = self.data['source'].fillna('Unknown') 

        # Trim long author names
        self.data['author'] = self.data['author'].apply(
            lambda x: x[:20] if isinstance(x, str) and len(x) > 30 else x
        ) 
    
        def clean_date(value):
            if pd.isna(value):
                return None
            try:
                # Fix '1:54 p.m. PT' style to 24hr
                value = re.sub(r'(\d+:\d+)\s*p\.m\.', r'\1 PM', value, flags=re.IGNORECASE)
                value = re.sub(r'(\d+:\d+)\s*a\.m\.', r'\1 AM', value, flags=re.IGNORECASE)

                # Remove unsupported timezone strings like "PT"
                value = re.sub(r'\b(P[ST]?)\b', '', value)

                # Parse with dateutil (handles most edge cases)
                dt = parser.parse(value)

                # Check if date is within pandas Timestamp bounds
                if dt < pd.Timestamp.min.to_pydatetime() or dt > pd.Timestamp.max.to_pydatetime():
                    return pd.NaT
                return dt
            except Exception:
                return pd.NaT
            
        self.data['publishedAt'] = self.data['publishedAt'].apply(clean_date)

    # Plot articles from top source
    def plot_by_source(self):
        self.data['source_name'] = self.data['source'].apply(lambda x: x['name'] if isinstance(x, dict) else 'Unknown')
        source_counts = self.data['source_name'].value_counts().reset_index()
        source_counts.columns = ['Source', 'Number of Articles']
        plt.figure(figsize=(10, 6))
        sns.barplot(data=source_counts, x='Source', y='Number of Articles')
        plt.title('Article Distribution by Source')
        plt.xlabel('Source')
        plt.ylabel('Number of Articles')
        plt.xticks(rotation=90)
        plt.tight_layout()
        return plt
    
    # Plot articles from top author
    def plot_top_authors(self):
        top_authors = self.data['author'].value_counts().head(10).reset_index()
        top_authors.columns = ['Author', 'Number of Articles']
        plt.figure(figsize=(10, 6))
        sns.barplot(data=top_authors, x='Number of Articles', y='Author')
        plt.title('Top 10 Authors by Article Count')
        plt.xlabel('Number of Articles')
        plt.ylabel('Author')
        plt.tight_layout()
        return plt

    # Plot articles from article lengths
    def plot_article_lengths(self):
        self.data['article_length'] = self.data['content'].apply(lambda x: len(str(x).split()))
        plt.figure(figsize=(10, 6))
        plt.hist(self.data['article_length'], bins=20)
        plt.title('Distribution of Article Lengths')
        plt.xlabel('Length of Articles (in words)')
        plt.ylabel('Frequency') 
        plt.tight_layout()
        return plt

    # Plot articles publication over time
    def plot_over_time(self):
        self.data['publishedAt'] = pd.to_datetime(self.data['publishedAt'], utc=True)
        self.data['publishedAt'] = self.data['publishedAt'].dt.tz_localize(None)

        # Drop rows with NaT in 'publishedAt' before resampling
        data_filtered = self.data.dropna(subset=['publishedAt'])

        # Set 'publishedAt' as index for resampling
        data_filtered = data_filtered.set_index('publishedAt')

        articles_over_time = data_filtered.resample('D').size().reset_index(name='count')

        plt.figure(figsize=(10, 6))
        plt.plot(articles_over_time['publishedAt'], articles_over_time['count'], marker='o')
        plt.title('Number of Articles Published Over Time')
        plt.xlabel('Date')
        plt.ylabel('Number of Articles')
        plt.xticks(rotation=45)
        plt.tight_layout()
        return plt
    
    # Plot top words used in titles
    def plot_wordcloud(self):
        stopwords_set = set(stopwords.words('english'))
        all_titles = ' '.join(self.data['title'].dropna())
        wordcloud = WordCloud(stopwords=stopwords_set, background_color='white', width=800, height=400).generate(all_titles)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Word Cloud of Article Titles')
        return plt
    
    # Plot articles times
    def plot_publication_times(self):
        self.data['publishedAt'] = pd.to_datetime(self.data['publishedAt'], errors='coerce')
        self.data['hour'] = self.data['publishedAt'].dt.hour
        self.data = self.data.dropna(subset=['hour'])
        plt.figure(figsize=(10, 6))
        sns.histplot(data=self.data, x='hour', bins=24, kde=True)
        plt.title('Article Publication Times')
        plt.xlabel('Hour of the Day')
        plt.ylabel('Frequency')
        plt.tight_layout()
        return plt
