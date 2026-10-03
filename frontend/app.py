import streamlit as st
import requests
import pandas as pd
from pathlib import Path
import pickle
import html

import altair as alt


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Customer Persona Segmenter",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# THEME
# ============================================================

THEME_CSS = """
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg:           #0a0a0a;
    --card:         #171717;
    --card-raised:  #1c1c1c;
    --fg:           #fafafa;
    --fg-soft:      #d4d4d8;
    --muted:        #a1a1aa;
    --faint:        #71717a;
    --green:        #22c55e;
    --green-hover:  #4ade80;
    --green-ink:    #052e16;
    --green-text:   #86efac;
    --green-tint:   rgba(34, 197, 94, 0.12);
    --green-line:   rgba(34, 197, 94, 0.35);
    --line:         rgba(255, 255, 255, 0.08);
    --line-strong:  rgba(255, 255, 255, 0.16);
    --shadow:       0 18px 44px rgba(0, 0, 0, 0.45);
}

/* ---------------- Background ---------------- */

.stApp {
    background-color: var(--bg);
    background-image:
        radial-gradient(900px 500px at 50% -12%, rgba(255, 255, 255, 0.035), transparent 60%);
    color: var(--fg);
}

[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu, footer {
    visibility: hidden;
}

/* hide the little link icon Streamlit adds next to headings */
[data-testid="stHeaderActionElements"] {
    display: none;
}

.block-container {
    padding-top: 4.2rem;
    padding-bottom: 4rem;
    max-width: 1280px;
}

html {
    scroll-behavior: smooth;
}

/* ---------------- Type ---------------- */

.stApp, .stApp p, .stApp li, .stApp label, .stApp input,
.stApp textarea, .stApp button, .stMarkdown {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

span[data-testid="stIconMaterial"] {
    font-family: "Material Symbols Rounded" !important;
}

.stApp h1, .stApp h2, .stApp h3, .stApp h4 {
    font-family: 'Inter', sans-serif;
    color: var(--fg);
    letter-spacing: -0.025em;
}

.stApp h1 {
    font-size: 2.4rem;
    font-weight: 800;
    line-height: 1.12;
}

.stApp h2 {
    font-size: 1.6rem;
    font-weight: 700;
    margin-top: 0.4rem;
}

.stApp h3 {
    font-size: 1.15rem;
    font-weight: 600;
}

.stApp h4 {
    font-size: 1rem;
    font-weight: 600;
}

.stApp p, .stApp li {
    color: var(--muted);
    line-height: 1.65;
}

.stApp strong {
    color: var(--fg);
    font-weight: 600;
}

[data-testid="stCaptionContainer"] p {
    color: var(--faint);
}

hr {
    border-color: var(--line);
    margin: 2.4rem 0;
}

a:focus-visible, button:focus-visible {
    outline: 2px solid var(--green);
    outline-offset: 2px;
}

/* ---------------- Top navigation ---------------- */

.stApp .topnav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding: 0.55rem 0 0.95rem 0;
    border-bottom: 1px solid var(--line);
    margin-bottom: 2.6rem;
}

.stApp .topnav .brand {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-weight: 700;
    font-size: 0.95rem;
    color: var(--fg);
}

.stApp .topnav .brand-mark {
    display: grid;
    place-items: center;
    width: 26px;
    height: 26px;
    border: 1px solid var(--line-strong);
    border-radius: 7px;
    color: var(--green);
    font-size: 0.8rem;
}

.stApp .topnav .links {
    display: flex;
    gap: 1.7rem;
}

.stApp .topnav a {
    color: var(--muted);
    text-decoration: none;
    font-size: 0.85rem;
    font-weight: 500;
    transition: color 0.15s ease;
}

.stApp .topnav a:hover {
    color: var(--fg);
}

.stApp .topnav a.nav-cta {
    color: var(--fg);
    background: var(--card);
    border: 1px solid var(--line-strong);
    border-radius: 8px;
    padding: 0.4rem 0.95rem;
}

.stApp .topnav a.nav-cta:hover {
    border-color: var(--green-line);
    background: var(--green-tint);
}

/* ---------------- Hero ---------------- */

.stApp .hero {
    position: relative;
    display: grid;
    grid-template-columns: 1fr 1.05fr;
    gap: 2.5rem;
    align-items: center;
    padding: 0.5rem 0 2.5rem 0;
}

.stApp .hero::before {
    content: "";
    position: absolute;
    inset: -140px 0;
    background: radial-gradient(
        ellipse 40% 50% at 66% 50%,
        rgba(34, 197, 94, 0.17),
        transparent 100%
    );
    pointer-events: none;
}

.stApp .hero > * {
    position: relative;
}

.stApp .hero-title {
    font-size: clamp(2.3rem, 4.4vw, 3.6rem);
    font-weight: 800;
    line-height: 1.08;
    letter-spacing: -0.035em;
    color: var(--fg);
}

.stApp .g-pink,
.stApp .g-cyan {
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    -webkit-text-fill-color: transparent;
}

.stApp .g-pink {
    background-image: linear-gradient(90deg, #f472b6, #c084fc);
}

.stApp .g-cyan {
    background-image: linear-gradient(90deg, #22d3ee, #38bdf8);
}

.stApp .hero .lede {
    max-width: 44ch;
    font-size: 1.02rem;
    line-height: 1.65;
    color: var(--muted);
    margin: 1.1rem 0 1.7rem 0;
}

.stApp .hero .lede strong {
    color: var(--fg);
}

.stApp .hero-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 0.8rem;
}

.stApp a.btn-primary,
.stApp a.btn-ghost {
    display: inline-block;
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 600;
    padding: 0.7rem 1.5rem;
    border-radius: 8px;
    transition: background 0.15s ease, border-color 0.15s ease;
}

.stApp a.btn-primary {
    background: var(--green);
    color: var(--green-ink);
    border: 1px solid var(--green);
}

.stApp a.btn-primary:hover {
    background: var(--green-hover);
    border-color: var(--green-hover);
}

.stApp a.btn-ghost {
    background: transparent;
    color: var(--fg);
    border: 1px solid var(--line-strong);
}

.stApp a.btn-ghost:hover {
    border-color: var(--green-line);
    background: var(--green-tint);
}

/* hero cards */

.stApp .hero-cards {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    align-items: start;
}

.stApp .hcard {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 1.1rem 1.2rem;
    box-shadow: var(--shadow);
}

.stApp .hc-tall {
    grid-row: 1 / span 2;
    margin-top: 2.2rem;
}

.stApp .hc-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.6rem;
}

.stApp .hc-title {
    font-size: 1rem;
    font-weight: 600;
    color: var(--fg);
    line-height: 1.3;
}

.stApp .pill {
    flex-shrink: 0;
    background: var(--green-tint);
    color: var(--green-text);
    border-radius: 999px;
    padding: 0.15rem 0.65rem;
    font-size: 0.72rem;
    font-weight: 600;
}

.stApp .hc-big {
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: var(--fg);
    margin-top: 0.5rem;
}

.stApp .hc-big span {
    font-size: 0.85rem;
    font-weight: 400;
    letter-spacing: 0;
    color: var(--faint);
    margin-left: 0.25rem;
}

.stApp .hc-desc {
    font-size: 0.84rem;
    line-height: 1.55;
    color: var(--muted);
    margin: 0.45rem 0 0.9rem 0;
}

.stApp .hc-bar {
    height: 8px;
    background: #262626;
    border-radius: 999px;
    overflow: hidden;
}

.stApp .hc-bar div {
    height: 100%;
    background: var(--green);
    border-radius: 999px;
}

.stApp .hc-list {
    list-style: none;
    padding: 0;
    margin: 1rem 0 0 0;
}

.stApp .hc-list li {
    display: flex;
    align-items: baseline;
    gap: 0.6rem;
    padding: 0.35rem 0;
    font-size: 0.86rem;
    line-height: 1.4;
    color: var(--fg-soft);
}

.stApp .hc-list li::before {
    content: "✓";
    color: var(--green);
    font-weight: 700;
}

.stApp .hc-list li span {
    margin-left: auto;
    color: var(--faint);
    font-variant-numeric: tabular-nums;
}

.stApp .hc-row {
    display: flex;
    align-items: center;
    gap: 0.85rem;
}

.stApp .hc-icon {
    flex-shrink: 0;
    display: grid;
    place-items: center;
    width: 44px;
    height: 44px;
    border-radius: 10px;
    background: var(--green-tint);
    border: 1px solid var(--green-line);
    color: var(--green);
    font-weight: 700;
    font-size: 1.05rem;
}

.stApp .hc-row .hc-desc {
    margin: 0.15rem 0 0 0;
}

/* ---------------- Cards (containers marked with span.glass) ---------------- */

div[data-testid="stVerticalBlockBorderWrapper"]:has(span.glass) {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 14px;
    box-shadow: var(--shadow);
}

/* ---------------- Buttons ---------------- */

.stButton > button {
    background: var(--green);
    color: var(--green-ink);
    border: 1px solid var(--green);
    border-radius: 8px;
    font-weight: 600;
    padding: 0.6rem 1.1rem;
    transition: background 0.15s ease, border-color 0.15s ease;
}

.stButton > button:hover,
.stButton > button:focus:not(:active) {
    background: var(--green-hover);
    border-color: var(--green-hover);
    color: var(--green-ink);
}

.stButton > button:active {
    background: var(--green);
    color: var(--green-ink);
}

.stButton > button p,
.stDownloadButton > button p {
    color: inherit;
    font-weight: 600;
}

.stDownloadButton > button {
    background: var(--bg);
    color: var(--fg);
    border: 1px solid var(--line-strong);
    border-radius: 8px;
    font-weight: 600;
    padding: 0.6rem 1.1rem;
    transition: background 0.15s ease, border-color 0.15s ease;
}

.stDownloadButton > button:hover,
.stDownloadButton > button:focus:not(:active) {
    background: var(--green-tint);
    border-color: var(--green-line);
    color: var(--green-text);
}

/* ---------------- Inputs ---------------- */

div[data-baseweb="input"],
div[data-baseweb="base-input"],
div[data-baseweb="select"] > div {
    background-color: var(--card);
    border-color: var(--line-strong);
    border-radius: 8px;
}

div[data-baseweb="input"]:focus-within,
div[data-baseweb="select"]:focus-within > div {
    border-color: var(--green);
}

span[data-baseweb="tag"] {
    background-color: var(--green-tint);
    border: 1px solid var(--green-line);
    border-radius: 6px;
    color: var(--green-text);
}

span[data-baseweb="tag"] span {
    color: var(--green-text);
}

[data-testid="stFileUploaderDropzone"] {
    background: var(--card);
    border: 1px dashed var(--line-strong);
    border-radius: 12px;
}

[data-testid="stFileUploaderDropzone"]:hover {
    border-color: var(--green-line);
}

/* ---------------- Alerts ---------------- */

div[data-testid="stAlertContainer"] {
    border-radius: 10px;
    border: 1px solid var(--line);
}

/* ---------------- Tables, charts, expander ---------------- */

[data-testid="stDataFrame"] {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 12px;
    overflow: hidden;
}

[data-testid="stExpander"] {
    background: transparent;
    border: none;
}

[data-testid="stExpander"] details {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 12px;
}

[data-testid="stExpander"] summary:hover {
    color: var(--green-text);
}

[data-testid="stVegaLiteChart"] {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 1.1rem;
}

/* ---------------- Sidebar ---------------- */

[data-testid="stSidebar"] {
    background: var(--bg);
    border-right: 1px solid var(--line);
}

[data-testid="stSidebar"] h1 {
    font-size: 1.25rem;
    font-weight: 700;
}

[data-testid="stSidebar"] h3 {
    font-size: 0.92rem;
    font-weight: 600;
    color: var(--green-text);
}

[data-testid="stSidebar"] li {
    font-size: 0.88rem;
}

/* ---------------- Metric cards ---------------- */

[data-testid="stMetric"] {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 0.85rem 1.1rem;
}

[data-testid="stMetricLabel"] p {
    color: var(--muted);
    font-size: 0.84rem;
}

[data-testid="stMetricValue"] {
    color: var(--fg);
    font-weight: 700;
}

/* ---------------- Responsive ---------------- */

@media (max-width: 900px) {
    .stApp .hero {
        grid-template-columns: 1fr;
    }
    .stApp .hero-cards {
        grid-template-columns: 1fr;
    }
    .stApp .hc-tall {
        grid-row: auto;
        margin-top: 0;
    }
    .stApp .topnav .links {
        display: none;
    }
}

/* ---------------- Motion preference ---------------- */

@media (prefers-reduced-motion: reduce) {
    * { transition: none !important; scroll-behavior: auto !important; }
}

</style>
"""

