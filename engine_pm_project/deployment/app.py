
"""
Engine Predictive Maintenance - Deployment App
Final submission: Load model from Hugging Face hub; get inputs and save into dataframe; predict.
Designed for Streamlit on Hugging Face Spaces.
"""
import os
# Avoid indefinite hang on model download (e.g. when Space health check runs before hub responds)
os.environ.setdefault("HF_HUB_DOWNLOAD_TIMEOUT", "60")

import streamlit as st
import pandas as pd
import joblib
import os
import plotly.graph_objects as go
from huggingface_hub import hf_hub_download

FEATURES = [
    "Engine_RPM", "Lub_Oil_Pressure", "Fuel_Pressure",
    "Coolant_Pressure", "Lub_Oil_Temperature", "Coolant_Temperature",
]
MODEL_REPO = "ananttripathiak/engine-pm-model"
MODEL_FILENAME = "best_model.joblib"

# Default sensor values = row with lowest maintenance prob in train set (~44% → Normal)
DEFAULT_SENSORS = {
    "Engine_RPM": 1437,
    "Lub_Oil_Pressure": 1.9,
    "Fuel_Pressure": 3.8,
    "Coolant_Pressure": 3.8,
    "Lub_Oil_Temperature": 77.5,
    "Coolant_Temperature": 79.8,
}

