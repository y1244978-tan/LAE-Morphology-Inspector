# LAE Morphology Inspector Ver2

JWST観測データを用いた

LAE・SF・Q銀河の形態判定および研究解析を支援するためのアプリケーションです。

SQLiteを利用した研究データ管理、
SQLサンプリングによる画像確認、
AI推論結果表示によるHuman-in-the-Loop分類環境を提供します。

修士研究で実施している

- LAE (Lyα Emitter)
- SF (Star Forming Galaxy)
- Q (Quiescent Galaxy)

の形態比較研究を対象としており、

- 画像判定
- SQLサンプリング
- SQLiteによるデータ管理
- 統計可視化

を統合的に行うことができます。

---

## 使用技術

- Python
- Streamlit
- SQLite
- Pandas
- NumPy
- Matplotlib

---

## コード構成

### src/app.py

アプリケーション本体です。

- Streamlit UI
- SQLサンプリング
- 銀河画像表示
- 形態判定
- 統計可視化
- LAE / SF / Q比較ダッシュボード

を実装しています。

### src/database.py

SQLiteによるデータ管理機能を実装しています。

- 判定結果保存
- 判定履歴取得
- SQLサンプリング
- 統計集計
- 保存済みサンプル管理

を担当しています。

### src/import_catalog.py

銀河カタログのインポート処理を実装しています。

- カタログ読込
- データ変換
- SQLite登録

を担当しています。

---

## 主な機能

- 銀河画像の閲覧・形態判定
- SQLiteによる判定結果管理
- SQLベースのサンプリング
- EW・log(M*)・Re・C・Aの可視化
- LAE / SF / Q比較解析

### AI分類支援

- AI予測確率表示
- AI予測バー表示
- prediction.csv対応
- prediction_SF.csv対応
- prediction_Q.csv対応
- uncertain.csv対応
- uncertain_SF.csv対応
- uncertain_Q.csv対応
- LAE / SF / Q 推論結果切替
- Human-in-the-Loop運用

### 判定支援

- 前回判定表示
- 判定差分表示
- 更新保存
- 同一判定保存スキップ
- Uncertainモード

---

## 開発ログ

Day1からDay12までの設計検討・実装内容・発見事項を記録しています。

詳細な開発記録は以下にまとめています。

- docs/development_log_v2.md

---

## 研究データについて

研究で使用する画像・カタログ・データベースは公開していません。

本リポジトリではアプリケーションのソースコードのみを公開しています。



## ディレクトリ構成

```text
data/
database/
docs/
images/
output/
src/
├─ app.py
├─ database.py
├─ import_catalog.py