st.markdown(THEME_CSS, unsafe_allow_html=True)


def glass_card():
    """Marks the enclosing st.container(border=True) as a frosted card."""
    st.markdown("<span class='glass'></span>", unsafe_allow_html=True)


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = "http://127.0.0.1:8000"
GREEN = "#22c55e"


# ============================================================
# PERSONA DESCRIPTIONS
# ============================================================

PERSONA_DESCRIPTIONS = {
    "High-Value Customers":
        "Customers with relatively high income and high spending scores.",

    "High-Spending Budget Customers":
        "Customers with relatively lower income but high spending scores.",

    "Low-Spending High-Income Customers":
        "Customers with relatively high income but low spending scores."
}


PERSONA_PROFILES = [
    (
        "High-Value Customers",
        "High-Value Customers",
        "High income paired with high spending. This segment combines stronger income and spending levels."
    ),
    (
        "High-Spending Budget Customers",
        "High-Spending Budget Customers",
        "Relatively lower income with high spending scores, indicating strong spending activity within this income range."
    ),
    (
        "Low-Spending High-Income",
        "Low-Spending High-Income Customers",
        "Relatively high income with lower spending scores, indicating a different income-to-spending pattern."
    )
]


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "segmented_customers.csv"

# ============================================================
# LOAD MODEL EVALUATION RESULTS
# ============================================================

