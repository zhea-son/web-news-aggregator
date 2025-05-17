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

nltk.download('punkt')
nltk.download('stopwords')

class NewsVisualizer:
    def __init__(self, articles):
        self.df = pd.DataFrame([{
            'title': a.title,
            'source': a.source,
            'publishedAt': a.published_date,
            'description': a.description,
            'author': a.author
        } for a in articles if a.title and a.source and a.published_date and a.description])
        # self._preprocess()

    # def _preprocess(self):
    #     self.df['publishedAt'] = pd.to_datetime(self.df['publishedAt'], errors='coerce')
    #     self.df.dropna(subset=['publishedAt'], inplace=True)
    #     self.df['desc_word_count'] = self.df['description'].apply(lambda x: len(str(x).split()))
    #     self.df['title_length'] = self.df['title'].apply(lambda x: len(str(x).split()))
        
    # def __init__(self, data):
    #     self.data = data
    #     self.data['author'] = self.data['author'].fillna('Unknown')
    #     self.data['title'] = self.data['title'].fillna('')
    #     self.data['source'] = self.data['source'].fillna('Unknown')
    #     self.data['publishedAt'] = pd.to_datetime(self.data['publishedAt'], errors='coerce')

    def plot_by_source(self):
        # self.data['source_name'] = self.data['source'].apply(lambda x: x['name'] if isinstance(x, dict) else 'Unknown')
        # source_counts = self.data['source_name'].value_counts().reset_index()
        # source_counts.columns = ['Source', 'Number of Articles']
        # plt.figure(figsize=(10, 6))
        # sns.barplot(data=source_counts, x='Source', y='Number of Articles')
        # plt.title('Article Distribution by Source')
        # plt.xlabel('Source')
        # plt.ylabel('Number of Articles')
        # plt.xticks(rotation=45)
        # plt.tight_layout()
        # return plt
    
        plt.figure(figsize=(6, 4))
        sns.countplot(y='source', data=self.df, order=self.df['source'].value_counts().head(10).index)
        plt.title("Top Sources")
        plt.tight_layout()
        return plt

    def plot_by_author(self):
        author_counts = self.data['author'].value_counts().reset_index()
        author_counts.columns = ['Author', 'Number of Articles']
        plt.figure(figsize=(10, 6))
        sns.barplot(data=author_counts, x='Author', y='Number of Articles')
        plt.title('Article Distribution by Author')
        plt.xlabel('Author')
        plt.ylabel('Number of Articles')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_article_lengths(self):
        self.data['article_length'] = self.data['content'].apply(lambda x: len(str(x).split()))
        plt.figure(figsize=(10, 6))
        plt.hist(self.data['article_length'], bins=20)
        plt.title('Distribution of Article Lengths')
        plt.xlabel('Length of Articles (in words)')
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.show()


    def plot_over_time(self):
        articles_over_time = self.data.resample('D', on='publishedAt').size().reset_index(name='count')
        plt.figure(figsize=(10, 6))
        plt.plot(articles_over_time['publishedAt'], articles_over_time['count'], marker='o')
        plt.title('Number of Articles Published Over Time')
        plt.xlabel('Date')
        plt.ylabel('Number of Articles')
        plt.tight_layout()
        plt.show()

    
    def plot_wordcloud(self):
        stopwords_set = set(stopwords.words('english'))
        all_titles = ' '.join(self.data['title'].dropna())
        wordcloud = WordCloud(stopwords=stopwords_set, background_color='white', width=800, height=400).generate(all_titles)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Word Cloud of Article Titles')
        plt.show()

    def plot_top_authors(self):
        top_authors = self.data['author'].value_counts().head(10).reset_index()
        top_authors.columns = ['Author', 'Number of Articles']
        plt.figure(figsize=(10, 6))
        sns.barplot(data=top_authors, x='Number of Articles', y='Author')
        plt.title('Top 10 Authors by Article Count')
        plt.xlabel('Number of Articles')
        plt.ylabel('Author')
        plt.tight_layout()
        plt.show()


    def plot_publication_times(self):
        self.data['hour'] = self.data['publishedAt'].dt.hour
        self.data = self.data.dropna(subset=['hour'])
        plt.figure(figsize=(10, 6))
        sns.histplot(data=self.data, x='hour', bins=24, kde=True)
        plt.title('Article Publication Times')
        plt.xlabel('Hour of the Day')
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.show()


    def plot_sentiments(self):
        self.data['title_sentiment'] = self.data['title'].apply(lambda x: TextBlob(str(x)).sentiment.polarity if isinstance(x, str) else 0)
        plt.figure(figsize=(10, 6))
        sns.histplot(data=self.data, x='title_sentiment', bins=20, kde=True)
        plt.title('Sentiment Analysis of Article Titles')
        plt.xlabel('Sentiment Polarity')
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.show()


    def plot_keywords(self):
        all_titles = ' '.join(self.data['title'].dropna())
        word_tokens = nltk.word_tokenize(all_titles)
        keywords = [word for word in word_tokens if word.isalpha() and word not in stopwords.words('english')]
        keywords_freq = nltk.FreqDist(keywords)
        top_keywords = keywords_freq.most_common(20)
        keywords_df = pd.DataFrame(top_keywords, columns=['Keyword', 'Frequency'])
        plt.figure(figsize=(10, 6))
        sns.barplot(data=keywords_df, x='Frequency', y='Keyword')
        plt.title('Top 20 Keywords in Article Titles')
        plt.xlabel('Frequency')
        plt.ylabel('Keyword')
        plt.tight_layout()
        plt.show()


    def plot_article_length_over_time(self):
        self.data['article_length'] = self.data['content'].apply(lambda x: len(str(x).split()))
        plt.figure(figsize=(10, 6))
        plt.scatter(self.data['publishedAt'], self.data['article_length'], alpha=0.5)
        plt.title('Article Lengths Over Time')
        plt.xlabel('Date')
        plt.ylabel('Length of Articles (in words)')
        plt.tight_layout()
        plt.show()


    def plot_sentiment_distribution(self):
        sentiment_counts = self.data['title_sentiment'].apply(lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral')).value_counts()
        plt.figure(figsize=(10, 6))
        sentiment_counts.plot(kind='bar')
        plt.title('Distribution of Sentiment Polarity')
        plt.xlabel('Sentiment')
        plt.ylabel('Number of Articles')
        plt.tight_layout()
        plt.show()


    def analyze_content(self):
        # Tokenize and preprocess content
        all_content = ' '.join(self.data['content'].dropna())
        tokens = nltk.word_tokenize(all_content)
        words = [word.lower() for word in tokens if word.isalpha() and word.lower() not in stopwords.words('english')]

        # Perform content analysis (e.g., word frequency)
        word_freq = Counter(words)
        top_words = word_freq.most_common(20)

        # Visualize results
        word_freq_df = pd.DataFrame(top_words, columns=['Word', 'Frequency'])
        fig = px.bar(word_freq_df, x='Frequency', y='Word', orientation='h', title='Top 20 Words in Article Content',
                     color='Frequency', color_continuous_scale='Plasma')
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        fig.show()       
