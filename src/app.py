import streamlit as st

#キャッシュ
@st.cache_data
def load_catalog(path):

    return pd.read_csv(
        path,
        sep=r"\s+",
        encoding="cp932"
    )

@st.cache_data
def load_prediction(target):

    if target == "LAE":

        file = "data/prediction.csv"

    elif target == "SF":

        file = "data/prediction_SF.csv"

    else:

        file = "data/prediction_Q.csv"

    return pd.read_csv(file)

@st.cache_data
def load_uncertain(target):

    if target == "LAE":

        file = "data/uncertain.csv"

    elif target == "SF":

        file = "data/uncertain_SF.csv"

    else:

        file = "data/uncertain_Q.csv"

    return pd.read_csv(file)

@st.cache_data
def get_fits_files(folder):

    return glob.glob(
        folder + r"\**\*.fits",
        recursive=True
    )

import pandas as pd
import glob
import re
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np
from database import (
    get_history,
    save_classification,
    get_saved_ids,
    get_classified_ids,
    get_lae_by_ew,
    get_sample_statistics,
    get_sampled_galaxies,
    get_sample_counts,
    get_classified_objects
)

# タイトル
st.title("LAE Morphology Inspector")

prediction_target = st.sidebar.radio(
    "推論結果",
    [
        "LAE",
        "SF",
        "Q"
    ]
)

uncertain_df = load_uncertain(
    prediction_target
)

prediction_df = load_prediction(
    prediction_target
)

# ------------------------
# Display Mode
# ------------------------

st.sidebar.markdown("---")

st.sidebar.subheader(
    "表示モード"
)

view_mode = st.sidebar.radio(
    "",
    [
        "🟦 未判定",
        "🟨 判定済み",
        "🟥 Uncertain"
    ]
)

st.sidebar.metric(
    f"{prediction_target} Uncertain",
    len(uncertain_df)
)


st.sidebar.markdown("---")


# ------------------------
# Main Mode Banner
# ------------------------

if view_mode == "🟦 未判定":

    st.info(
        "🟦 未判定天体表示モード"
    )

elif view_mode == "🟨 判定済み":

    st.warning(
        "🟨 判定済み天体表示モード"
    )

elif view_mode == "🟥 Uncertain":

    st.error(
        "🟥 AIが迷った天体（Uncertain）表示モード"
    )


# -----------------------------
# Session State 初期化
# -----------------------------

if "current_index" not in st.session_state:
    st.session_state.current_index = 0

if "saved" not in st.session_state:
    st.session_state.saved = False



#----------------
# サイドバー
#----------------

st.sidebar.subheader(
    "判定済み天体"
)

classified_ids = get_classified_ids()

st.sidebar.write(
    f"保存済み件数 : {len(classified_ids)}"
)

sample_counts = get_sample_counts()

st.sidebar.markdown(
    "### サンプル別件数"
)

for _, row in sample_counts.iterrows():

    st.sidebar.write(
        f"{row['image_subset']} : {row['n']}"
    )

saved_df = get_classified_objects()

options = {
    f"{row['image_subset']} | {row['id']}":
    row["id"]
    for _, row in saved_df.iterrows()
}

selected_label = st.sidebar.selectbox(
    "保存済みID",
    list(options.keys())
)

selected_id = options[selected_label]


# ----------------
# 判定基準
# ----------------

st.sidebar.markdown("---")

st.sidebar.subheader(
    "判定基準"
)

st.sidebar.markdown("""
### Detectable
・OBJで有意に検出されている

・OBJで中心に集中している

### Bright Neighbor
・近傍に独立した明るい天体が存在

### Multiple Component
・複数ピークが存在

### Point Source
・OBJがほぼ円形

・Bright Neighborなし

・Multiple Componentなし

・F277W PSF(FWHM)
  ≈ 0.12 - 0.13 arcsec

・r50 が
  0.12 - 0.13 arcsec
  に近いほど点源候補
""")




# -----------------------------
# SQLサンプリング抽出
# -----------------------------

