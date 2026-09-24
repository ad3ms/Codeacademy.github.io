from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="SharpScope | Sportsbook Quant Hub",
    page_icon="🎯",
    layout="wide",
)

# -----------------------------------------------------------------------------
# 1. APPLICATION DATA REGISTRY
# -----------------------------------------------------------------------------
SLATE_DATABASE = {
    "🏈 NFL": {
        "Patrick Mahomes (KC - QB)": {
            "team": "KC",
            "opponent": "BAL",
            "game_info": "KC +3.0 | O/U 48.5",
            "stat_category": "Passing Yards",
            "line": 265.5,
            "recent_logs": [272, 291, 240, 305, 280, 266, 310, 295, 220, 285],
            "opponents": [
                "DEN",
                "LV",
                "LAC",
                "BUF",
                "SF",
                "CIN",
                "MIA",
                "ATL",
                "NO",
                "CLE",
            ],
            "odds": {
                "DraftKings": -108,
                "FanDuel": -114,
                "BetMGM": -115,
                "Caesars": -110,
                "Pinnacle (Sharp)": -122,
            },
        },
        "Christian McCaffrey (SF - RB)": {
            "team": "SF",
            "opponent": "LAR",
            "game_info": "SF -4.5 | O/U 44.0",
            "stat_category": "Rushing Yards",
            "line": 74.5,
            "recent_logs": [95, 84, 110, 62, 90, 105, 82, 79, 70, 88],
            "opponents": [
                "ARI",
                "SEA",
                "LAR",
                "DAL",
                "KC",
                "MIN",
                "GB",
                "TB",
                "DET",
                "CHI",
            ],
            "odds": {
                "DraftKings": -110,
                "FanDuel": -118,
                "BetMGM": -115,
                "Caesars": -105,
                "Pinnacle (Sharp)": -124,
            },
        },
        "CeeDee Lamb (DAL - WR)": {
            "team": "DAL",
            "opponent": "PHI",
            "game_info": "DAL +2.5 | O/U 47.0",
            "stat_category": "Receiving Yards",
            "line": 82.5,
            "recent_logs": [98, 112, 74, 88, 105, 67, 92, 115, 85, 90],
            "opponents": [
                "NYG",
                "WAS",
                "BAL",
                "CLE",
                "DET",
                "SF",
                "ATL",
                "HOU",
                "CIN",
                "CAR",
            ],
            "odds": {
                "DraftKings": -112,
                "FanDuel": -115,
                "BetMGM": -108,
                "Caesars": -110,
                "Pinnacle (Sharp)": -121,
            },
        },
    },
    "⚾ MLB": {
        "Aaron Judge (NYY - OF)": {
            "team": "NYY",
            "opponent": "BOS",
            "game_info": "NYY -130 | O/U 8.5",
            "stat_category": "Total Bases",
            "line": 1.5,
            "recent_logs": [2, 4, 0, 3, 2, 1, 3, 2, 4, 2],
            "opponents": [
                "TOR",
                "TB",
                "BAL",
                "BOS",
                "MIN",
                "CWS",
                "DET",
                "CLE",
                "HOU",
                "TEX",
            ],
            "odds": {
                "DraftKings": -108,
                "FanDuel": -112,
                "BetMGM": -115,
                "Caesars": -105,
                "Pinnacle (Sharp)": -118,
            },
        },
        "Shohei Ohtani (LAD - DH)": {
            "team": "LAD",
            "opponent": "SD",
            "game_info": "LAD -145 | O/U 8.0",
            "stat_category": "Total Bases",
            "line": 1.5,
            "recent_logs": [3, 0, 4, 2, 1, 4, 0, 3, 2, 3],
            "opponents": [
                "SF",
                "ARI",
                "COL",
                "SD",
                "LAA",
                "OAK",
                "MIL",
                "CIN",
                "NYM",
                "PHI",
            ],
            "odds": {
                "DraftKings": -115,
                "FanDuel": -110,
                "BetMGM": -118,
                "Caesars": -105,
                "Pinnacle (Sharp)": -126,
            },
        },
        "Tarik Skubal (DET - SP)": {
            "team": "DET",
            "opponent": "CWS",
            "game_info": "DET -185 | O/U 7.5",
            "stat_category": "Strikeouts",
            "line": 6.5,
            "recent_logs": [8, 9, 7, 6, 8, 10, 7, 8, 6, 9],
            "opponents": [
                "KC",
                "CLE",
                "MIN",
                "TOR",
                "TEX",
                "OAK",
                "SEA",
                "BOS",
                "TB",
                "CWS",
            ],
            "odds": {
                "DraftKings": -135,
                "FanDuel": -142,
                "BetMGM": -130,
                "Caesars": -128,
                "Pinnacle (Sharp)": -150,
            },
        },
    },
}

