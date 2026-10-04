# LAE Morphology Inspector Ver2 開発ログ

## Day1

### 目的

Ver1では物理量カタログや判定結果をCSVで管理していた。

しかし、

- 条件検索
- 履歴管理
- データ集計
- データ追跡

を行う際には管理が複雑化していた。

そこでVer2ではSQLiteを導入し、研究データをデータベース管理へ移行することで、検索性・再利用性・追跡性の向上を目指す。

---

### 実施内容

#### プロジェクト準備

- LAE Morphology Inspector Ver2作成
- databaseフォルダ作成
- LAE.db作成

#### DB設計

- database_design.md作成
- classificationテーブル設計
- galaxyテーブル設計

#### SQLite導入

- sqlite3学習
- create_db.py作成
- classificationテーブル生成
- galaxyテーブル生成

#### カタログ調査

- catalog_LAE_F277W_with_err.txt読込
- 列名確認
- データ件数確認

#### データ登録

- import_catalog.py作成
- galaxyテーブルへLAEカタログ登録
- 347天体の登録確認

#### SQL動作確認

- SELECT文実行
- ORDER BY文実行
- LIMIT文実行
- EW上位天体抽出成功

---

### 発見

#### CSV管理の課題

CSV管理では条件検索や履歴確認を行うたびに全データを読み込む必要があった。

#### SQLite導入の利点

必要なデータのみを抽出できるため、検索処理や集計処理を効率的に実行できる。

#### データ件数

- LAEカタログ登録数：347天体

---

### 現在の状態

以下が可能な状態に到達。

- SQLiteデータベース作成
- galaxyテーブル管理
- SQL検索
- SQLソート
- 高EW天体抽出

---

### 課題

- classificationテーブルへの結果保存
- Streamlitとの接続
- SQLフィルタ実装
- 判定履歴管理機能実装

---

### 次回やること

#### 優先度高

- classificationテーブルDB化
- StreamlitからSQLite参照
- SQL検索機能実装

#### 優先度中

- 高EWフィルタ
- 未判定フィルタ
- 判定履歴表示

#### 優先度低

- SQL集計機能
- ダッシュボード機能

---

### 所感

Ver1では研究作業を効率化することに主眼を置いていた。

Ver2ではデータ管理とデータ活用へ焦点を移し、研究支援ツールを研究データ基盤へ発展させる取り組みを開始した。

研究データをSQLiteへ登録し、SQLによる検索を実行できたことで、データベースを用いた管理手法への理解が深まった。

# LAE Morphology Inspector Ver2 開発ログ

## Day2

### 目的

Ver1ではカタログ・判定結果・履歴をCSVで管理していた。

しかし、

- 同一IDの履歴管理
- 条件検索
- 統計集計
- データ追跡

を実施する際にCSV管理の限界が見え始めた。

そこでVer2ではSQLiteを導入し、研究データをデータベース管理へ移行することで、検索性・再利用性・追跡性の向上を目指す。

---

### 実施内容

#### プロジェクト作成

- Ver1をコピーしてVer2作成
- databaseフォルダ作成
- LAE.db作成

#### DB設計

- database_design.md作成
- classificationテーブル設計
- galaxyテーブル設計

#### SQLite導入

- sqlite3学習
- create_db.py作成
- classificationテーブル生成
- galaxyテーブル生成

#### カタログ確認

- catalog_LAE_F277W_with_err.txt読込
- 列名確認
- データ件数確認

#### データベース登録

- import_catalog.py作成
- LAEカタログをgalaxyテーブルへ登録
- 347天体の登録確認

#### SQL学習

- SELECT
- ORDER BY
- LIMIT

を実行

#### SQL検索

- EW上位天体取得
- SQLによる条件検索確認

---

### 発見

#### SQLite導入の利点

従来はCSV全体を読み込み、その後に条件抽出を実施していた。

SQLite導入後は必要なデータのみをSQLで取得できるようになった。

#### データ件数

- LAE登録数：347天体

#### Ver1の課題

運用を進める中で、

- results_master.csv肥大化
- 同一ID履歴管理
- 条件検索
- 複数画像セット比較

などの課題が見え始めていた。

これらはデータベースとの相性が良いと判明した。

---

### classificationテーブル実装

#### DB保存機能作成

- database.py作成
- get_connection()実装
- save_classification()実装

#### 履歴表示機能

- get_history()実装
- app.pyからSQLite履歴取得可能に変更

#### 保存機能

- 保存ボタンからSQLite保存実装
- classificationテーブルへのINSERT成功

---

### 動作確認

#### classificationテーブル

テストデータ登録確認

- ID 123456
- ID 999999

#### Streamlit経由保存確認

- 実データ保存確認
- ID 471055保存成功
- memo = SQLite_test 保存成功

#### 履歴表示確認

- app.py起動成功
- SQLiteから履歴取得成功

---