# Must be first Streamlit command
st.set_page_config(
    page_title="Engine Predictive Maintenance",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better visuals
st.markdown("""
<style>
    /* Header block */
    .main-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 50%, #3d7ab5 100%);
        padding: 1.5rem 1.5rem 1.8rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 14px rgba(0,0,0,0.15);
    }
    .main-header h1 {
        color: white !important;
        font-size: 1.85rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.3rem !important;
    }
    .main-header p {
        color: rgba(255,255,255,0.9) !important;
        font-size: 1rem !important;
        margin: 0 !important;
    }
    /* Sensor card */
    .sensor-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.25rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    /* Result card - Normal */
    .result-ok {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border: 1px solid #6ee7b7;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 2px 8px rgba(52,211,153,0.25);
    }
    .result-ok .status { font-size: 1.5rem; font-weight: 700; color: #065f46; }
    .result-ok .sub { font-size: 0.95rem; color: #047857; margin-top: 0.3rem; }
    /* Result card - Maintenance */
    .result-warn {
        background: linear-gradient(135deg, #fed7aa 0%, #fdba74 100%);
        border: 1px solid #fb923c;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 2px 8px rgba(251,146,60,0.3);
    }
    .result-warn .status { font-size: 1.5rem; font-weight: 700; color: #9a3412; }
    .result-warn .sub { font-size: 0.95rem; color: #c2410c; margin-top: 0.3rem; }
    /* Probability bar */
    .prob-bar {
        height: 12px;
        background: #e2e8f0;
        border-radius: 6px;
        overflow: hidden;
        margin: 0.8rem 0;
    }
    .prob-fill {
        height: 100%;
        border-radius: 6px;
        transition: width 0.5s ease;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 0.65rem 1.5rem !important;
        border-radius: 8px !important;
        border: none !important;
        box-shadow: 0 2px 6px rgba(30,58,95,0.35);
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #2d5a87 0%, #3d7ab5 100%) !important;
        box-shadow: 0 4px 12px rgba(30,58,95,0.4);
    }
    /* Sidebar */
    .sidebar .sidebar-content { background: #f1f5f9; }
    div[data-testid="stSidebar"] .stMarkdown { font-size: 0.9rem; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    path = hf_hub_download(
        repo_id=MODEL_REPO,
        filename=MODEL_FILENAME,
        repo_type="model",
        token=os.getenv("HF_TOKEN"),
    )
    return joblib.load(path)


def main():
    # Sidebar: info and legend
    with st.sidebar:
        st.markdown("### 🔧 About")
        st.markdown("Predict **engine condition** from six sensor readings. The model was trained on engine maintenance data and is hosted on the Hugging Face model hub.")
        st.markdown("---")
        st.markdown("**Sensors:**")
        st.markdown("- **RPM** – engine speed")
        st.markdown("- **Pressures** – lubricating oil, fuel, coolant (bar)")
        st.markdown("- **Temperatures** – oil & coolant (°C)")
        st.markdown("---")
        st.markdown("**Model:** Gradient Boosting (best by F1)")
        st.markdown("---")
        st.markdown("**Tip:** Change sensor values and click **Get prediction** again — the probability should change. If it stays the same, clear the app cache (⋮ → Clear cache) or re-run the GitHub pipeline to refresh the model on the hub.")

    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🔧 Engine Predictive Maintenance</h1>
        <p>Enter sensor readings below — get a Normal or Maintenance Required prediction</p>
    </div>
    """, unsafe_allow_html=True)

    # Load model only when needed (on first prediction), so Space startup is not blocked by model download
    model = None

    # Inputs OUTSIDE form so values update immediately; button triggers prediction
    # Defaults = row with lowest maintenance prob in train set (model gives ~44%)
    st.markdown("#### 📊 Sensor inputs")
    c1, c2 = st.columns(2)
    with c1:
        engine_rpm = st.number_input("Engine RPM", min_value=0, max_value=5000, value=DEFAULT_SENSORS["Engine_RPM"], key="rpm", help="Revolutions per minute")
        lub_oil_pressure = st.number_input("Lubricating oil pressure (bar)", min_value=0.0, max_value=15.0, value=DEFAULT_SENSORS["Lub_Oil_Pressure"], step=0.1, key="lop")
        fuel_pressure = st.number_input("Fuel pressure (bar)", min_value=0.0, max_value=25.0, value=DEFAULT_SENSORS["Fuel_Pressure"], step=0.1, key="fp")
    with c2:
        coolant_pressure = st.number_input("Coolant pressure (bar)", min_value=0.0, max_value=10.0, value=DEFAULT_SENSORS["Coolant_Pressure"], step=0.1, key="cp")
        lub_oil_temp = st.number_input("Lubricating oil temperature (°C)", min_value=50.0, max_value=120.0, value=DEFAULT_SENSORS["Lub_Oil_Temperature"], step=0.5, key="lot")
        coolant_temp = st.number_input("Coolant temperature (°C)", min_value=50.0, max_value=200.0, value=DEFAULT_SENSORS["Coolant_Temperature"], step=0.5, key="ct")
    submitted = st.button("🚀 Get prediction")

    # Build input from CURRENT widget values (no form = always in sync)
    input_df = pd.DataFrame([{
        "Engine_RPM": engine_rpm,
        "Lub_Oil_Pressure": lub_oil_pressure,
        "Fuel_Pressure": fuel_pressure,
        "Coolant_Pressure": coolant_pressure,
        "Lub_Oil_Temperature": lub_oil_temp,
        "Coolant_Temperature": coolant_temp,
    }])

    if submitted:
        # Load model on first prediction (keeps Space startup fast; download happens here)
        try:
            model = load_model()
        except Exception as e:
            st.error(f"Could not load model from Hugging Face ({MODEL_REPO}). Error: {e}")
            st.info("Ensure the model is uploaded to the hub and HF_TOKEN is set if the repo is private.")
            return

        # Ensure exact feature order and single row for the pipeline
        X = input_df[FEATURES].copy()
        st.caption(f"Predicting with: RPM={int(engine_rpm)}, oil P={lub_oil_pressure}, fuel P={fuel_pressure}, coolant P={coolant_pressure}, oil T={lub_oil_temp}, coolant T={coolant_temp}")
        prediction = model.predict(X)[0]
        proba = model.predict_proba(X)[0]
        # proba[0] = Normal, proba[1] = Maintenance Required
        prob_maintenance = float(proba[1])
        prob_normal = float(proba[0])
        label = "Maintenance Required" if prediction == 1 else "Normal"

        # Visual result card
        if prediction == 1:
            st.markdown(f"""
            <div class="result-warn">
                <div class="status">⚠️ {label}</div>
                <div class="sub">Consider scheduling maintenance based on sensor readings.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-ok">
                <div class="status">✓ {label}</div>
                <div class="sub">Engine parameters look within normal range.</div>
            </div>
            """, unsafe_allow_html=True)

        # Probability as metric + progress bar
        st.markdown("**Probability (Maintenance)**")
        fill_color = "#f59e0b" if prob_maintenance > 0.5 else "#10b981"
        st.markdown(f"""
        <div class="prob-bar">
            <div class="prob-fill" style="width: {prob_maintenance * 100:.0f}%; background: {fill_color};"></div>
        </div>
        """, unsafe_allow_html=True)
        st.metric("", f"{prob_maintenance:.1%}")
        st.caption(f"Normal: {prob_normal:.1%} · Maintenance: {prob_maintenance:.1%} (should change when you change sensor values)")

        # Visual summary: radar only, full width
        st.markdown("---")
        st.markdown("#### 📈 Visual summary")
        sensor_labels = ["Engine RPM", "Oil pressure", "Fuel pressure", "Coolant pressure", "Oil temp.", "Coolant temp."]
        mins = [0, 0, 0, 0, 50, 50]
        maxs = [5000, 15, 25, 10, 120, 200]
        units = ["RPM", "bar", "bar", "bar", "°C", "°C"]
        raw = [engine_rpm, lub_oil_pressure, fuel_pressure, coolant_pressure, lub_oil_temp, coolant_temp]
        pct = [100 * (v - mn) / (mx - mn) if mx > mn else 0 for v, mn, mx in zip(raw, mins, maxs)]
        r_filled = pct + [pct[0]]
        theta_labels = sensor_labels + [sensor_labels[0]]
        actual_str = [f"{raw[i]:.1f} {units[i]}" if i >= 1 else f"{int(raw[0])} {units[0]}" for i in range(6)]
        actual_str += [actual_str[0]]
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=[100] * 7,
            theta=theta_labels,
            fill="toself",
            fillcolor="rgba(148, 163, 184, 0.08)",
            line=dict(color="#94a3b8", width=1, dash="dot"),
            name="Max range",
            hoverinfo="skip",
        ))
        fig.add_trace(go.Scatterpolar(
            r=r_filled,
            theta=theta_labels,
            fill="toself",
            fillcolor="rgba(59, 130, 246, 0.28)",
            line=dict(color="#2563eb", width=2.2),
            name="Readings",
            customdata=actual_str,
            hovertemplate="<b>%{theta}</b><br>Actual: %{customdata}<extra></extra>",
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 105],
                    tickfont=dict(size=12, color="#64748b", family="Inter, system-ui, sans-serif"),
                    tickvals=[20, 40, 60, 80, 100],
                    ticktext=["20", "40", "60", "80", "100"],
                    gridcolor="rgba(203, 213, 225, 0.8)",
                    gridwidth=0.5,
                    linecolor="#e2e8f0",
                    linewidth=0.8,
                ),
                angularaxis=dict(
                    tickfont=dict(size=13, color="#1e293b", family="Inter, system-ui, sans-serif"),
                    gridcolor="rgba(226, 232, 240, 0.9)",
                    gridwidth=0.5,
                    linecolor="#e2e8f0",
                ),
                bgcolor="#fafbfc",
            ),
            showlegend=False,
            height=420,
            margin=dict(l=115, r=115, t=45, b=45),
            paper_bgcolor="#ffffff",
            plot_bgcolor="#ffffff",
            font=dict(size=13, color="#1e293b", family="Inter, system-ui, sans-serif"),
            annotations=[
                dict(
                    text="Scale: 0 = min, 100 = max allowed (hover for actual values)",
                    x=0.5, y=-0.08,
                    xref="paper", yref="paper",
                    showarrow=False,
                    font=dict(size=11, color="#94a3b8"),
                    xanchor="center",
                ),
            ],
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("**Sensor readings (actual values)**")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"Engine RPM: **{int(engine_rpm)}** RPM")
            st.markdown(f"Oil pressure: **{lub_oil_pressure}** bar")
        with c2:
            st.markdown(f"Fuel pressure: **{fuel_pressure}** bar")
            st.markdown(f"Coolant pressure: **{coolant_pressure}** bar")
        with c3:
            st.markdown(f"Oil temp.: **{lub_oil_temp}** °C")
            st.markdown(f"Coolant temp.: **{coolant_temp}** °C")

        # Suggested focus: use final estimator (pipeline wraps scaler + clf; only clf has feature_importances_)
        clf = model[-1] if hasattr(model, "steps") else model
        if prediction == 1 and hasattr(clf, "feature_importances_"):
            imp = clf.feature_importances_
            idx_sorted = sorted(range(6), key=lambda i: imp[i], reverse=True)
            top_sensors = [sensor_labels[i] for i in idx_sorted[:3]]
            extreme = []
            for i in range(6):
                if pct[i] >= 85:
                    extreme.append(f"{sensor_labels[i]} (high: {raw[i]:.1f} {units[i]})")
                elif pct[i] <= 15:
                    extreme.append(f"{sensor_labels[i]} (low: {raw[i]:.1f} {units[i]})")
            st.markdown("---")
            st.markdown("#### 🔍 Suggested focus (Maintenance Required)")
            st.markdown("Sensors the model weighs most in this prediction:")
            st.markdown("**" + " → ".join(top_sensors) + "**")
            if extreme:
                st.markdown("Readings that are high or low in this run:")
                for e in extreme:
                    st.markdown(f"- {e}")

        with st.expander("📋 Inputs (saved as dataframe)"):
            st.dataframe(input_df, use_container_width=True)


if __name__ == "__main__":
    main()

