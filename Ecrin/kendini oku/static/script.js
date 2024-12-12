import React, { useState, useEffect } from "react";

function App() {
  // State tanımlamaları
  const [input, setInput] = useState(""); // Kullanıcı girdisi
  const [quote, setQuote] = useState(null); // API'den gelen alıntı
  const [loading, setLoading] = useState(false); // Yükleme durumu
  const [error, setError] = useState(null); // Hata mesajı
  const [darkMode, setDarkMode] = useState(() => {
    return localStorage.getItem("theme") === "dark";
  });
  const [answers, setAnswers] = useState([]); // Sorulara verilen cevaplar
  const [submitMessage, setSubmitMessage] = useState(""); // Cevaplar gönderildi mesajı

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

  // Tema değiştirme fonksiyonu
  const toggleTheme = () => {
    const newTheme = !darkMode;
    setDarkMode(newTheme);
    localStorage.setItem("theme", newTheme ? "dark" : "light");
  };

  // Cevapları güncelleme fonksiyonu
  const handleAnswerChange = (index, value) => {
    const updatedAnswers = [...answers];
    updatedAnswers[index] = value;
    setAnswers(updatedAnswers);
  };

  // Gönder butonuna tıklanınca cevapları gönderme fonksiyonu
  const handleSubmit = () => {
    const answerData = answers.map((answer, index) => ({
      questionIndex: index,
      answer: answer.trim(),
    }));
    console.log("Cevaplar gönderiliyor:", answerData);

    // Cevaplar başarıyla gönderildiyse kullanıcıya mesaj göster
    setSubmitMessage("Cevaplarınız kaydedildi!");

    // Burada API'ye gönderme işlemi yapılabilir
    // fetch('/submit_answers', {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify({ answers: answerData })
    // });
  };

  // Tema başlangıç kontrolü
  useEffect(() => {
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark") {
      setDarkMode(true);
    } else {
      setDarkMode(false);
    }
  }, []);

  return (
    <div
      style={{
        padding: "20px",
        fontFamily: "Arial, sans-serif",
        maxWidth: "600px",
        margin: "auto",
        backgroundColor: darkMode ? "#333" : "#f9f9f9",
        color: darkMode ? "#f9f9f9" : "#333",
        minHeight: "100vh",
      }}
    >
      <header
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <h1 style={{ color: darkMode ? "#f9f9f9" : "#333" }}>Alıntı Bulucu</h1>
        <button
          onClick={toggleTheme}
          style={{
            padding: "10px",
            fontSize: "16px",
            borderRadius: "50%",
            backgroundColor: "transparent",
            border: "none",
            cursor: "pointer",
          }}
        >
          {darkMode ? "🌞" : "🌙"}
        </button>
      </header>

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
            backgroundColor: darkMode ? "#444" : "#f9f9f9",
          }}
        >
          <h2 style={{ marginBottom: "10px", color: darkMode ? "#f9f9f9" : "#333" }}>Alıntı:</h2>
          <p><strong>Başlık:</strong> {quote.title}</p>
          <p><strong>Yazar:</strong> {quote.author}</p>
          <p><strong>Metin:</strong> {quote.text}</p>

          {/* Sorular */}
          <h3 style={{ marginTop: "20px", color: darkMode ? "#f9f9f9" : "#555" }}>İlgili Sorular:</h3>
          <ul style={{ paddingLeft: "20px" }}>
            {quote.questions.map((q, index) => (
              <li key={index} style={{ marginBottom: "10px", color: darkMode ? "#f9f9f9" : "#333" }}>
                {q}
                <div style={{ marginTop: "10px" }}>
                  <textarea
                    placeholder={`Cevabınızı yazın...`}
                    value={answers[index] || ""}
                    onChange={(e) => handleAnswerChange(index, e.target.value)}
                    style={{
                      width: "100%",
                      padding: "10px",
                      borderRadius: "5px",
                      border: "1px solid #ccc",
                      marginBottom: "10px",
                      backgroundColor: darkMode ? "#333" : "#fff",
                      color: darkMode ? "#f9f9f9" : "#333",
                    }}
                  ></textarea>
                </div>
              </li>
            ))}
          </ul>

          {/* Gönder Butonu */}
          <button
            id="submit-button"
            onClick={handleSubmit}
            style={{
              padding: "10px 20px",
              fontSize: "16px",
              borderRadius: "5px",
              backgroundColor: "#28a745",
              color: "white",
              border: "none",
              cursor: "pointer",
            }}
          >
            Gönder
          </button>

          {/* Cevaplar gönderildi mesajı */}
          {submitMessage && (
            <p style={{ marginTop: "20px", textAlign: "center", color: "green" }}>
              {submitMessage}
            </p>
          )}
        </div>
      )}
    </div>
  );
}

// Clear the localStorage on window load
window.onload = function () {
  localStorage.clear();
  initializeTheme();
};

export default App;