### 現在の状態

#### Ver1

保存先

- results_master.csv

履歴

- CSV読込

検索

- pandas

#### Ver2

保存先

- classification(SQLite)

カタログ

- galaxy(SQLite)

履歴

- SQLite取得

検索

- SQL利用可能

---

### 現在実装済み

- SQLite導入
- galaxyテーブル
- classificationテーブル
- catalog登録
- SQL検索
- 履歴表示(SQLite)
- 保存(SQLite)

---

### 課題

- 保存済みスキップ機能のSQLite化
- results_master.csv依存の削減
- Streamlit全面SQLite化
- LAE/SF/Q全登録
- SQL集計機能追加

---

### 次回やること

#### 優先度高

- get_saved_ids()実装確認
- 保存済みスキップのDB化
- results_master.csv依存の削減

#### 優先度中

- SQLフィルタ実装
- 高EWフィルタ実装
- 履歴検索強化

#### 優先度低

- ダッシュボード化
- SQL集計機能
- README整備

---

### 所感

Ver1では研究画像判定の効率化を目的としていた。

Ver2では研究データ管理へ着目し、SQLiteおよびSQLを導入することで研究支援ツールを研究データ基盤へ発展させる取り組みを開始した。

特に、

- galaxyテーブルへの347天体登録
- 履歴表示のDB化
- StreamlitからのSQLite保存成功

により、Ver1には存在しなかったデータベース管理環境の構築に成功した。

今後はresults_master.csvに依存している機能を順次SQLiteへ移行し、Ver1の完全上位互換を目指す。

# LAE Morphology Inspector Ver2 開発ログ

## Day3

### 目的

Ver2ではSQLiteによる保存・履歴管理が可能になった。

次の段階として、

- 保存済みスキップ機能
- SQL検索
- SQL集計
- 判定結果集計
- 保存日時管理

を実装し、SQLiteを研究運用へ組み込むことを目的とした。

---

### 実施内容

#### 保存済みスキップ機能SQLite化

database.pyへ

- get_saved_ids()

を実装。

classificationテーブルから保存済みIDを取得できるようになった。

また、

- 保存済みID除外

を実装。

未判定天体のみを表示する運用へ移行した。

---

#### SQL検索機能

database.pyへ

- get_lae_by_ew()

を実装。

SQLによるEW条件検索を追加した。

実装SQL

SELECT *
FROM galaxy
WHERE sample='LAE'
AND ew >= ?
ORDER BY ew DESC

動作確認

EW ≥ 50

→ 316天体取得成功

---

#### SQL統計機能

database.pyへ

- get_sample_statistics()

を実装。

取得項目

- sample
- n
- mean_re
- mean_logM
- mean_c
- mean_a

Streamlitへ

Database Statistics

表示機能を追加。

サンプル統計をリアルタイムに確認可能となった。

---

#### 判定結果集計

database.pyへ

- get_classification_statistics()

を実装。

取得項目

- total
- detectable
- bright_neighbor
- multiple_component
- point_source

SQLite上で判定状況の集計が可能になった。

---

#### created_at追加

classificationテーブルへ

created_at

列を追加。

実行SQL

ALTER TABLE classification
ADD COLUMN created_at TEXT

---

#### 保存日時の自動記録

save_classification()

へ

datetime.now()

を導入。

保存時に

YYYY-MM-DD HH:MM:SS

形式で記録するよう変更した。

---

#### 動作確認

保存日時確認用スクリプトを作成。

created_atが正常に保存されることを確認した。

旧データについては

None

となることを確認。

---

### 保存済み天体管理機能

#### 課題

保存済みスキップ機能導入後、

- 前へボタン
- IDジャンプ

で保存済み天体へ戻れなくなった。

---

#### 設計変更

従来の

前へボタン方式

を廃止。

代わりに

- 未判定モード
- 判定済み天体表示モード

を分離する方針へ変更。

---

#### 保存済み一覧取得

database.pyへ

- get_classified_ids()

を実装。

classificationテーブルとgalaxyテーブルを結合し、

実在する天体のみ一覧へ表示するよう修正した。

---

#### サイドバー実装

追加機能

判定済み天体

保存済みID一覧

保存済み天体を表示

未判定モードへ戻る

---

#### all_df導入

保存済み表示専用に

all_df

を導入。

保存済み表示時はall_dfから取得することで、

- totalflux_lsig
- r20_lsig
- r50_lsig
- r80_lsig

など元カタログ情報を維持したまま再表示可能となった。

---

#### モード表示

通常時

🟦 未判定天体表示モード

判定済み表示時

🟨 判定済み天体表示モード

を表示するよう変更した。

---

#### UI改善

判定済みモードでは

現在: x/y

の表示を廃止。

また、

次へ

ボタンを非表示化した。

未判定処理と保存済み閲覧を明確に分離した。

---

### 発見

#### SQLite管理の有効性

