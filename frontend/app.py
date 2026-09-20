import streamlit as st
import requests
import pandas as pd
from pathlib import Path
import pickle


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

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');

:root {
    --ink:          #16181D;
    --ink-soft:     #5B6270;
    --ink-faint:    #8B93A1;
    --canvas:       #F3F4F7;
    --glass:        rgba(255, 255, 255, 0.72);
    --glass-strong: rgba(255, 255, 255, 0.88);
    --red:          #C1272D;
    --red-deep:     #97171D;
    --red-soft:     #E8827F;
    --red-tint:     #FBEDED;
    --line:         rgba(22, 24, 29, 0.08);
    --line-red:     rgba(193, 39, 45, 0.16);
    --shadow:       0 10px 30px rgba(22, 24, 29, 0.06);
}

/* ---------------- Background ---------------- */

.stApp {
    background-color: var(--canvas);
    background-image:
        radial-gradient(1000px 560px at 6% -10%, rgba(193, 39, 45, 0.12), transparent 58%),
        radial-gradient(820px 480px at 100% 0%, rgba(193, 39, 45, 0.08), transparent 55%),
        radial-gradient(700px 520px at 92% 92%, rgba(193, 39, 45, 0.07), transparent 60%),
        radial-gradient(600px 420px at -4% 88%, rgba(151, 23, 29, 0.06), transparent 60%),
        linear-gradient(180deg, #F7F7F9 0%, #F1F2F5 55%, #EFF0F3 100%);
    background-attachment: fixed;
    color: var(--ink);
}

[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu, footer {
    visibility: hidden;
}

.block-container {
    padding-top: 2.6rem;
    padding-bottom: 4rem;
    max-width: 1280px;
}

/* ---------------- Type ---------------- */

html, body, [class*="css"], .stMarkdown, p, li, label {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--ink);
}

h1, h2, h3, h4 {
    font-family: 'Plus Jakarta Sans', 'Inter', sans-serif;
    color: var(--ink);
    letter-spacing: -0.02em;
}

h1 {
    font-size: 2.6rem;
    font-weight: 800;
    line-height: 1.12;
    margin-bottom: 0.2rem;
}

h2 {
    font-size: 1.45rem;
    font-weight: 700;
    margin-top: 0.4rem;
    padding-left: 0.85rem;
    border-left: 3px solid var(--red);
}

h3 {
    font-size: 1.1rem;
    font-weight: 700;
}

p, li {
    color: var(--ink-soft);
    line-height: 1.65;
}

[data-testid="stCaptionContainer"] p {
    color: var(--ink-faint);
}

hr {
    border-color: var(--line);
    margin: 2.2rem 0;
}

/* ---------------- Lede paragraph ---------------- */

.lede {
    max-width: 62ch;
    font-size: 1.02rem;
    color: var(--ink-soft);
    margin: 0.6rem 0 0.2rem 0;
}

.lede strong {
    color: var(--red-deep);
    font-weight: 600;
}

/* ---------------- Glass cards ---------------- */

div[data-testid="stVerticalBlockBorderWrapper"]:has(span.glass) {
    background: var(--glass);
    backdrop-filter: blur(18px) saturate(160%);
    -webkit-backdrop-filter: blur(18px) saturate(160%);
    border: 1px solid var(--line-red);
    border-radius: 18px;
    box-shadow: var(--shadow);
}

/* ---------------- Alerts ---------------- */

div[data-testid="stAlertContainer"] {
    border-radius: 12px;
    border: 1px solid var(--line);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
}

/* ---------------- Tables, charts, expander ---------------- */

[data-testid="stDataFrame"],
[data-testid="stExpander"] {
    background: var(--glass);
    backdrop-filter: blur(14px) saturate(140%);
    -webkit-backdrop-filter: blur(14px) saturate(140%);
    border: 1px solid var(--line);
    border-radius: 14px;
    box-shadow: var(--shadow);
    overflow: hidden;
}

[data-testid="stExpander"] summary:hover {
    color: var(--red);
}

[data-testid="stVegaLiteChart"] {
    background: var(--glass);
    backdrop-filter: blur(14px) saturate(140%);
    -webkit-backdrop-filter: blur(14px) saturate(140%);
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 1.1rem;
    box-shadow: var(--shadow);
}

/* ---------------- Sidebar ---------------- */

[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.62);
    backdrop-filter: blur(24px) saturate(160%);
    -webkit-backdrop-filter: blur(24px) saturate(160%);
    border-right: 1px solid var(--line-red);
}

[data-testid="stSidebar"] h1 {
    font-size: 1.3rem;
    font-weight: 700;
}

[data-testid="stSidebar"] h3 {
    font-size: 0.95rem;
    color: var(--red-deep);
}

[data-testid="stSidebar"] li {
    font-size: 0.88rem;
}

/* ---------------- Metric cards ---------------- */

[data-testid="stMetric"] {
    background: var(--glass);
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 0.8rem 1rem;
    box-shadow: var(--shadow);
}

/* ---------------- Motion preference ---------------- */

@media (prefers-reduced-motion: reduce) {
    * { transition: none !important; }
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
RED = "#C1272D"


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
# HEADER
# ============================================================

st.title("Customer Persona Segmenter")

st.markdown(
    "<p class='lede'>Group customers into behavioural personas from annual "
    "income and spending score, using a <strong>K-Means</strong> clustering "
    "model served over FastAPI.</p>",
    unsafe_allow_html=True
)

st.caption("K-Means clustering · StandardScaler · FastAPI · Streamlit")

st.divider()


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

st.header("Predict a persona")

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

st.header("The three personas")

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

st.header("Advanced analytics overview")

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
    color=RED
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
    color=RED
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
    color=RED
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

st.header("🤖 Model Evaluation")

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
            elbow_df.set_index("K")
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
            silhouette_df.set_index("K")
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
    color=RED
)

st.divider()


# ============================================================
# CUSTOMER SEGMENTATION
# ============================================================

st.header("Segmentation map")

st.scatter_chart(
    df,
    x="annual_income_k",
    y="spending_score",
    color="persona"
)

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

st.header("📤 Upload Customer CSV")

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
                    y="Customers"
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
    cluster_counts.set_index("Cluster")["Customers"]
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
