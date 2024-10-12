document.getElementById('quoteForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const message = document.getElementById('messageInput').value;

    const formData = new FormData();
    formData.append('message', message);

    const response = await fetch('/get_quote/', {
        method: 'POST',
        body: formData
    });

    const data = await response.json();
    document.getElementById('quoteDisplay').innerText = data.quote;
});
