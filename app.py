import streamlit as st
import pickle
import pandas as pd

# 1. UI Title and Description
st.title('📚 E-Learning Course Recommender')
st.write("Apna pasandida course select karein aur AI aapko best matches batayega!")

# 2.(Pickle files)
courses_df = pickle.load(open('courses_data.pkl', 'rb'))
similarity = pickle.load(open('similarity_matrix.pkl', 'rb'))

# 3. Dropdown list 
course_list = courses_df['course_title'].values

# 4. UI: Dropdown Menu
selected_course = st.selectbox(
    "Kaunsa course aapne pehle padha hai ya padhna chahte hain?",
    course_list
)

# 5. Recommendation Logic 
def recommend(course):
    course_index = courses_df[courses_df['course_title'] == course].index[0]
    distances = similarity[course_index]
    
    # Top 5 courses 
    courses_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_courses = []
    for i in courses_list:
        recommended_courses.append(courses_df.iloc[i[0]]['course_title'])
    return recommended_courses

# 6. UI: Recommend Button
if st.button('Recommend Courses'):
    recommendations = recommend(selected_course)
    
    st.subheader("Aapke liye Top 5 Matches:")
    for i, course in enumerate(recommendations, 1):
        # formatting the output to show the course number and title
        st.info(f"{i}. {course}")