SQLite導入により

- 条件検索
- 履歴管理
- 判定統計
- サンプル統計

をSQLベースで実行できるようになった。

---

#### ワークフローの分離

運用を進める中で、

- 未判定天体処理
- 保存済み天体確認

は別作業であることが判明した。

そのため、

未判定モード

と

判定済み天体表示モード

を分離する設計へ変更した。

---

### 現在の状態

#### DB

✅ galaxyテーブル

✅ classificationテーブル

✅ created_at対応

---

#### SQL

✅ EW検索

✅ SQL集計

✅ 判定統計

---

#### 判定管理

✅ SQLite保存

✅ SQLite履歴

✅ 保存済みスキップ

✅ 保存日時保存

---

#### 保存済み閲覧

✅ 保存済み一覧取得

✅ 保存済み天体表示

✅ 未判定モード復帰

✅ モード分離

---

### 課題

#### 優先度高

- results_master.csv依存の削減
- SQLite単独運用
- 保存済み閲覧UI改善

#### 優先度中

- SQL検索機能拡張
- MassフィルタSQL化
- ReフィルタSQL化

#### 優先度低

- ダッシュボード化
- 統計グラフ表示
- README整備

---

### 所感

Day1ではSQLite導入とgalaxyテーブル構築を行った。

Day2ではclassificationテーブルとStreamlit連携を実装した。

Day3ではSQLiteを研究運用へ本格的に組み込み、

- 保存済みスキップ
- SQL検索
- SQL統計
- 判定統計
- 保存日時管理
- 保存済み天体再表示

を実装した。

特に、

未判定モード

と

判定済み天体表示モード

の分離は、研究運用上の利便性を大きく向上させる設計変更であった。

Ver2は単なるSQLite学習環境から、研究データ基盤として活用できる段階へ到達した。

# LAE Morphology Inspector Ver2 開発ログ

## Day4

### 目的

Ver2ではSQLiteを導入し、検索・履歴管理・統計集計を実装した。

一方で、形態パラメータのサイズ指標については、

- Re：kpc
- r20/r50/r80：pixel

と単位が混在しており、直接比較が困難であった。

そこで、カタログ内のサイズ指標を物理スケール（kpc）へ統一し、より直感的かつ研究利用しやすいデータ基盤への改善を行うことを目的とした。

---

### 実施内容

#### サイズ指標の定義確認

既存カタログを調査し、

- Re
- r20_lsig
- r50_lsig
- r80_lsig

の定義を再確認した。

その結果、

Reはkpc、
r20/r50/r80はpixel

で記録されていることを確認した。

---

#### 変換方法の確認

指導教員から共有されていた資料を確認し、

1 pixel = 0.03 arcsec

であることを確認した。

また、

arcsec/1Mpc

を利用することで、

pixel
↓
arcsec
↓
kpc

へ変換可能であることを確認した。

変換式

size[kpc]
=
size[pixel]
× 0.03
× (1000 / arcsec_1Mpc)

---

#### arcsec_1Mpc対応表作成

COSMOS2020SEDfit_ch126all_z1040.txtを利用し、

ID
arcsec_1Mpc

対応表

arcsec_1Mpc_nonLAE.dat

を作成した。

---

#### LAEカタログkpc化

IDをキーとして対応表と照合し、

- r20_lsig
- err_r20_lsig
- r80_lsig
- err_r80_lsig
- r50_lsig
- err_r50_lsig

をkpcへ変換した。

成果物

catalog_LAE_F277W_with_err_kpc.txt

---

#### SFカタログkpc化

SFカタログについても同様に変換を実施。

成果物

catalog_nonLAE_SF_F277W_with_err_kpc.txt

---

#### Qカタログkpc化

Qカタログについても同様に変換を実施。

成果物

catalog_nonLAE_Q_F277W_with_err_kpc.txt

---

#### Streamlit反映

変換後カタログをプロジェクトへ移行した。

既存コードは変更せず、読み込みカタログをkpc版へ置き換えることで対応した。

---

### 動作確認

#### Reとr50の比較

変換後データを確認したところ、

例：

Re       = 0.779384 kpc
r50_lsig = 0.779384 kpc

となり、

Re ≒ r50

となることを確認した。

変換処理が正しく実装されていることを確認した。

---

#### Streamlit表示確認

天体表示画面にて、

- r20
- r50
- r80

がkpc単位で表示されることを確認した。

例：

r20 = 0.899 kpc
r50 = 2.399 kpc
r80 = 5.963 kpc

---

### 発見

#### Reとr50の関係

当初は

Re < r50

が多く見られたため値の異常を疑った。

しかし調査の結果、

Re：kpc
r50：pixel

という単位の違いが原因であることが判明した。

kpc変換後は両者が一致した。

---

#### 表示単位の重要性

研究用途では単位の混在が誤解の原因となることが分かった。

