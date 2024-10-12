// Function to generate a temporary client key
function generateTemporaryClientKey() {
  const now = new Date().getTime();
  let timeHex = now.toString(16);
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
      const r = (Math.random() * 16 | 0) ^ (parseInt(timeHex.charAt(timeHex.length - 1), 16) || 0);
      timeHex = timeHex.slice(0, -1);
      return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
  });
}

// Get or generate a client key
let clientKey = localStorage.getItem('clientKey');
if (!clientKey) {
  clientKey = generateTemporaryClientKey();
  localStorage.setItem('clientKey', clientKey);
}

// State variables
let lastMessageText = null;
let isWaitingForResponse = false;
let currentThreadId = '';

// Function to send a message
async function sendMessage() {
  const rawText = document.getElementById("textInput").value.trim();
  const quoteType = document.getElementById("quote-type").value;

  if (!rawText) return;

  if (isWaitingForResponse) return;

  isWaitingForResponse = true;
  const userMessageElement = createMessageElement(rawText, "user");
  document.querySelector(".message-list").appendChild(userMessageElement);
  scrollToBottom();

  document.getElementById("textInput").value = "";
  document.getElementById("textInput").disabled = true;

  const botMessageElement = createMessageElement('Writing <iconify-icon icon="svg-spinners:3-dots-bounce"></iconify-icon>', "bot");
  document.querySelector(".message-list").appendChild(botMessageElement);
  scrollToBottom();

  try {
      const response = await fetchBotResponse('/animequotes', null, rawText, clientKey, currentThreadId, quoteType);

      const newBotMessageElement = createMessageElement(response.message, "bot");
      const botMessageList = document.querySelectorAll(".message-list .message.bot");
      if (botMessageList.length > 0) {
          botMessageList[botMessageList.length - 1].replaceWith(newBotMessageElement);
      } else {
          document.querySelector(".message-list").appendChild(newBotMessageElement);
      }
      scrollToBottom();

      localStorage.setItem(`${quoteType}_${rawText}`, response.message);
      lastMessageText = rawText;
      currentThreadId = response.thread_id;
  } catch (error) {
      handleFetchError(error);
  } finally {
      isWaitingForResponse = false;
      document.getElementById("textInput").disabled = false;
  }
}

// Create a message element
function createMessageElement(text, type) {
  const messageElement = document.createElement("div");
  messageElement.classList.add("message", type);

  const messageText = document.createElement("span");
  messageText.innerHTML = text.replace(/\n/g, "<br>");
  messageElement.appendChild(messageText);
  return messageElement;
}

// Fetch a bot response
async function fetchBotResponse(url, data, msg = null, key = null, threadId = '', quoteType) {
  const params = new URLSearchParams({ msg, key, thread_id: threadId, quote_type: quoteType });
  const response = await fetch(`${url}?${params.toString()}`, {
      method: 'POST',
      body: data
  });

  if (response.status === 429) {
      throw { status: 429 };
  }

  try {
      return await response.json();
  } catch (error) {
      const responseText = await response.text();
      return { message: responseText, thread_id: '' };
  }
}

// Scroll to the bottom of the chat
function scrollToBottom() {
  const chatContainer = document.querySelector(".chat-container");
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Handle fetch errors
function handleFetchError(error) {
  if (error.status === 429) {
      const botMessageElement = createMessageElement("Oops, too many requests! Please try again later.", "bot");
      document.querySelector(".message-list").appendChild(botMessageElement);
      scrollToBottom();
  } else {
      console.error("Error:", error);
      const botMessageElement = createMessageElement("Oops, something went wrong. Please try again later.", "bot");
      document.querySelector(".message-list").appendChild(botMessageElement);
      scrollToBottom();
  }
}

// Initialize the theme
function initializeTheme() {
  if (!document.body.classList.contains("dark-mode")) {
      toggleTheme();
  }
}

// Toggle the theme
function toggleTheme() {
  document.body.classList.toggle('dark-mode');
  document.body.classList.toggle('light-mode');
  const icon = document.getElementById("theme-icon");
  if (document.body.classList.contains('dark-mode')) {
      icon.setAttribute('icon', 'line-md:sun-rising-filled-loop');
  } else {
      icon.setAttribute('icon', 'line-md:moon-rising-filled-alt-loop');
  }
}

// Handle keypress events on the text input
document.getElementById("textInput").addEventListener("keypress", function (e) {
  if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
  }
});

// Clear the localStorage on window load
window.onload = function () {
  localStorage.clear();
  initializeTheme();
};