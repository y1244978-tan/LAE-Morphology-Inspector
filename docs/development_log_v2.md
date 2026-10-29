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

# LAE Morphology Inspector Ver2 開発ログ

## Day13

### 目的

Day12まででSQLiteによる研究データ管理およびSQLサンプリング機能を実装した。

本日は実際の研究運用を想定し、

- LAE
- SF
- Q

の全サンプルに対してサンプリング判定を行える環境を整備することを目的とした。

また、実運用中に発見されたカタログ異常値やUI上の課題について修正を実施した。

---

### 実施内容

#### サンプル共通運用確認

従来はLAEを中心に検証を行っていた。

本日は

- LAE
- SF
- Q

すべてのサンプルについて動作確認を実施した。

確認項目

- catalog切替
- SQLサンプリング
- 画像取得
- SQLite保存
- 保存済み閲覧

---

#### サンプリング巡回機能改善

従来

```text
保存
↓
次へ
```

の二段階操作であった。

研究運用では繰り返し回数が多いため、

```text
保存して次へ
```

へ統合した。

---

#### サンプル末尾処理実装

サンプリング対象の最終天体到達時、

```python
current_index
```

が更新されないため、

```text
40/40
```

表示のまま停止していることを確認した。

そこで、

```python
st.stop()
```

を利用し、

```text
🎉 サンプリング対象の判定が完了しました！
```

を表示する処理を実装した。

---

#### SFサンプル動作検証

LAEおよびQは正常動作した。

一方でSFサンプル表示時に、

```python
ValueError:
Unknown format code 'f' for object of type 'str'
```

が発生した。

---

#### 異常データ調査

エラー原因を調査した結果、

```text
ID 718922
ID 1103622
```

において、

```text
NaN
Inf
-Inf
```

および文字化けを含む異常データが存在することを確認した。

また、

```text
r20_lsig
r50_lsig
r80_lsig
```

列についても文字列型として読み込まれる事例を確認した。

---

#### SF異常天体除外

研究対象として利用困難と判断し、

```text
718922
1103622
```

を除外対象へ追加した。

実装内容

```python
if sample_select == "SF":

    exclude_ids = [
        1103622,
        718922
    ]

    matched_df = matched_df[
        ~matched_df["ID"].isin(
            exclude_ids
        )
    ]
```

---

#### カタログ品質管理強化

数値列について型変換処理を追加した。

```python
pd.to_numeric(
    errors="coerce"
)
```

を利用し、

- 文字列
- NaN
- Inf
- -Inf

を欠損値へ変換できるよう改善した。

これにより、

```python
:.3f
```

表示時のエラー発生リスクを低減した。

---

#### サンプリング完了動作確認

LAEサンプル40天体を実際に巡回し、

```text
1/40
↓
2/40
↓
...
↓
40/40
↓
完了表示
```

となることを確認した。

---

#### 保存済み管理UI改善開始

サイドバーの利便性向上を目的として、

- 保存済み件数表示
- サンプル別集計表示
- 保存済みID管理

の改善を開始した。

その過程で、

```python
get_sample_counts()
```

および

```python
get_classified_objects()
```

の設計を実施した。

---

### 動作確認

#### LAE

- SQLサンプリング正常動作
- 40天体巡回成功
- SQLite保存成功

#### SF

- 異常天体除外後に動作確認
- F277W表示成功
- OBJ表示成功
- ASY表示成功
- SQLite保存成功

#### Q

- SQLサンプリング成功
- 画像表示成功
- SQLite保存成功

---

### 発見

#### 実運用で初めて見つかる問題が存在する

Database Statisticsでは検出されなかった問題が、

実際にGUIから全サンプルを巡回したことで発見された。

研究用ソフトウェアでは、

```text
統計確認
+
GUI運用確認
```

の両方が重要であることを再認識した。

---

#### SFサンプルのデータ品質問題

SFサンプルには、

```text
nan
inf
-inf
```

を含む天体が存在することが判明した。

今後はカタログ投入前に品質確認処理を行う必要がある。

---

#### 全サンプル検証の重要性

LAEで正常動作する機能でも、

SFやQへ適用すると問題が発生する場合があることが分かった。

今後の機能追加では

- LAE
- SF
- Q

すべてで確認する方針とする。

---

### 現在の状態

#### サンプリング

✅ SQLサンプリング

✅ サンプル巡回

✅ 保存して次へ

✅ サンプリング完了表示

✅ サンプル数可変

---

#### SQLite

✅ 保存

✅ 履歴

✅ 保存済み管理

✅ 判定済み天体表示

---

