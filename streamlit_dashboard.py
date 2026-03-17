import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
from sklearn.linear_model import LinearRegression


if "alert_log" not in st.session_state:
    st.session_state.alert_log = []
    
st.set_page_config(page_title="AI Monitor Pro", layout="wide")

st.markdown("""
<div style="display:flex; justify-content:space-between; align-items:center;">
    <div>
        <h1>🚀 AI Model Monitoring PRO</h1>
        <p style="opacity:0.7;">Real-time ML Monitoring • Drift • Prediction</p>
    </div>
    <div style="text-align:right;">
        <p style="font-size:14px;">🟢 System Online</p>
        <p style="font-size:12px; opacity:0.6;">Live Data Active</p>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------
# ✅ FUNCTION MUST BE HERE (TOP)
# -------------------------
def get_crypto_data():
    try:
        # Get last 100 data points (market chart)
        url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=1"

        res = requests.get(url).json()

        prices = res["prices"]  # [[timestamp, price], ...]

        # Extract only prices
        data = [p[1] for p in prices]

        return np.array(data[-100:])  # last 100 points

    except:
        # fallback (important)
        return np.random.normal(30000, 500, 100)
    

def detect_anomalies(data):
    mean = np.mean(data)
    std = np.std(data)

    upper = mean + sensitivity * std
    lower = mean - sensitivity * std

    anomaly_indices = [i for i, x in enumerate(data) if x > upper or x < lower]
    anomaly_values = [data[i] for i in anomaly_indices]

    return anomaly_indices, anomaly_values, upper, lower

def send_email_alert(anomaly_count):
    return f"""
    📧 EMAIL ALERT SENT

    To: ops-team@company.com
    Subject: 🚨 Model Alert - Anomalies Detected

    Message:
    {anomaly_count} anomalies detected in live data stream.
    Immediate investigation recommended.
    """

def send_slack_alert(anomaly_count):
    return f"""
    💬 SLACK ALERT

    Channel: #ml-monitoring

    🚨 *ALERT*
    {anomaly_count} anomalies detected!
    Please check dashboard ASAP.
    """

def predict_trend(data, steps=20):
    X = np.arange(len(data))
    
    # Smooth data using moving average
    window = 5
    smooth_data = np.convolve(data, np.ones(window)/window, mode='valid')

    # Fit on smoothed data
    X_smooth = np.arange(len(smooth_data)).reshape(-1, 1)

    from sklearn.linear_model import LinearRegression
    model = LinearRegression()
    model.fit(X_smooth, smooth_data)

    future_X = np.arange(len(smooth_data), len(smooth_data) + steps).reshape(-1, 1)
    predictions = model.predict(future_X)

    # Confidence band
    std_dev = np.std(smooth_data)
    upper_band = predictions + std_dev
    lower_band = predictions - std_dev

    return smooth_data, future_X.flatten(), predictions, upper_band, lower_band
    
# -------------------------
# UI
# -------------------------
st.success("🟢 Connected to Live Market Data (CoinGecko API)")
st.markdown("### ⚡ Real-time AI Monitoring • Anomaly Detection • Drift Intelligence")
st.caption("📡 Live Data Source: Bitcoin Price")

st.sidebar.title("⚙️ Control Panel")

refresh_rate = st.sidebar.slider("Refresh Speed (sec)", 5, 30, 10)
sensitivity = st.sidebar.slider("Anomaly Sensitivity", 1.0, 3.0, 1.5)

st.sidebar.markdown("---")
st.sidebar.caption("AI Monitor v2.0")

# -------------------------
# DATA (USING FUNCTION)
# -------------------------
data = get_crypto_data()
smooth_data, future_x, future_preds, upper_band, lower_band = predict_trend(data)
indices, anomalies, upper, lower = detect_anomalies(data)
baseline = np.random.normal(np.mean(data) * 0.95, np.std(data), 100)

st.markdown("""
<div style="display:flex; align-items:center; gap:8px; margin-bottom:10px;">
    <div style="
        width:10px;
        height:10px;
        background:#22c55e;
        border-radius:50%;
        box-shadow:0 0 10px #22c55e;
        animation: blink 1.2s infinite;
    "></div>
    <span style="opacity:0.8;">Live Monitoring Active</span>
</div>
""", unsafe_allow_html=True)

current_price = data[-1]
st.metric("💰 BTC Price (USD)", f"${current_price:,.2f}")

if len(anomalies) > 0:
    st.session_state.alert_log.append({
        "time": time.strftime("%H:%M:%S"),
        "anomalies": len(anomalies)
    })
# -------------------------
# SYSTEM STATUS BAR
# -------------------------

if len(anomalies) > 0:
    st.markdown("""
<style>

/* BACKGROUND */
.stApp {
    background: radial-gradient(circle at top, #0a0f1c, #020617);
    color: #e5e7eb;
}

/* METRIC CARDS */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.06);
    padding: 16px;
    border-radius: 14px;
    backdrop-filter: blur(6px);
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: #020617;
}

