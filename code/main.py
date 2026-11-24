
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 한글 폰트 자동 설정
import koreanize_matplotlib

# 그래프 기본 설정
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.figsize"] = (10, 5)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -------------------------
# 페이지 설정
# -------------------------
st.set_page_config(
    page_title="손 씻기와 감염병 예방 분석",
    page_icon="🧼",
    layout="wide"
)

st.title("🧼 손 씻기 실천율과 감염병 발생의 데이터 분석")
st.subheader("손 씻기는 정말 질병 예방에 효과적일까?")

st.write("""
CDC의 손 씻기 교육 효과 자료와
병원 내 손 위생 실천율 및 의료 관련 감염 발생률 연구를
바탕으로 데이터를 분석합니다.
""")

st.divider()

# 한글 폰트 설정
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# -------------------------
# 1. CDC 실제 데이터
# -------------------------

st.header("1. CDC 손 씻기 교육에 따른 질병 감소율")

cdc = pd.DataFrame({
    "질병 종류": [
        "일반 인구의 설사 질환",
        "면역 저하자의 설사 질환",
        "일반 인구의 호흡기 질환",
        "학생의 위장관 질환 결석"
    ],
    "최소 감소율": [23, 58, 16, 29],
    "최대 감소율": [40, 58, 21, 57]
})

cdc["평균 감소율"] = (
    cdc["최소 감소율"] + cdc["최대 감소율"]
) / 2

fig, ax = plt.subplots(figsize=(10, 5))

y = np.arange(len(cdc))

ax.barh(
    y,
    cdc["평균 감소율"],
    color="skyblue",
    edgecolor="black"
)

# 감소율 범위 표시
for i, row in cdc.iterrows():
    ax.plot(
        [row["최소 감소율"], row["최대 감소율"]],
        [i, i],
        color="red",
        linewidth=3
    )
    ax.text(
        row["최대 감소율"] + 1,
        i,
        f'{row["최소 감소율"]}~{row["최대 감소율"]}%',
        va="center"
    )

ax.set_yticks(y)
ax.set_yticklabels(cdc["질병 종류"])
ax.set_xlabel("질병 감소율 (%)")
ax.set_title("손 씻기 교육에 따른 질병 감소 효과")
ax.set_xlim(0, 70)

st.pyplot(fig)

st.dataframe(cdc, use_container_width=True)

st.caption("출처: CDC Handwashing Facts (2024.04.17)")

st.divider()

# -------------------------
# 2. PMC 실제 데이터
# -------------------------

st.header("2. 병원 내 손 위생 실천율과 감염 발생률")

hospital = pd.DataFrame({
    "연도": ["2017", "2018", "2019", "2020"],
    "손 위생 실천율": [68.90, 81.70, 86.47, 91.76],
    "감염 발생률": [1.10, 0.92, 0.92, 0.91]
})

st.write("중국 허난대학교 제1부속병원의 4년간 연구 자료")

st.dataframe(hospital, use_container_width=True)

# -------------------------
# 3. 손 위생 실천율 변화
# -------------------------

st.subheader("① 손 위생 실천율 변화")

fig, ax = plt.subplots(figsize=(9, 5))

ax.plot(
    hospital["연도"],
    hospital["손 위생 실천율"],
    marker="o",
    markersize=9,
    linewidth=3,
    color="blue"
)

for x, y in zip(
    hospital["연도"],
    hospital["손 위생 실천율"]
):
    ax.text(x, y + 1, f"{y}%", ha="center")

ax.set_title("2017~2020년 손 위생 실천율 변화")
ax.set_xlabel("연도")
ax.set_ylabel("손 위생 실천율 (%)")
ax.set_ylim(0, 105)

st.pyplot(fig)

# -------------------------
# 4. 감염 발생률 변화
# -------------------------

st.subheader("② 의료 관련 감염 발생률 변화")

fig, ax = plt.subplots(figsize=(9, 5))

