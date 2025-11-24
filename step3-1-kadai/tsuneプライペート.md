## ダッシュボードを開くとき

私もローカルでの動作確認できました。
Nodeのバージョンでエラー出ましたが、
 ⨯ ./src/app/globals.css
Error evaluating Node.js code
Error: Cannot find module '../lightningcss.darwin-arm64.node'
Macの場合、以下のコードを順に行うと解消されました。
brew install node@20
brew link --overwrite node@20
rm -rf node_modules
rm package-lock.json
npm install
私のKainrisyaKuboshiのブランチはテスト用だったので、在庫管理画面はローカルで立ち上げ後、以下のURLから確認できます！！
http://localhost:3000/admin/inventory


 ## QRコードを開く時

 下記内容をブランチ作成して、上げてます！
・POST /api/users` エンドポイント（backendで table_id → user_id 返却）
・QRコード読み込みコンポーネント実装（frontendで QRスキャン → localStorage 保存）
https://github.com/KaoriOnodera/cl4-sakaba/tree/qr_kumapu#
＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
【既存ファイル修正】
・backend\main.py
・frontend/src/app/page.tsx
・frontend/src/app/success/page.tsx
・frontend/src/components/checkout-screen.tsx
【データベース修正】
・データベース内の特定のロール（ここではservice_role）に対して、データ操作やスキーマの使用に必要な広範な権限を設定
→下記SQLで実行。usersテーブルに追加されなかったので、下記実行
GRANT USAGE ON SCHEMA public TO service_role;

GRANT ALL ON TABLE public.users   TO service_role;
GRANT ALL ON TABLE public.payment TO service_role;
GRANT ALL ON TABLE public.orders  TO service_role;
GRANT ALL ON TABLE public.items   TO service_role;

GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO service_role;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT ALL ON TABLES TO service_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT USAGE, SELECT ON SEQUENCES TO service_role;
・データベースのordersテーブルにあるitem_idカラムのデータ型を変更し、それに伴って外部キー制約を再設定
→注文ボタンを押すとエラーが起きる。かつ、orderテーブルに追加されなかったの下記SQLを実行
ALTER TABLE orders DROP CONSTRAINT IF EXISTS orders_item_id_fkey;
ALTER TABLE orders ALTER COLUMN item_id TYPE integer USING NULL;
ALTER TABLE orders ADD CONSTRAINT orders_item_id_fkey FOREIGN KEY (item_id) REFERENCES items(id);
【新規ファイル作成】
1. frontend/src/app/scan/page.tsx(QRスキャンページ)
・html5-qrcode を統合
・カメラスキャン機能追加
・手動入力機能
2. frontend/src/app/scan/redirect/page.tsx (中継ページ)
・QRコード読み取り後のセッション自動作成
・POST /api/users 呼び出し
・localStorage保存
・メニューへリダイレクト
3. frontend/src/app/scan/generator/page.tsx (QRコード生成ページ)
・10個のQRコード生成
・テストリンク機能
・ダウンロード・印刷機能
＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
テストのやり方は下記です！
テストでやってみて、supabaseのusersテーブルに追加されるの確認できてます！
orderテーブルにも注文内容が入るテストもできていて、決済完了したらそれぞれのテーブルステータスが変更されて、
paymentテーブルに追加されるのも確認済みです！
（テストの流れは、画像を添付しときます！）
＜ PCでのテスト方法＞
①いつものバックエンド、フロントエンド立ち上げる
②http://localhost:3000/scan/generator にアクセス。ここでQRコードが10個生成されてます。
③各QRコードの「Test」ボタンを押すと、メニューにいく（ここでtable_idごとに、user_idが発行付与される）
※出来ない場合は、下記ターミナルで実行
cd frontend npm install qrcode @types/qrcode html5-qrcode
＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
スマホでQR読み込み確認は、デプロイ後できればと思います！