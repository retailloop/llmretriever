import statistics
from sqlalchemy.orm import Session
from models import BenchmarkResult, BenchmarkSummary

class Simulator:
    def __init__(self, db_adapter, queue_adapter):
        self.db_adapter = db_adapter
        self.queue_adapter = queue_adapter

    def store_results(self, llm_model: str, metric: str, data_points: list):
        # Calculate statistics
        mean_value = statistics.mean(data_points)
        median_value = statistics.median(data_points)
        std_dev = statistics.stdev(data_points)

        # Store summary statistics in the database
        self.db_adapter.store_summary(llm_model, metric, mean_value, median_value, std_dev)

        # Send message to queue for further processing if needed
        self.queue_adapter.send_message({
            'llm_model': llm_model,
            'metric': metric,
            'mean_value': mean_value,
            'median_value': median_value,
            'std_dev': std_dev
        })