EVALUATION_PATH = BASE_DIR / "models" / "model_evaluation.pkl"

try:
    with open(EVALUATION_PATH, "rb") as file:
        evaluation_data = pickle.load(file)

    k_values = evaluation_data["k_values"]
    inertia_values = evaluation_data["inertia"]
    silhouette_values = evaluation_data["silhouette_scores"]
    optimal_k = evaluation_data["optimal_k"]
    selected_silhouette_score = evaluation_data["selected_silhouette_score"]

except Exception as e:
    st.warning(f"Model evaluation data could not be loaded: {e}")
    evaluation_data = None


# ============================================================
# LOAD DATASET
# ============================================================

try:
    df = pd.read_csv(DATA_PATH)

except FileNotFoundError:
    st.error(
        "segmented_customers.csv is missing. "
        "Add the file to the data folder, then reload this page."
    )
    st.stop()


# ============================================================
# DATA VALIDATION
# ============================================================

required_columns = [
    "annual_income_k",
    "spending_score",
    "persona"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(
        "The dataset is missing required columns: "
        + ", ".join(missing_columns)
    )
    st.stop()


# ============================================================
# BASE ANALYTICS
# ============================================================

total_customers = len(df)
number_of_personas = df["persona"].nunique()
average_income = df["annual_income_k"].mean()
average_spending = df["spending_score"].mean()

correlation = df[
    ["annual_income_k", "spending_score"]
].corr().iloc[0, 1]

persona_counts = (
    df["persona"]
    .value_counts()
    .rename_axis("Persona")
    .reset_index(name="Customers")
)

persona_counts["Percentage"] = (
    persona_counts["Customers"] / total_customers * 100
).round(2)

persona_summary = (
    df.groupby("persona")
    .agg(
        Customers=("persona", "count"),
        Average_Income=("annual_income_k", "mean"),
        Average_Spending=("spending_score", "mean"),
        Minimum_Income=("annual_income_k", "min"),
        Maximum_Income=("annual_income_k", "max"),
        Minimum_Spending=("spending_score", "min"),
        Maximum_Spending=("spending_score", "max")
    )
    .round(2)
)

persona_summary["Percentage"] = (
    persona_summary["Customers"] / total_customers * 100
).round(2)


# ============================================================
# HEADER — NAVIGATION + HERO
# ============================================================

top_row = persona_counts.iloc[0]
top_persona = str(top_row["Persona"])
top_customers = int(top_row["Customers"])
top_share = float(top_row["Percentage"])
top_income = float(persona_summary.loc[top_persona, "Average_Income"])
top_spending = float(persona_summary.loc[top_persona, "Average_Spending"])

persona_list_html = "".join(
    f"<li>{html.escape(str(row.Persona))}<span>{int(row.Customers):,}</span></li>"
    for row in persona_counts.itertuples(index=False)
)

if evaluation_data is not None:
    model_note = f"Silhouette score {selected_silhouette_score:.2f} on scaled income and spending."
else:
    model_note = "Income and spending, scaled with StandardScaler."

nav_html = (
    "<div class='topnav'>"
    "<div class='brand'><span class='brand-mark'>◆</span>Customer Persona Segmenter</div>"
    "<div class='links'>"
    "<a href='#predict' target='_self'>Predict</a>"
    "<a href='#personas' target='_self'>Personas</a>"
    "<a href='#analytics' target='_self'>Analytics</a>"
    "<a href='#model' target='_self'>Model</a>"
    "</div>"
    "<a class='nav-cta' href='#upload' target='_self'>Upload CSV</a>"
    "</div>"
)

hero_html = (
    "<div class='hero'>"

    # left: headline, lede, actions
    "<div>"
    "<div class='hero-title'>"
    "<span class='g-pink'>Customer</span> personas<br>"
    "from <span class='g-cyan'>K-Means</span> clustering"
    "</div>"
    "<p class='lede'>Group customers into behavioural personas from annual "
    "income and spending score, using a <strong>K-Means</strong> clustering "
    "model served over FastAPI.</p>"
    "<div class='hero-actions'>"
    "<a class='btn-primary' href='#predict' target='_self'>Predict a persona</a>"
    "<a class='btn-ghost' href='#upload' target='_self'>Upload a CSV</a>"
    "</div>"
    "</div>"

    # right: live data cards
    "<div class='hero-cards'>"

    "<div class='hcard hc-tall'>"
    "<div class='hc-head'>"
    f"<span class='hc-title'>{html.escape(top_persona)}</span>"
    "<span class='pill'>Largest</span>"
    "</div>"
    f"<div class='hc-big'>{top_customers:,}<span>customers</span></div>"
    f"<p class='hc-desc'>Average income {top_income:.1f}k and average "
    f"spending score {top_spending:.1f}.</p>"
    f"<div class='hc-bar'><div style='width:{top_share:.1f}%'></div></div>"
    f"<ul class='hc-list'>{persona_list_html}</ul>"
    "</div>"

    "<div class='hcard'>"
    "<div class='hc-row'>"
    "<div class='hc-icon'>↔</div>"
    "<div>"
    "<div class='hc-title'>Income and spending</div>"
    f"<div class='hc-big'>{correlation:.2f}<span>correlation</span></div>"
    "</div>"
    "</div>"
    "<p class='hc-desc'>Pearson coefficient across all "
    f"{total_customers:,} customers.</p>"
    "</div>"

    "<div class='hcard'>"
    "<div class='hc-row'>"
    "<div class='hc-icon'>◆</div>"
    "<div>"
    "<div class='hc-title'>K-Means model</div>"
    f"<p class='hc-desc'>{number_of_personas} personas from 2 features.</p>"
    "</div>"
    "</div>"
    f"<p class='hc-desc'>{model_note}</p>"
    "</div>"

    "</div>"
    "</div>"
)

st.markdown(nav_html, unsafe_allow_html=True)
st.markdown(hero_html, unsafe_allow_html=True)

st.divider()


# ============================================================
# KPI DASHBOARD
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Customers analysed",
        f"{total_customers:,}"
    )

