# Web News Aggregator

## Overview

The **Web News Aggregator** is a Python-based application that collects, processes, and visualizes news articles from various online sources. It uses a combination of the **NewsAPI** and **web scraping** to deliver up-to-date news content in an interactive and insightful manner. Built with **Streamlit**, the app offers users a clean, simple interface to explore headlines, sentiment trends, and keyword patterns.

---

## Features

- **News Aggregation**  
  Fetches the latest headlines and articles using the [NewsAPI](https://newsapi.org/) and web scraping techniques.

- **Sentiment Analysis**  
  Uses `TextBlob` and `NLTK` to analyze the polarity of news headlines.

- **Data Visualization**  
  Displays word clouds, sentiment plots, and news category distributions using `Matplotlib`, `Seaborn`, and `Plotly`.

- **Interactive Dashboard**  
  Streamlit-powered UI lets users select news categories, enter keywords, and analyze results instantly.

---

## Setup Instructions

### Installation

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