サイズ指標を物理単位へ統一することで、

- サイズ比較
- EWとの比較
- 質量との比較

が容易になった。

---

### 現在の状態

#### カタログ

✅ LAE kpc化

✅ SF kpc化

✅ Q kpc化

---

#### サイズ指標

✅ r20 kpc

✅ r50 kpc

✅ r80 kpc

✅ Reとの単位統一

---

#### Streamlit

✅ kpc表示対応

✅ 動作確認完了

---

### 課題

#### 優先度高

- SQLiteへの再登録
- galaxyテーブルの更新
- kpc統一版DB構築

#### 優先度中

- SQLによるサイズ条件検索
- Mass条件検索
- EW条件検索拡張

#### 優先度低

- サイズ分布可視化
- ダッシュボード機能

---

### 所感

Day1〜Day3ではSQLite導入と研究データ管理基盤の構築を進めた。

Day4では、形態解析に用いるサイズ指標の単位統一を実施した。特に、Reとr50の不一致が単位の違いによるものであることを突き止め、LAE・SF・Qの全カタログをkpcへ統一できたことは大きな成果であった。

これにより、今後は形態パラメータを物理スケールで直接比較できる環境が整い、研究解析およびデータベース活用の信頼性が向上した。


# LAE Morphology Inspector Ver2 開発ログ

## Day5

### 目的

SQLiteへ移行した銀河カタログについて、統計表示機能の検証を行った。

その過程で、

- mean_logM が異常な値を示す
- SFサンプルの mean_a が表示されない

という問題を発見したため、原因調査と修正を実施した。

---

### 実施内容

#### 統計表示の異常を確認

Database Statisticsにおいて、

mean_logM = 14071941816

のような物理的に不自然な値が表示されることを確認した。

また、

SF の mean_a

のみ空欄となる問題を確認した。

---

#### logM異常値の原因調査

SQLite内の galaxy テーブルを直接確認した。

```sql
SELECT sample, logM
FROM galaxy
LIMIT 10;
```

その結果、

4.1×10^10
1.2×10^9

などの値が保存されていることを確認した。

本来の logM は

9～11

程度であるため、

```python
"logM": df["Ms_med"]
```

に近い状態で保存されていたことが判明した。

---

#### logM計算処理の修正

import_catalog.py を修正し、

```python
"logM": np.log10(df["Ms_med"])
```

を適用した。

その後、SQLiteの galaxy テーブルを再構築した。

---

#### 再インポート処理

kpc変換済みカタログ

- catalog_LAE_F277W_with_err_kpc.txt
- catalog_nonLAE_SF_F277W_with_err_kpc.txt
- catalog_nonLAE_Q_F277W_with_err_kpc.txt

を用いて再度SQLiteへ登録を行った。

```text
LAE: 347 imported.
SF: 3396 imported.
Q: 37 imported.
```

を確認した。

---

#### mean_a欠損問題の調査

初めに

```sql
SELECT COUNT(*)
FROM galaxy
WHERE sample='SF'
AND asymmetry IS NULL;
```

を実行した。

結果

```text
0
```

となり、NULLではないことを確認した。

---

#### -inf値の特定

次に、

```sql
SELECT sample, AVG(asymmetry)
FROM galaxy
GROUP BY sample;
```

を確認した。

結果

```text
LAE : 0.1779
Q   : 0.0873
SF  : -inf
```

となった。

そこで asymmetry に -inf を含む天体を探索した。

結果、

```text
ID 718922
ID 1103622
```

の2天体を特定した。

---

#### 元カタログ調査

対象天体についてカタログを確認したところ、

```text
C_1sig/C_n2p5 = -nan
A_1sig        = -inf
```

となっていることを確認した。

これらは物理的な値ではなく、形態解析の失敗または欠損値であると判断した。

---

#### 異常値処理の実装

import_catalog.py において、

```python
galaxy_df = galaxy_df.replace(
    [np.inf, -np.inf],
    np.nan
)
```

を追加した。

これにより、

```text
±inf
```

を統計計算可能な欠損値へ変換できるようになった。

---

### 結果

Database Statistics は以下のように正常表示されるようになった。

```text
sample   n     mean_re   mean_logM   mean_c   mean_a

LAE      347   1.8261     9.3152     1.384    0.1780

Q         37   2.2239    10.8060     1.4161   0.0873

SF      3396   2.2514     9.4631     1.0790   0.1694
```

---

### 発見

#### LAEの特徴

平均サイズ

```text
Re = 1.83 kpc
```

であり、

SF・Qよりコンパクトな傾向を示した。

---

#### Q銀河の特徴

平均質量

```text
logM = 10.81
```

であり、

LAE・SFより高質量であることを確認した。

また、

```text
mean_c = 1.416
```

であり、

最も中心集中度が高かった。

---

#### データ品質管理の重要性

統計表示の異常を調査した結果、

原因は

