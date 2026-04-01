# ================================================================
#  한국 주식 XGBoost 백테스트 대시보드  |  app.py
#  실행: streamlit run stock_backtest_app.py
# ================================================================

import streamlit as st
import FinanceDataReader as fdr
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import warnings
warnings.filterwarnings("ignore")

from xgboost import XGBClassifier

# ────────────────────────────────────────────────────────────────
# 0. 페이지 설정
# ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="한국 주식 XGBoost 백테스트",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ────────────────────────────────────────────────────────────────
# 1. 한글 폰트
# ────────────────────────────────────────────────────────────────
@st.cache_resource
def setup_font():
    """시스템에서 한글 폰트를 찾아 matplotlib에 등록"""
    candidates = ["Malgun Gothic", "NanumGothic", "AppleGothic", "NanumBarunGothic"]
    for font_name in candidates:
        for path in fm.findSystemFonts():
            if font_name.replace(" ", "").lower() in path.replace(" ", "").lower():
                fm.fontManager.addfont(path)
                plt.rcParams["font.family"] = font_name
                plt.rcParams["axes.unicode_minus"] = False
                return font_name
    # 못 찾으면 DejaVu 사용 (한글 깨짐 허용)
    return "DejaVu Sans"

FONT = setup_font()

# ────────────────────────────────────────────────────────────────
# 2. 종목 리스트 로드 (KRX 전체 + KOSPI/KOSDAQ)
# ────────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def load_stock_list():
    """KRX 전체 종목 로드. 실패 시 주요 종목 fallback."""
    try:
        kospi  = fdr.StockListing("KOSPI")[["Code", "Name"]].copy()
        kosdaq = fdr.StockListing("KOSDAQ")[["Code", "Name"]].copy()
        df = pd.concat([kospi, kosdaq], ignore_index=True)
        df = df.dropna(subset=["Code", "Name"])
        df["Code"] = df["Code"].astype(str).str.zfill(6)
        df["표시"] = df["Code"] + "  |  " + df["Name"]
        return df.reset_index(drop=True)
    except Exception:
        fallback = pd.DataFrame({
            "Code": ["005930","000660","035420","051910","005380","035720","000270","096770","003670","068270"],
            "Name": ["삼성전자","SK하이닉스","NAVER","LG화학","현대차","카카오","기아","SK이노베이션","포스코홀딩스","셀트리온"],
        })
        fallback["표시"] = fallback["Code"] + "  |  " + fallback["Name"]
        return fallback

stock_df = load_stock_list()
display_list = stock_df["표시"].tolist()

