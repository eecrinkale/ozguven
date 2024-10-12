# use.py
import joblib
import numpy as np
import pandas as pd

def load_resources(resources_path):
    resources = joblib.load(resources_path)
    return resources['model'], resources['vectorizer'], resources['data']

def get_closest_quote(input_phrase, n_responses=5):
    resources_path = 'quotes.pkl'
    model, vectorizer, data = load_resources(resources_path)
    input_vector = vectorizer.transform([input_phrase])
    distance, indices = model.kneighbors(input_vector, n_neighbors=n_responses)
    random_index = np.random.choice(indices[0])
    closest_quote = data.iloc[random_index]
    return {
        "Anime": closest_quote['Anime'],
        "Character": closest_quote['Character'],
        "Quote": closest_quote['Quote']
    }

if __name__ == "__main__":
    input_phrase = input("Enter a word or phrase: ")
    result = get_closest_quote(input_phrase, n_responses=10)
    print(f"Anime: {result['Anime']}\nCharacter: {result['Character']}\nQuote: \"{result['Quote']}\"")