- log変換漏れ
- ±inf混入

であった。

研究用データベースにおいて、

データ投入前の品質確認が重要であることを再確認した。

---

### 技術的な学び

今回の調査では、

1. SQLiteによるデータ確認
2. SQLによる集計確認
3. 異常値探索
4. 元データ追跡
5. ETL修正
6. DB再構築

を実施した。

単なる表示修正ではなく、

データ品質問題の発見から原因特定、修正、再投入までを一通り経験できた。

---

### 現在の状態

✅ kpc版カタログ運用

✅ logM修正完了

✅ galaxyテーブル再構築完了

✅ mean_a欠損解消

✅ 統計表示正常化

✅ 異常値検出フロー確立

---

### 今後の課題

#### 優先度高

- image_family/image_subset単位での進捗管理
- get_saved_ids()の改善

#### 優先度中

- SQLによる動的サンプル抽出
- A/C/Re/EW/Massランキング機能

#### 優先度低

- JOINを利用した統合分析機能
- 分布可視化ダッシュボード

# LAE Morphology Inspector Ver2 開発ログ

## Day6

### 目的

Ver2ではSQLiteを利用した検索・統計・履歴管理機能を実装してきた。

一方で、画像確認機能については、

- LAE_A
- LAE_C
- LAE_Re
- SF_A
- SF_C
- SF_Re
- Q_A
- Q_C
- Q_Re

といった静的サブセットに依存していた。

しかし研究運用を見直した結果、これらのサブセットは元々、

```text
上位群
中位群
下位群
```

に分割した後、

```text
10
20
10
```

をランダム抽出した確認用サンプルであることを再確認した。

そこでVer2では、

静的サブセット方式を廃止し、

SQLiteから動的にサンプル抽出を行う仕組みへの移行を開始した。

---

### 実施内容

#### サンプリング方針の再検討

当初は

```sql
ORDER BY
LIMIT
```

を利用したランキング抽出機能を実装した。

対象指標

- EW
- Re
- concentration
- asymmetry
- logM

しかし研究フローを再確認した結果、

上位天体のみを確認するのではなく、

```text
上位群
中位群
下位群
```

からランダムサンプリングしていたことが判明した。

そのためランキング機能は研究目的と一致しないと判断した。

---

#### SQLランキング機能の廃止

実装済みであった

```python
get_ranked_galaxies()
```

の利用を停止。

ランキングベースの確認機能から、

代表サンプル抽出機能へ方針転換した。

---

#### SQLサンプリング機能実装

database.pyへ

```python
get_sampled_galaxies()
```

を追加。

処理内容

```text
対象サンプル取得
↓
指定指標でソート
↓
3分割
↓
上位群
中位群
下位群
↓
ランダム抽出
↓
40天体取得
```

抽出数

```text
上位群 : 10
中位群 : 20
下位群 : 10
```

---

#### UI再設計

従来

```text
画像グループ
↓

LAE_A
LAE_C
LAE_Re
...
```

であった。

新方式では

```text
画像グループ
↓

サンプル
↓

指標
```

を選択する構成へ変更した。

追加項目

```python
sample_select
```

選択肢

- LAE
- SF
- Q

---

#### images_all運用への移行

従来は

```text
images_LAE_A
images_LAE_C
images_LAE_Re
```

などの静的サブセットを利用していた。

新たに

```text
images_all_LAE
images_all_SF
images_all_Q
```

を準備。

SQLで抽出したIDから直接画像を取得する方針へ変更した。

---

### 発見

#### 研究フローの再整理

当初は

```text
A最大20個
```

を調査していたと考えていた。

しかし実際には、

```text
A上位群
A中位群
A下位群
```

を利用していたことが判明した。

これにより、

ランキング抽出ではなく、

代表サンプリングが研究目的に適していることが明確になった。

---

#### 静的サブセットの限界

LAE_Aなどの画像セットは、

研究初期の一時的な確認用サンプルとしては有効であった。

しかし、

- SQL検索
- SQL集計
- 条件変更
- サンプル変更

を行うたびに再生成が必要となる。

SQLite導入後は動的抽出の方が運用効率に優れることが判明した。

---

#### パス設定ミスの発見

画像取得機能の検証中に

```text
fits_files数 = 0
```

となる問題が発生した。

調査の結果、

コード上では

```text
/home/tan/images/images_all_LAE
```

を参照していた。

一方で実際の保存先は

```text
/home/tan/images_all/images_all_LAE
```

であった。

画像ディレクトリ指定が誤っていたことを確認した。

---

### 現在の状態

#### SQLite

✅ galaxyテーブル

✅ classificationテーブル

✅ SQL検索

✅ SQL統計

✅ 判定履歴管理

---

#### サンプリング

✅ get_sampled_galaxies()

✅ 3分割処理

✅ ランダム抽出処理

✅ UI統合開始

---

#### 画像管理

