import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import pickle
from sklearn.metrics.pairwise import cosine_similarity


def prepare_model():
    print("Model train ho raha hai, thoda wait karo...\n")
    
    # 1. Data Load karna
    df = pd.read_csv("coursea_data.csv")
    
    # Remove unwanted files
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
        
    # 2. Title + Organization + Difficulty
    df['tags'] = df['course_title'] + " " + df['course_organization'] + " " + df['course_difficulty']
    
    # 3. Text ko Numbers (Vectors) mein convert karna
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(df['tags']).toarray()
    
    # 4. Cosine Similarity calculate karna
    similarity = cosine_similarity(vectors)
    
    print("Model Ready!\n" + "-"*30)
    return df, similarity

def recommend(course_name, df, similarity):
    try:
        # Course ka index nikalna
        course_index = df[df['course_title'] == course_name].index[0]
    except IndexError:
        print(f"Error: '{course_name}' naam ka koi course data mein nahi mila.")
        return
    
    # Match scores nikalna aur sort karna
    distances = similarity[course_index]
    courses_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    print(f"Agar aapko '{course_name}' pasand aaya, toh yeh 5 courses zaroor dekhein:\n")
    for i in courses_list:
        print(f"-> {df.iloc[i[0]]['course_title']}")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # Model prepare karte hain
    dataframe, similarity_matrix = prepare_model()
    print("Model save ho raha hai...")
    # Dataset ko save kar rahe hain (taaki courses ke naam mil sakein)
    pickle.dump(dataframe, open('courses_data.pkl', 'wb'))
    
    # Math (Similarity matrix) ko save kar rahe hain
    pickle.dump(similarity_matrix, open('similarity_matrix.pkl', 'wb'))
    
    print("Model successfully saved in .pkl files! 🎉")
    
    # Test karte hain! (Spelling ekdum same honi chahiye dataset jaisi)
    test_course = input("Enter the course you are searching for: ").title()
    recommend(test_course, dataframe, similarity_matrix)