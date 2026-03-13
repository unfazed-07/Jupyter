import streamlit as st
import anthropic
import plotly.graph_objects as go
import json
import math

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Pettiness Meter™",
    page_icon="⚖️",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {
    background-color: #0f0c1a;
    color: #ffffff;
    font-family: 'Space Mono', monospace;
}
.stApp {
    background: linear-gradient(135deg, #0f0c1a 0%, #1a1030 50%, #0f0c1a 100%);
}
.tribunal {
    text-align: center;
    letter-spacing: 0.3em;
    color: #a78bfa;
    font-size: 12px;
    margin-bottom: 4px;
    font-family: 'Space Mono', monospace;
}
.big-title {
    text-align: center;
    font-family: 'Playfair Display', serif;
    font-size: 3.2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #fff 0%, #c4b5fd 50%, #f9a8d4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.1;
    margin: 0;
}
.subtitle {
    text-align: center;
    color: rgba(255,255,255,0.4);
    font-size: 13px;
    letter-spacing: 0.1em;
    margin-top: 6px;
    font-family: 'Space Mono', monospace;
}
.section-label {
    font-size: 11px;
    letter-spacing: 0.25em;
    color: #a78bfa;
    font-family: 'Space Mono', monospace;
    margin-bottom: 8px;
}
.verdict-card {
    background: rgba(255,255,255,0.04);
    border-radius: 18px;
    padding: 22px;
    margin-top: 10px;
}
.verdict-title {
    font-size: 18px;
    font-weight: bold;
    font-family: 'Playfair Display', serif;
    margin-bottom: 14px;
    line-height: 1.4;
}
.roast-box {
    background: rgba(0,0,0,0.3);
    border-left: 3px solid #f97316;
    border-radius: 10px;
    padding: 12px 14px;
    font-style: italic;
    font-size: 14px;
    color: rgba(255,255,255,0.85);
    margin-bottom: 10px;
    line-height: 1.6;
}
.advice-box {
    background: rgba(0,0,0,0.3);
    border-left: 3px solid #60a5fa;
    border-radius: 10px;
    padding: 12px 14px;
    font-size: 14px;
    color: rgba(255,255,255,0.85);
    line-height: 1.6;
}
.box-label {
    font-size: 10px;
    letter-spacing: 0.2em;
    color: rgba(255,255,255,0.35);
    font-family: 'Space Mono', monospace;
    margin-bottom: 5px;
}
.history-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    font-size: 13px;
}
.badge {
    display: inline-block;
    padding: 5px 18px;
    border-radius: 100px;
    font-weight: bold;
    font-size: 14px;
    font-family: 'Space Mono', monospace;
    text-align: center;
    margin: 8px auto;
}
.footer-txt {
    text-align: center;
    font-size: 10px;
    color: rgba(255,255,255,0.2);
    letter-spacing: 0.2em;
    font-family: 'Space Mono', monospace;
    margin-top: 24px;
}
div[data-testid="stTextArea"] textarea {
    background: rgba(0,0,0,0.35) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
    color: #fff !important;
    font-size: 15px !important;
}
div[data-testid="stTextInput"] input {
    background: rgba(0,0,0,0.35) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: #fff !important;
}
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #7c3aed, #a855f7) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 0 !important;
    font-family: 'Space Mono', monospace !important;
    font-weight: 700 !important;
    letter-spacing: 0.15em !important;
    font-size: 15px !important;
    box-shadow: 0 4px 20px rgba(124,58,237,0.45) !important;
}
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Constants ─────────────────────────────────────────────────────────────────
EXAMPLES = [
    "My coworker microwaves fish in the break room every single day",
    "My friend liked everyone's posts except mine",
    "My roommate used the last of the milk and didn't tell me",
    "Someone took the parking spot I always use (it's not assigned)",
    "My partner breathes loudly while I'm trying to concentrate",
    "My colleague replied to everyone in the meeting except me",
]