#### 品質管理

✅ SF異常天体検出

✅ 異常天体除外

✅ 型変換処理

✅ エラー原因特定

---

### 課題

#### 優先度高

- 保存済み件数表示
- サンプル別進捗表示
- 保存済み一覧改善

#### 優先度中

- SQLによる進捗管理
- 判定統計ダッシュボード
- フィルタ機能強化

#### 優先度低

- GUIデザイン改善
- README更新
- コード整理

---

### 所感

Day13ではVer2で構築してきた機能を実際の研究運用へ適用し、LAE・SF・Qの全サンプルに対する判定環境を整備した。

特に、

```text
SQLサンプリング
↓
画像表示
↓
判定
↓
SQLite保存
↓
履歴管理
```

という一連のワークフローを実際の研究フローとして運用できることを確認できた。

また、SFサンプルに含まれる異常値を発見し、GUIレベルで問題を特定・修正できたことで、研究ツールとしての信頼性が向上した。


# LAE Morphology Inspector Ver2 開発ログ

## Day14

### 目的

Day13までで、

- SQLite中心運用
- SQLサンプリング
- 保存済み天体管理
- 研究ダッシュボード

の実装を完了した。

本日は実際にLAEサンプルの形態判定を進めるとともに、

- Point Source判定基準の整理
- ASY画像の解釈
- 教師データ作成
- 保存済み天体再編集機能

について検討・整備を行うことを目的とした。

---

### 実施内容

#### Point Source判定基準の再整理

研究運用中にPoint Source判定のばらつきが見られたため、

以下の基準へ整理した。

Point Source条件

・Detectable

・Bright Neighborなし

・Multiple Componentなし

・OBJが概ね円形

・F277W PSF(FWHM)
  ≈ 0.12 - 0.13 arcsec

・r50がPSFサイズに近い

参考指標

r50 ≲ 0.13 arcsec

---

#### ASY画像の解釈整理

ASY画像について再検討を実施。

定義

ASY
=
元画像
-
180°回転画像

であることを再確認した。

解釈

Point Source

→ ASY残差が小さい

Bright Neighbor

→ Neighbor位置に残差

Multiple Component

→ 中心付近に複数残差

---

#### 「残差が大きい」の定義見直し

当初は

「白画素が多い」

ことを残差が大きいと考えていた。

しかし実際には、

・中心周辺の微弱残差

と

・中心から離れた島状残差

では意味が異なることが分かった。

新しい見方

残差が大きい

↓

中心から離れた位置に

まとまった構造が残る

と定義した。

---

#### Point Source候補の比較

複数天体について

F277W
OBJ
ASY

を比較し、

以下の傾向を確認した。

Point Source候補

・r50 ≈ 0.09–0.12 arcsec

・r80/r50 ≈ 1.5–2.0

・OBJ単峰

・Neighborなし

・ASYが比較的静か

---

### 教師データ作成

#### export_labels.py作成

SQLiteから判定結果を出力する処理を作成。

取得項目

- id
- image_subset
- detectable
- bright_neighbor
- multiple_component
- point_source
- memo
- created_at

---

#### 重複除去実装

同一天体を再判定した場合、

最新判定のみ利用する方針を採用。

実装

df = df.sort_values(
    "created_at"
)

df = df.drop_duplicates(
    subset=["id"],
    keep="last"
)

---

#### 集計機能追加

出力時にラベル集計を表示するよう改善した。

---

### 判定結果

重複除去前

217件

重複除去後

200件

実質教師データ数

200天体

---

### 教師データ集計

総天体数

200

Detectable

177
(88.5%)

Bright Neighbor

46
(23.0%)

Multiple Component

71
(35.5%)

Point Source

55
(27.5%)

---

### 保存済み再編集機能の調査

#### 問題

保存済み天体表示モードでは

チェックボックスは表示されるが

保存ボタンが表示されない。

---

#### 原因調査

コード確認の結果、

以下の条件が存在することを確認。

if not saved_mode:

    if st.button(
        "保存して次へ"
    ):

保存済みモードでは

saved_mode = True

となるため、

保存ボタン自体が非表示となっていた。

---

#### 改善方針

保存済み天体についても

再判定

↓

再保存

↓

履歴追加

を実施可能とする。

実装予定

未判定モード

↓

「保存して次へ」

保存済みモード

↓

「更新保存」

---

### バグ調査

#### サンプリング完了表示

現象

フィルタ後天体数

44

が表示されているにも関わらず、

🎉 サンプリング対象の判定が完了しました！

が表示された。

---

#### 原因候補

current_index

と

matched_df