with col2:
    st.metric(
        "Personas identified",
        number_of_personas
    )

with col3:
    st.metric(
        "Average income",
        f"{average_income:.2f}k"
    )

with col4:
    st.metric(
        "Average spending",
        f"{average_spending:.2f}"
    )

st.divider()


# ============================================================
# CUSTOMER PERSONA PREDICTION
# ============================================================

st.header("Predict a persona", anchor="predict")

prediction_container = st.container(border=True)

with prediction_container:

    glass_card()

    st.write(
        "Enter a customer's annual income and spending score to see "
        "which persona they fall into."
    )

    input_col1, input_col2 = st.columns(2)

    with input_col1:
        annual_income = st.number_input(
            "Annual income (thousands)",
            min_value=1.0,
            max_value=200.0,
            value=50.0,
            step=1.0,
            help="Annual income expressed in thousands."
        )

    with input_col2:
        spending_score = st.number_input(
            "Spending score",
            min_value=0.0,
            max_value=100.0,
            value=50.0,
            step=1.0,
            help="Customer spending score between 0 and 100."
        )

    predict_button = st.button(
        "Predict persona",
        use_container_width=True
    )

    if predict_button:

        payload = {
            "annual_income_k": annual_income,
            "spending_score": spending_score
        }

        try:

            response = requests.post(
                f"{API_URL}/predict",
                json=payload,
                timeout=10
            )

            if response.status_code == 200:

                result = response.json()

                st.success("Persona predicted.")

                result_col1, result_col2 = st.columns(2)

                with result_col1:
                    st.metric(
                        "Cluster",
                        result["cluster"]
                    )

                with result_col2:
                    st.metric(
                        "Persona",
                        result["persona"]
                    )

                persona = result["persona"]

                st.info(
                    PERSONA_DESCRIPTIONS.get(
                        persona,
                        "Persona identified by the K-Means model."
                    )
                )

            else:

                st.error(
                    f"The prediction service returned status "
                    f"{response.status_code}. Check the backend logs."
                )

        except requests.exceptions.RequestException:

            st.error(
                f"No response from the prediction service at {API_URL}. "
                "Start the FastAPI backend and try again."
            )