# ────────────────────────────────────────────────────────────────
# 3. 사이드바 — 파라미터 설정
# ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ 분석 설정")

    # 종목 검색
    st.subheader("📌 종목 선택")
    search_query = st.text_input("종목명 또는 코드 검색", placeholder="예: 삼성전자, 005930")

    if search_query:
        mask = (
            stock_df["Name"].str.contains(search_query, case=False, na=False) |
            stock_df["Code"].str.contains(search_query, na=False)
        )
        filtered = stock_df[mask]
    else:
        filtered = stock_df

    if len(filtered) == 0:
        st.warning("검색 결과가 없습니다.")
        filtered = stock_df

    selected_display = st.selectbox(
        "종목",
        filtered["표시"].tolist(),
        index=0,
    )
    selected_code = selected_display.split("  |  ")[0].strip()
    selected_name = selected_display.split("  |  ")[1].strip()

    st.divider()

    # 기간 설정
    st.subheader("📅 기간 설정")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("시작일", value=datetime.date(2020, 1, 1),
                                    min_value=datetime.date(2010, 1, 1),
                                    max_value=datetime.date.today())
    with col2:
        end_date = st.date_input("종료일", value=datetime.date.today(),
                                  min_value=datetime.date(2010, 1, 1),
                                  max_value=datetime.date.today())

    st.divider()

    # 데이터 분할
    st.subheader("📂 데이터 분할")
    valid_start = st.date_input("검증 시작일", value=datetime.date(2023, 1, 1),
                                 min_value=start_date, max_value=end_date)
    test_start  = st.date_input("테스트 시작일", value=datetime.date(2024, 1, 1),
                                 min_value=valid_start, max_value=end_date)

    st.divider()

    # 모델 파라미터
    st.subheader("🤖 모델 파라미터")
    n_estimators  = st.slider("트리 수 (n_estimators)", 50, 500, 300, 50)
    max_depth     = st.slider("최대 깊이 (max_depth)", 2, 8, 4)
    learning_rate = st.select_slider("학습률", options=[0.005, 0.01, 0.02, 0.03, 0.05, 0.1], value=0.03)

    st.divider()

    # 전략 파라미터
    st.subheader("📊 전략 파라미터")
    signal_ratio = st.slider(
        "시그널 비율 (상하위 N%)",
        min_value=10, max_value=50, value=30, step=5,
        help="상위 N%를 매수, 하위 N%를 매도 시그널로 설정합니다.\n값이 클수록 거래 횟수 증가, 신뢰도 감소."
    )
    fee_rate = st.number_input("거래 수수료 (%)", min_value=0.0, max_value=1.0, value=0.15, step=0.01,
                                help="왕복 아님, 편도 수수료율")

    run_btn = st.button("▶  분석 실행", type="primary", use_container_width=True)

# ────────────────────────────────────────────────────────────────
# 4. 메인 영역
# ────────────────────────────────────────────────────────────────
st.title("📈 한국 주식 XGBoost 백테스트 대시보드")
st.caption("FinanceDataReader + XGBoost 기반 | 분포 적응형 threshold | 수수료 반영")

if not run_btn:
    st.info("👈 왼쪽 사이드바에서 종목과 파라미터를 설정한 뒤 **▶ 분석 실행**을 클릭하세요.")
    st.stop()

# ────────────────────────────────────────────────────────────────
# 5. 데이터 로드 & 피처 생성
# ────────────────────────────────────────────────────────────────
with st.spinner(f"📥 {selected_name}({selected_code}) 데이터 로딩 중..."):
    try:
        df = fdr.DataReader(selected_code, str(start_date), str(end_date))
        df.reset_index(inplace=True)
        if len(df) < 100:
            st.error("데이터가 너무 적습니다. 시작일을 더 앞으로 조정해주세요.")
            st.stop()
    except Exception as e:
        st.error(f"데이터 로딩 실패: {e}")
        st.stop()

# 피처 엔지니어링
df["return_1d"] = df["Close"].pct_change().shift(-1)

df["ma5"]  = df["Close"].rolling(5).mean()
df["ma20"] = df["Close"].rolling(20).mean()
df["ma60"] = df["Close"].rolling(60).mean()

df["disp_5"]  = df["Close"] / df["ma5"]  - 1
df["disp_20"] = df["Close"] / df["ma20"] - 1
df["disp_60"] = df["Close"] / df["ma60"] - 1

df["ma_ratio"]      = df["ma5"] / df["ma20"]
df["momentum_5"]    = df["Close"] / df["Close"].shift(5)  - 1
df["momentum_20"]   = df["Close"] / df["Close"].shift(20) - 1
df["volatility_20"] = df["Close"].pct_change().rolling(20).std()
df["volume_ma20"]   = df["Volume"].rolling(20).mean()
df["volume_ratio"]  = df["Volume"] / df["volume_ma20"]

df["target"] = (df["return_1d"] > 0).astype(int)
df.dropna(inplace=True)

FEATURES = [
    "disp_5", "disp_20", "disp_60",
    "ma_ratio",
    "momentum_5", "momentum_20",
    "volatility_20",
    "volume_ratio",
]

