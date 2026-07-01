from pydantic import BaseModel


class UsageSummaryResponse(BaseModel):
    product_name: str
    total_usage: int
    estimated_cost: int