ax.plot(
    hospital["연도"],
    hospital["감염 발생률"],
    marker="s",
    markersize=9,
    linewidth=3,
    color="red"
)

for x, y in zip(
    hospital["연도"],
    hospital["감염 발생률"]
):
    ax.text(x, y + 0.015, f"{y}%", ha="center")

ax.set_title("2017~2020년 의료 관련 감염 발생률 변화")
ax.set_xlabel("연도")
ax.set_ylabel("감염 발생률 (%)")

st.pyplot(fig)

# -------------------------
# 5. 두 변수 비교
# -------------------------

st.subheader("③ 손 위생 실천율과 감염 발생률 비교")

fig, ax1 = plt.subplots(figsize=(10, 5))

ax1.plot(
    hospital["연도"],
    hospital["손 위생 실천율"],
    marker="o",
    color="blue",
    linewidth=3,
    label="손 위생 실천율"
)

ax1.set_ylabel("손 위생 실천율 (%)", color="blue")

ax2 = ax1.twinx()

ax2.plot(
    hospital["연도"],
    hospital["감염 발생률"],
    marker="s",
    color="red",
    linewidth=3,
    label="감염 발생률"
)

ax2.set_ylabel("감염 발생률 (%)", color="red")

ax1.set_title("손 위생 실천율과 감염 발생률의 변화 비교")
ax1.set_xlabel("연도")

st.pyplot(fig)

# -------------------------
# 6. 평균 분석
# -------------------------

st.subheader("④ 평균값을 기준으로 한 분석")

mean_hand = hospital["손 위생 실천율"].mean()
mean_infection = hospital["감염 발생률"].mean()

col1, col2 = st.columns(2)

col1.metric(
    "평균 손 위생 실천율",
    f"{mean_hand:.2f}%"
)

col2.metric(
    "평균 감염 발생률",
    f"{mean_infection:.3f}%"
)

# -------------------------
# 7. 논문에 보고된 상관계수
# -------------------------

st.subheader("⑤ 상관관계 분석")

st.metric(
    "논문에 보고된 월별 Spearman 상관계수",
    "-0.27"
)

st.metric(
    "통계적 유의확률 (p-value)",
    "0.037"
)

st.info("""
상관계수 -0.27은 약한 음의 상관관계를 의미합니다.

즉, 손 위생 실천율이 높아질수록
의료 관련 감염 발생률이 낮아지는 경향이 관찰되었습니다.

p-value가 0.05보다 작으므로 통계적으로 유의한
음의 상관관계가 확인되었습니다.
""")

# -------------------------
# 8. 전체 결과 요약
# -------------------------

st.divider()

st.header("3. 최종 분석 결과")

st.markdown("""
### 분석 결과

1. 손 위생 실천율은 2017년 68.90%에서
   2020년 91.76%로 증가하였다.

2. 의료 관련 감염 발생률은 2017년 1.10%에서
   2020년 0.91%로 감소하였다.

3. 월별 손 위생 실천율과 감염 발생률 사이에는
   -0.27의 약한 음의 상관관계가 나타났다.

4. CDC 자료에서도 손 씻기 교육을 통해
   여러 질병의 발생과 결석을 줄일 수 있다는
   결과를 확인할 수 있었다.

### 최종 결론

손 씻기는 단순한 위생 습관이 아니라
질병 예방에 중요한 역할을 하는 행동이다.

특히 병원에서는 의료진의 손 위생 실천이
환자와 의료진 모두의 감염 예방에 중요하다.

다만 상관관계만으로 손 씻기가 감염 감소의
직접적인 원인이라고 단정할 수는 없다.
""")

st.caption("""
자료 출처:
CDC - Handwashing Facts
https://www.cdc.gov/clean-hands/data-research/facts-stats/index.html

PMC - Effects of a 4-year intervention on hand hygiene compliance
https://pmc.ncbi.nlm.nih.gov/articles/PMC8120257/
""")