# 날짜 필터
train = df[df["Date"] < pd.Timestamp(valid_start)].copy()
valid = df[(df["Date"] >= pd.Timestamp(valid_start)) & (df["Date"] < pd.Timestamp(test_start))].copy()
test  = df[df["Date"] >= pd.Timestamp(test_start)].copy()

if len(train) < 50 or len(valid) < 20 or len(test) < 20:
    st.error("각 구간 데이터가 너무 적습니다. 날짜 구간을 조정해주세요.")
    st.stop()

X_train, y_train = train[FEATURES], train["target"]
X_valid, y_valid = valid[FEATURES], valid["target"]
X_test,  y_test  = test[FEATURES],  test["target"]

# ────────────────────────────────────────────────────────────────
# 6. 모델 학습
# ────────────────────────────────────────────────────────────────
with st.spinner("🤖 모델 학습 중..."):
    model = XGBClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        learning_rate=learning_rate,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        n_jobs=-1,
        early_stopping_rounds=20,
        eval_metric="logloss",
    )
    model.fit(X_train, y_train,
              eval_set=[(X_valid, y_valid)],
              verbose=False)

# ────────────────────────────────────────────────────────────────
# 7. 분포 기반 Threshold 계산
# ────────────────────────────────────────────────────────────────
valid_proba = model.predict_proba(X_valid)[:, 1]
ratio = signal_ratio / 100
BUY_TH  = np.percentile(valid_proba, (1 - ratio) * 100)
SELL_TH = np.percentile(valid_proba, ratio * 100)
FEE = fee_rate / 100

# ────────────────────────────────────────────────────────────────
# 8. 백테스트 함수
# ────────────────────────────────────────────────────────────────
def run_backtest(df_in, X_in):
    bt = df_in.copy().reset_index(drop=True)
    bt["proba"] = model.predict_proba(X_in)[:, 1]
    bt["signal"] = np.where(bt["proba"] > BUY_TH,   1,
                   np.where(bt["proba"] < SELL_TH, -1, 0))

    prev    = bt["signal"].shift(1).fillna(0)
    changed = bt["signal"] != prev
    bt["fee"] = 0.0
    bt.loc[changed & (bt["signal"] == 0),              "fee"] = FEE
    bt.loc[changed & (prev == 0),                      "fee"] = FEE
    bt.loc[changed & (bt["signal"] != 0) & (prev != 0),"fee"] = FEE * 2

    bt["strategy_return"] = bt["signal"] * bt["return_1d"] - bt["fee"]
    bt["bh_return"]       = bt["Close"].pct_change()
    bt["cum_market"]      = (1 + bt["bh_return"]).cumprod()
    bt["cum_strategy"]    = (1 + bt["strategy_return"]).cumprod()

    n_trades  = int(changed.sum())
    active    = bt[bt["signal"] != 0]
    win_rate  = (active["strategy_return"] > 0).mean() * 100 if len(active) > 0 else 0
    roll_max  = bt["cum_strategy"].cummax()
    mdd       = ((bt["cum_strategy"] - roll_max) / roll_max).min() * 100
    sharpe    = (bt["strategy_return"].mean() / bt["strategy_return"].std() * np.sqrt(252)
                 if bt["strategy_return"].std() > 0 else 0)

    stats = {
        "bh_return":   (bt["cum_market"].iloc[-1]   - 1) * 100,
        "strat_return":(bt["cum_strategy"].iloc[-1] - 1) * 100,
        "n_trades":    n_trades,
        "n_long":      int((bt["signal"] ==  1).sum()),
        "n_short":     int((bt["signal"] == -1).sum()),
        "n_neutral":   int((bt["signal"] ==  0).sum()),
        "win_rate":    win_rate,
        "mdd":         mdd,
        "sharpe":      sharpe,
    }
    return bt, stats

with st.spinner("📊 백테스트 수행 중..."):
    valid_bt, valid_stats = run_backtest(valid, X_valid)
    test_bt,  test_stats  = run_backtest(test,  X_test)

