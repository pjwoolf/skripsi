import streamlit as st
import pandas as pd
from model import clean_text

df = pd.read_csv("cl_job_skills.csv")

session = st.session_state
session.setdefault("category", None)
session.setdefault("degree", None)
session.setdefault("select_degree", None)
session.setdefault("input_degree", None)
session.setdefault("department", None)
session.setdefault("select_department", None)
session.setdefault("input_department", None)
# session.setdefault("graduated", None)
session.setdefault("select_skill", None)
session.setdefault("input_skill", None)
session.setdefault("skills", [])
session.setdefault("input_year", 0)
session.setdefault("years", [])
session.setdefault("user_input", None)
session.setdefault("columns", [])
session.setdefault("num_columns", 1)

category_options = df['Category'].unique().tolist()
degree_options = ['BA', 'BS', 'Other']
department_options = ['Psychology', 'Business Administration', 'Computer Science', 'Other']
graduated_options = ["Graduated", "Not yet"]
skill_options = ["Python", "C++", "Tableau", "Other"]

def updateState():
    if session.select_skill is not None and session.select_skill != "Other":
        session.skills.append(session.select_skill)
        session.years.append(session.input_year)
        session.num_columns += 1
    elif session.select_skill == "Other" and session.input_skill:
        session.skills.append(session.input_skill)
        session.years.append(session.input_year)
        session.num_columns += 1

def removeSkill(delete_index):
    for num in range(delete_index, session.num_columns-2):
        session.skills[num] = session.skills[num+1]
        session.years[num] = session.years[num+1]
    session.num_columns -= 1
    session.skills.pop()
    session.years.pop()

with st.container():
    st.header("Category")
    session.category = st.multiselect(
        "Select a category", 
        category_options, 
        max_selections=5, 
        default=session.category if session.category is not None and session.category else None)

    st.header("Education")
    col1_degree, col2_degree = st.columns([1, 1])
    with col1_degree:
        session.select_degree = st.selectbox("Select degree", degree_options, key="other degree")
    if session.select_degree == "Other":
        with col2_degree:
            session.input_degree = st.text_input("Other degree")

    col1_department, col2_department = st.columns([1, 1])
    with col1_department:
        session.select_department = st.selectbox("Select department", department_options, key="other department")
    if session.select_department == "Other":
        with col2_department:
            session.input_department = st.text_input("Other department")

    if session.select_degree != "Other" and session.select_degree is not None:
        session.degree = session.select_degree
    elif session.select_degree == "Other" and session.input_degree is not None:
        session.degree = session.input_degree
    if session.select_department != "Other" and session.select_department is not None:
        session.department = session.select_department
    elif session.select_department == "Other" and session.input_department is not None:
        session.department = session.input_department
    
    # session.graduated = st.radio("Graduate", graduated_options, key="input", index=graduated_options.index(session.graduated) if session.graduated is not None else 0)

    st.header("Skill & Experience")
    new_column_name = f"Skill {session.num_columns}"
    session.columns.append(new_column_name)

    if session.num_columns < 6:
        with st.form(new_column_name):
            col1_skill, col2_skill = st.columns([2, 2])
            with col1_skill:
                st.caption(f"Skill {session.num_columns}")
                select_skill = st.empty() 
            st.caption(f"Years of experience {session.num_columns}")
            input_year = st.empty()
            skill_warn = st.empty()
            st.form_submit_button("Submit", use_container_width=True, on_click=updateState)

        with select_skill:
            session.select_skill = st.selectbox(f"Skill {session.num_columns}", skill_options, index=None, label_visibility="collapsed") 
            if session.select_skill == "Other":
                with col2_skill:
                    st.caption("Other skill")
                    session.input_skill = st.text_input("Other skill", label_visibility="collapsed") 
        with input_year:
            session.input_year = st.number_input(f"Years of experience {session.num_columns}", min_value=0, max_value=30, label_visibility="collapsed")
        
    if session.num_columns > 1:
        for num in range(session.num_columns-1):
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.caption(f"Skill {num+1}")
                st.text_input(f"Skill {num+1}", value=session.skills[num], disabled=True, label_visibility="collapsed")
            with col2:
                st.caption(f"Years of experience {num+1}")
                st.text_input(f"Years of experience {num+1}", value=session.years[num], disabled=True, label_visibility="collapsed")
            with col3:
                st.caption(f"Delete skill {num+1}")
                st.button("Remove", type="primary", key=num, use_container_width=True, on_click=removeSkill, args=(num,))
    # st.write(len(df))
                
 
    combined = " "
    combined_skill = [str(x) + " " + str(y) + " years" for x, y in zip(session.skills, session.years)]
    combined = combined.join(session.category) \
            + " " + session.degree \
            + " " + session.department \
            + " " + " ".join(combined_skill)
    session.user_input = clean_text(combined)
