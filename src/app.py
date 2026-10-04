import streamlit as st
import pandas as pd
import glob
import re
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from database import (
    get_history,
    save_classification,
    get_saved_ids,
    get_classified_ids,
    get_lae_by_ew,
    get_sample_statistics,
    get_sampled_galaxies
)

# タイトル
st.title("LAE Morphology Inspector")

# -----------------------------
# Session State 初期化
# -----------------------------

if "current_index" not in st.session_state:
    st.session_state.current_index = 0

if "saved" not in st.session_state:
    st.session_state.saved = False


# 現在モード表示
if "selected_saved_id" in st.session_state:

    st.warning(
        "🟨 判定済み天体表示モード"
    )

else:

    st.info(
        "🟦 未判定天体表示モード"
    )

#----------------
# サイドバー
#----------------
st.sidebar.subheader(
    "判定済み天体"
)

classified_ids = get_classified_ids()

selected_id = st.sidebar.selectbox(
    "保存済みID",
    classified_ids
)

# 判定済み天体表示
if st.sidebar.button("保存済み天体を表示"):

    st.session_state.selected_saved_id = (
        selected_id
    )

    st.session_state.show_saved_effect = True

    st.rerun()

# 未判定モードへ戻る
if st.sidebar.button("未判定モードへ戻る"):

    if "selected_saved_id" in st.session_state:

        del st.session_state.selected_saved_id

    st.session_state.show_unclassified_effect = True

    st.rerun()

# 判定済みモードへ切り替えエフェクト
if st.session_state.get(
    "show_saved_effect",
    False
):

    st.warning(
        "🟨 判定済み天体表示モードへ切り替えました"
    )

    st.balloons()

    st.session_state.show_saved_effect = False

# 未判定モードへ戻ったエフェクト
if st.session_state.get(
    "show_unclassified_effect",
    False
):

    st.success(
        "✅ 未判定モードへ戻りました"
    )

    st.balloons()

    st.session_state.show_unclassified_effect = False





# -----------------------------
# SQLサンプリング抽出
# -----------------------------

st.subheader("SQLサンプリング抽出")

#画像選択

image_family = st.selectbox(
    "画像グループ",
    [
        "images",
        "images_asy",
        "images_obj"
    ]
)

sample_select = st.selectbox(
    "サンプル",
    ["LAE", "SF", "Q"]
)

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

st.write(
    "sampled_df件数:",
    len(sampled_df)
)

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

st.write(catalog_file)

df = pd.read_csv(
    catalog_file,
    sep=r"\s+",
    encoding="cp932"
)

# フォルダ選択
if image_family == "images":

    folder_path = (
        rf"\\wsl.localhost\Ubuntu\home\tan\images_all"
        rf"\images_all_{sample_select}"
    )

elif image_family == "images_asy":

    folder_path = (
        rf"\\wsl.localhost\Ubuntu\home\tan\images_all"
        rf"\images_asy_all_{sample_select}"
    )

elif image_family == "images_obj":

    folder_path = (
        rf"\\wsl.localhost\Ubuntu\home\tan\images_all"
        rf"\images_obj_all_{sample_select}"
    )

st.write(folder_path)