の不整合が疑われる。

特に、

サンプリングモードを使用せずに

全体巡回した場合に、

完了判定条件が誤作動する可能性を確認した。

---

#### 今後の確認事項

確認用出力

st.write(
    st.session_state.current_index
)

st.write(
    len(matched_df)
)

を追加し、

完了判定条件の検証を行う。

---

### 品質管理

#### 0,0,0,0天体の再調査

運用中、

バグにより

チェックを付けられなかった可能性のある天体が存在することを確認した。

対象条件

detectable = 0

bright_neighbor = 0

multiple_component = 0

point_source = 0

---

#### 再確認方針

SQLiteまたは出力CSVから

0,0,0,0

天体を抽出し、

保存済みモードで再評価を実施する。

---

### 発見

#### Point Source判定は単一指標では不十分

r50だけでは判断困難な境界例が多数存在した。

今後は

・r50

・r80/r50

・OBJ形状

・ASY残差

を総合的に利用する。

---

#### ASY画像は重要な補助指標

ASYは

単なるノイズ画像ではなく、

Neighbor

Multiple

非対称構造

を発見する強力な補助情報であることが分かった。

---

#### 教師データとして十分な規模へ到達

重複除去後

200天体

の教師データを取得した。

今後は

Point Source群

vs

Non Point Source群

の統計比較へ進める段階に到達した。

---

### 現在の状態

#### 教師データ

✅ 判定数200件

✅ 重複除去実装

✅ CSV出力

✅ ラベル集計

---

#### Point Source評価

✅ r50表示

✅ r80表示

✅ r80/r50表示

✅ ASY運用開始

✅ 判定基準整理完了

---

#### SQLite

✅ 保存

✅ 履歴

✅ サンプリング

✅ 保存済み表示

⚠ 保存済み再編集機能改修中

---

### 課題

#### 優先度高

- 保存済み天体の更新保存
- 0,0,0,0天体の再判定
- サンプリング完了判定バグ修正

#### 優先度中

- Point Source群統計解析
- Re/C/A/r50比較
- 教師データ品質向上

#### 優先度低

- 自動分類開発
- 教師なし分類検討
- ダッシュボード拡張

---

### 所感

Day14では研究運用を通じてPoint Source判定基準を見直し、ASY画像の活用方法を整理した。

また、SQLiteに蓄積された判定結果から200天体の教師データを構築できたことは大きな成果であった。

特に、

Point Source

↓

定量基準

↓

統計解析

という流れが見え始めており、

LAE Morphology Inspector Ver2 は

単なる画像閲覧ツールから、

教師データ構築基盤および形態分類研究基盤として活用できる段階へ到達した。

# LAE Morphology Inspector Ver2 開発ログ

## Day15

### 目的

Day14までで、

- SQLite中心運用
- SQLサンプリング
- 教師データ構築
- 保存済み天体管理

を実装した。

一方で、
AI開発プロジェクトとの連携は未実装であり、

AI学習
↓
推論
↓
人間確認
↓
教師データ修正

という Human-in-the-Loop 運用をシステム上で実施できていなかった。

そこで本日は、

- AI推論結果表示
- Uncertain天体抽出
- 前回判定との比較
- SF/Q対応
- AI連携強化

を実装し、InspectorをAI分類支援システムへ発展させることを目的とした。

---

### 実施内容

#### AI推論結果表示機能

AIプロジェクトで生成した

prediction.csv

を読み込み、

- Detectable
- Bright Neighbor
- Multiple Component
- Point Source

の推論結果を画面上へ表示する機能を実装した。

表示内容

- AI予測確率
- 進捗バー

例

Detectable

96.4%

これにより、人間の判定とAI予測を同時に確認可能となった。

---

#### Human Label + AI Prediction表示

従来は現在のチェック状態のみ表示していた。

新たに

前回判定
↓
現在判定
↓
AI予測

を同時表示するUIへ変更した。

表示項目

- 前回判定
- 現在判定
- AI予測確率
- AI確率バー

これにより、

人間
vs
過去の自分
vs
AI

の比較が可能になった。

---

#### 前回判定比較機能

SQLite履歴取得機能を利用し、

get_history()

から最新判定を取得する処理を実装した。

判定変更検出機能を追加し、

前回と一致

の場合

✅ 前回判定と一致

を表示。

変更があった場合

⚠ 前回判定から変更あり

を表示するよう改善した。

---

#### 更新保存機能

保存済み天体表示モードについて改修を実施した。

従来

保存済み表示

↓

編集不可

であった。

変更後

保存済み表示

↓

更新保存

↓

