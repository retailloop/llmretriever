from dataclasses import dataclass
from datetime import datetime

@dataclass
class BenchmarkSummary:
    id: int
    llm_model: str
    metric: str
    mean_value: float
    median_value: float
    std_dev: float
    timestamp: datetime

@dataclass
class Ranking:
    llm_model: str
    avg_value: float
    std_dev: float
