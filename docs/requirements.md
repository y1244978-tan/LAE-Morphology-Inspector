# LAE Morphology Inspector Ver2 要件定義

## 概要

LAE Morphology Inspector Ver2 は、

```text
LAE
SF
Q
```

銀河の形態判定を効率化し、

```text
研究データベース
+
SQLサンプリング
+
画像判定
+
統計可視化
```

を統合した研究支援システムである。

---

# 目的

JWST F277W画像を用いて、

```text
サイズ (Re)
中心集中度 (C)
非対称度 (A)
```

に基づく形態判定を実施する。

また、

```text
LAE
SF
Q
```

の比較解析およびサンプリング研究を支援する。

---

# 入力データ

## カタログ

### LAE

```text
catalog_LAE_F277W_with_err_kpc.txt
```

### SF

```text
catalog_nonLAE_SF_F277W_with_err_kpc.txt
```

### Q

```text
catalog_nonLAE_Q_F277W_with_err_kpc.txt
```

---

## 画像グループ

### Science画像

```text
images_all
```

### Asymmetry画像

```text
images_asy
```

### Residual/Object画像

```text
images_obj
```

---

## 対応サンプル

```text
LAE
SF
Q
```

---

# 画像表示機能

## FITS画像表示

- FITS読込
- 中央切り出し
- ストレッチ表示

---

## 表示補助

- 明るさ調整
- ズーム
- 前画像
- 次画像

---

## 画像モード切替

```text
images_all
images_asy
images_obj
```

の切替が可能。

---

# データベース

## SQLite

データベース

```text
morphology.db
```

を使用する。

---

## galaxyテーブル

保持情報

```text
ID
sample
EW
logM
Re
C
A
```

---

## classificationテーブル

保持情報

```text
ID
sample
image_family

detectable
bright_neighbor
multiple_component
point_source

memo

timestamp
```

---

# 判定機能

## 判定項目

### Detectable

```text
Yes / No
```

---

### Bright Neighbor

```text
Yes / No
```

---

### Multiple Component

```text
Yes / No
```

---

### Point Source

```text
Yes / No
```

---

### Memo

自由入力コメント

---

# 保存機能

## SQLite保存

判定結果を

```text
classification
```

テーブルへ保存する。

---

## 保存済み管理

- 重複保存防止
- 保存済み取得
- 判定履歴保存

---

## 保存済みスキップ

保存済み天体は自動除外可能。

---

# SQL検索

## フィルタ条件

### LAE

- EW下限
- log(M*)下限
- Re下限
- C下限
- A下限

---

### SF

- log(M*)下限
- Re下限
- C下限
- A下限

---

### Q

- log(M*)下限
- Re下限
- C下限
- A下限

---

# SQLサンプリング

## サンプリング対象

```text
LAE
SF
Q
```

---

## 抽出条件

```text
EW
log(M*)
Re
C
A
```

---

## 抽出方式

### ランダムサンプリング

指定数をランダム抽出。

---

### 上位・中位・下位抽出

任意指標について

```text
上位
中位
下位
```

グループを利用した抽出が可能。

---

## セッション管理

```python
sampling_ids
```

により抽出結果を保持する。

---

# サンプル巡回

## current_index管理

サンプリング結果を順番に閲覧する。

---

## ナビゲーション

```text
前へ
次へ
```

---

## 現在位置表示

例

```text
現在: 15 / 40
```

---

## サンプリング対象表示

例

```text
サンプリング対象: 40天体
```

---

# 判定履歴

## 履歴表示

保存済みデータを表示。

---

## 判定済み表示モード

保存済み天体を再閲覧可能。

---

# Database Statistics

## 統計情報

サンプル毎に

```text
件数
平均Re
平均log(M*)
平均C
平均A
```

を表示する。

---

## 表示対象

```text
LAE
SF
Q
```

---

# 可視化機能

## 単独分布

### EW分布

対象

```text
LAE
```

---

### log(M*)分布

対象

```text
LAE
SF
Q
```

---

### Re分布

対象

```text
LAE
SF
Q
```

---

### C分布

対象

```text
LAE
SF
Q
```

---

### A分布

対象

```text
LAE
SF
Q
```

---

## 異常値処理

### A

```text
-inf
inf
```

を除外する。

---

### C

外れ値表示に対応し、

研究対象領域の可視化を優先する。

---

# LAE / SF / Q 比較ダッシュボード

## 比較対象

```text
Re
C
A
```

---

## 表示方式

正規化ヒストグラム

```python
density=True
```

を利用する。

---

## カラー設定

```text
SF  : Blue
LAE : Purple
Q   : Red
```

---

## 表示目的

```text
LAE
SF
Q
```

の形態分布比較を行う。

---

# 進捗管理

## 表示項目

```text
サンプリング対象数
現在位置
```

---

## 自動管理

- 保存済みスキップ
- 巡回連動

---

# UI構成

```text
LAE Morphology Inspector

↓

Database Statistics

↓

LAE / SF / Q 比較

↓

SQLサンプリング抽出

↓

画像表示

↓

判定入力

↓

判定履歴
```

---

# 現在の実装状況

## 実装済み

✅ SQLite導入

✅ galaxyテーブル

✅ classificationテーブル

✅ SQLite保存

✅ 判定履歴

✅ 保存済みスキップ

✅ SQL検索

✅ SQLサンプリング

✅ ランダムサンプリング

✅ サンプル巡回

✅ images_all

✅ images_asy

✅ images_obj

✅ Database Statistics

✅ EW分布

✅ log(M*)分布

✅ Re分布

✅ C分布

✅ A分布

✅ LAE / SF / Q比較

✅ 判定済み閲覧

---

# 今後の拡張候補

## 優先度高

- 判定結果再編集
- 判定条件別抽出
- 保存済みのみ表示強化
- 統計条件保存

---

## 優先度中

- CSVエクスポート
- SQLiteバックアップ
- KDE分布表示
- 平均値ライン表示

---

## 優先度低

- PDFレポート出力
- 自動集計レポート
- 図表保存機能
- 発表用図自動生成

---

# Ver2到達状態

```text
SQLite
↓
Database Statistics
↓
LAE/SF/Q比較
↓
SQLサンプリング
↓
画像確認
↓
判定保存
↓
履歴管理
↓
研究解析
```

を単一アプリケーション内で実現する。