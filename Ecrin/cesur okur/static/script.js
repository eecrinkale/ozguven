import React, { useState } from "react";

function App() {
  // State tanımlamaları
  const [input, setInput] = useState(""); // Kullanıcı girdisi
  const [quote, setQuote] = useState(null); // API'den gelen alıntı
  const [loading, setLoading] = useState(false); // Yükleme durumu
  const [error, setError] = useState(null); // Hata mesajı

  // Alıntı fetch etme fonksiyonu
  const fetchQuote = async () => {
    if (!input.trim()) {
      setError("Lütfen bir kelime giriniz.");
      return;
    }

    setLoading(true);
    setError(null);
    setQuote(null);

    try {
      // API isteği gönder
      const response = await fetch("http://127.0.0.1:8000", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ phrase: input }),
      });

      if (!response.ok) {
        throw new Error("API isteği başarısız oldu.");
      }

      // Yanıtı JSON olarak al
      const data = await response.json();
      setQuote(data); // Gelen alıntıyı state'e ata
    } catch (err) {
      setError("Bir hata oluştu: " + err.message);
    } finally {
      setLoading(false); // Yükleme durumunu kapat
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif", maxWidth: "600px", margin: "auto" }}>
      <h1 style={{ textAlign: "center", color: "#333" }}>Alıntı Bulucu</h1>
      
      {/* Kullanıcı girdisi */}
      <div style={{ marginBottom: "20px", textAlign: "center" }}>
        <input
          type="text"
          placeholder="Bir kelime girin..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          style={{
            marginRight: "10px",
            padding: "10px",
            fontSize: "16px",
            width: "70%",
            borderRadius: "5px",
            border: "1px solid #ccc",
          }}
        />
        <button
          onClick={fetchQuote}
          style={{
            padding: "10px 20px",
            fontSize: "16px",
            cursor: "pointer",
            borderRadius: "5px",
            border: "none",
            backgroundColor: "#007BFF",
            color: "white",
          }}
        >
          Alıntı Bul
        </button>
      </div>

      {/* Yükleniyor mesajı */}
      {loading && (
        <p style={{ marginTop: "20px", textAlign: "center", color: "#555" }}>
          Alıntı aranıyor...
        </p>
      )}

      {/* Hata mesajı */}
      {error && (
        <p style={{ marginTop: "20px", textAlign: "center", color: "red" }}>
          {error}
        </p>
      )}

      {/* Alıntı sonuçları */}
      {quote && (
        <div
          style={{
            marginTop: "20px",
            border: "1px solid #ddd",
            padding: "20px",
            borderRadius: "5px",
            backgroundColor: "#f9f9f9",
          }}
        >
          <h2 style={{ marginBottom: "10px", color: "#333" }}>Alıntı:</h2>
          <p><strong>Başlık:</strong> {quote.title}</p>
          <p><strong>Yazar:</strong> {quote.author}</p>
          <p><strong>Metin:</strong> {quote.text}</p>
          <h3 style={{ marginTop: "20px", color: "#555" }}>İlgili Sorular:</h3>
          <ul style={{ paddingLeft: "20px" }}>
            {quote.questions.map((q, index) => (
              <li key={index} style={{ marginBottom: "10px" }}>{q}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App