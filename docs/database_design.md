# LAE Morphology Inspector Ver2 DB設計

## classification

形態分類結果を保存

| カラム名 | 型 | 説明 |
|----------|----|------|
| id | INTEGER | 天体ID |
| image_family | TEXT | images/images_asy/images_obj |
| image_subset | TEXT | LAE_A等 |
| logM | REAL | 質量 |
| Re | REAL | 半光度半径 |
| Re_err | REAL | 誤差 |
| concentration | REAL | C |
| concentration_err | REAL | C誤差 |
| asymmetry | REAL | A |
| asymmetry_err | REAL | A誤差 |
| detectable | INTEGER | 0/1 |
| bright_neighbor | INTEGER | 0/1 |
| multiple_component | INTEGER | 0/1 |
| point_source | INTEGER | 0/1 |
| memo | TEXT | メモ |

## galaxy

研究対象天体の物理量を保存

| カラム名 | 型 | 説明 |
|----------|-----|------|
| id | INTEGER | 天体ID |
| sample | TEXT | LAE/SF/Q |
| ew | REAL | 等価幅 |
| logM | REAL | 質量 |
| Re | REAL | 半光度半径 |
| Re_err | REAL | 誤差 |
| concentration | REAL | C |
| concentration_err | REAL | C誤差 |
| asymmetry | REAL | A |
| asymmetry_err | REAL | A誤差 |

# 画像ディレクトリ構造

images_all/
├ images_all_LAE
├ images_all_SF
├ images_all_Q

├ images_asy_all_LAE
├ images_asy_all_SF
├ images_asy_all_Q

├ images_obj_all_LAE
├ images_obj_all_SF
└ images_obj_all_Q