✅ images_all_LAE

✅ images_all_SF

✅ images_all_Q

⚠ パス修正作業中

---

### 課題

#### 優先度高

- images_allへの参照修正
- fits_files取得確認
- sampling_ids動作確認
- サンプリング40天体巡回動作確認

#### 優先度中

- results_master.csv依存削減
- SQLite単独運用化
- image_subset完全撤去

#### 優先度低

- SQL条件サンプリング
- ダッシュボード機能
- 分布比較機能

---

### 所感

Day1〜Day5ではSQLite導入および研究データ基盤の構築を進めてきた。

Day6では研究フローそのものを再確認した結果、従来利用していた静的サブセットが研究本質ではなく、一時的な確認用サンプルであったことが判明した。

この発見により、

```text
静的サブセット運用
↓
SQL動的サンプリング運用
```

への移行方針が明確になった。

また、画像管理についても

```text
images_all_LAE
images_all_SF
images_all_Q
```

を利用した統一管理へ移行する方向性が固まり、Ver2は単なるSQLite対応版から、研究ワークフロー全体を再設計する段階へ進んだ。

#### 画像管理構造の再編

従来は

```text
images_LAE_A
images_LAE_C
images_LAE_Re
...
```

のような静的サブセット構造を利用していた。

動的サンプリング方式へ移行するため、画像を再整理した。

新構成

```text
images_all
├ images_all_LAE
├ images_all_SF
└ images_all_Q

images_asy_all
├ images_all_LAE
├ images_all_SF
└ images_all_Q

images_obj_all
├ images_all_LAE
├ images_all_SF
└ images_all_Q
```

これにより、

- 元画像
- asy画像
- obj画像

のいずれについても、

```text
サンプル選択
↓
SQLサンプリング
↓
画像表示
```

という統一ワークフローを実現できるようになった。

# LAE Morphology Inspector Ver2 開発ログ

## Day7

### 目的

Day6にてSQLサンプリング機能および動的サンプリング運用への移行を開始した。

一方で画面上には、

- 未判定天体数
- 保存済み数
- 進捗率
- サンプリング対象数

など類似する情報が重複して表示されていた。

研究運用では、

```text
何個のサンプルを見ているか
今どこを見ているか
```

が分かれば十分であるため、UIの簡素化を実施した。

---

### 実施内容

#### 進捗表示の整理

従来表示

```text
進捗バー
未判定天体数
保存済み
未判定
進捗率
```

を整理した。

---

#### サンプリング進捗表示実装

sampling_ids を利用し、

```python
current_index
```

から現在位置を算出する処理を追加した。

取得内容

```python
total_num
current_num
```

---

#### UI簡素化

表示内容を

```text
サンプリング対象: 40天体
現在: 1/40
```

へ変更した。

---

### 動作確認

#### 初期表示

```text
サンプリング対象: 40天体
現在: 1/40
```

を確認。

---

#### 巡回表示

```text
次へ
↓
現在: 2/40
```

へ正常更新されることを確認した。

---

### 発見

#### 研究運用に必要な情報

実際の目視判定では、

```text
現在何個見たか
あと何個残っているか
```

のみが重要であることを再認識した。

---

#### UIの簡潔化

情報量を削減することで、

画像確認作業への集中度が向上した。

---

### 現在の状態

✅ サンプリング対象数表示

✅ 現在位置表示

✅ current_index連動

✅ UI整理完了

---

### 所感

機能追加ではなくUI整理であったが、研究運用における作業効率向上への効果は大きかった。

余分な進捗情報を削除することで、サンプリング判定専用UIとしての完成度が向上した。

---

# LAE Morphology Inspector Ver2 開発ログ

## Day8

### 目的

Day6にて導入したSQLサンプリング機能について、

```text
サンプル巡回
```

が正しく動作するかを検証する。

---

### 実施内容

#### current_index管理確認

サンプリング開始時に

```python
st.session_state.current_index = 0
```

となることを確認した。

---

#### 巡回処理確認

次へボタンにより

```python
st.session_state.current_index += 1
```

が実行されることを確認した。

---

#### 停止条件確認

サンプル末尾到達時に

```python
current_index < len(...)
```

条件により停止することを検証した。

---

### 動作確認

サンプル数

```text
5天体
```

でテスト。

結果

```text
1/5
↓
2/5
↓
3/5
↓
4/5
↓
5/5
```

となることを確認した。

---

#### 終端確認

```text
5/5
```

到達後は次へ進まないことを確認した。

---

### 発見

#### sampling_ids運用の有効性

SQL抽出結果を

```python
sampling_ids
```

へ保持することで、

サンプリングデータセットを固定したまま巡回可能であることを確認した。

---

### 現在の状態

✅ サンプル巡回

✅ current_index管理

✅ 末尾停止

✅ 動作確認完了

---

### 所感

サンプリング結果を順番に目視確認するという研究フローを問題なく再現できることを確認した。

