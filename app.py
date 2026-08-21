import streamlit as st
import pickle

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="E-Learning Course Recommender",
    page_icon="📚",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #F7F1E8;
        color: #3F3328;
    }

    /* Remove default Streamlit top padding */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 2rem;
        max-width: 1000px;
    }

    /* Main title */
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        color: #4A392B;
        margin-bottom: 0.3rem;
    }

    /* Subtitle */
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #7A6A5B;
        margin-bottom: 3rem;
    }

    /* Main card */
    .main-card {
        background: #FFFDF9;
        padding: 2rem;
        border-radius: 18px;
        border: 1px solid #E5D8C8;
        box-shadow: 0px 4px 15px rgba(80, 60, 40, 0.08);
        margin-bottom: 2rem;
    }

    /* Section title */
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #4A392B;
        margin-bottom: 1.2rem;
    }

    /* Recommendation heading */
    .recommendation-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #4A392B;
        margin-bottom: 1.5rem;
    }

    /* Course recommendation cards */
    .course-card {
        background: #FFFDF9;
        padding: 1rem 1.3rem;
        border-radius: 12px;
        border: 1px solid #E5D8C8;
        margin-bottom: 0.8rem;
        font-size: 1.1rem;
        color: #44372C;
        box-shadow: 0px 2px 8px rgba(80, 60, 40, 0.05);
    }

    .course-number {
        display: inline-block;
        background-color: #DDE8DA;
        color: #46634B;
        font-weight: 700;
        padding: 0.35rem 0.7rem;
        border-radius: 8px;
        margin-right: 0.8rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #8B7B6B;
        margin-top: 3rem;
        font-size: 0.9rem;
    }

    /* Button */
    div.stButton > button {
        width: 100%;
        background-color: #557A5A;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.7rem;
        font-size: 1.1rem;
        font-weight: 600;
        transition: 0.3s;
    }

    div.stButton > button:hover {
        background-color: #46684B;
        color: white;
        border: none;
    }

    /* Selectbox */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF;
        border-radius: 10px;
    }

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_resource
def load_data():
    courses_df = pickle.load(open("courses_data.pkl", "rb"))
    similarity = pickle.load(open("similarity_matrix.pkl", "rb"))
    return courses_df, similarity


courses_df, similarity = load_data()

course_list = courses_df["course_title"].values


# --------------------------------------------------
# RECOMMENDATION FUNCTION
# --------------------------------------------------
def recommend(course):
    course_index = courses_df[
        courses_df["course_title"] == course
    ].index[0]

    distances = similarity[course_index]

    courses_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_courses = []

    for i in courses_list:
        recommended_courses.append(
            courses_df.iloc[i[0]]["course_title"]
        )

    return recommended_courses


# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown(
    """
    <div class="main-title">
        📚 E-Learning Course Recommender
    </div>

    <div class="subtitle">
        Apna pasandida course select karein aur AI aapko best matches batayega!
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# COURSE SELECTION CARD
# --------------------------------------------------
st.markdown('<div class="main-card">', unsafe_allow_html=True)

st.markdown(
    '<div class="section-title">🎓 Which course have you studied or would like to explore?</div>',
    unsafe_allow_html=True
)

selected_course = st.selectbox(
    "Select a course",
    course_list,
    label_visibility="collapsed"
)

st.write("")

if st.button("✨ Recommend Courses"):
    st.session_state.recommendations = recommend(selected_course)
    st.session_state.selected_course = selected_course

st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------------------------
# RECOMMENDATION RESULTS
# --------------------------------------------------
if "recommendations" in st.session_state:

    st.markdown(
        '<div class="main-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="recommendation-title">⭐ Top 5 Course Recommendations:</div>',
        unsafe_allow_html=True
    )

    for i, course in enumerate(
        st.session_state.recommendations,
        1
    ):
        st.markdown(
            f"""
            <div class="course-card">
                <span class="course-number">{i}</span>
                <strong>{course}</strong>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown(
    """
    <div class="footer">
        ❤️ Made with Streamlit
    </div>
    """,
    unsafe_allow_html=True
)