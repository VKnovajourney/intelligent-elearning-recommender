# Intelligent Recommendation System for E-Learning Platforms 🎓

This project is an AI-based recommendation system designed to suggest the best e-learning courses (like those on Coursera) to users based on course content and similarities. 

## 🚀 Features
* Recommends relevant courses based on similarity algorithms.
* Interactive and user-friendly web interface.
* Fast recommendations using pre-computed similarity matrices.

## 📂 Project Structure
* `app.py`: The main Streamlit web application file.
* `recommend.py`: Contains the core recommendation logic and functions.
* `coursea_data.csv`: The raw dataset containing e-learning course details.
* `courses_data.pkl`: Serialized model data for the courses.
* `similarity_matrix.pkl`: Pre-computed similarity scores for fast querying.

## 🛠️ Tech Stack
* Python
* Streamlit
* Pandas
* Scikit-Learn

## 💻 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sudhanshuthakur2006/Intelligent-Recommendation-System-for-E-Learning-Platforms.git
   ```

2. **Activate the virtual environment (Windows):**
   ```bash
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   *(Make sure you have your required libraries installed)*
   ```bash
   pip install streamlit pandas scikit-learn
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```