st.divider()


# ============================================================
# CUSTOMER PERSONA PROFILES
# ============================================================

st.header("The three personas", anchor="personas")

profile_columns = st.columns(3)

for column, (title, persona_key, blurb) in zip(
    profile_columns,
    PERSONA_PROFILES
):

    with column:

        with st.container(border=True):

            glass_card()

            st.subheader(title)

            st.write(blurb)

            st.metric(
                "Customers in group",
                int((df["persona"] == persona_key).sum())
            )


st.divider()


# ============================================================
# PHASE 12 — ANALYTICS OVERVIEW
# ============================================================

st.header("Advanced analytics overview", anchor="analytics")

analytics_col1, analytics_col2, analytics_col3 = st.columns(3)

with analytics_col1:
    st.metric(
        "Average annual income",
        f"{average_income:.2f}k"
    )

with analytics_col2:
    st.metric(
        "Average spending score",
        f"{average_spending:.2f}"
    )

with analytics_col3:
    st.metric(
        "Income ↔ spending correlation",
        f"{correlation:.2f}"
    )

st.caption(
    "Correlation is Pearson's correlation coefficient. "
    "Values closer to +1 indicate a stronger positive linear relationship, "
    "while values closer to -1 indicate a stronger negative linear relationship."
)

st.divider()


# ============================================================
# PERSONA SUMMARY
# ============================================================

st.header("Persona analytics")

display_summary = persona_summary[
    [
        "Customers",
        "Percentage",
        "Average_Income",
        "Average_Spending"
    ]
].copy()

display_summary.columns = [
    "Customers",
    "Share (%)",
    "Average Income (k)",
    "Average Spending"
]

st.dataframe(
    display_summary,
    use_container_width=True
)


# ============================================================
# PERSONA PERCENTAGE DISTRIBUTION
# ============================================================

st.subheader("Persona percentage distribution")

distribution_chart = persona_counts[
    ["Persona", "Percentage"]
].copy()

st.bar_chart(
    distribution_chart,
    x="Persona",
    y="Percentage",
    color=GREEN
)

st.caption(
    "Percentage represents each persona's share of the customers in the loaded dataset."
)


# ============================================================
# AVERAGE INCOME COMPARISON
# ============================================================

st.subheader("Average income by persona")

income_chart = (
    persona_summary["Average_Income"]
    .sort_values(ascending=False)
    .rename("Average Income (k)")
    .reset_index()
)

st.bar_chart(
    income_chart,
    x="persona",
    y="Average Income (k)",
    color=GREEN
)


# ============================================================
# AVERAGE SPENDING COMPARISON
# ============================================================

st.subheader("Average spending score by persona")

spending_chart = (
    persona_summary["Average_Spending"]
    .sort_values(ascending=False)
    .rename("Average Spending")
    .reset_index()
)

st.bar_chart(
    spending_chart,
    x="persona",
    y="Average Spending",
    color=GREEN
)

st.divider()


# ============================================================
# DETAILED PERSONA PROFILE TABLE
# ============================================================

st.header("Detailed persona profiles")

