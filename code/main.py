
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import urllib.request
import os

# =====================================
# 1. 페이지 설정
# =====================================

st.set_page_config(
    page_title="손 씻기와 감염병 예방 데이터 분석",
    page_icon="🧼",
    layout="wide"
)

# =====================================
# 2. 한글 폰트 설정
# =====================================

FONT_PATH = "/tmp/NanumGothic.ttf"

@st.cache_resource
def setup_korean_font():

    if not os.path.exists(FONT_PATH):
        font_url = (
            "https://github.com/google/fonts/raw/main/"
            "ofl/nanumgothic/NanumGothic-Regular.ttf"
        )

        urllib.request.urlretrieve(font_url, FONT_PATH)

    fm.fontManager.addfont(FONT_PATH)

    font_name = fm.FontProperties(
        fname=FONT_PATH
    ).get_name()

    plt.rcParams["font.family"] = font_name
    plt.rcParams["axes.unicode_minus"] = False

    return font_name


try:
    setup_korean_font()
except Exception as e:
    st.error("한글 폰트를 불러오지 못했습니다.")
    st.error(str(e))
    st.stop()


# =====================================
# 3. 제목
# =====================================

st.title("🧼 손 씻기 실천율과 감염병 발생의 데이터 분석")

st.subheader("손 씻기는 정말 질병 예방에 효과적일까?")

st.markdown("""
CDC의 손 씻기 교육 효과 자료와
병원 내 손 위생 실천율 및 의료 관련 감염 발생률 연구를
활용하여 손 씻기의 질병 예방 효과를 분석합니다.
""")

st.divider()


# =====================================
# 4. CDC 데이터
# =====================================

st.header("1. CDC 손 씻기 교육에 따른 질병 감소율")

st.write("""
미국 질병통제예방센터(CDC)에서 제시한
손 씻기 교육에 따른 질병 감소 효과입니다.
""")

cdc = pd.DataFrame({
    "질병 종류": [
        "일반 인구의 설사 질환",
        "면역 저하자의 설사 질환",
        "일반 인구의 호흡기 질환",
        "학생의 위장관 질환 결석"
    ],
    "최소 감소율(%)": [23, 58, 16, 29],
    "최대 감소율(%)": [40, 58, 21, 57]
})

cdc["평균 감소율(%)"] = (
    cdc["최소 감소율(%)"] +
    cdc["최대 감소율(%)"]
) / 2

st.dataframe(
    cdc,
    use_container_width=True,
    hide_index=True
)

fig, ax = plt.subplots(figsize=(10, 5))

y = np.arange(len(cdc))

ax.barh(
    y,
    cdc["평균 감소율(%)"],
    color="#70B7E6",
    edgecolor="black",
    height=0.55
)

for i, row in cdc.iterrows():

    ax.plot(
        [
            row["최소 감소율(%)"],
            row["최대 감소율(%)"]
        ],
        [i, i],
        color="red",
        linewidth=3
    )

    ax.text(
        row["최대 감소율(%)"] + 1,
        i,
        f'{row["최소 감소율(%)"]}~{row["최대 감소율(%)"]}%',
        va="center",
        fontsize=10
    )

ax.set_yticks(y)
ax.set_yticklabels(cdc["질병 종류"])
ax.set_xlabel("질병 감소율 (%)")
ax.set_title("손 씻기 교육에 따른 질병 감소 효과")
ax.set_xlim(0, 75)
ax.grid(axis="x", alpha=0.3)

st.pyplot(fig)
plt.close(fig)

st.caption(
    "출처: CDC - Handwashing Facts (2024.04.17)"
)

st.divider()


# =====================================
# 5. PMC 병원 연구 데이터
# =====================================

st.header("2. 병원 내 손 위생 실천율과 감염 발생률")

st.write("""
병원에서 조사한 2017~2020년 손 위생 실천율과
의료 관련 감염 발생률 자료입니다.
""")

