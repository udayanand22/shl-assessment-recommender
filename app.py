import streamlit as st
from recommender import SHLRecommender

st.title("SHL Assessment Recommender")
recommender = SHLRecommender()

query = st.text_input("Enter job description or query:")
if query:
    results = recommender.recommend(query)
    for item in results:
        st.write(f"**{item['name']}**")
        st.write(f"- [View on SHL]({item['url']})")
        st.write(f"- Remote Testing: {item['remote_testing']}")
        st.write(f"- Adaptive/IRT: {item['adaptive_irt']}")
        st.write(f"- Duration: {item['duration']}")
        st.write(f"- Type: {item['test_type']}")
        st.write("---")