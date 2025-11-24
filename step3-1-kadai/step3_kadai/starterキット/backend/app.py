from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# CORSの設定 フロントエンドからの接続を許可する部分
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# データのスキーマを定義するためのクラス
class EchoMessage(BaseModel):
    message: str | None = None

# Must課題①【簡易メッセージAPI】自身の氏名をレスポンスするエンドポイントとなるように変更してください
# Hello!氏名 とレスポンスするイメージです
# 【注意！】この課題は生成AIを使わずにトライください！
@app.get("/")
def hello():
    return {"message": "hello!つね"}

@app.get("/api/hello")
def hello_world():
    return {"message": "Hello World つね"}

@app.get("/api/multiply/{id}")
def multiply(id: int):
    print("multiply")
    doubled_value = id * 2
    return {"doubled_value": doubled_value}


@app.post("/api/echo")
def echo(message: EchoMessage):
    print("echo")
    if not message:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    echo_message = message.message if message.message else "No message provided"
    return {"message": f"echo: {echo_message}"}

# Must課題②-1【割り算API】フロントエンドから送られた数値を2で割ってレスポンスするエンドポイントを以下に作成してください
# 【注意！】この課題は生成AIを使わずにトライください！（上記の既存エンドポイントをアレンジしてみてください）
# 整数は「int(*integer)」型、文字列は「str(*string)」型になります

@app.get("/api/warizan/{id}")
def warizan(id: int):
    print("warizan")
    half_value = id / 2
    return {"half_value": half_value}


# Want課題①-1【文字数カウントAPI】フロントエンドから送られた文字列をカウントしてレスポンスするエンドポイントを以下に作成してください
# 【注意！】この課題は生成AIを使わずにトライください！（上記の既存エンドポイントをアレンジしてみてください）
# 整数は「int(*integer)」型、文字列は「str(*string)」型になります
# 文字数のカウントは、len関数でカウントできます *例:text_length = len(カウントしたい文字列)

@app.get("/api/counter/{id}")
def counter(id: int):
    print(id)
    print("counter")
    counter_value = len(str(id))
    print(f"合計値：{counter_value}")
    return {"counter_value": counter_value}


# 超Want課題①【HTMLをレスポンスする】backendフォルダ直下のindex.htmlをレスポンスするエンドポイントを以下に作成してください
# Jinja2Templatesライブラリを使うと便利です
# よりライトなアプリを想定し、フロントエンドをNext.jsを使用せずにHTML1ページをレスポンスする練習です


# 超Want課題②【簡単な業務効率化アプリ作成】超Want課題①のHTMLからアップロードしたcsvファイルを受け取り、請求書形式のに変換してレスポンスするプログラムを作成してください
# csvファイルはbackend直下のsample.csvを使用してください
# 請求書形式は任意ですが、参考としてbackend直下に請求書.pngを添付しています


# 超Want課題③【自身の業務効率化アプリ作成】Want課題①を参考に、自身の業務を効率化するアプリを作成してください
# (例)csvファイルをアップロード→取引先別に請求書を作成してPDFで保存するプログラム等
# 上記に限らず、どんな業務でもOKです


# 超Want課題④【超Want課題③アプリのFBをもらう】社内の誰か1人に作成した業務効率化アプリを操作してもらい、FBをもらってください
# 進め方：業務PCでPython環境構築の上、超Want③を実装する→FastAPIを起動する→→社内LANの自身のIPアドレス+PORT番号 で誰かのPCからアクセスしてもらう
# 進め方の詳細は、Starter補足資料の【参考】FastAPIアプリを社内公開する方法 を参照してください
# Python環境構築にあたっては、必要に応じて社内IT部門へポリシーを確認してください

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)