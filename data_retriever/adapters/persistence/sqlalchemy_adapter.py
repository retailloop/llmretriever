from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from ports.repositories import BenchmarkRepository
from domain.models import Ranking, BenchmarkSummary
from utils.logger import setup_logger

logger = setup_logger(__name__)

Base = declarative_base()


class BenchmarkSummaryModel(Base):
    __tablename__ = "benchmark_summaries"

    id = Column(Integer, primary_key=True, index=True)
    llm_model = Column(String, index=True)
    metric = Column(String, index=True)
    mean_value = Column(Float)
    median_value = Column(Float)
    std_dev = Column(Float)
    timestamp = Column(DateTime)


class SQLAlchemyRepository(BenchmarkRepository):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def get_ranking(self, metric: str):
        try:
            with self.session_factory() as session:
                query = session.query(BenchmarkSummaryModel.llm_model,
                                      func.avg(BenchmarkSummaryModel.mean_value).label('avg_value'),
                                      func.avg(BenchmarkSummaryModel.std_dev).label('std_dev')) \
                    .filter(BenchmarkSummaryModel.metric == metric) \
                    .group_by(BenchmarkSummaryModel.llm_model) \
                    .order_by(func.avg(BenchmarkSummaryModel.mean_value).desc())

                result = query.all()
                return [{"llm_model": row.llm_model, "avg_value": row.avg_value, "std_dev": row.std_dev}
                        for row in result] if result else []
        except Exception as e:
            logger.error(f"Error getting ranking for metric {metric}: {str(e)}", exc_info=True)
            raise

    def get_available_metrics(self):
        try:
            with self.session_factory() as session:
                query = session.query(BenchmarkSummaryModel.metric).distinct()
                result = query.all()
                return [row.metric for row in result]
        except Exception as e:
            logger.error(f"Error getting available metrics: {str(e)}", exc_info=True)
            raise

    def get_available_models(self):
        try:
            with self.session_factory() as session:
                query = session.query(BenchmarkSummaryModel.llm_model).distinct()
                result = query.all()
                return [row.llm_model for row in result]
        except Exception as e:
            logger.error(f"Error getting available models: {str(e)}", exc_info=True)
            raise


def init_db(database_url):
    try:
        engine = create_engine(database_url)
        Base.metadata.create_all(bind=engine)
        return sessionmaker(bind=engine)
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}", exc_info=True)
        raise