detailed_profiles = persona_summary[
    [
        "Customers",
        "Percentage",
        "Average_Income",
        "Average_Spending",
        "Minimum_Income",
        "Maximum_Income",
        "Minimum_Spending",
        "Maximum_Spending"
    ]
].copy()

detailed_profiles.columns = [
    "Customers",
    "Share (%)",
    "Avg Income (k)",
    "Avg Spending",
    "Min Income (k)",
    "Max Income (k)",
    "Min Spending",
    "Max Spending"
]

st.dataframe(
    detailed_profiles,
    use_container_width=True
)


# ============================================================
# PERSONA INCOME / SPENDING RANGES
# ============================================================

st.subheader("Income and spending ranges")

range_table = persona_summary[
    [
        "Minimum_Income",
        "Maximum_Income",
        "Minimum_Spending",
        "Maximum_Spending"
    ]
].copy()

range_table.columns = [
    "Minimum Income (k)",
    "Maximum Income (k)",
    "Minimum Spending",
    "Maximum Spending"
]

st.dataframe(
    range_table,
    use_container_width=True
)

st.caption(
    "Ranges show the minimum and maximum observed values within each persona."
)

st.divider()


# ============================================================
# AUTOMATIC PERSONA INSIGHTS
# ============================================================

st.header("Automatic persona insights")

for persona_name, row in persona_summary.iterrows():

    share = row["Percentage"]
    avg_income = row["Average_Income"]
    avg_spending = row["Average_Spending"]

    if avg_income >= average_income and avg_spending >= average_spending:
        pattern = "above the overall dataset average for both income and spending."

    elif avg_income < average_income and avg_spending >= average_spending:
        pattern = "below the overall dataset average for income but above it for spending."

    elif avg_income >= average_income and avg_spending < average_spending:
        pattern = "above the overall dataset average for income but below it for spending."

    else:
        pattern = "below the overall dataset average for both income and spending."

    st.markdown(
        f"**{persona_name}** — represents **{share:.2f}%** of customers, "
        f"with average income of **{avg_income:.2f}k** and average spending "
        f"of **{avg_spending:.2f}**. Relative to the full dataset, this segment is "
        f"{pattern}"
    )


# ============================================================
# SEGMENT INTERPRETATION
# ============================================================

st.subheader("Segment interpretation")

highest_income_persona = persona_summary["Average_Income"].idxmax()
highest_spending_persona = persona_summary["Average_Spending"].idxmax()
largest_persona = persona_summary["Customers"].idxmax()

st.markdown(
    f"""
- **Highest average income:** {highest_income_persona}
- **Highest average spending score:** {highest_spending_persona}
- **Largest customer segment:** {largest_persona}
- **Income-spending relationship:** correlation = {correlation:.2f}
"""
)

st.caption(
    "These statements describe patterns in the loaded dataset and do not "
    "establish causation or predict future customer behaviour."
)

# ============================================================
# PHASE 13 — MODEL EVALUATION
# ============================================================

st.divider()

st.header("🤖 Model Evaluation", anchor="model")

st.caption(
    "Evaluation of the K-Means clustering model using "
    "the Elbow Method, Silhouette Score, cluster distribution, "
    "and centroid analysis."
)


# ============================================================
# MODEL CONFIGURATION
# ============================================================

st.subheader("⚙️ Model Configuration")

eval_col1, eval_col2, eval_col3, eval_col4 = st.columns(4)

with eval_col1:
    st.metric("Algorithm", "K-Means")

with eval_col2:
    st.metric("Clusters", int(optimal_k))

with eval_col3:
    st.metric("Features", 2)

with eval_col4:
    st.metric("Customers", len(df))


# ============================================================
# ELBOW + SILHOUETTE
# ============================================================

if evaluation_data is not None:

    st.subheader("📈 Clustering Quality Analysis")

    chart_col1, chart_col2 = st.columns(2)

    # --------------------------------------------------------
    # ELBOW METHOD
    # --------------------------------------------------------

    with chart_col1:

        st.markdown("#### 📉 Elbow Method")

        elbow_df = pd.DataFrame({
            "K": k_values,
            "Inertia": inertia_values
        })

        st.line_chart(
            elbow_df.set_index("K"),
            color=GREEN
        )

        st.caption(
            "Lower inertia indicates tighter clusters. "
            "The elbow helps identify a suitable number of clusters."
        )


    # --------------------------------------------------------
    # SILHOUETTE SCORE
    # --------------------------------------------------------

    with chart_col2:

        st.markdown("#### 📊 Silhouette Score")

        silhouette_df = pd.DataFrame({
            "K": k_values,
            "Silhouette Score": silhouette_values
        })

        st.line_chart(
            silhouette_df.set_index("K"),
            color=GREEN
        )

        st.caption(
            "Higher silhouette scores indicate better-defined "
            "and more separated clusters."
        )


    # ========================================================
    # SELECTED MODEL
    # ========================================================

    st.subheader("🎯 Selected Model")

    model_col1, model_col2, model_col3 = st.columns(3)

    with model_col1:
        st.metric(
            "Selected K",
            int(optimal_k)
        )

    with model_col2:
        st.metric(
            "Silhouette Score",
            f"{selected_silhouette_score:.4f}"
        )

    with model_col3:
        st.metric(
            "Tested K Range",
            f"{min(k_values)} – {max(k_values)}"
        )


