import streamlit as st
import pandas as pd
import pickle
import json

import base64

def get_base64_gif(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

gif_base64 = get_base64_gif("bg.gif")

st.set_page_config(page_title="Threat Anomaly Detector", page_icon="🛡️", layout="wide")

with open("model.pkl", "rb") as f:
    model = pickle.load(f)
with open("top_features.json", "r") as f:
    top_features = json.load(f)



if "prediction" not in st.session_state:
    st.session_state.prediction = None
if "confidence" not in st.session_state:
    st.session_state.confidence = None

if "reset_count" not in st.session_state:
    st.session_state.reset_count = 0

pred = st.session_state.prediction
if pred == 1:
    node_color = "#ff3232"
    line_color = "220,50,50"
    pulse_color = "#ff3232"
    glow = "rgba(255,50,50,0.15)"
elif pred == 0:
    node_color = "#00ff9d"
    line_color = "0,255,157"
    pulse_color = "#00ff9d"
    glow = "rgba(0,255,157,0.10)"
else:
    node_color = "#00b4d8"
    line_color = "0,180,216"
    pulse_color = "#00b4d8"
    glow = "rgba(0,180,216,0.08)"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Share+Tech+Mono&display=swap');

*, body, .stApp {{ font-family: 'Inter', sans-serif !important; }}

.stApp {{
    background-image: url("data:image/gif;base64,{gif_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    color: #e0e0e0;
}}

.stApp::before {{
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: rgba(6, 10, 20, 0.88);
    z-index: 0;
    pointer-events: none;
}}

#network-canvas {{
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    z-index: 0;
    pointer-events: none;
}}

.block-container {{
    position: relative;
    z-index: 1;
    padding-top: 2rem !important;
}}

