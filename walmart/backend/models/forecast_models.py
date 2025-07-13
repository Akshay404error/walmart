from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from enum import Enum

class ForecastPeriod(str, Enum):
    WEEK = "week"
    MONTH = "month"
    QUARTER = "quarter"
    YEAR = "year"

class SignalType(str, Enum):
    POS = "pos"
    SOCIAL = "social"
    WEATHER = "weather"
    EVENTS = "events"

class ForecastRequest(BaseModel):
    product_ids: List[str] = Field(..., description="List of product IDs to forecast")
    forecast_period: ForecastPeriod = Field(default=ForecastPeriod.MONTH, description="Forecast period")
    include_external_signals: bool = Field(default=True, description="Include external signals")
    confidence_level: float = Field(default=0.95, ge=0.8, le=0.99, description="Confidence level")
    store_id: Optional[str] = Field(None, description="Specific store ID")
    category: Optional[str] = Field(None, description="Product category")

class ForecastResponse(BaseModel):
    message: str
    forecast_id: str
    status: str
    estimated_completion: datetime

class TrendAnalysis(BaseModel):
    product_ids: List[str]
    category: Optional[str]
    time_period: str
    trends: List[Dict[str, Any]]
    seasonality: Dict[str, float]
    anomalies: List[Dict[str, Any]]
    confidence_score: float
    generated_at: datetime

class ForecastData(BaseModel):
    product_id: str
    date: date
    predicted_demand: float
    lower_bound: float
    upper_bound: float
    confidence: float
    signals_used: List[SignalType]
    model_version: str
    created_at: datetime

class SocialSignal(BaseModel):
    product_id: str
    sentiment_score: float = Field(..., ge=-1.0, le=1.0)
    trending_score: float = Field(..., ge=0.0, le=1.0)
    mentions_count: int = Field(..., ge=0)
    platform: str
    timestamp: datetime

class WeatherSignal(BaseModel):
    location: str
    product_id: str
    temperature: float
    humidity: float
    precipitation: float
    weather_condition: str
    impact_score: float = Field(..., ge=-1.0, le=1.0)
    timestamp: datetime

class EventSignal(BaseModel):
    event_name: str
    event_date: date
    location: str
    product_ids: List[str]
    expected_impact: float = Field(..., ge=-1.0, le=1.0)
    event_type: str
    attendance_estimate: Optional[int]

class ModelAccuracy(BaseModel):
    model_name: str
    mape: float = Field(..., ge=0.0)
    rmse: float = Field(..., ge=0.0)
    mae: float = Field(..., ge=0.0)
    overall_accuracy: float = Field(..., ge=0.0, le=1.0)
    last_evaluation: datetime
    training_data_size: int
    test_data_size: int

class ForecastComparison(BaseModel):
    product_id: str
    actual_demand: List[float]
    predicted_demand: List[float]
    dates: List[date]
    accuracy_metrics: ModelAccuracy
    comparison_period: str

class MultiSignalForecast(BaseModel):
    product_id: str
    base_forecast: float
    social_adjustment: float
    weather_adjustment: float
    event_adjustment: float
    final_forecast: float
    signal_weights: Dict[SignalType, float]
    confidence_interval: Dict[str, float]
    generated_at: datetime 