st.subheader("SQLサンプリング抽出")

#画像選択

sample_select = prediction_target

metric_rank = st.selectbox(
    "指標",
    [
        "Re",
        "concentration",
        "asymmetry",
        "logM",
        "ew"
    ]
)

high_n = st.number_input(
    "上位群サンプル数",
    min_value=0,
    value=10
)

mid_n = st.number_input(
    "中位群サンプル数",
    min_value=0,
    value=20
)

low_n = st.number_input(
    "下位群サンプル数",
    min_value=0,
    value=10
)



sampled_df = get_sampled_galaxies(
    sample=sample_select,
    metric=metric_rank,
    high_n=high_n,
    mid_n=mid_n,
    low_n=low_n
)

with st.expander(
    f"サンプリング結果 ({len(sampled_df)}件)"
):

    st.dataframe(
        sampled_df[
            [
                "id",
                "logM",
                "Re",
                "concentration",
                "asymmetry"
            ]
        ]
    )

if st.button("サンプリング結果を閲覧対象にする"):

    st.session_state.sampling_ids = (
        sampled_df["id"].tolist()
    )

    st.session_state.current_index = 0

    st.rerun()

if (
    "sampling_ids"
    in st.session_state
):

    if st.button(
        "サンプリング解除"
    ):

        del st.session_state[
            "sampling_ids"
        ]

        st.session_state.current_index = 0

        st.rerun()




# 観測カタログ読み込み（絶対消さない）

if sample_select == "LAE":

    catalog_file = (
        "data/catalog_LAE_F277W_with_err_kpc.txt"
    )

elif sample_select == "SF":

    catalog_file = (
        "data/catalog_nonLAE_SF_F277W_with_err_kpc.txt"
    )

elif sample_select == "Q":

    catalog_file = (
        "data/catalog_nonLAE_Q_F277W_with_err_kpc.txt"
    )


df = load_catalog(
    catalog_file,
    
)

#pixelカタログ
if sample_select == "LAE":

    pixel_catalog_file = (
        "data/catalog_LAE_F277W_with_err.txt"
    )

elif sample_select == "SF":

    pixel_catalog_file = (
        "data/catalog_nonLAE_SF_F277W_with_err.txt"
    )

else:

    pixel_catalog_file = (
        "data/catalog_nonLAE_Q_F277W_with_err.txt"
    )

pixel_df = load_catalog(
    pixel_catalog_file,
    
)



with st.expander("Prediction CSV Check"):

    st.write(prediction_df.head())

    st.write(
        f"prediction件数: {len(prediction_df)}"
    )





#SF動作用
for col in [
    "r20_lsig",
    "err_r20_lsig",
    "r50_lsig",
    "err_r50_lsig",
    "r80_lsig",
    "err_r80_lsig"
]:
    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

# --------------------------------
# 画像フォルダ
# --------------------------------

base_path = (
    r"\\wsl.localhost\Ubuntu\home\tan\images_all"
)

f277w_folder = (
    rf"{base_path}\images_all_{sample_select}"
)

obj_folder = (
    rf"{base_path}\images_obj_all_{sample_select}"
)

asy_folder = (
    rf"{base_path}\images_asy_all_{sample_select}"
)

with st.expander("画像フォルダ情報"):

    st.write("F277W :", f277w_folder)
    st.write("OBJ   :", obj_folder)
    st.write("ASY   :", asy_folder)

fits_files = glob.glob(
    f277w_folder + r"\**\*.fits",
    recursive=True
)


# FITSファイル名からID抽出
id_list = []

for file in fits_files:

    match = re.search(r"id(\d+)\.fits", file)

    if match:
        id_list.append(int(match.group(1)))


# catalogと画像IDを照合

matched_df = df[df["ID"].isin(id_list)]

# SFの異常データを除外
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
    

if (
    "sampling_ids"
    in st.session_state
):

    matched_df = matched_df[
        matched_df["ID"].isin(
            st.session_state.sampling_ids
        )
    ]
    