h1 {{ color: {node_color} !important; font-family: 'Share Tech Mono', monospace !important; letter-spacing: 2px; }}
h5 {{ color: #8899aa !important; font-weight: 300; }}

.section-header {{
    color: {node_color};
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 1rem;
    border-bottom: 1px solid #1a2535;
    padding-bottom: 0.5rem;
}}

.stNumberInput > label {{
    color: #8899aa !important;
    font-size: 0.82rem !important;
    font-weight: 400 !important;
    letter-spacing: 0.3px;
}}

div[data-testid="stNumberInput"] input {{
    background-color: #0d1526 !important;
    color: #e0e0e0 !important;
    border: 1px solid #1a2535 !important;
    border-radius: 6px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
}}

div[data-testid="stNumberInput"] input:focus {{
    border-color: {node_color} !important;
    box-shadow: 0 0 0 2px {glow} !important;
}}

.stButton {{ display: flex; justify-content: center; }}
.stButton > button {{
    background: linear-gradient(90deg, {node_color}, #00b4d8);
    color: #060a14;
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    border: none;
    padding: 0.75rem 3rem;
    font-size: 0.95rem;
    border-radius: 6px;
    letter-spacing: 2px;
    text-transform: uppercase;
    transition: all 0.3s ease;
    min-width: 280px;
}}

.stButton > button:hover {{
    opacity: 0.9;
    transform: translateY(-2px);
    box-shadow: 0 8px 25px {glow};
}}

.result-attack {{
    background: rgba(255,50,50,0.08);
    border: 1px solid #ff3232;
    border-left: 4px solid #ff3232;
    padding: 2rem;
    border-radius: 8px;
    text-align: center;
    font-family: 'Share Tech Mono', monospace;
    font-size: 1.5rem;
    color: #ff3232;
    letter-spacing: 3px;
    box-shadow: 0 0 30px rgba(255,50,50,0.2);
    animation: pulse-red 1.5s infinite;
}}

.result-benign {{
    background: rgba(0,255,157,0.05);
    border: 1px solid #00ff9d;
    border-left: 4px solid #00ff9d;
    padding: 2rem;
    border-radius: 8px;
    text-align: center;
    font-family: 'Share Tech Mono', monospace;
    font-size: 1.5rem;
    color: #00ff9d;
    letter-spacing: 3px;
    box-shadow: 0 0 30px rgba(0,255,157,0.15);
}}

@keyframes pulse-red {{
    0%, 100% {{ box-shadow: 0 0 20px rgba(255,50,50,0.2); }}
    50% {{ box-shadow: 0 0 40px rgba(255,50,50,0.5); }}
}}

.card {{
    background: rgba(13,21,38,0.85);
    border: 1px solid #1a2535;
    border-radius: 10px;
    padding: 1.5rem;
    backdrop-filter: blur(10px);
}}

footer {{ visibility: hidden; }}
</style>

<canvas id="network-canvas"></canvas>

<script>
const canvas = document.getElementById('network-canvas');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const nodeColor = '{node_color}';
const lineColor = '{line_color}';

const nodes = [];
const packets = [];
const NUM_NODES = 40;

for (let i = 0; i < NUM_NODES; i++) {{
    nodes.push({{
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 0.4,
        vy: (Math.random() - 0.5) * 0.4,
        r: Math.random() * 2.5 + 1
    }});
}}

function spawnPacket() {{
    const from = Math.floor(Math.random() * nodes.length);
    let to = Math.floor(Math.random() * nodes.length);
    while (to === from) to = Math.floor(Math.random() * nodes.length);
    packets.push({{ from, to, progress: 0, speed: Math.random() * 0.015 + 0.008 }});
}}

for (let i = 0; i < 10; i++) spawnPacket();

function draw() {{
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let i = 0; i < nodes.length; i++) {{
        for (let j = i + 1; j < nodes.length; j++) {{
            const dx = nodes[i].x - nodes[j].x;
            const dy = nodes[i].y - nodes[j].y;
            const dist = Math.sqrt(dx*dx + dy*dy);
            if (dist < 160) {{
                ctx.beginPath();
                ctx.strokeStyle = `rgba(${{lineColor}},${{0.12 * (1 - dist/160)}})`;
                ctx.lineWidth = 0.5;
                ctx.moveTo(nodes[i].x, nodes[i].y);
                ctx.lineTo(nodes[j].x, nodes[j].y);
                ctx.stroke();
            }}
        }}
    }}

    nodes.forEach(n => {{
        ctx.beginPath();
        ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${{lineColor}},0.5)`;
        ctx.fill();
        n.x += n.vx;
        n.y += n.vy;
        if (n.x < 0 || n.x > canvas.width) n.vx *= -1;
        if (n.y < 0 || n.y > canvas.height) n.vy *= -1;
    }});

    for (let i = packets.length - 1; i >= 0; i--) {{
        const p = packets[i];
        const from = nodes[p.from];
        const to = nodes[p.to];
        const x = from.x + (to.x - from.x) * p.progress;
        const y = from.y + (to.y - from.y) * p.progress;
        ctx.beginPath();
        ctx.arc(x, y, 3, 0, Math.PI * 2);
        ctx.fillStyle = nodeColor;
        ctx.shadowBlur = 8;
        ctx.shadowColor = nodeColor;
        ctx.fill();
        ctx.shadowBlur = 0;
        p.progress += p.speed;
        if (p.progress >= 1) {{
            packets.splice(i, 1);
            spawnPacket();
        }}
    }}

    requestAnimationFrame(draw);
}}

draw();
window.addEventListener('resize', () => {{
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}});
</script>
""", unsafe_allow_html=True)

st.markdown("# 🛡️ THREAT ANOMALY DETECTOR")
st.markdown("##### Real-time network traffic classification · Random Forest ML · CICIDS2017")
st.markdown("---")

with st.container():
    col1, col2, col3 = st.columns(3)


with col1:
    st.markdown('<div class="card"><p class="section-header">📦 Packet Size Metrics</p>', unsafe_allow_html=True)
    avg_bwd_seg = st.number_input("Avg Bwd Segment Size", value=0.0, key=f"avg_bwd_{st.session_state.reset_count}")
    bwd_pkt_std = st.number_input("Bwd Packet Length Std", value=0.0, key=f"bwd_std_{st.session_state.reset_count}")
    bwd_pkt_mean = st.number_input("Bwd Packet Length Mean", value=0.0, key=f"bwd_mean_{st.session_state.reset_count}")
    pkt_variance = st.number_input("Packet Length Variance", value=0.0, key=f"pkt_var_{st.session_state.reset_count}")
    bwd_pkt_max = st.number_input("Bwd Packet Length Max", value=0.0, key=f"bwd_max_{st.session_state.reset_count}")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card"><p class="section-header">⚡ Flow Statistics</p>', unsafe_allow_html=True)
    pkt_std = st.number_input("Packet Length Std", value=0.0, key=f"pkt_std_{st.session_state.reset_count}")
    bwd_total = st.number_input("Bwd Packets Length Total", value=0.0, key=f"bwd_total_{st.session_state.reset_count}")
    avg_pkt_size = st.number_input("Avg Packet Size", value=0.0, key=f"avg_pkt_{st.session_state.reset_count}")
    pkt_max = st.number_input("Packet Length Max", value=0.0, key=f"pkt_max_{st.session_state.reset_count}")
    pkt_mean = st.number_input("Packet Length Mean", value=0.0, key=f"pkt_mean_{st.session_state.reset_count}")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card"><p class="section-header">⏱️ Timing & Headers</p>', unsafe_allow_html=True)
    fwd_iat_std = st.number_input("Fwd IAT Std", value=0.0, key=f"fwd_iat_{st.session_state.reset_count}")
    fwd_header = st.number_input("Fwd Header Length", value=0.0, key=f"fwd_hdr_{st.session_state.reset_count}")
    subflow_bwd = st.number_input("Subflow Bwd Bytes", value=0.0, key=f"subflow_{st.session_state.reset_count}")
    flow_iat_max = st.number_input("Flow IAT Max", value=0.0, key=f"flow_iat_{st.session_state.reset_count}")
    total_fwd = st.number_input("Total Fwd Packets", value=0.0, key=f"total_fwd_{st.session_state.reset_count}")
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

_, btn_col, reset_col, _ = st.columns([1.5, 1, 1, 1.5])
with btn_col:
    analyse = st.button("🔍 ANALYSE TRAFFIC")
with reset_col:
    reset = st.button("🔄 RESET")

if reset:
    st.session_state.prediction = None
    st.session_state.confidence = None
    st.session_state.reset_count +=1
    st.rerun()

if analyse:
    input_data = pd.DataFrame([[0.0] * len(top_features)], columns=top_features)
    input_data['Avg Bwd Segment Size'] = avg_bwd_seg
    input_data['Bwd Packet Length Std'] = bwd_pkt_std
    input_data['Bwd Packet Length Mean'] = bwd_pkt_mean
    input_data['Packet Length Variance'] = pkt_variance
    input_data['Bwd Packet Length Max'] = bwd_pkt_max
    input_data['Packet Length Std'] = pkt_std
    input_data['Bwd Packets Length Total'] = bwd_total
    input_data['Avg Packet Size'] = avg_pkt_size
    input_data['Packet Length Max'] = pkt_max
    input_data['Packet Length Mean'] = pkt_mean
    input_data['Fwd IAT Std'] = fwd_iat_std
    input_data['Fwd Header Length'] = fwd_header
    input_data['Subflow Bwd Bytes'] = subflow_bwd
    input_data['Flow IAT Max'] = flow_iat_max
    input_data['Total Fwd Packets'] = total_fwd

    prediction = model.predict(input_data)[0]
    proba = model.predict_proba(input_data)[0]
    confidence = round(max(proba) * 100, 2)

    st.session_state.prediction = int(prediction)
    st.session_state.confidence = confidence

if st.session_state.prediction is not None:
    st.markdown("---")
    _, res_col, _ = st.columns([1, 2, 1])
    with res_col:
        if st.session_state.prediction == 0:
            st.markdown(f'<div class="result-benign">✅ BENIGN TRAFFIC<br><small style="font-size:0.9rem;letter-spacing:1px">Confidence: {st.session_state.confidence}%</small></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="result-attack">🚨 ATTACK DETECTED<br><small style="font-size:0.9rem;letter-spacing:1px">Confidence: {st.session_state.confidence}%</small></div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("CICIDS2017 Dataset · Random Forest Classifier · 99% Accuracy · Built by Sujot")
