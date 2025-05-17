import streamlit as st
import pandas as pd
from article import Article
from news_aggregator import NewsAggregator
from news_visualizer import NewsVisualizer

def main():
    st.set_page_config(page_title="Information News Aggregator", layout="wide")
    st.markdown( "<h1 style='text-align: center; color: #4B8BBE;'>Information News Aggregator</h1>", unsafe_allow_html=True )
    st.markdown( "<p style='text-align: center; font-size: 18px;'>Welcome to your information aggregator using Web API and Scrapping</p>", unsafe_allow_html=True )

    api_key = "64bb097053f8400da84a0ac149e0b884"
    aggregator = NewsAggregator(api_key)

    with st.sidebar:
        st.header("Search News")
        user_input = st.text_input("Enter the category", key="category_input")
        num_articles = st.slider("Number of articles per page", min_value=1, max_value=20, value=5, step=1)
        if st.button("Search"):
            if user_input:
                aggregator.fetch_news(user_input)
                st.session_state.articles = aggregator.get_articles()
                st.session_state.last_category = user_input
            else:
                st.warning("Please enter a category to search.")
        if st.button("Refresh"):
            if st.session_state.get("last_category"):
                aggregator.fetch_news(st.session_state.last_category)
                st.session_state.articles = aggregator.get_articles()
            else:
                st.info("No previous category to refresh. Please enter a category and click 'Search' first.")

    tab1, tab2 = st.tabs(["News", "Trending"])

    with tab1:
        articles = st.session_state.get("articles", [])

        if "page" not in st.session_state:
            st.session_state.page = 1

        articles_per_page = num_articles
        total_pages = (len(articles) + articles_per_page - 1) // articles_per_page

        start_idx = (st.session_state.page - 1) * articles_per_page
        end_idx = start_idx + articles_per_page
        page_articles = articles[start_idx:end_idx]

        if page_articles:
            for article in page_articles:
                with st.container():
                    cols = st.columns([1, 2])
                    with cols[0]:
                        
                        if article.image_url:
                            st.image(article.image_url, width=250)
                    with cols[1]:
                        st.subheader(article.title)
                        description = article.description or ""
                        if len(description) > 200:
                            description = description[:200] + "..."
                        st.write(description)
                        pretty_date = article.format_date()
                        st.markdown(f"**Author:** {article.author}")
                        st.markdown(f"**Published on:** {pretty_date}")
                        st.markdown(f"**Source:** {article.source}")
                        content_preview = article.content or ""
                        if len(content_preview) > 300:
                            content_preview = content_preview[:300] + "..."
                        ##st.write(f"Content preview: {content_preview}")
                        st.markdown(f"[Read more]({article.url})")
                        st.markdown("---")
        else:
            st.info("No articles found for this topic.")

    with tab2:
        st.header("Trending Publishers and Categories Visualization")
        articles = st.session_state.get("articles", [])
        if not articles:
            st.info("No articles to visualize. Please fetch news first.")
        else:
            visualizer = NewsVisualizer( aggregator.get_refined_data() )
            cols = st.columns(4)
            with cols[0]:
                publishers = [article.source for article in articles]
                publisher_counts = pd.Series(publishers).value_counts()
                st.subheader("Top Publishers")
                st.pyplot(visualizer.plot_by_source())

            with cols[1]:
                trending_categories = ["technology", "business", "sports", "entertainment", "health", "science"]
                st.subheader("Trending Categories")
                st.bar_chart(pd.Series(trending_categories).value_counts())


            # visualizer = NewsVisualizer(aggregator.get_articles())
            # visualizer.show_articles_per_source()
            # visualizer.show_publication_timeline()
            # visualizer.show_description_wordcount_dist()
            # visualizer.show_title_wordcloud()

if __name__ == "__main__":
    main()