---

# LAE Morphology Inspector Ver2 開発ログ

## Day9

### 目的

旧システムから残存している静的サブセット依存を除去し、

```text
image_subset
```

に依存しない構造への完全移行を行う。

---

### 実施内容

#### コード全体調査

検索機能を利用し、

```text
image_subset
```

の残存確認を実施した。

---

#### 依存除去確認

結果

```text
0件
```

であることを確認した。

---

### 発見

#### 設計移行の完了

従来

```text
LAE_A
LAE_C
LAE_Re
```

等に依存していた処理は全て撤去されていた。

現在は

```text
画像グループ
↓
サンプル
↓
指標
```

による動的構成へ完全移行していることを確認した。

---

### 現在の状態

✅ image_subset依存なし

✅ 動的サンプリング運用

✅ 新UI運用

---

### 所感

Ver1系統の構造が完全に整理され、Ver2独自の設計へ移行できた。

---

# LAE Morphology Inspector Ver2 開発ログ

## Day10

### 目的

SQLite中心設計を完成させるため、

```text
results_master.csv
```

への依存を撤去する。

---

### 実施内容

#### CSV依存箇所の探索

以下を全体検索した。

```text
results_master
read_csv
to_csv
os.path.exists
```

---

#### 旧保存処理の削除

発見された

```python
results_master.csv
```

への保存処理を削除した。

削除内容

```python
pd.read_csv(...)
pd.concat(...)
to_csv(...)
```

---

#### 旧管理処理の削除

不要となった

```python
os.path.exists(...)
```

判定を削除した。

---

### 動作確認

検索結果

```text
results_master    0件
to_csv            0件
os.path.exists    0件
```

を確認した。

また、

```python
read_csv(...)
```

についてはカタログ読込用途のみが残り、

results_master.csvとの関連が完全になくなったことを確認した。

---

### 発見

#### SQLite単独運用達成

保存

履歴

進捗管理

保存済み管理

についてCSVを利用しなくても運用可能であることを確認した。

---

### 現在の状態

✅ CSV保存廃止

✅ SQLite保存

✅ SQLite履歴

✅ SQLite進捗管理

✅ CSV依存除去完了

---

### 所感

Ver2最大の目的であったSQLite中心設計へ大きく前進した。

Ver1で運用していた

```text
results_master.csv
```

は不要となり、研究データ管理の一元化を実現できた。

---

# LAE Morphology Inspector Ver2 開発ログ

## Day11

### 目的

SQLite移行状況を総点検し、

Ver1完全上位互換の達成状況を確認する。

---

### 実施内容

#### save_classification確認

database.pyを確認し、

```python
save_classification()
```

がSQLiteへ直接保存していることを確認した。

---

#### get_saved_ids確認

database.pyを確認し、

```sql
SELECT id
FROM classification
WHERE image_family = ?
AND image_subset = ?
```

によって保存済みIDを取得していることを確認した。

---

#### SQLite依存確認

以下を確認した。

```text
保存
履歴
判定済み管理
進捗管理
```

---

### 結果

Ver2運用の主要機能はすべてSQLite管理となった。

---

### 現在の状態

✅ galaxyテーブル

✅ classificationテーブル

✅ SQLite保存

✅ SQLite履歴

✅ SQL検索

✅ SQL統計

✅ 動的サンプリング

✅ サンプル巡回

✅ UI簡素化

---

### 最終到達状態

```text
SQLite
↓
SQL検索
↓
SQLサンプリング
↓
画像確認
↓
判定保存
↓
履歴管理
↓
統計集計
```

を単一システム内で実行可能となった。

---

### Ver2達成事項

✅ SQLite導入

✅ galaxyテーブル

✅ classificationテーブル

✅ SQL検索

✅ SQL統計

✅ 保存済みスキップ

✅ 判定履歴表示

✅ 判定済み天体表示モード

✅ kpc版カタログ対応

✅ images_all化

✅ images_asy_all化

✅ images_obj_all化

✅ SQLサンプリング実装

✅ sampling_ids適用

✅ サンプリング数可変化

✅ サンプル巡回

✅ image_subset完全撤去

✅ results_master.csv依存除去

✅ SQLite単独運用

---

### 所感

Day1からDay11までを通して、

```text
CSV中心運用
↓
SQLite中心運用
↓
SQLサンプリング
↓
研究運用特化UI
```

への移行を完了した。

Ver2は単なる画像判定ツールではなく、

```text
研究データベース
+
形態判定システム
+
サンプリング基盤
```

を統合した研究支援システムへ発展した。

また、

```text
画像グループ
↓
サンプル
↓
指標
↓
SQLサンプリング
↓
画像確認
↓
判定保存
```

という研究運用フローをシステム上で再現できるようになり、Ver1の完全上位互換を達成した。

# LAE Morphology Inspector Ver2 開発ログ