ZONE_META = [
    (0,  20,  "#22c55e", "✅ Totally Valid",  "LEGITIMATE CONCERN"),
    (20, 40,  "#84cc16", "🤔 Kinda Valid",    "KINDA VALID"),
    (40, 60,  "#eab308", "⚖️  Debatable...", "DEBATABLE"),
    (60, 80,  "#f97316", "😤 Pretty Petty",   "PETTY"),
    (80, 101, "#ef4444", "🎈 LET IT GO!",     "LET IT GO"),
]


def get_meta(score):
    for lo, hi, color, label, zone in ZONE_META:
        if lo <= score < hi:
            return color, label, zone
    return "#ef4444", "🎈 LET IT GO!", "LET IT GO"


# ── Gauge chart ───────────────────────────────────────────────────────────────
def draw_gauge(score):
    color, label, zone = get_meta(score)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={
            "font": {"size": 44, "color": "#ffffff", "family": "Space Mono"},
        },
        gauge={
            "axis": {
                "range": [0, 100],
                "tickwidth": 1,
                "tickcolor": "rgba(255,255,255,0.3)",
                "tickfont": {"color": "rgba(255,255,255,0.4)", "size": 10, "family": "Space Mono"},
                "nticks": 11,
            },
            "bar": {"color": color, "thickness": 0.18},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 0,
            "steps": [
                {"range": [0,  20],  "color": "rgba(34,197,94,0.15)"},
                {"range": [20, 40],  "color": "rgba(132,204,22,0.15)"},
                {"range": [40, 60],  "color": "rgba(234,179,8,0.15)"},
                {"range": [60, 80],  "color": "rgba(249,115,22,0.15)"},
                {"range": [80, 100], "color": "rgba(239,68,68,0.15)"},
            ],
            "threshold": {
                "line": {"color": color, "width": 5},
                "thickness": 0.85,
                "value": score,
            },
        },
        title={
            "text": f"<b style='font-family:Space Mono'>{zone}</b>",
            "font": {"size": 14, "color": color, "family": "Space Mono"},
        },
        domain={"x": [0, 1], "y": [0, 1]},
    ))

    # Zone arc labels
    arc_labels = [
        (10,  "LEGITIMATE\nCONCERN", "#22c55e"),
        (30,  "KINDA\nVALID",        "#84cc16"),
        (50,  "DEBATABLE",           "#eab308"),
        (70,  "PETTY",               "#f97316"),
        (90,  "LET IT\nGO",          "#ef4444"),
    ]
    for pct, txt, lc in arc_labels:
        angle = math.radians(180 - pct * 1.8)
        rx = 0.44 * math.cos(angle)
        ry = 0.44 * math.sin(angle)
        fig.add_annotation(
            x=0.5 + rx,
            y=0.18 + ry,
            text=f"<b>{txt}</b>",
            showarrow=False,
            font={"size": 8, "color": lc, "family": "Space Mono"},
            align="center",
            xref="paper",
            yref="paper",
        )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=300,
        margin={"t": 60, "b": 10, "l": 30, "r": 30},
        font={"color": "#fff"},
    )
    return fig


# ── Claude API call ───────────────────────────────────────────────────────────
def analyze_grievance(grievance: str, api_key: str) -> dict:
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=512,
        system="""You are the Pettiness Meter — a snarky but kind judge of human grievances.
Analyze the grievance and respond ONLY with a valid JSON object.
No markdown, no backticks, no extra text. Just the raw JSON:
{
  "score": <integer 0-100, where 0=completely legitimate concern and 100=maximum pettiness>,
  "verdict": "<one punchy sentence verdict>",
  "roast": "<funny, slightly teasing 1-2 sentence roast about the grievance>",
  "advice": "<one sentence of actual advice or validation>"
}
Be funny and warm, not mean. Think: sassy best friend energy.""",
        messages=[{"role": "user", "content": grievance}],
    )
    raw = message.content[0].text.strip()
    return json.loads(raw)


# ── Session state ─────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "result" not in st.session_state:
    st.session_state.result = None
if "score" not in st.session_state:
    st.session_state.score = 0
