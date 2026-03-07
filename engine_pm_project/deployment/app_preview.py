"""
Preview-only UI: same layout as app.py, no Hugging Face model required.
Run: streamlit run engine_pm_project/deployment/app_preview.py
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.ensemble import GradientBoostingClassifier

# Must be the very first Streamlit command (no st.* or @st.* above this)
st.set_page_config(
    page_title="Engine Predictive Maintenance",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded",
)

FEATURES = [
    "Engine_RPM", "Lub_Oil_Pressure", "Fuel_Pressure",
    "Coolant_Pressure", "Lub_Oil_Temperature", "Coolant_Temperature",
]

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 50%, #3d7ab5 100%);
        padding: 1.5rem 1.5rem 1.8rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 14px rgba(0,0,0,0.15);
    }
    .main-header h1 { color: white !important; font-size: 1.85rem !important; font-weight: 700 !important; margin-bottom: 0.3rem !important; }
    .main-header p { color: rgba(255,255,255,0.9) !important; font-size: 1rem !important; margin: 0 !important; }
    .sensor-card { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 1.25rem; margin-bottom: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
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
    .prob-bar { height: 12px; background: #e2e8f0; border-radius: 6px; overflow: hidden; margin: 0.8rem 0; }
    .prob-fill { height: 100%; border-radius: 6px; transition: width 0.5s ease; }
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
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_dummy_model():
    clf = GradientBoostingClassifier(n_estimators=10, max_depth=3, random_state=42)
    X_dummy = np.random.RandomState(42).rand(100, 6) * 100
    y_dummy = (X_dummy[:, 0] + X_dummy[:, 4] > 120).astype(int)
    clf.fit(X_dummy, y_dummy)
    return clf


def main():
    with st.sidebar:
        st.markdown("### 🔧 About")
        st.markdown("Predict **engine condition** from six sensor readings. The model was trained on engine maintenance data.")
        st.markdown("---")
        st.markdown("**Sensors:** RPM, pressures (oil, fuel, coolant), temperatures (oil & coolant).")
        st.markdown("---")
        st.caption("Preview mode — local dummy model (same UI as HF Space)")

    st.markdown("""
    <div class="main-header">
        <h1>🔧 Engine Predictive Maintenance</h1>
        <p>Enter sensor readings below — get a Normal or Maintenance Required prediction</p>
    </div>
    """, unsafe_allow_html=True)

    model = load_dummy_model()

    st.markdown("#### 📊 Sensor inputs")
    with st.form("sensor_inputs"):
        c1, c2 = st.columns(2)
        with c1:
            engine_rpm = st.number_input("Engine RPM", min_value=0, max_value=5000, value=700, help="Revolutions per minute")
            lub_oil_pressure = st.number_input("Lubricating oil pressure (bar)", min_value=0.0, max_value=15.0, value=3.0, step=0.1)
            fuel_pressure = st.number_input("Fuel pressure (bar)", min_value=0.0, max_value=25.0, value=6.0, step=0.1)
        with c2:
            coolant_pressure = st.number_input("Coolant pressure (bar)", min_value=0.0, max_value=10.0, value=2.5, step=0.1)
            lub_oil_temp = st.number_input("Lubricating oil temperature (°C)", min_value=50.0, max_value=120.0, value=77.0, step=0.5)
            coolant_temp = st.number_input("Coolant temperature (°C)", min_value=50.0, max_value=200.0, value=78.0, step=0.5)
        submitted = st.form_submit_button("🚀 Get prediction")

    input_df = pd.DataFrame([{
        "Engine_RPM": engine_rpm,
        "Lub_Oil_Pressure": lub_oil_pressure,
        "Fuel_Pressure": fuel_pressure,
        "Coolant_Pressure": coolant_pressure,
        "Lub_Oil_Temperature": lub_oil_temp,
        "Coolant_Temperature": coolant_temp,
    }])

    if submitted:
        prediction = model.predict(input_df[FEATURES])[0]
        proba = model.predict_proba(input_df[FEATURES])[0]
        prob_maintenance = float(proba[1])
        label = "Maintenance Required" if prediction == 1 else "Normal"

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

        st.markdown("**Probability (Maintenance)**")
        fill_color = "#f59e0b" if prob_maintenance > 0.5 else "#10b981"
        st.markdown(f"""
        <div class="prob-bar">
            <div class="prob-fill" style="width: {prob_maintenance * 100:.0f}%; background: {fill_color};"></div>
        </div>
        """, unsafe_allow_html=True)
        st.metric("", f"{prob_maintenance:.1%}")

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

        if prediction == 1 and hasattr(model, "feature_importances_"):
            imp = model.feature_importances_
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
