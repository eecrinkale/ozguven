import joblib
import numpy as np
import pandas as pd

# Kaydedilmiş model ve vektörleyiciyi yükleme
def load_resources(resources_path):
    resources = joblib.load(resources_path)
    return resources['model'], resources['vectorizer'], resources['data']

# Kullanıcıdan gelen kelimeye en yakın metni bulma
def get_closest_quote(input_phrase):
    resources_path = 'quotes.pkl'  # Kaydedilen modelin yolu
    model, vectorizer, data = load_resources(resources_path)

    # Kullanıcıdan gelen kelimeyi vektörleştir
    input_vector = vectorizer.transform([input_phrase])

    # Cosine similarity ile en yakın komşuları bulma
    distances, indices = model.kneighbors(input_vector, n_neighbors=5)

    # En yakın komşulardan birini seçiyoruz
    closest_index = indices[0][0]  # En yakın olan metni alıyoruz

    closest_quote = data.iloc[closest_index]
    return {
        "Title": closest_quote['Title'],
        "Author": closest_quote['Author'],
        "Text": closest_quote['Text']
    }

# Soruları ekleyen fonksiyon
def display_questions():
    questions = [
        "1. Bu metin size ne ifade ediyor?",
        "2. Metindeki ana mesajı nasıl yorumlarsınız?",
        "3. Bu metnin günlük hayatınıza bir katkısı olabilir mi? Eğer evet, nasıl?"
    ]
    return questions

# Ana program
if __name__ == "__main__":
    input_phrase = input("Bir kelime veya ifade girin: ")  # Kullanıcıdan kelime alıyoruz
    result = get_closest_quote(input_phrase)  # En yakın metni buluyoruz

    # Metni yazdır
    print(f"Başlık: {result['Title']}")
    print(f"Yazar: {result['Author']}")
    print(f"Metin: \"{result['Text']}\"")

    # Soruları yazdır
    print("\nLütfen aşağıdaki soruları cevaplayın:")
    questions = display_questions()
    for question in questions:
        print(question)

    # Kullanıcı cevapları
    print("\nCevaplarınız:")
    for i, question in enumerate(questions, start=1):
        answer = input(f"Cevap {i}: ")  # Her soruya kullanıcıdan cevap alıyoruz
        print(f"Sorunun cevabı {i}: {answer}")  # Kullanıcının verdiği cevapları yazdırıyoruz
 # Kaydetme mesajı
    print("Cevaplarınız kaydedildi.")