# ============================================================
# CLUSTER SIZE VALIDATION
# ============================================================

st.subheader("👥 Cluster Size Validation")

cluster_counts = (
    df["cluster"]
    .value_counts()
    .sort_index()
    .reset_index()
)

cluster_counts.columns = [
    "Cluster",
    "Customers"
]

cluster_counts["Percentage"] = (
    cluster_counts["Customers"] /
    len(df) * 100
).round(2)

st.dataframe(
    cluster_counts,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# CLUSTER CENTROIDS
# ============================================================

st.subheader("🎯 Cluster Centroids")

centroid_table = (
    df.groupby("cluster")[
        ["annual_income_k", "spending_score"]
    ]
    .mean()
    .round(2)
)

centroid_table.index.name = "Cluster"

st.dataframe(
    centroid_table,
    use_container_width=True
)


# ============================================================
# PERSONA EVALUATION
# ============================================================

st.subheader("🧩 Persona Evaluation")

persona_evaluation = (
    df.groupby("persona")
    .agg(
        Customers=("persona", "count"),
        Average_Income=("annual_income_k", "mean"),
        Average_Spending=("spending_score", "mean"),
        Minimum_Income=("annual_income_k", "min"),
        Maximum_Income=("annual_income_k", "max"),
        Minimum_Spending=("spending_score", "min"),
        Maximum_Spending=("spending_score", "max")
    )
    .round(2)
    .reset_index()
)

st.dataframe(
    persona_evaluation,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# MODEL INTERPRETATION
# ============================================================

st.subheader("💡 Model Interpretation")

st.info(
    """
The K-Means model segments customers using two features:

• Annual Income  
• Spending Score

Customers are assigned to clusters based on their distance
from the cluster centroids after feature scaling.

The selected model uses 3 clusters, which are interpreted
as distinct customer personas based on their income and
spending characteristics.
"""
)

st.divider()


# ============================================================
# DOWNLOAD PERSONA ANALYTICS
# ============================================================


# ============================================================
# DOWNLOAD PERSONA ANALYTICS
# ============================================================

st.subheader("Download persona analytics")

analytics_download = detailed_profiles.reset_index()
analytics_download = analytics_download.rename(
    columns={"persona": "Persona"}
)

analytics_csv = analytics_download.to_csv(index=False)

st.download_button(
    label="⬇️ Download Persona Analytics CSV",
    data=analytics_csv,
    file_name="persona_analytics.csv",
    mime="text/csv",
    use_container_width=True
)


st.divider()


# ============================================================
# PERSONA DISTRIBUTION
# ============================================================

st.subheader("How customers are distributed")

st.bar_chart(
    persona_counts,
    x="Persona",
    y="Customers",
    color=GREEN
)

st.divider()


# ============================================================
# CUSTOMER SEGMENTATION
# ============================================================

st.header("Segmentation map")

persona_order = sorted(df["persona"].unique())
persona_palette = ["#22c55e", "#f472b6", "#22d3ee", "#facc15", "#a78bfa"]

segmentation_map = (
    alt.Chart(df[["annual_income_k", "spending_score", "persona"]])
    .mark_circle(size=70, opacity=0.85)
    .encode(
        x=alt.X("annual_income_k:Q", title="Annual income (k)"),
        y=alt.Y("spending_score:Q", title="Spending score"),
        color=alt.Color(
            "persona:N",
            scale=alt.Scale(
                domain=persona_order,
                range=persona_palette[:len(persona_order)]
            ),
            legend=alt.Legend(title="Persona", orient="bottom")
        ),
        tooltip=[
            alt.Tooltip("persona:N", title="Persona"),
            alt.Tooltip("annual_income_k:Q", title="Income (k)"),
            alt.Tooltip("spending_score:Q", title="Spending score")
        ]
    )
    .properties(height=420)
    .interactive()
)

st.altair_chart(segmentation_map, use_container_width=True)

st.caption(
    "Each point is one customer, coloured by the persona assigned "
    "by the K-Means model."
)

st.divider()


# ============================================================
# FILTER CUSTOMERS
# ============================================================

st.header("Browse the data")

selected_persona = st.multiselect(
    "Personas to include",
    options=sorted(df["persona"].unique()),
    default=sorted(df["persona"].unique())
)

filtered_df = df[df["persona"].isin(selected_persona)]

if filtered_df.empty:

    st.info("Select at least one persona to see customers here.")

else:

    st.write(f"Showing **{len(filtered_df):,}** customers.")

    with st.expander("View filtered customer records"):

        st.dataframe(
            filtered_df,
            use_container_width=True,
            height=400
        )


st.divider()


# ============================================================
# UPLOAD CUSTOMER CSV
# ============================================================

st.header("📤 Upload Customer CSV", anchor="upload")

st.write(
    "Upload a CSV containing `annual_income_k` and "
    "`spending_score` to segment new customers."
)

uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    st.success(
        f"File selected: {uploaded_file.name}"
    )

    segment_button = st.button(
        "🚀 Segment Uploaded Customers",
        use_container_width=True
    )

    if segment_button:

        try:

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "text/csv"
                )
            }

            response = requests.post(
                f"{API_URL}/segment-csv",
                files=files,
                timeout=30
            )

            if response.status_code == 200:

                result = response.json()

                st.success(
                    "CSV segmentation completed successfully!"
                )

                segmented_data = pd.DataFrame(
                    result["data"]
                )

                st.subheader(
                    "📊 Segmentation Results"
                )

                st.metric(
                    "Customers Processed",
                    result["total_customers"]
                )

                st.dataframe(
                    segmented_data,
                    use_container_width=True
                )

                st.subheader(
                    "🎯 Uploaded Customer Personas"
                )

                uploaded_distribution = pd.DataFrame(
                    result["persona_distribution"].items(),
                    columns=[
                        "Persona",
                        "Customers"
                    ]
                )

                st.bar_chart(
                    uploaded_distribution,
                    x="Persona",
                    y="Customers",
                    color=GREEN
                )

                csv_data = segmented_data.to_csv(
                    index=False
                )

                st.download_button(
                    label="⬇️ Download Segmented CSV",
                    data=csv_data,
                    file_name="segmented_customers.csv",
                    mime="text/csv",
                    use_container_width=True
                )

            else:

                try:
                    error_detail = response.json().get(
                        "detail",
                        "Unknown API error"
                    )
                except ValueError:
                    error_detail = response.text or "Unknown API error"

                st.error(
                    f"API Error: {error_detail}"
                )

        except requests.exceptions.RequestException:

            st.error(
                "Unable to connect to the FastAPI backend."
            )
