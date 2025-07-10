import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_recommendations(user_input, property_csv='formatted_properties.csv', top_n=5):
    # Load data
    df = pd.read_csv(property_csv)

    # Debug: print column names
    print("CSV Columns:", df.columns.tolist())

    # Combine only existing fields
    df['features'] = (
        df['city'].fillna('') + ' ' +
        df['description'].fillna('') + ' ' +
        df['price'].astype(str).fillna('')
    )

    # Vectorize
    cv = CountVectorizer()
    matrix = cv.fit_transform(df['features'])

    # Input
    user_vec = cv.transform([user_input])
    scores = cosine_similarity(user_vec, matrix)

    top_indices = scores[0].argsort()[-top_n:][::-1]
    return df.iloc[top_indices]