all_df = matched_df.copy()

if "sampling_ids" in st.session_state:

    matched_df = matched_df[
        matched_df["ID"].isin(
            st.session_state.sampling_ids
        )
    ]

    total_objects = len(
        st.session_state.sampling_ids
    )

    remaining_objects = len(
        matched_df
    )

    completed_objects = (
        total_objects
        - remaining_objects
    )

    total_num = len(
        st.session_state.sampling_ids
    )

    current_num = (
        st.session_state.current_index + 1
    )

    st.info(
        f"サンプリング対象: {total_num}天体 | "
        f"現在: {current_num}/{total_num}"
    )

else:

    saved_ids = get_saved_ids(
        "all",
        sample_select
    )

    if view_mode == "🟦 未判定":

        matched_df = matched_df[
            ~matched_df["ID"].isin(saved_ids)
        ]

    elif view_mode == "🟨 判定済み":

        matched_df = matched_df[
            matched_df["ID"].isin(saved_ids)
        ]

    elif view_mode == "🟥 Uncertain":

        uncertain_ids = (
            uncertain_df["id"]
            .astype(int)
            .tolist()
        )

        matched_df = matched_df[
            matched_df["ID"].isin(
                uncertain_ids
            )
        ]

    total_objects = len(
        df[df["ID"].isin(id_list)]
    )

    remaining_objects = len(
        matched_df
    )

    completed_objects = (
        total_objects
        - remaining_objects
    )








#EWフィルタ(LAEのみ作用/SFとQでは作用しない)
if sample_select == "LAE":

    min_ew = st.number_input(
        "最小EW",
        min_value=0.0,
        value=0.0
    )

if sample_select == "LAE":

    matched_df = matched_df[
        matched_df["EW"] >= min_ew
    ]
#追加したもの
if sample_select == "LAE":

    sql_df = get_lae_by_ew(min_ew)

    st.write(
        f"SQL取得件数: {len(sql_df)}"
    )    

#Massフィルタ
min_log_mass = st.slider(
    "最小 log(M*)",
    min_value=7.0,
    max_value=12.0,
    value=7.0,
    step=0.1
)

matched_df = matched_df[
    matched_df["Ms_med"] >= 10**min_log_mass
]

matched_df["logM"] = np.log10(
    matched_df["Ms_med"]
)



st.metric(
    "フィルタ後天体数",
    len(matched_df)
)

# -----------------------
# Statistics
# -----------------------

with st.expander("📊 サンプル統計"):

    # EW
    st.subheader("EW分布")

    fig, ax = plt.subplots()

    if sample_select == "LAE":

        ax.hist(
            matched_df["EW"],
            bins=20
        )

    ax.set_title("EW Distribution")
    ax.set_xlabel("EW")
    ax.set_ylabel("Number")

    st.pyplot(fig)

    # Re
    st.subheader("Re分布")

    fig, ax = plt.subplots()

    ax.hist(
        matched_df["Re"],
        bins=20
    )

    ax.set_title("Re Distribution")
    ax.set_xlabel("Re (kpc)")
    ax.set_ylabel("Number")

    st.pyplot(fig)

    # C
    st.subheader("C分布")

    c_data = matched_df[
        matched_df["C_1sig/C_n2p5"] < 5
    ]["C_1sig/C_n2p5"]

    fig, ax = plt.subplots()

    ax.hist(
        c_data,
        bins=50
    )

    ax.set_xlim(0, 3)

    ax.set_title("C Distribution")
    ax.set_xlabel("Concentration")
    ax.set_ylabel("Number")

    st.pyplot(fig)

    # A
    st.subheader("A分布")

    a_data = matched_df["A_1sig"]

    a_data = a_data.replace(
        [np.inf, -np.inf],
        np.nan
    )

    a_data = a_data.dropna()

    fig, ax = plt.subplots()

    ax.hist(
        a_data,
        bins=50
    )

    ax.set_title("A Distribution")
    ax.set_xlabel("Asymmetry")
    ax.set_ylabel("Number")

    st.pyplot(fig)

    # Mass
    st.subheader("log(M*)分布")

    fig, ax = plt.subplots()

    ax.hist(
        np.log10(
            matched_df["Ms_med"]
        ),
        bins=20
    )

    ax.set_title("Mass Distribution")
    ax.set_xlabel("log(M*)")
    ax.set_ylabel("Number")

    st.pyplot(fig)


