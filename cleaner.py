import pandas as pd

class DataCleaner:
    def merge_data(self, articles, additional_data):
        merged = []
        for article in articles:
            url = article['url']
            if url in additional_data:
                article.update(additional_data[url])
            merged.append(article)
        return merged

    def refine_data(self, articles):
        df = pd.DataFrame(articles)
        df.drop_duplicates(subset=['url'], inplace=True)
        df.dropna(subset=['title', 'url'], inplace=True)
        return df