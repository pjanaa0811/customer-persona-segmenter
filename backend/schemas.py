from pydantic import BaseModel, Field


class CustomerInput(BaseModel):
    annual_income_k: float = Field(
        ...,
        gt=0,
        description="Annual income in thousands"
    )

    spending_score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Customer spending score from 0 to 100"
    )


class PredictionResponse(BaseModel):
    cluster: int
    persona: str
    annual_income_k: float
    spending_score: float