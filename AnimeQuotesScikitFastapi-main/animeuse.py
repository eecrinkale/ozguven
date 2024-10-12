# use.py
import joblib
import numpy as np
import os
import pickle
 
script_path = os.path.dirname(os.path.realpath(__file__))
pkl = os.path.join(script_path, 'animequotes.pkl')

def load_resources(resources_path):
    try:
        resources = joblib.load(resources_path)
        return resources['model'], resources['vectorizer'], resources['data']
    except KeyError as e:
        print(f"Error loading resources: {e}")
        print("Make sure the 'animequotes.pkl' file is in the correct format.")
        raise

def get_closest_quote(input_phrase, n_responses=5):
    resources_path = pkl
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
    input_phrase = "love"
    result = get_closest_quote(input_phrase, n_responses=10)
    print(f"Anime: {result['Anime']}\nCharacter: {result['Character']}\nQuote: \"{result['Quote']}\"")
