import streamlit as st
import numpy as np

st.title("Mixed-Risk Insurance Claims Simulator")

# --- Interactive controls (sidebar) ---
st.sidebar.header("Parameters")
n = st.sidebar.slider("Number of policyholders", 1_000, 1_000_000, 100_000, step=1_000)
pct_high_risk = st.sidebar.slider("% high-risk", 0.0, 1.0, 0.30, step=0.01)
mean_low = st.sidebar.slider("Low-risk mean claim", 0.1, 10.0, 1.0)
mean_high = st.sidebar.slider("High-risk mean claim", 0.1, 20.0, 5.0)
threshold = st.sidebar.slider("Claim threshold for Bayes' calc", 0.0, 20.0, 3.0)
seed = st.sidebar.number_input("Random seed", value=42)

# --- Simulation ---
np.random.seed(seed)
is_high_risk = np.random.rand(n) < pct_high_risk
claims = np.where(
    is_high_risk,
    np.random.exponential(scale=mean_high, size=n),
    np.random.exponential(scale=mean_low, size=n)
)

# --- Results ---
st.subheader("Results")
col1, col2 = st.columns(2)
col1.metric("Simulated mean claim", f"{claims.mean():.3f}")
col2.metric("Simulated variance", f"{claims.var():.3f}")

mask = claims > threshold
if mask.sum() > 0:
    p_high_given_large = is_high_risk[mask].mean()
    st.metric(f"P(high-risk | claim > {threshold})", f"{p_high_given_large:.3f}")
else:
    st.write("No claims exceeded that threshold — try lowering it.")

# --- Visualization ---
st.subheader("Claims distribution")
st.bar_chart(np.histogram(claims, bins=50)[0])