with st.expander("📈 LAE / SF / Q 比較"):

    compare_param = st.selectbox(
        "比較パラメータ",
        ["Re", "C", "A"]
    )

    lae_df = load_catalog(
        "data/catalog_LAE_F277W_with_err_kpc.txt"
    )

    sf_df = load_catalog(
        "data/catalog_nonLAE_SF_F277W_with_err_kpc.txt"
    )

    q_df = load_catalog(
        "data/catalog_nonLAE_Q_F277W_with_err_kpc.txt"
    )

    if compare_param == "Re":

        fig, ax = plt.subplots()

        ax.hist(
            lae_df["Re"],
            bins=30,
            density=True,
            alpha=0.5,
            label="LAE",
            color="purple"
        )

        ax.hist(
            sf_df["Re"],
            bins=30,
            density=True,
            alpha=0.5,
            label="SF",
            color="blue"
        )

        ax.hist(
            q_df["Re"],
            bins=30,
            density=True,
            alpha=0.5,
            label="Q",
            color="red"
        )

        ax.set_xlabel("Re (kpc)")
        ax.set_ylabel("Density")
        ax.legend()

        st.pyplot(fig)

    elif compare_param == "C":

        fig, ax = plt.subplots()

        ax.hist(
            lae_df["C_1sig/C_n2p5"],
            bins=30,
            density=True,
            alpha=0.5,
            label="LAE",
            color="purple"
        )

        ax.hist(
            sf_df["C_1sig/C_n2p5"],
            bins=30,
            density=True,
            alpha=0.5,
            label="SF",
            color="blue"
        )

        ax.hist(
            q_df["C_1sig/C_n2p5"],
            bins=30,
            density=True,
            alpha=0.5,
            label="Q",
            color="red"
        )

        ax.set_xlim(0, 3)

        ax.set_xlabel("Concentration")
        ax.set_ylabel("Density")
        ax.legend()

        st.pyplot(fig)

    elif compare_param == "A":

        fig, ax = plt.subplots()

        lae_a = (
            lae_df["A_1sig"]
            .replace([np.inf, -np.inf], np.nan)
            .dropna()
        )

        sf_a = (
            sf_df["A_1sig"]
            .replace([np.inf, -np.inf], np.nan)
            .dropna()
        )

        q_a = (
            q_df["A_1sig"]
            .replace([np.inf, -np.inf], np.nan)
            .dropna()
        )

        ax.hist(
            lae_a,
            bins=30,
            density=True,
            alpha=0.5,
            label="LAE",
            color="purple"
        )

        ax.hist(
            sf_a,
            bins=30,
            density=True,
            alpha=0.5,
            label="SF",
            color="blue"
        )

        ax.hist(
            q_a,
            bins=30,
            density=True,
            alpha=0.5,
            label="Q",
            color="red"
        )

        ax.set_xlabel("Asymmetry")
        ax.set_ylabel("Density")
        ax.legend()

        st.pyplot(fig)


with st.expander("📋 Database Statistics"):

    stats_df = get_sample_statistics()

    st.dataframe(
        stats_df
    )

#ジャンプ検索
jump_id = st.number_input(
    "ジャンプ先ID",
    min_value=0,
    value=0,
    step=1
)

if st.button("IDへジャンプ"):

    target = all_df[
        all_df["ID"] == jump_id
    ]


    if len(target) > 0:

        row_index = all_df.index.get_loc(
            target.index[0]
        )

        st.session_state.current_index = row_index

        st.rerun()

    else:

        st.warning(
            "そのIDは現在の一覧に存在しません"
        )




