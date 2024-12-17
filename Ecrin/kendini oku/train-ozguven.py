import os
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

# Eğitim verisi dosyasını yükleme
excel_path = "quotes.xlsx"

# Dosya varlığını kontrol et
if not os.path.exists(excel_path):
    raise FileNotFoundError(f"{excel_path} dosyası bulunamadı. Lütfen dosyanın doğru bir konumda olduğunu doğrulayın.")

# Veriyi yükleme
data = pd.read_excel(excel_path)

# Beklenen sütunların varlığını kontrol et
required_columns = {'Title', 'Author', 'Text', 'Kelimeler'}
if not required_columns.issubset(data.columns):
    raise ValueError(f"Beklenen sütunlar {required_columns}, ancak bulunan sütunlar: {set(data.columns)}")

# Boş değerleri çıkar
data.dropna(subset=['Text'], inplace=True)
if data.empty:
    raise ValueError("Veri seti boş. Lütfen geçerli bir veri sağlayın.")

# Verinin başına göz atma
print("Veri örnekleri:")
print(data[['Title', 'Author', 'Text', 'Kelimeler']].head())

# TF-IDF vektörleştirici
vectorizer = TfidfVectorizer(stop_words='english', max_features=10000)
X = vectorizer.fit_transform(data['Text'])

# KNN modeli
model = NearestNeighbors(n_neighbors=5, metric='cosine')
model.fit(X)

# Model, vektörleyici ve veriyi kaydetme
resources = {'model': model, 'vectorizer': vectorizer, 'data': data}
output_path = "quotes.pkl"

try:
    joblib.dump(resources, output_path)
    print(f"Model, vektörleyici ve veriler başarıyla {output_path} olarak kaydedildi.")
except Exception as e:
    print(f"Kaydetme işlemi sırasında bir hata oluştu: {e}")