# ────────────────────────────────────────────────────────────────
# 9. 결과 출력
# ────────────────────────────────────────────────────────────────
st.divider()
st.subheader(f"🏷️ {selected_name}  ({selected_code})")

# 탭
tab1, tab2, tab3, tab4 = st.tabs(["📊 수익률 비교", "🔍 확률 분포", "📋 상세 통계", "📁 원본 데이터"])

# ── 탭 1: 수익률 비교 ──────────────────────────────────────────
with tab1:
    col_v, col_t = st.columns(2)

    def summary_metrics(col, stats, label):
        with col:
            st.markdown(f"**{label}**")
            excess = stats["strat_return"] - stats["bh_return"]
            m1, m2, m3 = st.columns(3)
            m1.metric("Buy&Hold 수익률",  f"{stats['bh_return']:+.2f}%")
            m2.metric("전략 수익률",       f"{stats['strat_return']:+.2f}%",
                      delta=f"초과 {excess:+.2f}%p")
            m3.metric("최대 낙폭 (MDD)",   f"{stats['mdd']:.2f}%")

    summary_metrics(col_v, valid_stats, f"📌 검증 구간  ({valid_start} ~ {test_start})")
    summary_metrics(col_t, test_stats,  f"📌 테스트 구간  ({test_start} ~ {end_date})")

    st.divider()

    # 차트
    fig, axes = plt.subplots(1, 2, figsize=(14, 4))
    for ax, bt, stats, label in [
        (axes[0], valid_bt, valid_stats, f"검증 ({valid_start}~{test_start})"),
        (axes[1], test_bt,  test_stats,  f"테스트 ({test_start}~{end_date})"),
    ]:
        ax.plot(bt["Date"], bt["cum_market"],   label="Buy & Hold", linewidth=1.8, color="#6c8ebf")
        ax.plot(bt["Date"], bt["cum_strategy"], label="XGBoost 전략", linewidth=1.8, color="#d6a931")
        ax.fill_between(bt["Date"],
                        bt["cum_market"], bt["cum_strategy"],
                        where=bt["cum_strategy"] >= bt["cum_market"],
                        alpha=0.08, color="green", label="_nolegend_")
        ax.fill_between(bt["Date"],
                        bt["cum_market"], bt["cum_strategy"],
                        where=bt["cum_strategy"] < bt["cum_market"],
                        alpha=0.08, color="red", label="_nolegend_")
        ax.set_title(label)
        ax.set_ylabel("누적 수익률 (기준=1)")
        ax.legend()
        ax.grid(True, alpha=0.25)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    # 일별 시그널 차트
    st.markdown("#### 📍 매매 시그널 (테스트 구간)")
    fig2, ax2 = plt.subplots(figsize=(14, 3))
    ax2.plot(test_bt["Date"], test_bt["Close"], color="gray", linewidth=1, alpha=0.6)
    long_days  = test_bt[test_bt["signal"] ==  1]
    short_days = test_bt[test_bt["signal"] == -1]
    ax2.scatter(long_days["Date"],  long_days["Close"],  marker="^", color="red",  s=30, label="매수", zorder=5)
    ax2.scatter(short_days["Date"], short_days["Close"], marker="v", color="blue", s=30, label="매도", zorder=5)
    ax2.set_ylabel("주가 (원)")
    ax2.legend(); ax2.grid(True, alpha=0.25)
    plt.tight_layout()
    st.pyplot(fig2)
    plt.close()

