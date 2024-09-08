from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class BenchmarkResult(Base):
    __tablename__ = "benchmark_results"

    id = Column(Integer, primary_key=True, index=True)
    llm_model = Column(String, index=True)
    metric = Column(String, index=True)
    value = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

class BenchmarkSummary(Base):
    __tablename__ = "benchmark_summaries"

    id = Column(Integer, primary_key=True, index=True)
    llm_model = Column(String, index=True)
    metric = Column(String, index=True)
    mean_value = Column(Float)
    median_value = Column(Float)
    std_dev = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)