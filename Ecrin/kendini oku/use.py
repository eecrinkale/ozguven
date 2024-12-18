import joblib
import numpy as np
import pandas as pd
import random

# Kaydedilmiş model ve vektörleyiciyi yükleme
def load_resources(resources_path):
    resources = joblib.load(resources_path)
    return resources['data']  # Verileri döndürüyoruz (model ve vektörleyici yerine)

# Kullanıcıdan gelen kelimeye uygun metni rastgele seçme
def get_random_quote(input_phrase):
    resources_path = 'quotes.pkl'  # Kaydedilen veri setinin yolu
    data = load_resources(resources_path)

    # 'Kelimeler' sütununda arama yapıyoruz
    matching_quotes = data[data['Kelimeler'].str.contains(input_phrase, case=False, na=False)]

    # Eğer eşleşen bir alıntı varsa
    if not matching_quotes.empty:
        # Zar yöntemi: Rastgele bir metin seçiyoruz
        random_index = random.choice(matching_quotes.index)
        selected_quote = matching_quotes.loc[random_index]

        return {
            "Title": selected_quote['Title'],
            "Author": selected_quote['Author'],
            "Text": selected_quote['Text']
        }
    else:
        # Eşleşme bulunamadıysa
        return None

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
    result = get_random_quote(input_phrase)  # Zar yöntemiyle rastgele bir alıntı seçiyoruz

    if result:
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
    else:
        print("Girdiğiniz kelimeyle eşleşen bir alıntı bulunamadı.")