if "selected_saved_id" in st.session_state:

    target = all_df[
        all_df["ID"]
        == st.session_state.selected_saved_id
    ]

    if len(target) == 0:

        st.error("そのIDは存在しません")

        st.stop()

    galaxy = target.iloc[0]

else:

    if len(matched_df) == 0:

        st.success(
            "🎉 全ての天体の判定が完了しました！"
        )

        st.balloons()

        st.stop()

    if (
        st.session_state.current_index
        >= len(matched_df)
    ):
        st.session_state.current_index = (
            len(matched_df) - 1
        )

    galaxy = matched_df.iloc[
        st.session_state.current_index
    ]

saved_mode = (
    "selected_saved_id"
    in st.session_state
)

if saved_mode:

    position_text = (
        "判定済み天体表示モード"
    )

else:

    position_text = (
        f"現在: "
        f"{st.session_state.current_index + 1}"
        f"/{len(matched_df)}"
    )

if "EW" in galaxy.index:
    sn = (
        galaxy["totalflux_lsig"]
        / galaxy["err_totalflux_lsig"]
    )

    st.info(
    f"""
{position_text}

ID : {int(galaxy["ID"])}

EW : {galaxy["EW"]:.2f}

log(M*) : {np.log10(galaxy["Ms_med"]):.2f}

S/N : {sn:.2f}

Re : {galaxy["Re"]:.3f} ± {galaxy["Re_err"]:.3f}

C : {galaxy["C_1sig/C_n2p5"]:.3f} ± {galaxy["C_err"]:.3f}

A : {galaxy["A_1sig"]:.3f} ± {galaxy["A_err"]:.3f}

r20 : {galaxy["r20_lsig"]:.3f} ± {galaxy["err_r20_lsig"]:.3f}

r50 : {galaxy["r50_lsig"]:.3f} ± {galaxy["err_r50_lsig"]:.3f}

r80 : {galaxy["r80_lsig"]:.3f} ± {galaxy["err_r80_lsig"]:.3f}
"""
)

else:
    sn = (
        galaxy["totalflux_lsig"]
        / galaxy["err_totalflux_lsig"]
    )

    st.info(
        f"""

{position_text}

ID : {int(galaxy["ID"])}

log(M*) : {np.log10(galaxy["Ms_med"]):.2f}

S/N : {sn:.2f}

Re : {galaxy["Re"]:.3f} ± {galaxy["Re_err"]:.3f}

C : {galaxy["C_1sig/C_n2p5"]:.3f} ± {galaxy["C_err"]:.3f}

A : {galaxy["A_1sig"]:.3f} ± {galaxy["A_err"]:.3f}

r20 : {galaxy["r20_lsig"]:.3f} ± {galaxy["err_r20_lsig"]:.3f}

r50 : {galaxy["r50_lsig"]:.3f} ± {galaxy["err_r50_lsig"]:.3f}

r80 : {galaxy["r80_lsig"]:.3f} ± {galaxy["err_r80_lsig"]:.3f}
"""
)



galaxy_id = int(galaxy["ID"])

pred = prediction_df[
    prediction_df["id"] == galaxy_id
]

ai_pred = None

if len(pred) > 0:

    ai_pred = pred.iloc[0]

    scores = [
        ai_pred["detectable"],
        ai_pred["bright_neighbor"],
        ai_pred["multiple_component"],
        ai_pred["point_source"]
    ]

    distance = min(
        abs(s - 0.5)
        for s in scores
    )

    if distance < 0.10:

        st.warning(
            "⚠ AIが迷っている天体です（Uncertain Candidate）"
        )

pixel_galaxy = pixel_df[
    pixel_df["ID"] == galaxy_id
].iloc[0]

# ----------------
# Point Source補助
# ----------------

r50_pix = float(
    pixel_galaxy["r50_lsig"]
)

r80_pix = float(
    pixel_galaxy["r80_lsig"]
)

r50_arcsec = r50_pix * 0.03
r80_arcsec = r80_pix * 0.03

ratio = r80_pix / r50_pix

