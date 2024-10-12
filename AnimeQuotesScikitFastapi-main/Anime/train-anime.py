# train.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import joblib

def train_and_save_model(excel_file_path, pkl_file_path):
    # Load the data
    data = pd.read_excel(excel_file_path)
    
    # Vectorization
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(data['Quote'])
    
    # Model Training
    model = NearestNeighbors(n_neighbors=5, metric='cosine')
    model.fit(X)
    
    # Save the model, vectorizer, and data together
    joblib.dump({'model': model, 'vectorizer': vectorizer, 'data': data}, pkl_file_path)
    print("Model, vectorizer, and data have been saved together.")

if __name__ == "__main__":
    train_and_save_model('animequotes.xlsx', 'quotes.pkl')