# -----------------------------------------------------------------------------
# 2. TOP CONTROLS & HEADER
# -----------------------------------------------------------------------------
st.title("🎯 SharpScope Quantitative Dashboard")

col_sport, col_player, col_sync = st.columns([2, 4, 2])

with col_sport:
    selected_sport = st.selectbox("Sport", list(SLATE_DATABASE.keys()))

players_available = list(SLATE_DATABASE[selected_sport].keys())

with col_player:
    selected_player = st.selectbox("Player Target", players_available)

with col_sync:
    st.write("")
    if st.button("🔄 Sync Feed / Refresh", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

current_poll = datetime.now().strftime("%I:%M:%S %p")
st.caption(f"System status: Connected • Last poll at {current_poll}")

# Extract selected player payload
data = SLATE_DATABASE[selected_sport][selected_player]
logs = data["recent_logs"]
opps = data["opponents"]

st.divider()

# -----------------------------------------------------------------------------
# 3. CONTEXT & METRICS (PROPSMADNESS-STYLE OVERVIEW)
# -----------------------------------------------------------------------------
st.subheader(f"{selected_player} — {data['team']} vs @{data['opponent']}")
st.write(f"**Matchup Context:** {data['game_info']} | Stat: **{data['stat_category']}**")

target_line = st.number_input(
    f"Target Line ({data['stat_category']})",
    value=float(data["line"]),
    step=0.5,
)

# Calculate Hits
hits_l5 = sum(1 for val in logs[-5:] if val > target_line)
hits_l10 = sum(1 for val in logs[-10:] if val > target_line)
hit_rate_pct = int((hits_l10 / len(logs)) * 100)

m1, m2, m3, m4 = st.columns(4)
m1.metric(label="L5 Hit Rate", value=f"{int(hits_l5/5*100)}%", delta=f"{hits_l5}/5 Over")
m2.metric(label="L10 Hit Rate", value=f"{hit_rate_pct}%", delta=f"{hits_l10}/10 Over")
m3.metric(label="Season Benchmark", value="73%", delta="11/15 Over")
m4.metric(
    label="Hit Trend Status",
    value="🔥 Over 75% Trend" if hit_rate_pct >= 75 else "Standard",
    delta="Edge Detected" if hit_rate_pct >= 75 else "Neutral",
)

# -----------------------------------------------------------------------------
# 4. GAME LOG VISUALIZER (OVER/UNDER BARS)
# -----------------------------------------------------------------------------
st.markdown("### 📊 Game-by-Game Visualizer")

bar_colors = ["#2ecc71" if val > target_line else "#e74c3c" for val in logs]

fig = go.Figure()
fig.add_trace(
    go.Bar(
        x=[f"{opps[i]} (G{i+1})" for i in range(len(logs))],
        y=logs,
        marker_color=bar_colors,
        text=[str(v) for v in logs],
        textposition="outside",
        name="Stat Value",
    )
)

fig.add_shape(
    type="line",
    x0=-0.5,
    x1=len(logs) - 0.5,
    y0=target_line,
    y1=target_line,
    line=dict(color="#f1c40f", width=2.5, dash="dash"),
)

fig.update_layout(
    height=320,
    margin=dict(l=10, r=10, t=20, b=20),
    template="plotly_dark",
    yaxis_title=data["stat_category"],
    xaxis_title="Recent Games",
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# 5. LINE SHOPPER (ODDS COMPARISON)
# -----------------------------------------------------------------------------
st.markdown("### 🛒 Sportsbook Odds Comparison")

odds_dict = data["odds"]
best_book = max(odds_dict, key=lambda k: odds_dict[k])

cards = st.columns(len(odds_dict))
for idx, (book, odds_val) in enumerate(odds_dict.items()):
    is_best = book == best_book
    sign = "+" if odds_val > 0 else ""
    with cards[idx]:
        st.metric(
            label=f"⭐ {book}" if is_best else book,
            value=f"{sign}{odds_val}",
            delta="Best Line" if is_best else f"Over {target_line}",
        )
