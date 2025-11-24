# MCP統合型TODOアプリ実装レポート

## 📌 課題概要

**参考記事:** [Qiita: 【検証開始】MCPサーバーの実装から使用まで](https://qiita.com/Sicut_study/items/e0fbbbf51cdd54d76b1a)

**目的:** Model Context Protocol (MCP) を統合した AI 駆動型 TODO 管理アプリケーションの実装

---

## 🔧 実装過程で発生した問題と解決方法

### 1️⃣ Next.js バージョン不一致

**状況:**
- 参考記事のバージョンと異なっていたが、そのまま進めた
- 初期段階ではバージョン差による問題が顕在化しなかった

**学習ポイント:**
- ✅ バージョン差は後続の手順で累積的に影響する
- ✅ 最初の段階でバージョンを確認することが重要
- ✅ 参考記事と異なる場合は、公式ドキュメントで最新の実装方法を確認する必要がある

---

### 2️⃣ Prisma データベースファイルの位置問題

**問題内容:**
```
参考記事: api/prisma/dev.db が想定される位置
実際: 異なる位置に生成されてしまった
```

**解決方法:**
- `prisma/schema.prisma` の `datasource db` 設定を修正
- `DATABASE_URL` 環境変数の パス指定を正確化

**修正例:**
```env
# 修正前
DATABASE_URL="file:./prisma/dev.db"

# 修正後（プロジェクト構造に合わせて調整）
DATABASE_URL="file:./prisma/dev.db"
```

**学習ポイント:**
- ✅ ORMのファイルパスはプロジェクト構造に依存する
- ✅ `DATABASE_URL` の相対パスを確認する
- ✅ Prisma のマイグレーション実行時に初期化位置が決定される

---

### 3️⃣ @prisma/client バージョン不一致

**エラーメッセージ例:**
```
Error: The provided database string is invalid.
Query engine version mismatch.
```

**原因:**
- Prisma のバージョンが複数インストールされていた
- `@prisma/client` と `prisma` のバージョンが一致していない

**解決手順:**
```bash
# 1. node_modules と lock ファイルをクリア
rm -rf node_modules package-lock.json

# 2. 最新バージョンを指定してインストール
npm install

# 3. Prisma クライアントを再生成
npx prisma generate
```

**関連するバージョン情報:**
| パッケージ | 問題のあったバージョン | 解決後のバージョン |
|----------|-------------------|-----------------|
| prisma | 不一致 | ^5.22.0 |
| @prisma/client | 不一致 | ^5.22.0 |

**学習ポイント:**
- ✅ `prisma` と `@prisma/client` のバージョンは完全に一致させる必要がある
- ✅ バージョン不一致は Query Engine の再ダウンロードを必要とする
- ✅ `npm ls prisma` でバージョン重複を検出できる

---

### 4️⃣ 🔴 **最大の課題：Gemini AI 連携エラー**

#### 症状
```
ブラウザ: チャットに「こんにちは」と入力
結果: レスポンスが返ってこない
ブラウザコンソール: 無反応
サーバーログ: エラーメッセージなし
```

#### 原因調査プロセス

**最初の仮説:** Gemini API キー周りの問題
- API キー が正しく設定されているか確認
- `.env.local` に `GOOGLE_GENERATIVE_AI_API_KEY` が存在するか確認
- ❌ これは原因ではなかった

**第2の仮説:** MCP サーバー接続の問題
- MCP サーバー (port 3001) が正常に起動しているか確認
- SSE トランスポートの設定が正しいか確認
- ❌ これも原因ではなかった

**第3の仮説（正解）:** `ai` パッケージのバージョン互換性

#### 根本原因：パッケージバージョンの不一致

**エラーコード：**
```
Export experimental_createMCPClient doesn't exist in target module
```

**原因の詳細:**
| パッケージ | 初期バージョン | 問題 | 解決後のバージョン |
|----------|-------------|------|-----------------|
| `ai` | ^3.4.33 | `experimental_createMCPClient` が存在しない | ^4.3.19 |
| `@ai-sdk/google` | ^2.0.42 | LanguageModelV2 との互換性問題 | ^1.2.22 |

**バージョン依存関係の解決フロー:**
```
ai@3.4.33
  ↓
ai@4.3.19 にアップグレード
  ↓ experimental_createMCPClient が追加
  ↓
@ai-sdk/google@2.0.42 で型エラー発生
  ↓
Property 'defaultObjectGenerationMode' is missing
in type 'LanguageModelV2' but required in type 'LanguageModelV1'
  ↓
@ai-sdk/google@1.2.22 にダウングレード
  ↓
✅ 問題解決
```

#### 発生したエラーメッセージ

**エラー1：MCP クライアント不在**
```
Build error occurred
Error: Turbopack build failed with 1 errors:
./app/api/chat/route.ts:3:1
Export experimental_createMCPClient doesn't exist in target module
```

**原因：** ai@3.4.33 にはこの機能が存在しない

**エラー2：型の互換性**
```
Type error: Property 'defaultObjectGenerationMode' is missing in type 'LanguageModelV2'
but required in type 'LanguageModelV1'.
```

**原因：** @ai-sdk/google@2.0.42 は LanguageModelV2、ai@4 は LanguageModelV1 を要求

#### 解決手順（詳細）

```bash
# ステップ1: ai パッケージをアップグレード
npm install ai@4
# 結果: ai@4.3.19 がインストールされる

# ステップ2: ビルド試行
npm run build
# 結果: @ai-sdk/google の型エラーが発生

# ステップ3: Google SDK をダウングレード
npm install @ai-sdk/google@1
# 結果: @ai-sdk/google@1.2.22 がインストールされる

# ステップ4: ビルド確認
npm run build
# 結果: ✅ ビルド成功
```

**学習ポイント：**
- ✅ 単一パッケージのアップグレードは依存関係のカスケード効果を起こす
- ✅ バージョン互換性エラーは「型エラー」として表現される
- ✅ AI SDK の公式パッケージ間でバージョン互換性が重要
- ✅ エラーメッセージから原因パッケージを特定することが鍵

---

## 📈 実装中のバージョン調整一覧

### サーバー側（api/）

| パッケージ | 参考記事想定 | 実装後 | 変更理由 |
|----------|-----------|-------|--------|
| Hono | ^4.10.6 | ^4.10.6 | 変更なし |
| Prisma | ^5.22.0 | ^5.22.0 | 変更なし |
| Node SDK | 最新 | 最新 | 変更なし |

### MCP サーバー側（mcp/）

| パッケージ | 参考記事想定 | 実装後 | 変更理由 |
|----------|-----------|-------|--------|
| @modelcontextprotocol/sdk | ^1.0.4 | ^1.0.4 | 変更なし |
| Hono | ^4.10.6 | ^4.10.6 | 変更なし |

### フロントエンド側（client/）

| パッケージ | 参考記事想定 | 初期実装 | 最終実装 | 変更理由 |
|----------|----------|--------|--------|---------|
| ai | 最新 | ^3.4.33 | ^4.3.19 | experimental_createMCPClient 必須 |
| @ai-sdk/google | 最新 | ^2.0.42 | ^1.2.22 | LanguageModelV1 互換性 |
| @ai-sdk/react | - | ❌ | ✅ ^1.2.9 | useChat フック標準化 |
| Next.js | 最新 | 16.0.3 | 16.0.3 | 変更なし |
| React | 19.x | 19.2.0 | 19.2.0 | 変更なし |
| TailwindCSS | 4.x | ^4 | ^4 | 変更なし |

---

## 💾 実装と模範解答の差分

### 主要な違い（修正版 vs 模範解答）

#### 1. useChat インポート元の違い

**修正版:**
```typescript
import { useChat } from "ai/react";
```

**模範解答:**
```typescript
import { useChat } from "@ai-sdk/react";
```

**解説:**
- 修正版：`ai` パッケージの React サブパッケージを使用
- 模範解答：専用の `@ai-sdk/react` パッケージを使用
- 推奨：模範解答の方が公式推奨パッケージ

#### 2. chat/route.ts の実装方針

**修正版（エラーハンドリング強化版）:**
```typescript
// 詳細なコンソールログ
console.log("[API] Chat request received");
console.log("[API] Creating MCP client...");
console.log("[API] MCP client created successfully");
console.log("[API] Messages received:", messages.length);
console.log("[API] Fetching tools from MCP server...");
console.log("[API] Tools retrieved:", Object.keys(tools || {}).length);

// 段階的なエラーキャッチ
try {
  mcpClient = await createMcpClient({...});
} catch (err) {
  throw new Error(`MCP Client Error: ...`);
}

// 最終的なエラーハンドリング
} catch (error) {
  console.error("[API] Error in POST handler:", error);
  return new Response(
    JSON.stringify({ error: ... }),
    { status: 500, headers: { "Content-Type": "application/json" } }
  );
}
```

**模範解答（シンプル版）:**
```typescript
export async function POST(req: NextRequest) {
  const mcpClient = await createMcpClient({
    transport: {
      type: "sse",
      url: "http://localhost:3001/sse",
    },
  });

  const { messages } = await req.json();
  const tools = await mcpClient.tools();

  const result = streamText({
    model: google("gemini-2.0-flash-lite"),
    messages,
    tools,
    onFinish: () => {
      mcpClient.close();
    },
  });

  return result.toDataStreamResponse();
}
```

**比較:**

| 項目 | 修正版 | 模範解答 | メリット |
|------|-------|--------|---------|
| **行数** | 65行 | 27行 | 模範解答がシンプル |
| **デバッグログ** | ✅ 詳細 | ❌ なし | 修正版が開発時に有利 |
| **エラーハンドリング** | ✅ あり | ❌ なし | 修正版が本番環境に有利 |
| **可読性** | ⭐⭐ | ⭐⭐⭐ | 模範解答がシンプル |
| **学習効果** | 高い | 高い | 用途による |

**推奨:**
- 開発環境：修正版のエラーハンドリングを参考にする
- 本番環境：模範解答のシンプルさを活用しつつ、エラーハンドリングを統合

#### 3. page.tsx の UI 実装

**主な差分:**

| 機能 | 修正版 | 模範解答 | 説明 |
|------|-------|--------|------|
| **isLoading 状態** | ❌ なし | ✅ あり | 送信中に入力欄を無効化 |
| **タイムスタンプ** | ❌ なし | ✅ あり | メッセージの時刻表示 |
| **Badge コンポーネント** | ❌ なし | ✅ あり | UI の洗練度向上 |
| **formatTime 関数** | ❌ なし | ✅ あり | タイムスタンプのフォーマット |

**修正版での改善提案:**
```typescript
// 1. isLoading 状態を追加
const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
  api: "/api/chat",
  experimental_throttle: 50,
});

// 2. 入力欄の無効化
<Input
  value={input}
  onChange={handleInputChange}
  placeholder="メッセージを入力..."
  disabled={isLoading}  // これを追加
/>

// 3. 送信ボタンの無効化
<Button
  type="submit"
  disabled={isLoading || !input.trim()}  // これを追加
>
  <Send className="h-4 w-4" />
</Button>
```

---

## 🎓 学んだこと・得た知見

### 1. バージョン依存関係の重要性

**教訓:**
```
単一パッケージのアップグレード
  ↓
依存パッケージの互換性チェック必須
  ↓
バージョン情報は `package.json` だけでなく
  型定義ファイル（.d.ts）でも確認が必要
```

**実例：**
- `ai@3.4.33` → `ai@4.3.19` へのアップグレード
- 追加機能：`experimental_createMCPClient` が利用可能
- 副作用：`@ai-sdk/google` との互換性が変わる
- 対応：`@ai-sdk/google@2.0.42` → `@ai-sdk/google@1.2.22` へダウングレード

### 2. エラーメッセージの読み解き方

**バージョン不一致エラーの特徴：**
```
✅ ビルドエラーが「型エラー」として表現される
✅ "Property X is missing in type Y" = 型互換性の問題
✅ "Export X doesn't exist" = パッケージバージョン不足
```

**デバッグのコツ：**
1. エラーメッセージから「どのパッケージ」「どの機能」が問題か特定
2. `npm ls` でバージョン構成を確認
3. 型定義ファイル（`node_modules/*/dist/*.d.ts`）で実装を確認
4. 公式ドキュメントでバージョン互換表を確認

### 3. 開発環境と本番環境のバージョン戦略

**推奨アプローチ：**

| フェーズ | 戦略 | 理由 |
|---------|------|------|
| **開発中** | 最新バージョン + 詳細ログ | 最新機能活用 + デバッグ容易 |
| **テスト** | 互換性確認 + エラーハンドリング | 安定性確保 |
| **本番** | 検証済みバージョン + エラー処理 | 予測可能性 + 保守性 |

**修正版の take-away:**
- ✅ 開発時のログは保持する価値がある
- ✅ エラーハンドリングは本番必須
- ✅ でもシンプルさも大事（模範解答も参考に）

### 4. MCP（Model Context Protocol）の実装パターン

**基本フロー:**
```
1. MCP クライアント作成（SSE トランスポート）
2. ツール情報を MCP サーバーから取得
3. AI モデルに渡す
4. AI がツール呼び出しを実行
5. 結果をストリーム返却
```

**実装時の注意点：**
- ✅ MCP サーバーとクライアントの通信は非同期
- ✅ 接続のクリーンアップ（`mcpClient.close()`）は重要
- ✅ SSE トランスポートはコネクション保持型

---

## 📚 参考資料

### 公式ドキュメント
- [Vercel AI SDK](https://ai-sdk.dev/)
- [Prisma ORM](https://www.prisma.io/docs/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

### バージョン確認コマンド
```bash
# 全パッケージのバージョン構成確認
npm ls

# 特定パッケージの詳細確認
npm ls ai @ai-sdk/google

# キャッシュクリアとクリーンインストール
rm -rf node_modules package-lock.json
npm install
```

### トラブルシューティング
```bash
# Prisma クライアント再生成
npx prisma generate

# キャッシュクリア
npm cache clean --force

# バージョン更新チェック
npm outdated
```

---

## 🎯 今後への改善案

### 短期（すぐに実施可能）
- [ ] 模範解答の `@ai-sdk/react` パッケージに乗り換え
- [ ] `isLoading` 状態管理を実装
- [ ] エラーハンドリングとログを統合

### 中期（構造改善）
- [ ] バージョン互換表をプロジェクト wiki に記載
- [ ] CI/CD で定期的なバージョン更新テストを実施
- [ ] パッケージのバージョンピン（固定）と更新ポリシーを明確化

### 長期（体系化）
- [ ] TypeScript の型チェック厳格化（strict mode）
- [ ] リント・フォーマットルールの統一
- [ ] 依存関係の可視化ツール導入（dependency cruiser など）

---

## 📝 まとめ

### 達成したこと
✅ AI 駆動型 TODO アプリが完全に動作する状態を実装
✅ MCP プロトコルの実装を理解
✅ バージョン依存関係の問題解決方法を習得
✅ エラーメッセージの読み解き方を体得

### 得た教訓
**「バージョンの違いが影響でエラーになっているかどうかを理解する力」は、システム開発に必須のスキル**

パッケージの単純なバージョンアップが連鎖的に影響を及ぼすことを体験し、以下の力が身についた：
1. **依存関係の追跡能力** - どのパッケージが何に依存しているか
2. **型エラーの読解能力** - バージョン不一致を型エラーから特定する
3. **デバッグ戦略** - エラーからパッケージバージョン問題を仮説できる
4. **公式ドキュメント活用** - バージョン互換表を参照できる

---

**レポート作成日:** 2024年11月24日
**プロジェクト:** mcp-todos-tsunekawa-main
**最終バージョン:** 修正版（エラーハンドリング強化版）