# ── 탭 2: 확률 분포 ────────────────────────────────────────────
with tab2:
    col_a, col_b = st.columns(2)

    for col, proba_arr, label in [
        (col_a, valid_proba,                    f"검증 구간 ({valid_start}~{test_start})"),
        (col_b, model.predict_proba(X_test)[:,1], f"테스트 구간 ({test_start}~{end_date})"),
    ]:
        with col:
            st.markdown(f"**{label}**")
            fig, ax = plt.subplots(figsize=(6, 3.5))
            ax.hist(proba_arr, bins=30, color="steelblue", alpha=0.7, edgecolor="white")
            ax.axvline(BUY_TH,  color="red",  linestyle="--", linewidth=1.5, label=f"매수 기준 {BUY_TH:.3f}")
            ax.axvline(SELL_TH, color="blue", linestyle="--", linewidth=1.5, label=f"매도 기준 {SELL_TH:.3f}")
            ax.axvline(0.5,     color="gray", linestyle=":",  linewidth=1.0, label="0.5 기준선")
            ax.set_xlabel("예측 확률 (상승 확률)")
            ax.set_ylabel("빈도")
            ax.legend(fontsize=8)
            ax.grid(True, alpha=0.25)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

            c1, c2, c3 = st.columns(3)
            c1.metric("평균",      f"{proba_arr.mean():.4f}")
            c2.metric("표준편차",  f"{proba_arr.std():.4f}")
            c3.metric("범위",      f"{proba_arr.min():.3f}~{proba_arr.max():.3f}")

    st.info(f"**분포 기반 Threshold** | 매수: **{BUY_TH:.4f}** | 매도: **{SELL_TH:.4f}** | 시그널 비율: 상하위 **{signal_ratio}%**")

    # 피처 중요도
    st.markdown("#### 🔑 피처 중요도")
    feat_imp = pd.Series(model.feature_importances_, index=FEATURES).sort_values(ascending=True)
    fig3, ax3 = plt.subplots(figsize=(7, 3.5))
    colors = ["#d6a931" if v == feat_imp.max() else "#6c8ebf" for v in feat_imp]
    ax3.barh(feat_imp.index, feat_imp.values, color=colors)
    ax3.set_xlabel("중요도 (gain)")
    ax3.grid(True, alpha=0.2, axis="x")
    plt.tight_layout()
    st.pyplot(fig3)
    plt.close()