履歴追加

を実行可能とした。

ボタン表示

未判定モード

↓

保存して次へ

保存済みモード

↓

更新保存

へ変更した。

---

#### 同一判定保存スキップ機能

前回判定と同一内容の場合、

SQLiteへ不要な履歴を追加しない処理を実装した。

判定内容比較

- Detectable
- Bright Neighbor
- Multiple Component
- Point Source

が完全一致した場合

保存をスキップ

するよう変更した。

---

#### Uncertain表示機能

AI推論結果から

uncertain.csv

を読み込み、

AIが迷った天体のみを表示するモードを実装した。

追加モード

🟥 Uncertain

判定条件

min(|p - 0.5|) < 0.10

これにより、

AIが自信を持てない天体

のみを優先的に確認できるようになった。

---

#### モード表示追加

表示モードを整理し、

🟦 未判定

🟨 判定済み

🟥 Uncertain

を切り替えられるよう改善した。

現在の状態を画面上部へ表示するよう変更した。

---

#### SF推論結果対応

AIプロジェクトで生成した

prediction_SF.csv

uncertain_SF.csv

へ対応した。

サイドバーへ

推論結果

- LAE
- SF
- Q

を追加した。

選択したサンプルに応じて、

prediction

および

uncertain

を自動切替する構成へ変更した。

---

#### Q推論結果対応

追加ファイル

- prediction_Q.csv
- uncertain_Q.csv

へ対応した。

これにより、

LAE
SF
Q

すべてについてAI結果を閲覧可能となった。

---

#### LAE / SF / Q統合化

従来は

サンプル選択

と

推論結果選択

が独立していた。

運用上のミス防止のため、

推論結果

↓

サンプル自動切替

へ変更した。

例

推論結果 = SF

↓

sample_select = SF

と自動設定される。

---

### 動作確認

#### LAE

- AI確率表示成功
- 前回判定取得成功
- Uncertain表示成功

---

#### SF

- prediction_SF.csv読込成功
- uncertain_SF.csv読込成功
- AI確率表示成功
- Uncertain件数表示成功

結果

SF Uncertain

764件

を確認した。

---

#### Q

- prediction_Q.csv読込成功
- uncertain_Q.csv読込成功
- AI確率表示成功

を確認した。

---

### 発見

#### Human-in-the-Loop運用の有効性

これまでの運用は

人間
↓
教師データ作成

のみであった。

今回、

AI
↓
Uncertain抽出
↓
人間確認

というループを構築したことで、

人間が優先的に確認すべき天体を絞り込めるようになった。

---

#### AIは判定支援ツールとして有効

AI予測と人間判定を比較することで、

- AIの誤分類
- 人間の誤判定
- ラベル不整合

を発見しやすくなった。

今後の教師データ改善に有効であると考えられる。

---

#### SFへの展開

LAE教師データのみを利用して学習したAIを、

3394天体のSFサンプルへ適用できた。

その結果、

764件

のUncertainサンプルへ絞り込むことに成功した。

人間確認対象を大幅に削減できる可能性がある。

---

### 現在の状態

#### AI連携

✅ AI確率表示

✅ AIバー表示

✅ prediction.csv対応

✅ prediction_SF.csv対応

✅ prediction_Q.csv対応

✅ Uncertain対応

---

#### 判定支援

✅ 前回判定表示

✅ 判定差分表示

✅ 更新保存

✅ 保存スキップ

---

#### サンプル対応

✅ LAE

✅ SF

✅ Q

✅ 自動切替

---

#### Human-in-the-Loop

✅ AI推論

✅ Uncertain抽出

✅ 人間確認

✅ 教師データ改善基盤

---

### 課題

#### 優先度高

- Uncertain優先巡回機能
- AI予測による並び替え
- 誤分類レビュー機能

#### 優先度中

- AI予測履歴保存
- AIと人間の一致率集計
- 誤分類統計ダッシュボード

#### 優先度低

- Active Learning導入
- 半教師あり学習連携
- ラベル推薦機能

---

### 所感

Day15ではInspectorとAIシステムを統合し、

教師データ作成ツール

から

AI分類支援システム

へ発展させることができた。

特に、

AI推論
↓
Uncertain抽出
↓
人間確認
↓
教師データ修正
↓
再学習

という継続的改善サイクルをシステム上で実現できたことは大きな成果であった。

また、

LAE
SF
Q

の全サンプルに対して同一UI上でAI結果を確認できるようになり、Inspectorは単なる画像閲覧ソフトではなく、形態分類研究のためのHuman-in-the-Loop基盤へ発展した。
