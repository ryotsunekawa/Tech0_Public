# API仕様書

## 【項目1】概要
本サービスは、Next.jsとFastAPIの連携方法を理解し、フロントエンドとバックエンド間の通信処理を学習することを目的とした教習用サービスです。  
APIを通して、文字列や数値データのやり取り・演算処理を体験できます。

---

## 【項目2】認証方式
- 認証は不要です。  
  （学習用のため、認証・認可処理は実装しません）

---

## 【項目3】エンドポイント一覧

| エンドポイント | メソッド | 概要 |
|----------------|-----------|------|
| `http://localhost:8000/api/hello` | GET | 「Hello World つね」のテキストを返す |
| `http://localhost:8000/api/multiply/{multiplyNumber}` | GET | 指定した数値を倍にして返す |
| `http://localhost:8000/api/warizan/{warizanNumber}` | GET | 指定した数値を半分にして返す |
| `http://localhost:8000/api/counter/{text}` | GET | 入力した文字列の文字数を返す |
| `http://localhost:8000/api/echo` | POST | 送信したJSONデータをそのまま返す |

---

## 【項目4】リクエスト・レスポンス仕様

### ① `/api/hello`
**Method:** GET  
**Response:**
```json
{
  "message": "Hello World つね"
}
```

---

### ② `/api/multiply/${multiplyNumber}`
**Method:** GET  
**Example:**  
リクエスト：`GET /api/multiply/5`  
レスポンス：
```json
{
  "doubled_value": 10
}
```

---

### ③ `/api/warizan/${warizanNumber}`
**Method:** GET  
**Example:**  
リクエスト：`GET /api/warizan/10`  
レスポンス：
```json
{
  "half_value": 5
}
```

---

### ④ `/api/counter/${counterNumber}`
**Method:** GET  
**Example:**  
リクエスト：`GET /api/counter/Hello`  
レスポンス：
```json
{
  "counter_value": 5
}
```

---

### ⑤ `/api/echo`
**Method:** POST  
**Request Body:**
```json
{
  "message": "こんにちは"
}
```
**Response:**
```json
{
  "message": "こんにちは"
}
```

---

## 【項目5】FastAPI 実装例
```python
@app.get("/api/hello")
def hello_world():
    return {"message": "Hello World つね"}

@app.get("/api/multiply/{id}")
def multiply(id: int):
    print("multiply")
    doubled_value = id * 2
    return {"doubled_value": doubled_value}

@app.get("/api/warizan/{id}")
def warizan(id: int):
    print("warizan")
    half_value = id / 2
    return {"half_value": half_value}

@app.get("/api/counter/{id}")
def counter(id: int):
    print(id)
    print("counter")
    counter_value = len(str(id))
    print(f"合計値：{counter_value}")
    return {"counter_value": counter_value}

@app.get("/api/warizan/{id}")
def warizan(id: int):
    print("warizan")
    half_value = id / 2
    return {"half_value": half_value}
```

---

## 【項目6】エラーハンドリング
- 予期しないエラーが発生した場合は、以下の形式で返却します。

```jsx
{
      console.error('Error:', error);
}
```


---

## 【項目7】利用制限
- 利用制限なし（学習目的のため）

---

## 【項目8】セキュリティ
- 学習目的のため、特別なセキュリティ対策は不要。  
- 外部公開は行わないことを前提とする。

---

## 【項目9】FAQ

| 質問 | 回答 |
|------|------|
| 誰でも利用できますか？ | はい、ローカル環境であればどなたでも利用できます。 |
| データベースを使用していますか？ | いいえ、DBは使用していません。 |

---

## 【項目10】問い合わせ先
困ったことがあれば、恒川までお問い合わせください。

---

## 補足
- すべてのエンドポイントは **JSON形式** でレスポンスを返します。  
- 文字列・数値の変換エラーなどが発生する可能性があるため、Next.js側では `try...catch` によるエラーハンドリングを推奨します。