st.sidebar.markdown("---")

st.sidebar.subheader(
    "Point Source補助"
)

st.sidebar.write(
    f"r50 = {r50_pix:.2f} pix"
)

st.sidebar.write(
    f"r50 = {r50_arcsec:.3f} arcsec"
)

st.sidebar.write(
    f"r80 = {r80_pix:.2f} pix"
)

st.sidebar.write(
    f"r80 = {r80_arcsec:.3f} arcsec"
)

st.sidebar.write(
    f"r80/r50 = {ratio:.2f}"
)

history_df = get_history(galaxy_id)

previous = None

if len(history_df) > 0:
    previous = history_df.iloc[0]



f277w_file = None
obj_file = None
asy_file = None

for file in glob.glob(
    f277w_folder + r"\**\*.fits",
    recursive=True
):

    if f"id{galaxy_id}.fits" in file:

        f277w_file = file

        break

for file in glob.glob(
    obj_folder + r"\**\*.fits",
    recursive=True
):

    if f"id{galaxy_id}.fits" in file:

        obj_file = file

        break

for file in glob.glob(
    asy_folder + r"\**\*.fits",
    recursive=True
):

    if f"id{galaxy_id}.fits" in file:

        asy_file = file

        break

if (
    f277w_file
    and obj_file
    and asy_file
):

    st.success(
        "F277W / OBJ / ASY 発見"
    )

else:

    st.error(
        "画像が見つかりません"
    )


# FITS画像表示