## Day12

### 目的

Ver2ではSQLiteを中心とした研究データ管理および形態判定機能の実装を進めてきた。

一方で、

```text
LAE
SF
Q
```

の物理量および形態パラメータの分布を比較する際には、都度SQL集計や外部解析を行う必要があった。

そこで、

```text
EW
Mass
Re
C
A
```

の分布をアプリ上で直接確認できる研究ダッシュボード機能の実装を行った。

---

### 実施内容

#### ヒストグラム表示機能追加

以下のパラメータについてヒストグラム表示機能を追加した。

```text
EW
log(M*)
Re
C
A
```

各サンプルについてアプリ上で分布を確認可能となった。

---

#### Re分布可視化

```python
matched_df["Re"]
```

を利用し、

```text
Re Distribution
```

を実装した。

サイズ分布を視覚的に確認できるようになった。

---

#### C分布可視化

```python
matched_df["C_1sig/C_n2p5"]
```

を利用し、

```text
C Distribution
```

を実装した。

---

#### 外れ値調査

C分布表示時に、

```text
max = 59.18
```

という極端な値を持つ天体が存在することを確認した。

その結果、

```text
通常天体
→ C ≈ 1

外れ値
→ C ≈ 59
```

であることが判明した。

---

#### 表示改善

外れ値によりヒストグラム全体が圧縮されていたため、

```python
ax.set_xlim(0,3)
```

を導入した。

これにより研究上重要な領域の分布を視覚的に確認できるようになった。

---

#### A分布可視化

```python
matched_df["A_1sig"]
```

を利用したヒストグラムを実装した。

---

#### 異常値対応

A分布表示時に

```text
ValueError
-inf
```

が発生した。

調査の結果、

```text
A = -inf
```

を持つ天体が存在することを確認した。

---

#### 品質管理処理追加

```python
replace([np.inf,-np.inf],np.nan)
dropna()
```

を導入。

異常値を除外してヒストグラムを描画する方式へ変更した。

---

### LAE / SF / Q 比較機能

#### 比較ダッシュボード追加

新機能

```text
LAE / SF / Q比較
```

を実装した。

選択可能パラメータ

```text
Re
C
A
```

---

#### 正規化ヒストグラム導入

天体数

```text
LAE = 347
SF = 3396
Q = 37
```

と大きく異なるため、

```python
density=True
```

を採用した。

---

#### 比較表示

以下のサンプルを重ね描き可能となった。

```text
LAE
SF
Q
```

色設定

```text
LAE : 紫
SF  : 青
Q   : 赤
```

---

#### UI改善

比較ダッシュボードを

```text
Database Statistics
```

直下へ移動した。

配置後

```text
Database Statistics

↓

LAE / SF / Q比較

↓

SQLサンプリング抽出
```

という研究上自然な流れとなった。

---

### 画像管理修正

#### images_asy

画像表示時に

```text
fits_files = 0
```

となる問題を確認した。

---

#### 原因調査

調査の結果、

```text
/home/tan/images_asy_all/
```

を参照していた。

一方、

実際の構成は

```text
/home/tan/images_all/

├ images_all_LAE
├ images_all_SF
├ images_all_Q

├ images_asy_all_LAE
├ images_asy_all_SF
├ images_asy_all_Q
```

であることを確認した。

---

#### パス修正

参照先を修正し、

```text
images_asy_all_LAE
images_asy_all_SF
images_asy_all_Q
```

を正常取得できるようになった。

---

#### 動作確認

```text
images_all
images_asy
images_obj
```

の各画像グループで正常に画像表示できることを確認した。

---

### 発見

#### Re分布

LAEはSFおよびQより小サイズ側へ集中する傾向が確認された。

---

#### C分布

```text
SF
↓
LAE
↓
Q
```

の順に高集中度側へ移行する傾向が視覚的に確認された。

---

#### A分布

LAE・SF・Qの分布は比較的類似しており、

過去の解析結果で得られていた

```text
Aに明確な依存性は見られない
```

という結果と整合した。

---

### 現在の状態

✅ SQLite管理

✅ SQLサンプリング

✅ サンプル巡回

✅ images_all

✅ images_asy

✅ images_obj

✅ EW分布

✅ log(M*)分布

✅ Re分布

✅ C分布

✅ A分布

✅ LAE / SF / Q比較

✅ 研究ダッシュボード実装

---

### 所感

Day12では研究運用を支援する可視化機能を大幅に強化した。

従来は統計値によってのみ確認していた

```text
Re
C
A
```

の違いを、ヒストグラムおよびサンプル比較機能によって直感的に把握できるようになった。

また、

```text
Database Statistics
↓
LAE / SF / Q 比較
↓
SQLサンプリング
↓
画像確認
```

という研究フローに沿ったUI構成が実現され、Ver2は研究データ管理システムから研究解析支援システムへ発展した。

