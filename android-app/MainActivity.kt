val imagePixelLength = 213.5  // Flaskから取得したピクセル長
val realWorldRefLengthMM = 100.0  // ユーザーがARで測った基準距離（たとえば10cm）

// スケーリング係数を計算（1pxあたり何mmか）
val mmPerPixel = realWorldRefLengthMM / imagePixelLength

// 実物大の亀裂長（mm）を算出
val actualCrackLengthMM = imagePixelLength * mmPerPixel

// 表示
val resultText = "実物の亀裂長: %.2f mm".format(actualCrackLengthMM)
textViewResult.text = resultText
