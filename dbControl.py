import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///weather.db")
Base = declarative_base()

class Weather_data(Base):
    __tablename__ = "Orai"
    id = Column(Integer, primary_key=True)
    city = Column("Miestas", String)
    temperature = Column("Temperatūra", String)
    humidity = Column("Dregmė", String)
    wind_speed = Column("Vėjo greitis", String)
    description = Column("Horizontas", String)
    fix_date = Column("Fiksavimo data", DateTime, default=datetime.datetime.utcnow)

    def __init__(self, city, temperature, humidity, wind_speed, description):
        self.city = city
        self.temperature = temperature
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.description = description

    def __repr__(self):
        return f"{self.id} {self.city} {self.temperature} {self.humidity} {self.wind_speed} {self.description} {self.fix_date}"

Base.metadata.create_all(engine)