from __future__ import annotations

from math import comb, sqrt

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="PulseGrid | Probability Lab",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    :root {
        --navy: #071b3b;
        --cyan: #13b8c8;
        --ink: #102543;
        --line: #e4ebf4;
    }
    .stApp {
        background:
            radial-gradient(ellipse at 78% 0%, rgba(19,184,200,.10), transparent 32%),
            linear-gradient(180deg, #f6f9fd 0%, #eef3f9 100%);
        color: var(--ink);
    }
    [data-testid="stHeader"] { background: rgba(246,249,253,.72); }
    .block-container { max-width:1440px; padding-top:1.2rem; padding-bottom:3rem; }
    section[data-testid="stSidebar"] {
        background:linear-gradient(180deg,#071b3b 0%,#0b2d58 100%);
        border-right:1px solid rgba(255,255,255,.08);
    }
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color:#eaf3ff !important;
    }
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p { color:#a9bfd9 !important; }
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p { color:#edf5ff !important; }
    .brand-lockup { display:flex; align-items:center; gap:10px; margin:.35rem 0 1.35rem; }
    .brand-mark {
        width:34px; height:34px; border-radius:11px; display:grid; place-items:center;
        color:white; font-size:19px; font-weight:800;
        background:linear-gradient(135deg,#15c4d0,#3278c5);
        box-shadow:0 0 24px rgba(19,184,200,.35);
    }
    .brand-name { color:#f6fbff; font-weight:800; letter-spacing:.09em; font-size:.9rem; }
    .brand-sub { color:#9eb7d5; font-size:.68rem; letter-spacing:.14em; margin-top:2px; }
    .hero {
        position:relative; overflow:hidden; isolation:isolate;
        padding:2.1rem 2.3rem; border-radius:24px; margin-bottom:1.3rem;
        color:white; background:linear-gradient(112deg,#071b3b 0%,#103969 60%,#087c91 130%);
        box-shadow:0 18px 45px rgba(7,27,59,.17);
        animation:heroRise .65s cubic-bezier(.2,.75,.3,1) both;
    }
    .hero::before {
        content:""; position:absolute; z-index:-1; width:390px; height:390px; right:-62px; top:-228px;
        border-radius:50%; border:1px solid rgba(255,255,255,.15);
        box-shadow:0 0 0 28px rgba(255,255,255,.035),0 0 0 62px rgba(255,255,255,.025);
    }
    .hero::after {
        content:""; position:absolute; z-index:-1; width:210px; height:210px; right:16%; bottom:-184px;
        border-radius:50%; background:rgba(19,184,200,.25); filter:blur(22px);
    }
    .hero-topline { display:flex; align-items:center; gap:9px; color:#aeeaf0; font-size:.74rem; letter-spacing:.16em; text-transform:uppercase; font-weight:700; }
    .signal-dot { width:8px; height:8px; border-radius:50%; background:#41e1d4; box-shadow:0 0 0 0 rgba(65,225,212,.65); animation:signalPulse 1.8s infinite; }
    .hero h1 { color:#fff; font-size:clamp(2.2rem,4vw,3.6rem); line-height:1.02; letter-spacing:-.045em; margin:.75rem 0 .65rem; }
    .hero p { color:#d1e1f2; max-width:750px; font-size:1.04rem; line-height:1.6; margin:0; }
    .hero-meta { color:#a9c5de; font-size:.78rem; margin-top:1.15rem; letter-spacing:.04em; }
    @keyframes signalPulse { 0% { box-shadow:0 0 0 0 rgba(65,225,212,.65); } 70% { box-shadow:0 0 0 9px rgba(65,225,212,0); } 100% { box-shadow:0 0 0 0 rgba(65,225,212,0); } }
    @keyframes heroRise { from { opacity:0; transform:translateY(10px); } to { opacity:1; transform:translateY(0); } }
    div[data-testid="stMetric"] {
        background:#fff; border:1px solid var(--line); border-radius:16px; padding:15px 17px;
        box-shadow:0 6px 20px rgba(17,43,78,.045); animation:heroRise .45s ease both;
    }
    div[data-testid="stMetricLabel"] { color:#657991; font-weight:600; }
    div[data-testid="stMetricValue"] { color:#0b2851; }
    .stTabs [data-baseweb="tab-list"] { gap:.38rem; border-bottom:1px solid #dce5f0; }
    .stTabs [data-baseweb="tab"] {
        background:#e8eef6; border-radius:12px 12px 0 0; padding:.65rem 1rem;
        color:#38536f; border-bottom:2px solid transparent; font-weight:650;
    }
    .stTabs [aria-selected="true"] { background:#fff; color:#0b2851; border-bottom-color:#12b8c8; }
    .stTabs [data-baseweb="tab-panel"] { padding-top:1.15rem; }
    h2, h3 { color:#0d2a50; letter-spacing:-.02em; }
    div[data-testid="stAlert"] { border-radius:14px; }
    div[data-testid="stDataFrame"] { border:1px solid #e4ebf4; border-radius:14px; overflow:hidden; }
    .small-caps { color:#66809b; font-size:.72rem; font-weight:750; letter-spacing:.14em; text-transform:uppercase; }
    .formula-card {
        min-height:100px; padding:1rem 1.15rem; margin:.25rem 0 .75rem;
        border:1px solid #e2eaf4; border-radius:16px; background:#fff;
        box-shadow:0 5px 18px rgba(17,43,78,.035);
    }
    .formula-card h3 { font-size:1rem; margin:0 0 .35rem; color:#163a63; }
    .formula-card p { color:#657991; margin:0; font-size:.9rem; line-height:1.5; }
    .footnote { color:#6c7e94; font-size:.82rem; line-height:1.55; }
    @media (max-width:700px) {
        .hero { padding:1.5rem; border-radius:19px; }
        .hero p { font-size:.94rem; }
        .block-container { padding-left:1rem; padding-right:1rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def binomial_probability(total_nodes: int, overloaded_nodes: int, probability: float) -> float:
    """Probability that exactly overloaded_nodes out of total_nodes overload."""
    return comb(total_nodes, overloaded_nodes) * probability**overloaded_nodes * (1 - probability) ** (
        total_nodes - overloaded_nodes
    )


def chart_layout(fig: go.Figure, height: int = 360) -> go.Figure:
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=12, r=12, t=45, b=15),
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        font=dict(family="Inter, Segoe UI, sans-serif", color="#304764"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        hoverlabel=dict(bgcolor="#0b2851", font_color="white"),
    )
    fig.update_xaxes(showgrid=False, linecolor="#dce5f0", zeroline=False)
    fig.update_yaxes(gridcolor="#e9eef5", zeroline=False)
    return fig


with st.sidebar:
    st.markdown(
        """
        <div class="brand-lockup">
          <div class="brand-mark">∿</div>
          <div><div class="brand-name">PULSEGRID</div><div class="brand-sub">PROBABILITY LAB</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("### Mission controls")
    node_count = st.slider("Server nodes (n)", min_value=2, max_value=20, value=8, step=1)
    overload_rate = st.slider(
        "Overload chance per node (p)", min_value=0.01, max_value=0.50, value=0.12, step=0.01, format="%.2f"
    )
    exact_count = st.slider("Exact overloaded nodes (m)", min_value=0, max_value=node_count, value=min(2, node_count))
    simulation_rounds = st.slider(
        "Simulated minutes", min_value=100, max_value=100_000, value=20_000, step=100, format="%d"
    )
    st.markdown("---")
    st.caption("Adjust the model, then move through the four tabs. Every result uses these settings.")
    st.markdown(
        '<div class="footnote">Model: each node has the same overload chance, and node events are independent.</div>',
        unsafe_allow_html=True,
    )


st.markdown(
    """
    <div class="hero">
      <div class="hero-topline"><span class="signal-dot"></span> Live model · interactive systems lab</div>
      <h1>PulseGrid</h1>
      <p>Can a server cluster stay online when traffic spikes? Explore the odds, simulate thousands of minutes, and see probability theory become a reliability tool.</p>
      <div class="hero-meta">INDIVIDUAL PROJECT &nbsp;·&nbsp; MAKHMETOV ALIKHAN &nbsp;·&nbsp; PROBABILITY IN ACTION</div>
    </div>
    """,
    unsafe_allow_html=True,
)

tab_combinatorics, tab_simulation, tab_events, tab_formulas = st.tabs(
    ["01  Combinatorics", "02  Simulation", "03  Events", "04  Formula deck"]
)


with tab_combinatorics:
    st.markdown('<div class="small-caps">Pattern space</div>', unsafe_allow_html=True)
    st.subheader("How many ways can a cluster overload?")
    st.write(
        "Treat each server as a node that can overload during one minute. "
        "The combination count tells us how many different failure patterns contain exactly the selected number of overloaded nodes."
    )

    exact_probability = binomial_probability(node_count, exact_count, overload_rate)
    all_nodes_probability = overload_rate**node_count
    pattern_count = comb(node_count, exact_count)

    metric_a, metric_b, metric_c = st.columns(3)
    metric_a.metric(f"Patterns with exactly {exact_count} overloads", f"{pattern_count:,}")
    metric_b.metric(f"P(exactly {exact_count})", f"{exact_probability:.2%}")
    metric_c.metric("P(full-cluster overload)", f"{all_nodes_probability:.6%}")

    st.latex(r"\Pr(X=m)=\binom{n}{m}p^m(1-p)^{n-m}")
    st.caption(
        f"With n = {node_count}, m = {exact_count}, and p = {overload_rate:.0%}, "
        f"there are {pattern_count:,} distinct patterns that produce this outcome."
    )

    outcomes = list(range(node_count + 1))
    probabilities = [binomial_probability(node_count, r, overload_rate) for r in outcomes]
    ways = [comb(node_count, r) for r in outcomes]
    probability_colors = ["#13b8c8" if r == exact_count else "#7da9d2" for r in outcomes]
    pattern_colors = ["#13b8c8" if r == exact_count else "#9bb3ce" for r in outcomes]

    left_chart, right_chart = st.columns(2)
    with left_chart:
        probability_fig = go.Figure(
            go.Bar(
                x=outcomes,
                y=probabilities,
                marker_color=probability_colors,
                hovertemplate="Overloaded nodes: %{x}<br>Probability: %{y:.2%}<extra></extra>",
            )
        )
        probability_fig.update_layout(title="Probability of each overload count", xaxis_title="Overloaded nodes", yaxis_title="Probability")
        probability_fig.update_yaxes(tickformat=".0%")
        st.plotly_chart(chart_layout(probability_fig), use_container_width=True, config={"displayModeBar": False})
    with right_chart:
        patterns_fig = go.Figure(
            go.Bar(
                x=outcomes,
                y=ways,
                marker_color=pattern_colors,
                hovertemplate="Overloaded nodes: %{x}<br>Distinct patterns: %{y:,}<extra></extra>",
            )
        )
        patterns_fig.update_layout(title="Distinct patterns for each count", xaxis_title="Overloaded nodes", yaxis_title="Number of patterns")
        st.plotly_chart(chart_layout(patterns_fig), use_container_width=True, config={"displayModeBar": False})

    distribution = pd.DataFrame(
        {
            "Overloaded nodes (r)": outcomes,
            "Distinct patterns C(n, r)": ways,
            "Model probability": probabilities,
        }
    )
    st.markdown("#### Outcome table")
    st.dataframe(
        distribution.style.format({"Model probability": "{:.2%}"}),
        use_container_width=True,
        hide_index=True,
    )
    st.markdown(
        '<div class="footnote">A full-cluster overload is the extreme-case outage: every server node overloads at once.</div>',
        unsafe_allow_html=True,
    )


with tab_simulation:
    st.markdown('<div class="small-caps">Hypothesis → experiment → interpretation</div>', unsafe_allow_html=True)
    st.subheader("Let the model play out")
    mean_theory = node_count * overload_rate
    sd_theory = sqrt(node_count * overload_rate * (1 - overload_rate))
    st.info(
        f"Prediction: over {simulation_rounds:,} simulated minutes, the average should settle near "
        f"{mean_theory:.2f} overloaded nodes per minute. Each minute is one independent trial."
    )

    refresh_simulation = st.button("Run a fresh simulation", type="primary")
    simulation_key = (node_count, round(overload_rate, 4), simulation_rounds)
    if (
        refresh_simulation
        or st.session_state.get("simulation_key") != simulation_key
        or "simulation_samples" not in st.session_state
    ):
        rng = np.random.default_rng()
        st.session_state["simulation_samples"] = rng.binomial(node_count, overload_rate, size=simulation_rounds)
        st.session_state["simulation_key"] = simulation_key

    samples = st.session_state["simulation_samples"]
    observed_mean = float(np.mean(samples))
    observed_median = float(np.median(samples))
    observed_sd = float(np.std(samples))
    metric_mean, metric_median, metric_sd = st.columns(3)
    metric_mean.metric("Observed mean", f"{observed_mean:.2f}", f"{observed_mean - mean_theory:+.2f} vs theory")
    metric_median.metric("Observed median", f"{observed_median:g}", "overloaded nodes")
    metric_sd.metric("Observed standard deviation", f"{observed_sd:.2f}", f"{observed_sd - sd_theory:+.2f} vs theory")

    observed_counts = np.bincount(samples, minlength=node_count + 1)
    observed_shares = observed_counts / simulation_rounds
    model_shares = [binomial_probability(node_count, r, overload_rate) for r in outcomes]
    comparison_fig = go.Figure()
    comparison_fig.add_trace(
        go.Bar(
            name="Simulation",
            x=outcomes,
            y=observed_shares,
            marker_color="#13b8c8",
            opacity=0.82,
            hovertemplate="Overloaded nodes: %{x}<br>Observed: %{y:.2%}<extra></extra>",
        )
    )
    comparison_fig.add_trace(
        go.Scatter(
            name="Theory",
            x=outcomes,
            y=model_shares,
            mode="lines+markers",
            line=dict(color="#123d70", width=3),
            marker=dict(size=7, color="#123d70"),
            hovertemplate="Overloaded nodes: %{x}<br>Theory: %{y:.2%}<extra></extra>",
        )
    )
    comparison_fig.update_layout(title="Simulated frequency vs. theoretical probability", barmode="overlay", xaxis_title="Overloaded nodes", yaxis_title="Share of minutes")
    comparison_fig.update_yaxes(tickformat=".0%")
    st.plotly_chart(chart_layout(comparison_fig, height=410), use_container_width=True, config={"displayModeBar": False})

    observed_percent = observed_shares * 100
    theoretical_percent = np.array(model_shares) * 100
    comparison = pd.DataFrame(
        {
            "Overloaded nodes": outcomes,
            "Observed minutes": observed_counts,
            "Observed share": observed_percent,
            "Theoretical share": theoretical_percent,
            "Gap (percentage points)": observed_percent - theoretical_percent,
        }
    )
    st.markdown("#### Frequency table")
    st.dataframe(
        comparison.style.format(
            {
                "Observed share": "{:.2f}%",
                "Theoretical share": "{:.2f}%",
                "Gap (percentage points)": "{:+.2f}",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )
    st.caption(
        "Interpretation: observed bars will not match the theory perfectly in a finite run. "
        "As the number of simulated minutes grows, the frequencies usually move closer to the model."
    )


with tab_events:
    st.markdown('<div class="small-caps">Conditional probability & independence</div>', unsafe_allow_html=True)
    st.subheader("What changes after an overload is observed?")
    at_least_one_probability = 1 - (1 - overload_rate) ** node_count
    selected_probability = binomial_probability(node_count, exact_count, overload_rate)
    conditional_probability = (
        selected_probability / at_least_one_probability if exact_count >= 1 and at_least_one_probability > 0 else 0.0
    )
    two_minute_probability = at_least_one_probability**2

    event_left, event_right = st.columns(2)
    with event_left:
        st.markdown("### The clue: at least one node is overloaded")
        st.write(
            f"Let A mean “one or more nodes overload,” and B mean “exactly {exact_count} nodes overload.” "
            "For m ≥ 1, B is contained inside A, so the conditional probability is the exact-count probability divided by the chance of any overload."
        )
        st.latex(r"\Pr(A)=1-(1-p)^n")
        st.latex(r"\Pr(B\mid A)=\frac{\Pr(B)}{\Pr(A)}\quad (m\geq1)")
        st.metric("P(at least one overload)", f"{at_least_one_probability:.2%}")
        st.metric(f"P(exactly {exact_count} | at least one)", f"{conditional_probability:.2%}")
        if exact_count == 0:
            st.caption("Because zero overloads cannot happen after event A has occurred, this conditional probability is 0.")
    with event_right:
        st.markdown("### Two independent minutes")
        st.write(
            "Assume each minute starts fresh and overloads in one minute do not affect the next. "
            "Knowing that minute 1 had an overload does not change the risk in minute 2."
        )
        st.latex(r"\Pr(A_1\cap A_2)=\Pr(A_1)\Pr(A_2)")
        st.metric("P(overload in both minutes)", f"{two_minute_probability:.2%}")
        st.metric("P(minute 2 overloads | minute 1 did)", f"{at_least_one_probability:.2%}")

    st.markdown("---")
    st.markdown("#### Independence in one line")
    st.latex(r"\Pr(E\cap F)=\Pr(E)\Pr(F)\quad\text{when }E\text{ and }F\text{ are independent}")
    st.caption(
        "The two-minute result depends on the independence assumption. In a real system, one bad minute may overload queues and make the next minute riskier."
    )


with tab_formulas:
    st.markdown('<div class="small-caps">Defense-ready reference</div>', unsafe_allow_html=True)
    st.subheader("Formula deck")
    st.write("The full set of probability ideas used in PulseGrid, with each symbol tied to the server-cluster model.")

    formula_rows = [
        (
            "Combinations",
            r"\binom{n}{m}=\frac{n!}{m!(n-m)!}",
            "Counts the distinct ways to choose which m of the n nodes overload.",
        ),
        (
            "Binomial probability",
            r"\Pr(X=m)=\binom{n}{m}p^m(1-p)^{n-m}",
            "Probability that exactly m nodes overload when every node has chance p.",
        ),
        (
            "At least one overload",
            r"\Pr(X\geq1)=1-(1-p)^n",
            "Use the complement: subtract the chance that no nodes overload.",
        ),
        (
            "Expected count and spread",
            r"\mathbb{E}[X]=np,\qquad \operatorname{Var}(X)=np(1-p),\qquad \sigma=\sqrt{np(1-p)}",
            "Predicts the average number of overloaded nodes and the model's standard deviation.",
        ),
        (
            "Conditional probability",
            r"\Pr(B\mid A)=\frac{\Pr(A\cap B)}{\Pr(A)}",
            "Updates a probability after new information A is known.",
        ),
        (
            "Independent events",
            r"\Pr(A\cap B)=\Pr(A)\Pr(B)",
            "The probability that both events occur when neither changes the chance of the other.",
        ),
        (
            "Empirical frequency",
            r"\widehat{\Pr}(E)=\frac{\text{number of simulated trials where }E\text{ occurs}}{\text{total trials}}",
            "Estimates a probability from the simulation by counting observed outcomes.",
        ),
    ]

    for offset in range(0, len(formula_rows), 2):
        cols = st.columns(2)
        for col, (title, equation, explanation) in zip(cols, formula_rows[offset : offset + 2]):
            with col:
                st.markdown(f'<div class="formula-card"><h3>{title}</h3><p>{explanation}</p></div>', unsafe_allow_html=True)
                st.latex(equation)

    st.markdown("---")
    st.markdown("#### Symbol key")
    symbol_table = pd.DataFrame(
        [
            ("n", str(node_count), "Total number of server nodes"),
            ("m", str(exact_count), "Selected exact number of overloaded nodes"),
            ("p", f"{overload_rate:.0%}", "Overload probability for one node in one minute"),
            ("X", "0, 1, …, n", "Random variable: overloaded-node count in one minute"),
            ("A", "X ≥ 1", "Event that at least one node overloads"),
        ],
        columns=["Symbol", "Current value", "Meaning"],
    )
    st.dataframe(symbol_table, use_container_width=True, hide_index=True)
    st.markdown(
        '<div class="footnote">Assumptions: identical per-node overload chance, independent nodes, and independent minutes. '
        "These let the model stay clear enough to explore, while making its limits visible.</div>",
        unsafe_allow_html=True,
    )

st.markdown("---")
st.markdown(
    '<div class="footnote">PulseGrid · Theory of Probability · Individual project by Makhmetov Alikhan</div>',
    unsafe_allow_html=True,
)

