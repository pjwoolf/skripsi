import streamlit as st
from Home import df
from model import raw_data, clean_data, tfidf_data, cosine_sim_data, recommandation

session = st.session_state

if (
    session.category
    and session.degree is not None
    and session.department is not None
    and session.user_input is not None
):
    
    data_raw = raw_data(df=df, user_input=session.user_input)
    st.write('Raw Data')
    st.write(data_raw)

    data_clean = clean_data(df=df, user_input=session.user_input)
    st.write('Clean Data')
    st.write(data_clean)

    data_tfidf = tfidf_data(df=df, user_input=session.user_input)
    st.write('TF-IDF')
    st.write(data_tfidf)

    data_cosine_sim = cosine_sim_data(df=df, user_input=session.user_input)
    st.write('Cosine Similarity')
    st.write(data_cosine_sim)

    data_rec = recommandation(df=df, user_input=session.user_input)
    st.write('Recommendation')
    st.write(data_rec)
        