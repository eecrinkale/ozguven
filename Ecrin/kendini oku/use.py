import pandas as pd

# Geçerli kelimeler listesini yüklemek için
valid_words = pd.read_excel("quotes.xlsx")['Kelimeler'].dropna().apply(lambda x: str(x).strip().lower()).tolist()

# Geçerli kelimeyi kontrol eden fonksiyon
def validate_word(word):
    word = word.strip().lower()  # Kullanıcıdan alınan kelimeyi küçük harfe dönüştür ve boşlukları temizle
    return word in valid_words  # Kelime listede varsa True, yoksa False döner

# Excel'den kelimeye uygun alıntıyı getirme
def get_quote_for_word(word):
    # Excel dosyasındaki veriyi yükle
    data = pd.read_excel("quotes.xlsx")

    # Kelimenin olduğu alıntıları tam eşleşme ile kontrol et
    matching_quotes = data[data['Kelimeler'].str.strip().str.lower() == word]

    if matching_quotes.empty:
        return None  # Hiçbir alıntı bulunamazsa None döndür

    # Bulunan ilk alıntıyı döndür
    quote = matching_quotes.iloc[0]
    return {
        "Title": quote['Title'],
        "Author": quote['Author'],
        "Text": quote['Text']
    }

# Ana program
if __name__ == "__main__":
    input_phrase = input("Bir kelime veya ifade girin: ")  # Kullanıcıdan kelime alıyoruz

    # Kelimenin geçerli olup olmadığını kontrol et
    if not validate_word(input_phrase):
        exit()  # Kelime geçerli değilse hiçbir şey göstermeden çıkış yapar
    else:
        # Kelime geçerli, alıntıyı alıyoruz
        result = get_quote_for_word(input_phrase)

        if result:  # Eğer bir alıntı bulduysak
            # Metni yazdır
            print(f"Başlık: {result['Title']}")
            print(f"Yazar: {result['Author']}")
            print(f"Metin: \"{result['Text']}\"")
