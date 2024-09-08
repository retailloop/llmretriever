from pydantic import BaseModel
from datetime import datetime


class BenchmarkSummary(BaseModel):
    id: int
    llm_model: str
    metric: str
    mean_value: float
    median_value: float
    std_dev: float
    timestamp: datetime


class Ranking(BaseModel):
    llm_model: str
    avg_value: float
    std_dev: float