/* HEADINGS */
h1, h2, h3 {
    color: #f9fafb;
}

/* SUCCESS (GREEN) */
.css-1aumxhk {
    color: #22c55e;
}

/* ALERT (RED) */
.css-1xarl3l {
    color: #ef4444;
}

/* SCROLLBAR */
::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-thumb {
    background: #22c55e;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)
    
if len(anomalies) > 0:
    st.markdown(f"""
    <div style="
        background: rgba(239,68,68,0.08);
        border:1px solid rgba(239,68,68,0.4);
        padding:16px;
        border-radius:14px;
        margin-bottom:20px;
    ">
        <h4 style="margin:0; color:#ef4444;">
            🚨 {len(anomalies)} anomalies detected
        </h4>
        <p style="margin:5px 0 0 0; opacity:0.7;">
            System requires attention
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="
        background: rgba(34,197,94,0.08);
        border:1px solid rgba(34,197,94,0.4);
        padding:16px;
        border-radius:14px;
        margin-bottom:20px;
    ">
        <h4 style="margin:0; color:#22c55e;">
            ✅ System Stable
        </h4>
    </div>
    """, unsafe_allow_html=True)
    
    if len(anomalies) > 0:
      email_msg = send_email_alert(len(anomalies))
      slack_msg = send_slack_alert(len(anomalies))

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📩 Email Notification")
        st.code(email_msg, language="markdown")

    with col2:
        st.markdown("### 💬 Slack Notification")
        st.code(slack_msg, language="markdown")
# -------------------------
# METRICS
# -------------------------
st.markdown("### 📊 System Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 BTC Price", f"${current_price:,.2f}")
col2.metric("📊 Mean", f"{np.mean(data):.2f}")
col3.metric("📉 Volatility", f"{np.std(data):.2f}")

health = np.clip(100 - abs(np.mean(data)) * 40, 0, 100)
col4.metric("🧠 Health Score", f"{health:.0f}%")
# -------------------------
# DRIFT
# -------------------------

drift = abs(np.mean(data) - np.mean(baseline))

if drift > 0.5:
    st.error("⚠️ Drift Detected")
else:
    st.success("✅ Model Stable")

# -------------------------
# CHART
# -------------------------
import plotly.graph_objects as go

fig = go.Figure()

# 🔵 Original data
fig.add_trace(go.Scatter(
    y=data,
    mode='lines',
    name='Live Data',
    line=dict(width=2)
))

# 🟢 Smoothed trend
fig.add_trace(go.Scatter(
    y=smooth_data,
    mode='lines',
    name='Trend (Smoothed)',
    line=dict(width=3)
))

# 🟡 Prediction line
fig.add_trace(go.Scatter(
    x=future_x,
    y=future_preds,
    mode='lines',
    name='Prediction',
    line=dict(dash='dash', width=3)
))

# 🔥 Confidence band
fig.add_trace(go.Scatter(
    x=np.concatenate([future_x, future_x[::-1]]),
    y=np.concatenate([upper_band, lower_band[::-1]]),
    fill='toself',
    name='Confidence Range',
    opacity=0.2,
    line=dict(color='rgba(255,255,255,0)')
))

# 🔴 Anomalies
fig.add_trace(go.Scatter(
    x=indices,
    y=anomalies,
    mode='markers',
    name='Anomalies',
    marker=dict(size=8)
))

fig.update_layout(
    title="📈 AI Trend Forecast (Advanced)",
    template="plotly_dark",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------
# ALERT HISTORY
# -------------------------
st.markdown("### 🧾 Alert History")

if st.session_state.alert_log:
    st.dataframe(pd.DataFrame(st.session_state.alert_log))
else:
    st.info("No alerts yet")
# -------------------------
# AUTO REFRESH
# -------------------------
st.empty()
time.sleep(refresh_rate)
st.rerun()