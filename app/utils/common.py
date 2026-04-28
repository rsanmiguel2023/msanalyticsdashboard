from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
PROCESSED = DATA / "processed"
FIGURES = ROOT / "figures"

THEME_CSS = """
<style>
.msft-tip-title { display:flex; align-items:center; margin-bottom:.35rem; }
.msft-tip-title h2 { margin:0; padding:0; font-size:1.5rem; font-weight:700; letter-spacing:-.01em; }
.msft-tip-title h3 { margin:0; padding:0; font-size:1.28rem; font-weight:650; letter-spacing:-.01em; }
.msft-tip { position:relative; display:inline-flex; align-items:center; cursor:help; margin-left:10px; flex-shrink:0; }
.msft-tip-icon { font-size:.9rem; color:#888; user-select:none; }
.msft-tip-box { visibility:hidden; opacity:0; width:390px; background-color:rgba(28,28,44,.97); color:#e4e4f0; text-align:left; border-radius:8px; padding:14px 18px; font-size:.94rem; line-height:1.65; position:absolute; z-index:9999; bottom:calc(100% + 10px); left:50%; transform:translateX(-50%); transition:opacity .2s ease; box-shadow:0 6px 24px rgba(0,0,0,.45); pointer-events:none; white-space:normal; }
.msft-tip-box::after { content:""; position:absolute; top:100%; left:50%; margin-left:-6px; border:6px solid transparent; border-top-color:rgba(28,28,44,.97); }
.msft-tip:hover .msft-tip-box { visibility:visible; opacity:1; }
.step-badge { background:#f0f4ff; border-radius:6px; padding:8px 14px; margin-bottom:8px; font-size:.75rem; font-weight:700; color:#2c5282; letter-spacing:.08em; text-transform:uppercase; }
.executive-banner { background:linear-gradient(135deg,#0f2440 0%,#1a3660 100%); border-left:5px solid #7986CB; border-radius:10px; padding:22px 28px; margin-bottom:8px; }
.executive-label { color:#f0c040; font-size:.78rem; font-weight:700; letter-spacing:.12em; text-transform:uppercase; margin:0 0 10px 0; }
.executive-text { color:#e8eaf0; font-size:1rem; line-height:1.75; margin:0; }
.small-note { color:#6b7280; font-size:.9rem; }
@media (max-width:768px) { .msft-tip-box { width:260px; font-size:.85rem; } .step-badge { font-size:.68rem; padding:6px 10px; } }
</style>
"""

def apply_theme():
    st.markdown(THEME_CSS, unsafe_allow_html=True)

def tip_header(label: str, tooltip: str, level: int = 3):
    parts = tooltip.split("**")
    tip_html = "".join(f"<strong>{p}</strong>" if i % 2 else p for i, p in enumerate(parts))
    st.markdown(f'<div class="msft-tip-title"><h{level}>{label}</h{level}><span class="msft-tip"><span class="msft-tip-icon">ℹ️</span><span class="msft-tip-box">{tip_html}</span></span></div>', unsafe_allow_html=True)

def banner(label: str, text: str):
    st.markdown(f'<div class="executive-banner"><p class="executive-label">{label}</p><p class="executive-text">{text}</p></div>', unsafe_allow_html=True)

def load_csv(name: str, nrows=None):
    path = PROCESSED / name
    if path.exists():
        return pd.read_csv(path, nrows=nrows)
    st.warning(f"Missing processed file: {path}")
    return pd.DataFrame()

def show_image(path: Path, caption: str | None = None):
    if path.exists():
        st.image(str(path), caption=caption, use_container_width=True)
    else:
        st.info(f"Figure not found yet: {path.name}")
