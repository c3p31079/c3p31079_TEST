async function sendImage() {
  const file = document.getElementById("imageInput").files[0];
  const formData = new FormData();
  formData.append("image", file);

  const response = await fetch("https://your-api.onrender.com/analyze", {
    method: "POST",
    body: formData
  });

  const result = await response.json();
  document.getElementById("result").textContent = `サイズ：${result.width}×${result.height}`;
}
