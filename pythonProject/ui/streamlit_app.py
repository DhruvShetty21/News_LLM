import streamlit as st
from scraping.rss_scraper import fetch_articles
from chains.filter_chain import classify_article

st.title("📰 EduNews Filter")

region = st.selectbox("Select Region", ["india", "global"])
content_type = st.selectbox("Content Type", ["general", "sensitive"])

if st.button("Fetch Educational News"):
    articles = fetch_articles()
    filtered = []
    for article in articles:
        result = classify_article(article['content'])
        if result['is_educational'] and result['region'] == region and result['content_type'] == content_type:
            filtered.append(article)

    if not filtered:
        st.write("No matching educational news found.")
    else:
        for art in filtered:
            st.markdown(f"### [{art['title']}]({art['link']})")
            st.write(art['summary'])