if (
    f277w_file
    and obj_file
    and asy_file
):

    zoom_size = st.slider(
        "ズームサイズ",
        min_value=30,
        max_value=200,
        value=100
    )

    brightness_factor = st.slider(
        "明るさ倍率",
        min_value=0.1,
        max_value=5.0,
        value=1.0,
        step=0.1
    )

    col_img1, col_img2, col_img3 = st.columns(3)

    # ------------------
    # F277W
    # ------------------
    with col_img1:

        image_data = fits.getdata(f277w_file)

        center_y = image_data.shape[0] // 2
        center_x = image_data.shape[1] // 2

        half = zoom_size // 2

        crop = image_data[
            center_y-half:center_y+half,
            center_x-half:center_x+half
        ]

        default_vmax = np.percentile(
            crop,
            99
        )

        vmax = (
            default_vmax
            * brightness_factor
        )

        fig, ax = plt.subplots()

        ax.imshow(
            crop,
            origin="lower",
            cmap="gray",
            vmax=vmax
        )

        # 中心十字
        ax.axhline(
            crop.shape[0] / 2,
            color="yellow",
            lw=1
        )

        ax.axvline(
            crop.shape[1] / 2,
            color="yellow",
            lw=1
        )

        #R50_円形
        r50_pix = float(
            pixel_galaxy["r50_lsig"]
        )


        circle50 = Circle(
            (
                crop.shape[1] / 2,
                crop.shape[0] / 2
            ),
            r50_pix,
            color="red",
            fill=False,
            lw=2
        )

        ax.add_patch(circle50)

        #R80_円形
        r80_pix = float(
        pixel_galaxy["r80_lsig"]
        )

        circle80 = Circle(
            (
                crop.shape[1] / 2,
                crop.shape[0] / 2
            ),
            r80_pix,
            color="cyan",
            fill=False,
            lw=2
        )

        ax.add_patch(circle80)


        ax.set_title("F277W")

        st.pyplot(fig)

    # ------------------
    # OBJ
    # ------------------
    with col_img2:

        image_data = fits.getdata(obj_file)

        center_y = image_data.shape[0] // 2
        center_x = image_data.shape[1] // 2

        half = zoom_size // 2

        crop = image_data[
            center_y-half:center_y+half,
            center_x-half:center_x+half
        ]

        default_vmax = np.percentile(
            crop,
            99
        )

        vmax = (
            default_vmax
            * brightness_factor
        )

        fig, ax = plt.subplots()

        ax.imshow(
            crop,
            origin="lower",
            cmap="gray",
            vmax=vmax
        )

        # 中心十字
        ax.axhline(
            crop.shape[0] / 2,
            color="yellow",
            lw=1
        )

        ax.axvline(
            crop.shape[1] / 2,
            color="yellow",
            lw=1
        )

        #R50_円形
        r50_pix = float(
            pixel_galaxy["r50_lsig"]
        )

        circle50 = Circle(
            (
                crop.shape[1] / 2,
                crop.shape[0] / 2
            ),
            r50_pix,
            color="red",
            fill=False,
            lw=2
        )

        ax.add_patch(circle50)

        #R80_円形
        r80_pix = float(
        pixel_galaxy["r80_lsig"]
        )

        circle80 = Circle(
            (
                crop.shape[1] / 2,
                crop.shape[0] / 2
            ),
            r80_pix,
            color="cyan",
            fill=False,
            lw=2
        )

        ax.add_patch(circle80)

        

        ax.set_title("OBJ")

        st.pyplot(fig)

    # ------------------
    # ASY
    # ------------------
    with col_img3:

        image_data = fits.getdata(asy_file)

        center_y = image_data.shape[0] // 2
        center_x = image_data.shape[1] // 2

        half = zoom_size // 2

        crop = image_data[
            center_y-half:center_y+half,
            center_x-half:center_x+half
        ]

        default_vmax = np.percentile(
            crop,
            99
        )

        vmax = (
            default_vmax
            * brightness_factor
        )

        fig, ax = plt.subplots()

        ax.imshow(
            crop,
            origin="lower",
            cmap="gray",
            vmax=vmax
        )

        # 中心十字
        ax.axhline(
            crop.shape[0] / 2,
            color="yellow",
            lw=1
        )

        ax.axvline(
            crop.shape[1] / 2,
            color="yellow",
            lw=1
        )

        #R50_円形
        r50_pix = float(
            pixel_galaxy["r50_lsig"]
        )

        circle50 = Circle(
            (
                crop.shape[1] / 2,
                crop.shape[0] / 2
            ),
            r50_pix,
            color="red",
            fill=False,
            lw=2
        )

        ax.add_patch(circle50)

        #R80_円形
        r80_pix = float(
        pixel_galaxy["r80_lsig"]
        )

        circle80 = Circle(
            (
                crop.shape[1] / 2,
                crop.shape[0] / 2
            ),
            r80_pix,
            color="cyan",
            fill=False,
            lw=2
        )

        ax.add_patch(circle80)

        ax.set_title("ASY")

        st.pyplot(fig)

# --------------------
# Human Label + AI Prediction
# --------------------

st.caption(
    "左: 前回判定　中央: 今回判定　右: AI予測"
)

col_old, col_check, col_prob, col_bar = st.columns(
    [1, 5, 1, 3]
)

with col_old:

    if previous is not None:

        st.write(
            "✅"
            if previous["detectable"]
            else "⬜"
        )

    else:

        st.write("－")

with col_check:

    detectable = st.checkbox(
        "Detectable（有意に検出されている）",
        value=(
            bool(previous["detectable"])
            if previous is not None
            else False
        ),
        key=f"detectable_{galaxy_id}"
    )

with col_prob:

    if ai_pred is not None:
        st.write(
            f"{ai_pred['detectable']:.1%}"
        )

with col_bar:

    if ai_pred is not None:
        st.progress(
            float(ai_pred["detectable"])
        )


col_old, col_check, col_prob, col_bar = st.columns(
    [1, 5, 1, 3]
)

with col_old:

    if previous is not None:

        st.write(
            "✅"
            if previous["bright_neighbor"]
            else "⬜"
        )

    else:

        st.write("－")

with col_check:

    bright_neighbor = st.checkbox(
        "Bright Neighbor（近傍の明るい天体の影響あり）",
        value=(
            bool(previous["bright_neighbor"])
            if previous is not None
            else False
        ),
        key=f"bright_{galaxy_id}"
    )

