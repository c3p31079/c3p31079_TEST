const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
if (isMobile) {
  document.getElementById("mobileNotice").style.display = "block";
}

const cameraInput = document.getElementById("cameraInput");
const analyzeBtn = document.getElementById("analyzeBtn");
const resultArea = document.getElementById("result");

analyzeBtn.addEventListener("click", async () => {
  const file = cameraInput.files[0];
  if (!file) {
    alert("画像を選択または撮影してください");
    return;
  }

  const formData = new FormData();
  formData.append("image", file);

  resultArea.textContent = "解析中...";

  try {
    const response = await fetch("https://c3p31079-test.onrender.com/analyze", {
      method: "POST",
      body: formData
    });

    if (!response.ok) throw new Error("サーバーエラー");

    const result = await response.json();
    resultArea.textContent = `✅ 画像サイズ: 幅 ${result.width}px / 高さ ${result.height}px`;
  } catch (error) {
    resultArea.textContent = "❌ エラーが発生しました: " + error.message;
  }
});
