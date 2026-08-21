import streamlit as st
import pickle


# ==================================================
# PAGE CONFIGURATION
# ==================================================
st.set_page_config(
    page_title="E-Learning Course Recommender",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# ==================================================
# CUSTOM CSS
# ==================================================
st.markdown("""
<style>

/* ---------- MAIN APP ---------- */

.stApp {
    background-color: #F5EFE6 !important;
    color: #40362E !important;
}

.block-container {
    max-width: 850px;
    padding-top: 3rem;
    padding-bottom: 3rem;
}


/* ---------- HEADER ---------- */

.main-title {
    text-align: center;
    font-size: 2.8rem;
    font-weight: 700;
    color: #40362E !important;
    margin-bottom: 0.3rem;
}

.subtitle {
    text-align: center;
    font-size: 1.05rem;
    color: #75685C !important;
    margin-bottom: 2.5rem;
}


/* ---------- COURSE SECTION ---------- */

.section-title {
    font-size: 1.3rem;
    font-weight: 600;
    color: #40362E !important;
    margin-bottom: 1rem;
}


/* ---------- STREAMLIT CONTAINER ---------- */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #FFFCF7 !important;
    border: 1px solid #DED2C2 !important;
    border-radius: 18px !important;
    padding: 1rem !important;
    box-shadow: 0px 4px 12px rgba(80, 60, 40, 0.06);
}


/* ---------- SELECTBOX ---------- */

div[data-testid="stSelectbox"] label {
    color: #5F5246 !important;
    font-weight: 500 !important;
}

/* Dropdown box */
div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border: 1px solid #B8AA9A !important;
    border-radius: 10px !important;
}

/* Selected course text */
div[data-baseweb="select"] {
    color: #40362E !important;
}

/* Text inside selectbox */
div[data-baseweb="select"] * {
    color: #40362E !important;
}


/* ---------- BUTTON ---------- */

div.stButton > button {
    width: 100%;
    background-color: #5D7964 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
}

div.stButton > button:hover {
    background-color: #496650 !important;
    color: #FFFFFF !important;
}


/* ---------- RECOMMENDATIONS ---------- */

.recommendation-title {
    font-size: 1.6rem;
    font-weight: 700;
    color: #40362E !important;
    margin-top: 2rem;
    margin-bottom: 1.2rem;
}

.course-card {
    background-color: #FFFCF7 !important;
    border: 1px solid #DED2C2 !important;
    border-radius: 12px !important;
    padding: 1rem 1.2rem !important;
    margin-bottom: 0.8rem !important;
    color: #40362E !important;
    box-shadow: 0px 2px 6px rgba(80, 60, 40, 0.04);
}

.course-number {
    display: inline-block;
    background-color: #DCE6D9;
    color: #49634E !important;
    font-weight: 700;
    padding: 0.4rem 0.7rem;
    border-radius: 8px;
    margin-right: 0.8rem;
}

.course-name {
    color: #40362E !important;
    font-weight: 600;
}


/* ---------- FOOTER ---------- */

.footer {
    text-align: center;
    color: #8B7B6B !important;
    margin-top: 3rem;
    font-size: 0.9rem;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# LOAD DATA
# ==================================================
@st.cache_resource
def load_data():

    with open("courses_data.pkl", "rb") as file:
        courses_df = pickle.load(file)

    with open("similarity_matrix.pkl", "rb") as file:
        similarity = pickle.load(file)

    return courses_df, similarity


courses_df, similarity = load_data()


# ==================================================
# CREATE COURSE LIST
# ==================================================
course_list = sorted(
    courses_df["course_title"]
    .dropna()
    .unique()
)


# ==================================================
# RECOMMENDATION FUNCTION
# ==================================================
def recommend(course):

    course_matches = courses_df[
        courses_df["course_title"] == course
    ]

    if course_matches.empty:
        return []

    course_index = course_matches.index[0]

    distances = similarity[course_index]

    courses_list = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    recommended_courses = []

    for index, score in courses_list:

        recommended_courses.append(
            courses_df.iloc[index]["course_title"]
        )

    return recommended_courses


# ==================================================
# HEADER
# ==================================================
st.markdown(
    """
<div class="main-title">
📚 E-Learning Course Recommender
</div>

<div class="subtitle">
Discover courses similar to the ones you've studied or are interested in.
</div>
""",
    unsafe_allow_html=True
)


# ==================================================
# COURSE SELECTION
# ==================================================
with st.container(border=True):

    st.markdown(
        """
<div class="section-title">
🎓 Which course would you like to explore?
</div>
""",
        unsafe_allow_html=True
    )

    selected_course = st.selectbox(
        "Select a course",
        course_list,
        index=None,
        placeholder="Choose a course"
    )

    st.write("")

    if st.button("✨ Recommend Courses"):

        if selected_course is None:

            st.warning(
                "Please select a course first."
            )

        else:

            recommendations = recommend(selected_course)

            if recommendations:

                st.session_state.recommendations = recommendations

            else:

                st.error(
                    "Unable to find recommendations for this course."
                )


# ==================================================
# RECOMMENDATION RESULTS
# ==================================================
if "recommendations" in st.session_state:

    st.markdown(
        """
<div class="recommendation-title">
⭐ Top 5 Course Recommendations
</div>
""",
        unsafe_allow_html=True
    )

    for number, course in enumerate(
        st.session_state.recommendations,
        start=1
    ):

        st.markdown(
            f'<div class="course-card">'
            f'<span class="course-number">{number}</span>'
            f'<span class="course-name">{course}</span>'
            f'</div>',
            unsafe_allow_html=True
        )


# ==================================================
# FOOTER
# ==================================================
st.markdown(
    """
<div class="footer">
❤️ Made with Streamlit
</div>
""",
    unsafe_allow_html=True
)