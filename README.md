# Web News Aggregator App

This is a Web News Aggregator application that searches news categories from a news API and also performs web scraping to display aggregated news results.

## Features

- Fetches news articles from various sources using a news API
- Web scraping to gather additional news content
- Visualizes news data with charts and word clouds
- Sentiment analysis of news article titles
- Interactive and user-friendly interface powered by Streamlit

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/zhea-son/web-news-aggregator.git
   cd web-news-aggregator
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the application using Streamlit:
```
streamlit run app.py
```

This will start the web app locally and open it in your default browser.

## Dependencies

- pandas
- plotly
- seaborn
- wordcloud
- textblob
- nltk
- matplotlib
- dateutil
- streamlit

Make sure to install all dependencies listed in `requirements.txt`.

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
