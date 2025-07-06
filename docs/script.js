// スマホかどうかを判定（User-Agentを使う）
// スマホなら「📸 スマホで撮影してね」という案内文を表示
const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
if (isMobile) {
  document.getElementById("mobileNotice").style.display = "block";
}

// HTMLで定義した要素をJSで操作するために取得（IDで指定）
const cameraInput = document.getElementById("cameraInput");
const analyzeBtn = document.getElementById("analyzeBtn");
const resultArea = document.getElementById("result");

// 「解析する」ボタンが押されたときに実行される処理
// 画像ファイルが選ばれていない場合は警告を出して終了
analyzeBtn.addEventListener("click", async () => {
  const file = cameraInput.files[0];
  if (!file) {
    alert("画像を選択または撮影してください");
    return;
  }

//   画像をAPIに送るためのデータ（FormData）を準備
// ⇒image という名前で送信（Flask側でも request.files['image']）
  const formData = new FormData();
  formData.append("image", file);

// Loading now
  resultArea.textContent = "解析中...";

// Render上のFlask APIに画像をPOST（非同期通信）
  try {
    const response = await fetch("https://c3p31079-test.onrender.com/analyze", {
      method: "POST",
      body: formData
    });

    if (!response.ok) throw new Error("サーバーエラー");

// レスポンスのJSONを受け取り、HTML内に結果を表示
// 失敗した場合はエラーを表示
    const result = await response.json();
    resultArea.textContent = `画像サイズ: 幅 ${result.width}px / 高さ ${result.height}px`;
  } catch (error) {
    resultArea.textContent = "エラーが発生しました: " + error.message;
  }
});