# ============================================================
# MODEL EVALUATION
# ============================================================

st.markdown("---")
st.markdown("## 🤖 Model Evaluation")
st.caption(
    "Evaluation of the K-Means clustering model using "
    "cluster quality, distribution, and centroid analysis."
)

# ------------------------------------------------------------
# Model Configuration
# ------------------------------------------------------------

st.markdown("### ⚙️ Model Configuration")

eval_col1, eval_col2, eval_col3, eval_col4 = st.columns(4)

with eval_col1:
    st.metric("Algorithm", "K-Means")

with eval_col2:
    st.metric("Clusters", 3)

with eval_col3:
    st.metric("Features", 2)

with eval_col4:
    st.metric("Customers", len(df))


# ------------------------------------------------------------
# Cluster Size Validation
# ------------------------------------------------------------

st.markdown("### 👥 Cluster Size Validation")

cluster_counts = (
    df["cluster"]
    .value_counts()
    .sort_index()
    .reset_index()
)

cluster_counts.columns = ["Cluster", "Customers"]

cluster_counts["Percentage"] = (
    cluster_counts["Customers"] / len(df) * 100
).round(2)

st.dataframe(
    cluster_counts,
    use_container_width=True,
    hide_index=True
)

st.bar_chart(
    cluster_counts.set_index("Cluster")["Customers"],
    color=GREEN
)


# ------------------------------------------------------------
# Cluster Centroids
# ------------------------------------------------------------

st.markdown("### 🎯 Cluster Centroids")

centroid_table = (
    df.groupby("cluster")[
        ["annual_income_k", "spending_score"]
    ]
    .mean()
    .round(2)
)

centroid_table.index.name = "Cluster"

st.dataframe(
    centroid_table,
    use_container_width=True
)


# ------------------------------------------------------------
# Persona-level Evaluation
# ------------------------------------------------------------

st.markdown("### 🧩 Persona Evaluation")

persona_evaluation = (
    df.groupby("persona")
    .agg(
        Customers=("persona", "count"),
        Average_Income=("annual_income_k", "mean"),
        Average_Spending=("spending_score", "mean"),
        Minimum_Income=("annual_income_k", "min"),
        Maximum_Income=("annual_income_k", "max"),
        Minimum_Spending=("spending_score", "min"),
        Maximum_Spending=("spending_score", "max")
    )
    .round(2)
    .reset_index()
)

st.dataframe(
    persona_evaluation,
    use_container_width=True,
    hide_index=True
)


# ------------------------------------------------------------
# Model Interpretation
# ------------------------------------------------------------

st.markdown("### 💡 Model Interpretation")

st.info(
    """
The K-Means model segments customers using two behavioral features:

• Annual Income  
• Spending Score

Each customer is assigned to the cluster whose centroid is closest
to the customer's scaled feature values.

The resulting clusters are interpreted as different customer
personas based on their income and spending characteristics.
"""
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("Customer Persona Segmenter")

    st.markdown(
        """
        ### Model

        - K-Means clustering
        - StandardScaler normalisation
        - 3 customer personas

        ### Inputs

        - Annual income
        - Spending score

        ### Analytics

        - Persona distribution
        - Average income
        - Average spending
        - Income/spending ranges
        - Correlation analysis
        - Automatic insights
        - Downloadable analytics

        ### Stack

        - FastAPI backend
        - Streamlit interface
        """
    )

    st.divider()

    st.caption("Segmentation for marketing and retention planning.")