# LAE Morphology Inspector Ver2

修士研究で実施している銀河形態解析を支援するために開発したアプリケーションです。

JWST観測データを用いた

- LAE（Lyα Emitter）
- SF（Star Forming Galaxy）
- Q（Quiescent Galaxy）

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

## 主な機能

### 画像判定

- FITS画像表示
- images_all表示
- images_asy表示
- images_obj表示
- サンプル巡回
- 判定履歴確認

### データベース

- SQLite保存
- 判定履歴管理
- 保存済みスキップ

### SQLサンプリング

- EW条件抽出
- log(M*)条件抽出
- Re条件抽出
- C条件抽出
- A条件抽出
- ランダムサンプリング

### 可視化

- EW分布
- log(M*)分布
- Re分布
- C分布
- A分布

### 比較ダッシュボード

- LAE / SF / Q 比較
- Re比較
- C比較
- A比較

---

## ディレクトリ構成

```text
data/
database/
docs/
images/
output/
src/
