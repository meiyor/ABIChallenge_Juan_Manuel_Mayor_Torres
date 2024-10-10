from sqlalchemy import Column, Integer, String, PickleType
from database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, index=True)
    date = Column(String, index=True)
    username = Column(String, index=True)
    model = Column(String, index=True)
    prediction = Column(PickleType, nullable=False)
    prediction_probability = Column(PickleType, nullable=False)
    explainability_file = Column(String, index=True)
    results_file = Column(String, index=True)