if "prefill" not in st.session_state:
    st.session_state.prefill = ""


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<p class="tribunal">◆ OFFICIAL TRIBUNAL OF GRIEVANCES ◆</p>', unsafe_allow_html=True)
st.markdown('<h1 class="big-title">Pettiness<br>Meter™</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Submit your grievance. Face the truth.</p>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ── API key ───────────────────────────────────────────────────────────────────
with st.expander("🔑 Anthropic API Key", expanded="api_key" not in st.session_state):
    key_val = st.text_input(
        "API Key",
        type="password",
        placeholder="sk-ant-...",
        label_visibility="collapsed",
    )
    if key_val:
        st.session_state.api_key = key_val

# ── Gauge ─────────────────────────────────────────────────────────────────────
gauge_slot = st.empty()
gauge_slot.plotly_chart(
    draw_gauge(st.session_state.score),
    use_container_width=True,
    config={"displayModeBar": False},
)

# ── Input ─────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">◆ YOUR GRIEVANCE</p>', unsafe_allow_html=True)

grievance = st.text_area(
    "grievance",
    value=st.session_state.prefill,
    placeholder="Tell me what they did… 👀",
    height=110,
    label_visibility="collapsed",
    key="grievance_area",
)

# Example pills
st.markdown('<p class="section-label" style="margin-top:6px;">TRY AN EXAMPLE:</p>', unsafe_allow_html=True)
cols = st.columns(3)
for i, ex in enumerate(EXAMPLES):
    with cols[i % 3]:
        if st.button(ex[:30] + "…", key=f"ex_{i}"):
            st.session_state.prefill = ex
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# ── Submit ────────────────────────────────────────────────────────────────────
if st.button("⚖️  JUDGE MY GRIEVANCE"):
    if not grievance.strip():
        st.warning("Please type a grievance first!")
    elif "api_key" not in st.session_state or not st.session_state.api_key:
        st.warning("Please enter your Anthropic API key above.")
    else:
        with st.spinner("The tribunal is deliberating…"):
            try:
                result = analyze_grievance(grievance, st.session_state.api_key)
                score = max(0, min(100, int(result["score"])))
                st.session_state.score = score
                st.session_state.result = result
                st.session_state.history.insert(0, {
                    "grievance": grievance[:65] + ("…" if len(grievance) > 65 else ""),
                    "score": score,
                })
                st.session_state.history = st.session_state.history[:6]
                # Redraw gauge with new score
                gauge_slot.plotly_chart(
                    draw_gauge(score),
                    use_container_width=True,
                    config={"displayModeBar": False},
                )
            except json.JSONDecodeError:
                st.error("The tribunal is confused. Try rephrasing your grievance.")
            except Exception as e:
                st.error(f"Something went wrong: {e}")

# ── Verdict card ──────────────────────────────────────────────────────────────
if st.session_state.result:
    result = st.session_state.result
    score = st.session_state.score
    color, label, zone = get_meta(score)

    st.markdown(f"""
    <div class="verdict-card" style="border: 1px solid {color}55;">
        <div class="section-label">◆ THE VERDICT</div>
        <div class="verdict-title">{result.get('verdict', '')}</div>
        <div style="text-align:center; margin-bottom:16px;">
            <span class="badge" style="background:{color}22; border:1px solid {color}66; color:{color};">
                {label} &nbsp;·&nbsp; {score} / 100
            </span>
        </div>
        <div class="roast-box">
            <div class="box-label">THE ROAST</div>
            {result.get('roast', '')}
        </div>
        <div class="advice-box">
            <div class="box-label">MY ADVICE</div>
            {result.get('advice', '')}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── History ───────────────────────────────────────────────────────────────────
if len(st.session_state.history) > 1:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="section-label">◆ RECENT GRIEVANCES</p>', unsafe_allow_html=True)
    for h in st.session_state.history:
        c, lbl, _ = get_meta(h["score"])
        emoji = lbl.split(" ")[0]
        st.markdown(f"""
        <div class="history-row">
            <span style="color:rgba(255,255,255,0.6); flex:1; margin-right:12px;">{h['grievance']}</span>
            <span style="color:{c}; white-space:nowrap; font-family:'Space Mono',monospace; font-size:12px;">
                {h['score']} {emoji}
            </span>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<p class="footer-txt">ALL JUDGMENTS ARE FINAL · NO APPEALS ACCEPTED</p>', unsafe_allow_html=True)