class MainActivity : AppCompatActivity() {

    private lateinit var imageView: ImageView
    private lateinit var resultText: TextView
    private lateinit var arMeasureBtn: Button
    private var pixelLength = 0.0
    private var mmPerPixel = 0.0  // ARCoreで測定したスケーリング係数

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        imageView = findViewById(R.id.imageView)
        resultText = findViewById(R.id.resultText)
        arMeasureBtn = findViewById(R.id.arButton)

        val pickImage = registerForActivityResult(ActivityResultContracts.GetContent()) { uri ->
            uri?.let {
                imageView.setImageURI(it)
                sendImageToFlask(it)
            }
        }

        findViewById<Button>(R.id.selectImageButton).setOnClickListener {
            pickImage.launch("image/*")
        }

        arMeasureBtn.setOnClickListener {
            // 仮に AR で測定した長さが100mmとする（本来はARCoreで測定）
            val realWorldLengthMM = 100.0
            mmPerPixel = realWorldLengthMM / pixelLength
            val actualLength = pixelLength * mmPerPixel
            resultText.text = "実物の亀裂長: %.2f mm".format(actualLength)
        }
    }

    private fun sendImageToFlask(uri: Uri) {
        val file = FileUtil.from(this, uri)
        val requestFile = file.asRequestBody("image/*".toMediaTypeOrNull())
        val body = MultipartBody.Part.createFormData("image", file.name, requestFile)

        RetrofitClient.api.analyzeImage(body).enqueue(object : Callback<CrackResponse> {
            override fun onResponse(call: Call<CrackResponse>, response: Response<CrackResponse>) {
                if (response.isSuccessful) {
                    pixelLength = response.body()?.pixelLength ?: 0.0
                    resultText.text = "画像からのピクセル長: $pixelLength px"
                } else {
                    resultText.text = "Flask API からの応答に失敗"
                }
            }

            override fun onFailure(call: Call<CrackResponse>, t: Throwable) {
                resultText.text = "通信エラー: ${t.localizedMessage}"
            }
        })
    }
}
