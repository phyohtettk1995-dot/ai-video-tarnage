async function processVideo() {
    const apiKey = document.getElementById('apiKey').value;
    const fileInput = document.getElementById('videoFile');
    const targetLang = document.getElementById('targetLang').value;
    const statusDiv = document.getElementById('status');

    if (!apiKey || !fileInput.files[0]) {
        alert("API Key နှင့် Video ဖိုင်ကို အရင်ရွေးပါ!");
        return;
    }

    statusDiv.innerHTML = "Processing...";
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('api_key', apiKey);
    formData.append('target_lang', targetLang);

    try {
        const response = await fetch('/dub-video', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        statusDiv.innerHTML = result.message;
    } catch (error) {
        statusDiv.innerHTML = "Error: " + error;
    }
}