fits_files = glob.glob(
    folder_path + r"\**\*.fits",
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
        image_family,
        sample_select
    )

    matched_df = matched_df[
        ~matched_df["ID"].isin(saved_ids)
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

#-----------------------
#EW,A,C,Re,M*ヒストグラム
#-----------------------

#EWヒストグラム(LAEのみ作用/SFとQでは作用せず)
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


#Reヒストグラム
st.subheader("Re分布")

fig, ax = plt.subplots()

ax.hist(
    matched_df["Re"],
    bins=20
)

ax.set_title(
    "Re Distribution"
)

ax.set_xlabel("Re (kpc)")
ax.set_ylabel("Number")

st.pyplot(fig)

#Cヒストグラム
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

#Aヒストグラム
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

ax.set_title(
    "A Distribution"
)

ax.set_xlabel("Asymmetry")
ax.set_ylabel("Number")

st.pyplot(fig)



#log(M*)ヒストグラム

st.subheader("log(M*)分布")

fig, ax = plt.subplots()

ax.hist(
    np.log10(matched_df["Ms_med"]),
    bins=20
)

ax.set_title("Mass Distribution")

ax.set_xlabel("log(M*)")
ax.set_ylabel("Number")

st.pyplot(fig)


#比較パラメータ
st.subheader("LAE / SF / Q 比較")

compare_param = st.selectbox(
    "比較パラメータ",
    ["Re", "C", "A"]
)

lae_df = pd.read_csv(
    "data/catalog_LAE_F277W_with_err_kpc.txt",
    sep=r"\s+",
    encoding="cp932"
)

sf_df = pd.read_csv(
    "data/catalog_nonLAE_SF_F277W_with_err_kpc.txt",
    sep=r"\s+",
    encoding="cp932"
)

q_df = pd.read_csv(
    "data/catalog_nonLAE_Q_F277W_with_err_kpc.txt",
    sep=r"\s+",
    encoding="cp932"
)

#Re比較
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

#C比較
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

#A比較
elif compare_param == "A":

    fig, ax = plt.subplots()

    lae_a = lae_df["A_1sig"].replace(
        [np.inf, -np.inf],
        np.nan
    ).dropna()

    sf_a = sf_df["A_1sig"].replace(
        [np.inf, -np.inf],
        np.nan
    ).dropna()

    q_a = q_df["A_1sig"].replace(
        [np.inf, -np.inf],
        np.nan
    ).dropna()

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

#Re,A,Cの代表値
stats_df = get_sample_statistics()

st.subheader("Database Statistics")

st.dataframe(stats_df)


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

    


if sample_select == "LAE":

    st.dataframe(
    matched_df[
        [
            "ID",
            "EW",
            "logM",
            "Re",
            "Re_err",
            "C_1sig/C_n2p5",
            "C_err",
            "A_1sig",
            "A_err"
        ]
    ].head()
    )

else:

    st.dataframe(
    matched_df[
        [
            "ID",
            "logM",
            "Re",
            "Re_err",
            "C_1sig/C_n2p5",
            "C_err",
            "A_1sig",
            "A_err"
        ]
    ].head()
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

history_df = get_history(galaxy_id)

st.subheader("このIDの判定履歴")
st.dataframe(history_df)

target_file = None

for file in fits_files:

    if f"id{galaxy_id}.fits" in file:
        target_file = file
        break

if target_file:
    st.success("対応画像発見")
    st.write(target_file)

else:
    st.error("画像が見つかりません")

# FITS画像表示

if target_file:

    image_data = fits.getdata(target_file)

    # 画像中心取得
    center_y = image_data.shape[0] // 2
    center_x = image_data.shape[1] // 2

    zoom_size = st.slider(
    "ズームサイズ",
    min_value=30,
    max_value=200,
    value=100
    )

    half = zoom_size // 2

    crop = image_data[
        center_y - half:center_y + half,
        center_x - half:center_x + half
    ]

    default_vmax = np.percentile(
        crop,
        99
    )


    #明るさスライダー（画像ごとに自動設定）
    vmax = st.slider(
        "明るさ",
        min_value=float(default_vmax * 0.1),
        max_value=float(default_vmax * 5),
        value=float(default_vmax)
    )

    fig, ax = plt.subplots()

    ax.imshow(
        crop,
        origin="lower",
        cmap="gray",
        vmax=vmax
    )

    ax.set_title(f"ID {galaxy_id}")

    st.pyplot(fig)
    detectable = st.checkbox(
    "Detectable（有意に検出されている）"
    )

    
    
    bright_neighbor = st.checkbox(
    "Bright Neighbor（近傍の明るい天体の影響あり）"
    )

    

    multiple_component = st.checkbox(
    "Multiple Component（複数成分）"
    )

    

    point_source = st.checkbox(
    "Point Source（点源）"
    )

    

    memo = st.text_area(
    "Memo"
    )



    if "last_saved_id" in st.session_state:

        st.success(
        f"ID {st.session_state.last_saved_id} を保存しました"
        )


col1, col2 = st.columns(2)


with col1:

    if st.button("保存"):

        save_data = (
            galaxy_id,
            image_family,
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

        save_classification(save_data)

        result = pd.DataFrame([{
            "ID": galaxy_id,

            "image_family": image_family,
            "sample_select": sample_select,

            "logM": np.log10(galaxy["Ms_med"]),

            "Re": galaxy["Re"],
            "Re_err": galaxy["Re_err"],

            "C_1sig/C_n2p5":
                galaxy["C_1sig/C_n2p5"],

            "C_err": galaxy["C_err"],

            "A_1sig": galaxy["A_1sig"],

            "A_err": galaxy["A_err"],

            "detectable": detectable,
            "bright_neighbor": bright_neighbor,
            "multiple_component": multiple_component,
            "point_source": point_source,

            "memo": memo
        }])

        


        st.session_state.last_saved_id = galaxy_id
        st.session_state.saved = True
        st.success(f"ID {galaxy_id} を保存しました")

       

if not saved_mode:

    with col2:

        if st.button("次へ"):

            st.session_state.saved = False

            if "last_saved_id" in st.session_state:
                del st.session_state["last_saved_id"]

            if (
                st.session_state.current_index
                < len(matched_df) - 1
            ):

                st.session_state.current_index += 1

                st.rerun()