with col_prob:

    if ai_pred is not None:
        st.write(
            f"{ai_pred['bright_neighbor']:.1%}"
        )

with col_bar:

    if ai_pred is not None:
        st.progress(
            float(ai_pred["bright_neighbor"])
        )


col_old, col_check, col_prob, col_bar = st.columns(
    [1, 5, 1, 3]
)

with col_old:

    if previous is not None:

        st.write(
            "✅"
            if previous["multiple_component"]
            else "⬜"
        )

    else:

        st.write("－")

with col_check:

    multiple_component = st.checkbox(
        "Multiple Component（複数成分）",
        value=(
            bool(previous["multiple_component"])
            if previous is not None
            else False
        ),
        key=f"multiple_{galaxy_id}"
    )

with col_prob:

    if ai_pred is not None:
        st.write(
            f"{ai_pred['multiple_component']:.1%}"
        )

with col_bar:

    if ai_pred is not None:
        st.progress(
            float(ai_pred["multiple_component"])
        )


col_old, col_check, col_prob, col_bar = st.columns(
    [1, 5, 1, 3]
)

with col_old:

    if previous is not None:

        st.write(
            "✅"
            if previous["point_source"]
            else "⬜"
        )

    else:

        st.write("－")

with col_check:

    point_source = st.checkbox(
        "Point Source（点源）",
        value=(
            bool(previous["point_source"])
            if previous is not None
            else False
        ),
        key=f"point_{galaxy_id}"
    )


with col_prob:

    if ai_pred is not None:
        st.write(
            f"{ai_pred['point_source']:.1%}"
        )

with col_bar:

    if ai_pred is not None:
        st.progress(
            float(ai_pred["point_source"])
        )


changed = True

if previous is not None:

    changed = (

        int(previous["detectable"]) != int(detectable)

        or

        int(previous["bright_neighbor"]) != int(bright_neighbor)

        or

        int(previous["multiple_component"]) != int(multiple_component)

        or

        int(previous["point_source"]) != int(point_source)

    )

    if changed:

        st.warning(
            "⚠ 前回判定から変更あり"
        )

    else:

        st.success(
            "✅ 前回判定と一致"
        )

st.info(
    "AI予測確率（0〜100%）。バー長はモデルの予測確率を表し、判定の参考情報として利用してください。"
)

memo = st.text_area(
    "Memo"
)

if "last_saved_id" in st.session_state:

    st.success(
        f"ID {st.session_state.last_saved_id} を保存しました"
    )


col1, col2 = st.columns(2)


button_label = (
    "更新保存"
    if saved_mode
    else "保存して次へ"
)

if st.button(button_label):

    changed = True

    if previous is not None:

        changed = (

            int(previous["detectable"]) != int(detectable)

            or

            int(previous["bright_neighbor"]) != int(bright_neighbor)

            or

            int(previous["multiple_component"]) != int(multiple_component)

            or

            int(previous["point_source"]) != int(point_source)

        )

    save_data = (
        galaxy_id,
        "all",
        sample_select,

        float(np.log10(galaxy["Ms_med"])),

        float(galaxy["Re"]),
        float(galaxy["Re_err"]),

        float(galaxy["C_1sig/C_n2p5"]),
        float(galaxy["C_err"]),

        float(galaxy["A_1sig"]),
        float(galaxy["A_err"]),

        int(detectable),
        int(bright_neighbor),
        int(multiple_component),
        int(point_source),

        memo
    )

    if changed:

        save_classification(save_data)

        st.session_state.last_saved_id = galaxy_id

        st.session_state.saved = True

    else:

        st.info(
            "✅ 前回判定と同一のため保存をスキップしました"
        )

    if saved_mode:

        if changed:

            st.success(
                f"ID {galaxy_id} を更新しました"
            )

    else:

        if (
            st.session_state.current_index
            < len(matched_df) - 1
        ):

            st.session_state.current_index += 1

            st.rerun()

        else:

            st.success(
                "🎉 全ての天体の判定が完了しました！"
            )

            st.balloons()

            st.stop()