hospital = pd.DataFrame({
    "연도": ["2017", "2018", "2019", "2020"],
    "손 위생 실천율(%)": [
        68.90, 81.70, 86.47, 91.76
    ],
    "감염 발생률(%)": [
        1.10, 0.92, 0.92, 0.91
    ]
})

st.dataframe(
    hospital,
    use_container_width=True,
    hide_index=True
)

st.caption(
    "출처: PMC - 병원 내 손 위생 중재 연구"
)

st.divider()


# =====================================
# 6. 손 위생 실천율 변화 그래프
# =====================================

st.header("3. 기간별 손 위생 실천율 변화")

fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(
    hospital["연도"],
    hospital["손 위생 실천율(%)"],
    marker="o",
    markersize=9,
    linewidth=3,
    color="#2878B5"
)

for x, y in zip(
    hospital["연도"],
    hospital["손 위생 실천율(%)"]
):
    ax.annotate(
        f"{y:.2f}%",
        (x, y),
        xytext=(0, 10),
        textcoords="offset points",
        ha="center"
    )

ax.set_title("2017~2020년 손 위생 실천율 변화")
ax.set_xlabel("조사 연도")
ax.set_ylabel("손 위생 실천율 (%)")
ax.set_ylim(0, 105)
ax.grid(alpha=0.3)

st.pyplot(fig)
plt.close(fig)

st.divider()


# =====================================
# 7. 감염 발생률 변화 그래프
# =====================================

st.header("4. 기간별 의료 관련 감염 발생률 변화")

fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(
    hospital["연도"],
    hospital["감염 발생률(%)"],
    marker="s",
    markersize=9,
    linewidth=3,
    color="#E45757"
)

for x, y in zip(
    hospital["연도"],
    hospital["감염 발생률(%)"]
):
    ax.annotate(
        f"{y:.2f}%",
        (x, y),
        xytext=(0, 10),
        textcoords="offset points",
        ha="center"
    )

ax.set_title("2017~2020년 의료 관련 감염 발생률 변화")
ax.set_xlabel("조사 연도")
ax.set_ylabel("감염 발생률 (%)")
ax.grid(alpha=0.3)

st.pyplot(fig)
plt.close(fig)

st.divider()


# =====================================
# 8. 두 변수 변화 비교
# =====================================

st.header("5. 손 위생 실천율과 감염 발생률 비교")

fig, ax1 = plt.subplots(figsize=(10, 5))

ax1.plot(
    hospital["연도"],
    hospital["손 위생 실천율(%)"],
    marker="o",
    linewidth=3,
    color="blue",
    label="손 위생 실천율"
)

ax1.set_xlabel("조사 연도")
ax1.set_ylabel(
    "손 위생 실천율 (%)",
    color="blue"
)

ax1.tick_params(
    axis="y",
    labelcolor="blue"
)

ax2 = ax1.twinx()

ax2.plot(
    hospital["연도"],
    hospital["감염 발생률(%)"],
    marker="s",
    linewidth=3,
    color="red",
    label="감염 발생률"
)

ax2.set_ylabel(
    "감염 발생률 (%)",
    color="red"
)

ax2.tick_params(
    axis="y",
    labelcolor="red"
)

ax1.set_title(
    "손 위생 실천율과 감염 발생률의 변화 비교"
)

ax1.grid(alpha=0.3)

st.pyplot(fig)
plt.close(fig)

st.divider()


# =====================================
# 9. 평균값 분석
# =====================================

st.header("6. 평균값을 기준으로 한 분석")

mean_hand = hospital["손 위생 실천율(%)"].mean()
mean_infection = hospital["감염 발생률(%)"].mean()

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "평균 손 위생 실천율",
        f"{mean_hand:.2f}%"
    )

with col2:
    st.metric(
        "평균 감염 발생률",
        f"{mean_infection:.3f}%"
    )

hospital_compare = hospital.copy()

hospital_compare["손 위생 평균 비교"] = np.where(
    hospital_compare["손 위생 실천율(%)"] >= mean_hand,
    "평균 이상",
    "평균 미만"
)

