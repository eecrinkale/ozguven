import React, { useState, useEffect } from "react";

function App() {
  const [input, setInput] = useState("");
  const [quote, setQuote] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [darkMode, setDarkMode] = useState(() => {
    return localStorage.getItem("theme") === "dark";
  });
  const [answers, setAnswers] = useState([]);
  const [submitMessage, setSubmitMessage] = useState("");

  // İzin verilen kelimeler listesi
  const izinliKelimeler = ["takıntı", "özgüven", "zorluk", "eleştiri"];

  // Initialize the theme
  useEffect(() => {
    initializeTheme();
  }, []);

  const initializeTheme = () => {
    if (darkMode) {
      document.body.classList.add("dark-mode");
      document.body.classList.remove("light-mode");
    } else {
      document.body.classList.add("light-mode");
      document.body.classList.remove("dark-mode");
    }
  };

  const toggleTheme = () => {
    const newTheme = !darkMode;
    setDarkMode(newTheme);
    localStorage.setItem("theme", newTheme ? "dark" : "light");

    document.body.classList.toggle("dark-mode");
    document.body.classList.toggle("light-mode");

    const icon = document.getElementById("theme-icon");
    if (newTheme) {
      icon.setAttribute("icon", "line-md:sun-rising-filled-loop");
    } else {
      icon.setAttribute("icon", "line-md:moon-rising-filled-alt-loop");
    }
  };

  const fetchQuote = async () => {
    if (!input.trim()) {
      setError("Lütfen bir kelime giriniz.");
      return;
    }

    // İzin verilen kelimeler kontrolü
    if (!izinliKelimeler.includes(input.trim())) {
      setError("Hata: Geçersiz kelime girdiniz. Lütfen izin verilen bir kelime girin!");
      return;
    }

    setLoading(true);
    setError(null);
    setQuote(null);

    try {
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

      const data = await response.json();
      setQuote(data);
      setAnswers(new Array(data.questions.length).fill(""));
    } catch (err) {
      setError("Bir hata oluştu: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerChange = (index, value) => {
    const updatedAnswers = [...answers];
    updatedAnswers[index] = value;
    setAnswers(updatedAnswers);
  };

  const handleSubmit = () => {
    if (answers.some((answer) => answer.trim() === "")) {
      setError("Lütfen tüm sorulara cevap verin.");
      return;
    }

    const answerData = answers.map((answer, index) => ({
      questionIndex: index,
      answer: answer.trim(),
    }));

    console.log("Cevaplar gönderiliyor:", answerData);
    setSubmitMessage("Cevaplar kaydedildi!");
  };

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
          id="theme-icon"
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

      {loading && <p>Alıntı aranıyor...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {quote && (
        <div>
          <h2>Alıntı:</h2>
          <p>Başlık: {quote.title}</p>
          <p>Yazar: {quote.author}</p>
          <p>Metin: {quote.text}</p>
          <ul>
            {quote.questions.map((q, index) => (
              <li key={index}>
                {q}
                <textarea
                  value={answers[index] || ""}
                  onChange={(e) => handleAnswerChange(index, e.target.value)}
                />
              </li>
            ))}
          </ul>
          <button onClick={handleSubmit}>Gönder</button>
        </div>
      )}

      {submitMessage && <p>{submitMessage}</p>}
    </div>
  );
}

export default App;
