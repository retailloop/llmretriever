from sqlalchemy.orm import Session
from models import BenchmarkResult, BenchmarkSummary

class DatabaseAdapter:
    def __init__(self, session_maker):
        self.session_maker = session_maker

    def store_result(self, llm_model: str, metric: str, value: float):
        with self.session_maker() as session:
            result = BenchmarkResult(llm_model=llm_model, metric=metric, value=value)
            session.add(result)
            session.commit()

    def store_summary(self, llm_model: str, metric: str, mean: float, median: float, std_dev: float):
        with self.session_maker() as session:
            summary = BenchmarkSummary(
                llm_model=llm_model,
                metric=metric,
                mean_value=mean,
                median_value=median,
                std_dev=std_dev
            )
            session.add(summary)
            session.commit()