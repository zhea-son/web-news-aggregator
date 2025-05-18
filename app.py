import streamlit as st
import pandas as pd
from article import Article
from news_aggregator import NewsAggregator
from news_visualizer import NewsVisualizer

def main():
    st.set_page_config(page_title="Information News Aggregator", layout="wide")
    st.markdown("<h1 style='text-align: center; color: #4B8BBE;'>Information News Aggregator</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px;'>Welcome to your information aggregator using Web API and Scrapping</p>", unsafe_allow_html=True)

    api_key = "64bb097053f8400da84a0ac149e0b884"
    aggregator = NewsAggregator(api_key)

    with st.sidebar:
        st.image("3016.png", use_column_width=True)
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
                        article_date = article.format_date()
                        st.markdown(f"**Author:** {article.author}")
                        st.markdown(f"**Published on:** {article_date}")
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
        st.header("Trends and Insights")
        articles = st.session_state.get("articles", [])
        if not articles:
            st.info("No articles to visualize. Please fetch news first.")
        else:
            df = aggregator.get_refined_data(articles)
                
            visualizer = NewsVisualizer(df)

            with st.expander("Articles by Source", expanded=False):
                fig1 = visualizer.plot_by_source()
                st.pyplot(fig1)

            with st.expander("Articles by Authors", expanded=False):
                fig2 = visualizer.plot_top_authors() 
                st.pyplot(fig2) 

            with st.expander("Article Length Over Time", expanded=False):
                fig3 = visualizer.plot_article_lengths()
                st.pyplot(fig3) 
            
            with st.expander("Articles by Time", expanded=False):
                fig4 = visualizer.plot_over_time()
                st.pyplot(fig4) 
            
            with st.expander("Most Used Words in Title", expanded=False):
                fig5 = visualizer.plot_wordcloud()
                st.pyplot(fig5) 

if __name__ == "__main__":
    main()