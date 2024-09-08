import os
import random
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, BenchmarkResult
from adapters.database import DatabaseAdapter
from adapters.queue import RabbitMQAdapter
from core.simulator import Simulator

DATABASE_URL = os.getenv("DATABASE_URL").replace('postgres://', 'postgresql://')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

RABBITMQ_URL = os.getenv("RABBITMQ_URL")

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize adapters
db_adapter = DatabaseAdapter(SessionLocal)
queue_adapter = RabbitMQAdapter(RABBITMQ_URL)

# Initialize simulator
simulator = Simulator(db_adapter, queue_adapter)

LLM_MODELS = [
    "GPT-4o", "Llama 3.1 405", "Mistral Large2", "Claude 3.5 Sonnet", "Gemini 1.5 Pro",
    "GPT-4o mini", "Llama 3.1 70B", "amba 1.5Large", "Mixtral 8x22B", "Gemini 1.5Flash",
    "Claude 3 Haiku", "Llama 3.1 8B"
]

METRICS = ["TTFT", "TPS", "e2e_latency", "RPS"]


def generate_realistic_data(metric, num_points=100000):
    if metric == "TTFT":
        return [random.uniform(10, 1000) for _ in range(num_points)]
    elif metric == "TPS":
        return [random.uniform(1, 100) for _ in range(num_points)]
    elif metric == "e2e_latency":
        return [random.uniform(100, 5000) for _ in range(num_points)]
    elif metric == "RPS":
        return [random.uniform(0.1, 10) for _ in range(num_points)]
    else:
        raise ValueError(f"Unknown metric: {metric}")


def simulate_data():
    for llm in LLM_MODELS:
        for metric in METRICS:
            data_points = generate_realistic_data(metric)
            simulator.store_results(llm, metric, data_points)
            print(f"Generated and stored 100,000 datapoints for {llm} - {metric}")


if __name__ == "__main__":
    while True:
        simulate_data()
        print("Completed one round of data simulation for all models and metrics.")
        time.sleep(3600) # Run every hour
