import streamlit as st
from Home import df
import model
from model import recommandation, clean_text

session = st.session_state

session.setdefault("page", "home")
session.setdefault("data", None)
session.setdefault("rec", None)

def show_homepage():
    session.rec = recommandation(df=df,user_input=session.user_input)
    # st.write(session.rec)

    num_columns = 3
    num_elements = len(session.rec)
    if num_elements > 10: num_elements = 10
    num_rows = (num_elements + num_columns - 1) // num_columns
    if num_rows > 5: num_rows = 5

    count = 0

    for i in range(num_elements):
        st.write(f"{count + 1}. {session.rec['Title'][count]}")
        st.caption(f"{'&nbsp;' * 11}Cosine similarity: {session['rec']['Score'][count]:.3f}")
        st.caption(f"{'&nbsp;' * 11}Match words: {session['rec']['Match Words'][count]}")
        left_column, right_column = st.columns([3, 1])
        with right_column:
            if st.button("Select", key=session.rec['Title'][count]):
                session.page = "detail"
                session.data = count
        count += 1
    

def show_detail():
    if st.button("Back"):
        session.page = "home"
    st.header(session.rec["Title"][session.data])
    st.write(session.rec['Category'][session.data])
    st.subheader("Responsibilities")
    st.write(session.rec['Responsibilities'][session.data])
    st.subheader("Minimum Qualifications")
    st.write(session.rec['Minimum Qualifications'][session.data])
    st.subheader("Preferred Qualifications")
    st.write(session.rec['Preferred Qualifications'][session.data])

if (
    session.category
    and session.degree is not None
    and session.department is not None
    and session.user_input is not None
):  
    if session.page == "home":
        show_homepage()
    else:
        show_detail()
else: 
    centered_text = """
        <div style="display: flex; justify-content: center; align-items: center; height: 100vh;">
            <h2 style="text-align: center;">No Content</h2>
        </div>
    """
    st.markdown(centered_text, unsafe_allow_html=True)