# ── 탭 3: 상세 통계 ────────────────────────────────────────────
with tab3:
    def stats_table(stats, period_label):
        rows = [
            ("구분",            period_label),
            ("Buy&Hold 수익률", f"{stats['bh_return']:+.2f}%"),
            ("전략 수익률",      f"{stats['strat_return']:+.2f}%"),
            ("초과 수익",        f"{stats['strat_return'] - stats['bh_return']:+.2f}%p"),
            ("총 거래 횟수",     f"{stats['n_trades']}회"),
            ("매수 일수",        f"{stats['n_long']}일"),
            ("매도 일수",        f"{stats['n_short']}일"),
            ("관망 일수",        f"{stats['n_neutral']}일"),
            ("활성 구간 승률",   f"{stats['win_rate']:.1f}%"),
            ("최대 낙폭 (MDD)",  f"{stats['mdd']:.2f}%"),
            ("연환산 샤프지수",  f"{stats['sharpe']:.3f}"),
        ]
        return pd.DataFrame(rows, columns=["항목", "값"])

    col_vs, col_ts = st.columns(2)
    with col_vs:
        st.markdown(f"**검증 구간 ({valid_start} ~ {test_start})**")
        st.dataframe(stats_table(valid_stats, "검증"), use_container_width=True, hide_index=True)
    with col_ts:
        st.markdown(f"**테스트 구간 ({test_start} ~ {end_date})**")
        st.dataframe(stats_table(test_stats, "테스트"), use_container_width=True, hide_index=True)

    # 날짜별 비교 선택
    st.markdown("#### 📅 날짜별 시그널 상세 조회")
    view_period = st.radio("조회 구간", ["검증", "테스트"], horizontal=True)
    bt_view = valid_bt if view_period == "검증" else test_bt

    date_range = st.date_input(
        "날짜 범위",
        value=(bt_view["Date"].min().date(), bt_view["Date"].max().date()),
        min_value=bt_view["Date"].min().date(),
        max_value=bt_view["Date"].max().date(),
    )
    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        d1, d2 = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
        filtered_bt = bt_view[(bt_view["Date"] >= d1) & (bt_view["Date"] <= d2)].copy()
    else:
        filtered_bt = bt_view.copy()

    sig_filter = st.multiselect(
        "시그널 필터",
        options=["매수(1)", "매도(-1)", "관망(0)"],
        default=["매수(1)", "매도(-1)", "관망(0)"],
    )
    sig_map = {"매수(1)": 1, "매도(-1)": -1, "관망(0)": 0}
    sig_vals = [sig_map[s] for s in sig_filter]
    filtered_bt = filtered_bt[filtered_bt["signal"].isin(sig_vals)]

    display_cols = ["Date", "Close", "Volume", "proba", "signal",
                    "return_1d", "strategy_return", "cum_market", "cum_strategy"]
    display_cols = [c for c in display_cols if c in filtered_bt.columns]
    rename_map = {
        "Date": "날짜", "Close": "종가", "Volume": "거래량",
        "proba": "상승확률", "signal": "시그널",
        "return_1d": "익일수익률", "strategy_return": "전략수익률",
        "cum_market": "BH누적", "cum_strategy": "전략누적",
    }
    show_df = (
        filtered_bt[display_cols]
        .rename(columns=rename_map)
        .sort_values("날짜", ascending=False)
        .reset_index(drop=True)
    )
    # 포맷
    fmt = {
        "종가": "{:,.0f}",
        "거래량": "{:,.0f}",
        "상승확률": "{:.4f}",
        "익일수익률": "{:.4f}",
        "전략수익률": "{:.4f}",
        "BH누적": "{:.4f}",
        "전략누적": "{:.4f}",
    }
    st.dataframe(show_df.style.format(fmt, na_rep="-"), use_container_width=True, height=400)
    st.caption(f"총 {len(show_df):,}행 표시 중")

# ── 탭 4: 원본 데이터 ──────────────────────────────────────────
with tab4:
    st.markdown("#### 📁 전체 원본 데이터")
    st.dataframe(
        df[["Date", "Open", "High", "Low", "Close", "Volume"]].sort_values("Date", ascending=False).reset_index(drop=True),
        use_container_width=True, height=400
    )
    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        label="⬇️  CSV 다운로드",
        data=csv,
        file_name=f"{selected_code}_{selected_name}_{start_date}_{end_date}.csv",
        mime="text/csv",
    )

# ────────────────────────────────────────────────────────────────
# 10. 하단 정보
# ────────────────────────────────────────────────────────────────
st.divider()
with st.expander("ℹ️  사용 방법 및 주의사항"):
    st.markdown("""
**분석 흐름**
1. 사이드바에서 종목 검색 → 기간 설정 → 파라미터 조정 → **분석 실행** 클릭
2. **수익률 비교** 탭에서 전략 성과와 Buy&Hold 비교
3. **확률 분포** 탭에서 모델 신뢰도 및 피처 중요도 확인
4. **상세 통계** 탭에서 날짜별 시그널 및 수익률 조회

**파라미터 가이드**
| 파라미터 | 낮은 값 | 높은 값 |
|---|---|---|
| 시그널 비율 | 거래 적음, 신뢰도 높음 | 거래 많음, 노이즈 증가 |
| max_depth | 과소적합 위험 | 과적합 위험 |
| 학습률 | 안정적, 학습 느림 | 빠르지만 불안정 |

**주의사항**
- 본 결과는 **과거 데이터 기반 시뮬레이션**이며 실제 수익을 보장하지 않습니다.
- 숏 포지션은 공매도를 가정하며, 실제 거래에서는 추가 제약이 있습니다.
- 삼성전자(005930)처럼 거래량이 많고 데이터가 풍부한 종목에서 가장 안정적입니다.
    """)