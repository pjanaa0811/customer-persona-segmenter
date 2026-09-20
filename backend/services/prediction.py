from pathlib import Path

import joblib
import pandas as pd


# --------------------------------------------------
# Locate project root
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_DIR = BASE_DIR / "models"


# --------------------------------------------------
# Load saved ML artifacts
# --------------------------------------------------

kmeans_model = joblib.load(
    MODEL_DIR / "kmeans_model.pkl"
)

scaler = joblib.load(
    MODEL_DIR / "scaler.pkl"
)

persona_mapping = joblib.load(
    MODEL_DIR / "persona_mapping.pkl"
)


# --------------------------------------------------
# Prediction function
# --------------------------------------------------

def predict_persona(
    annual_income_k: float,
    spending_score: float
):
    """
    Predict the cluster and persona for a new customer.
    """

    customer_data = pd.DataFrame({
        "annual_income_k": [annual_income_k],
        "spending_score": [spending_score]
    })

    # Scale using the saved scaler
    customer_scaled = scaler.transform(
        customer_data
    )

    # Predict cluster
    cluster = int(
        kmeans_model.predict(customer_scaled)[0]
    )

    # Convert cluster to persona
    persona = persona_mapping[cluster]

    return {
        "cluster": cluster,
        "persona": persona,
        "annual_income_k": annual_income_k,
        "spending_score": spending_score
    }
def segment_dataframe(df):
    """
    Segment multiple customers using the trained K-Means model.
    """

    required_columns = [
        "annual_income_k",
        "spending_score"
    ]

    # Check required columns
    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Keep only required features
    customer_data = df[
        required_columns
    ].copy()

    # Scale customer data
    customer_scaled = scaler.transform(
        customer_data
    )

    # Predict clusters
    clusters = kmeans_model.predict(
        customer_scaled
    )

    # Add cluster column
    result_df = customer_data.copy()

    result_df["cluster"] = clusters

    # Add persona
    result_df["persona"] = (
        result_df["cluster"]
        .map(persona_mapping)
    )

    return result_df