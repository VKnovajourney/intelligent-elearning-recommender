import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------
# PREPARE RECOMMENDATION MODEL
# --------------------------------------------------
def prepare_model():

    print("Preparing recommendation model...\n")

    # Load dataset
    df = pd.read_csv("coursea_data.csv")

    # Remove unnecessary column if it exists
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    # Check required columns
    required_columns = [
        "course_title",
        "course_organization",
        "course_difficulty"
    ]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(
                f"Required column '{column}' not found in coursea_data.csv"
            )

    # Remove missing values
    df = df.dropna(
        subset=[
            "course_title",
            "course_organization",
            "course_difficulty"
        ]
    )

    # Create tags for recommendation
    df["tags"] = (
        df["course_title"].astype(str)
        + " "
        + df["course_organization"].astype(str)
        + " "
        + df["course_difficulty"].astype(str)
    )

    # Convert text into vectors
    cv = CountVectorizer(
        max_features=5000,
        stop_words="english"
    )

    vectors = cv.fit_transform(df["tags"])

    # Calculate cosine similarity
    similarity = cosine_similarity(vectors)

    print("Model ready!")
    print("-" * 40)

    return df, similarity


# --------------------------------------------------
# RECOMMEND COURSES
# --------------------------------------------------
def recommend(course_name, df, similarity):

    matching_courses = df[
        df["course_title"].str.lower()
        == course_name.lower()
    ]

    if matching_courses.empty:
        print(f"\nCourse '{course_name}' was not found.")
        return

    course_index = matching_courses.index[0]

    # Get similarity scores
    distances = similarity[course_index]

    # Get top 5 similar courses
    courses_list = sorted(
        enumerate(distances),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    print(f"\nTop 5 recommendations for '{course_name}':\n")

    for rank, (index, score) in enumerate(courses_list, start=1):

        recommended_course = df.iloc[index]["course_title"]

        print(
            f"{rank}. {recommended_course}"
        )


# --------------------------------------------------
# MAIN
# --------------------------------------------------
if __name__ == "__main__":

    # Prepare model
    dataframe, similarity_matrix = prepare_model()

    print("\nSaving model files...")

    # Save dataframe
    with open("courses_data.pkl", "wb") as file:
        pickle.dump(dataframe, file)

    # Save similarity matrix
    with open("similarity_matrix.pkl", "wb") as file:
        pickle.dump(similarity_matrix, file)

    print("Model files saved successfully!")
    print("courses_data.pkl")
    print("similarity_matrix.pkl")

    # Optional test
    print("\nTesting the recommendation system...\n")

    test_course = input(
        "Enter a course name to test: "
    ).strip()

    recommend(
        test_course,
        dataframe,
        similarity_matrix
    )