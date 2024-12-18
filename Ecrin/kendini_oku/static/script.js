document.addEventListener("DOMContentLoaded", () => {
  const phraseInput = document.getElementById("phraseInput");
  const searchBtn = document.getElementById("searchBtn");
  const quoteSection = document.getElementById("quoteSection");
  const quoteTitle = document.getElementById("quoteTitle");
  const quoteAuthor = document.getElementById("quoteAuthor");
  const quoteText = document.getElementById("quoteText");
  const questionsContainer = document.getElementById("questionsContainer");
  const answersSection = document.getElementById("answersSection");
  const answersForm = document.getElementById("answersForm");
  const submitAnswersBtn = document.getElementById("submitAnswersBtn");

  let currentTitle = "";
  let currentAuthor = "";
  let questions = [];

  searchBtn.addEventListener("click", () => {
      const phrase = phraseInput.value.trim();
      if (!phrase) {
          alert("Lütfen bir kelime giriniz.");
          return;
      }

      fetch("/get_quote", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({ phrase })
      })
      .then(response => {
          if (!response.ok) {
              return response.json().then(data => { throw new Error(data.detail); });
          }
          return response.json();
      })
      .then(data => {
          currentTitle = data.title;
          currentAuthor = data.author;
          quoteTitle.textContent = data.title;
          quoteAuthor.textContent = data.author;
          quoteText.textContent = data.text;

          questions = data.questions;
          questionsContainer.innerHTML = "";
          questions.forEach((q) => {
              const qDiv = document.createElement("div");
              qDiv.classList.add("question-item");
              qDiv.innerHTML = `<p>${q}</p>`;
              questionsContainer.appendChild(qDiv);
          });

          answersForm.innerHTML = "";
          questions.forEach((_, idx) => {
              const textarea = document.createElement("textarea");
              textarea.setAttribute("data-question-index", idx);
              answersForm.appendChild(textarea);
          });

          quoteSection.style.display = "block";
          answersSection.style.display = "block";
      })
      .catch(err => {
          alert("Hata: " + err.message);
      });
  });

  submitAnswersBtn.addEventListener("click", () => {
      const textareas = answersForm.querySelectorAll("textarea");
      const userAnswers = [];
      textareas.forEach(t => userAnswers.push(t.value.trim()));

      if (userAnswers.some(ans => ans === "")) {
          alert("Lütfen tüm sorulara cevap veriniz.");
          return;
      }

      fetch("/submit_answers", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({
              title: currentTitle,
              author: currentAuthor,
              user_answers: userAnswers
          })
      })
      .then(response => response.json())
      .then(data => {
          alert("Cevaplar başarıyla gönderildi!");
      })
      .catch(err => {
          alert("Cevap gönderilirken hata oluştu.");
      });
  });
});