hospital_compare["감염 평균 비교"] = np.where(
    hospital_compare["감염 발생률(%)"] >= mean_infection,
    "평균 이상",
    "평균 미만"
)

st.dataframe(
    hospital_compare,
    use_container_width=True,
    hide_index=True
)

st.divider()


# =====================================
# 10. 산점도
# =====================================

st.header("7. 손 위생 실천율과 감염 발생률의 관계")

fig, ax = plt.subplots(figsize=(9, 6))

ax.scatter(
    hospital["손 위생 실천율(%)"],
    hospital["감염 발생률(%)"],
    color="#2878B5",
    s=120,
    edgecolors="black"
)

for _, row in hospital.iterrows():
    ax.annotate(
        row["연도"],
        (
            row["손 위생 실천율(%)"],
            row["감염 발생률(%)"]
        ),
        xytext=(7, 7),
        textcoords="offset points"
    )

ax.set_title(
    "손 위생 실천율과 의료 관련 감염 발생률의 관계"
)

ax.set_xlabel("손 위생 실천율 (%)")
ax.set_ylabel("감염 발생률 (%)")
ax.grid(alpha=0.3)

st.pyplot(fig)
plt.close(fig)

st.divider()


# =====================================
# 11. 논문 상관계수
# =====================================

st.header("8. 논문에 보고된 상관관계 분석")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "월별 Spearman 상관계수",
        "-0.27"
    )

with col2:
    st.metric(
        "p-value",
        "0.037"
    )

st.info("""
상관계수 -0.27은 약한 음의 상관관계를 의미합니다.

p-value가 0.05보다 작으므로 통계적으로 유의한
음의 상관관계가 확인되었습니다.

즉, 손 위생 실천율이 높을수록 의료 관련 감염 발생률이
낮아지는 경향이 관찰되었습니다.
""")

st.caption(
    "주의: 논문에 보고된 월별 Spearman 상관계수이며, "
    "위의 연도별 4개 데이터로 계산한 값이 아닙니다."
)

st.divider()


# =====================================
# 12. 최종 분석 결과
# =====================================

st.header("9. 최종 분석 결과 및 결론")

st.subheader("핵심 분석 결과")

st.markdown("""
**① 손 위생 실천율 증가**

2017년 68.90%에서 2020년 91.76%로 증가했습니다.

**② 의료 관련 감염 발생률 감소**

2017년 1.10%에서 2020년 0.91%로 감소했습니다.

**③ 음의 상관관계 확인**

논문에서 보고된 월별 Spearman 상관계수는 -0.27입니다.

**④ CDC 자료에서도 질병 예방 효과 확인**

손 씻기 교육은 설사 질환과 호흡기 질환 등
여러 질병의 감소와 관련이 있습니다.
""")

st.success("""
최종 결론

손 씻기는 단순한 위생 습관이 아니라
감염병 예방에 중요한 역할을 하는 행동입니다.

특히 병원에서는 의료진의 손 위생 실천이
환자와 의료진의 안전을 지키는 데 중요합니다.
""")

st.subheader("분석의 한계")

st.markdown("""
- 상관관계가 반드시 인과관계를 의미하지는 않습니다.
- 병원 환경, 환자의 건강 상태, 소독 수준 등
  다양한 요인이 감염 발생률에 영향을 줄 수 있습니다.
- 특정 병원에서 진행된 연구이므로
  모든 병원에 동일하게 적용하기 어렵습니다.
- CDC와 PMC 자료는 조사 대상과 측정 방법이 다르므로
  두 자료의 수치를 직접 비교할 수 없습니다.
""")

st.divider()

st.caption("""
데이터 출처

1. CDC - Handwashing Facts
https://www.cdc.gov/clean-hands/data-research/facts-stats/index.html

2. PMC - 병원 내 손 위생 연구
https://pmc.ncbi.nlm.nih.gov/articles/PMC8120257/
""")

st.markdown(
    "🧼 **손 씻기는 나 자신뿐 아니라 다른 사람의 건강도 지키는 행동입니다.**"
)
