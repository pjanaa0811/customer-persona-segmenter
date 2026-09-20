from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException
)

import pandas as pd
from io import BytesIO

from backend.schemas import (
    CustomerInput,
    PredictionResponse
)

from backend.services.prediction import (
    predict_persona,
    segment_dataframe
)


# --------------------------------------------------
# Create FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="Customer Persona Segmenter API",
    description=(
        "API for predicting customer personas "
        "using K-Means clustering."
    ),
    version="1.0.0"
)


# --------------------------------------------------
# Root endpoint
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Customer Persona Segmenter API is running",
        "status": "success"
    }


# --------------------------------------------------
# Health check
# --------------------------------------------------

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# --------------------------------------------------
# Prediction endpoint
# --------------------------------------------------

@app.post(
    "/predict",
    response_model=PredictionResponse
)
def predict(customer: CustomerInput):

    result = predict_persona(
        annual_income_k=customer.annual_income_k,
        spending_score=customer.spending_score
    )

    return result
@app.post("/segment-csv")
async def segment_csv(
    file: UploadFile = File(...)
):

    # Check file type
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported."
        )

    try:

        # Read uploaded file
        contents = await file.read()

        df = pd.read_csv(
            BytesIO(contents)
        )

        # Segment customers
        result_df = segment_dataframe(
            df
        )

        # Persona distribution
        persona_distribution = (
            result_df["persona"]
            .value_counts()
            .to_dict()
        )

        return {
            "filename": file.filename,
            "total_customers": len(result_df),
            "persona_distribution":
                persona_distribution,
            "data":
                result_df.to_dict(
                    orient="records"
                )
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Error processing CSV: {str(e)}"
        )