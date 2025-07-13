from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging

from services.forecasting_service import ForecastingService
from models.forecast_models import ForecastRequest, ForecastResponse, TrendAnalysis

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize forecasting service
forecasting_service = ForecastingService()

@router.post("/generate", response_model=ForecastResponse)
async def generate_forecast(
    request: ForecastRequest,
    background_tasks: BackgroundTasks
):
    """
    Generate demand forecast for specified products and time period
    """
    try:
        logger.info(f"Generating forecast for {len(request.product_ids)} products")
        
        # Add to background tasks for processing
        background_tasks.add_task(
            forecasting_service.generate_forecast_async,
            request.product_ids,
            request.forecast_period,
            request.include_external_signals
        )
        
        return ForecastResponse(
            message="Forecast generation started",
            forecast_id=f"fc_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            status="processing",
            estimated_completion=datetime.now() + timedelta(minutes=5)
        )
    except Exception as e:
        logger.error(f"Error generating forecast: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{product_id}", response_model=Dict[str, Any])
async def get_product_forecast(product_id: str, days: int = 30):
    """
    Get forecast for a specific product
    """
    try:
        forecast_data = await forecasting_service.get_product_forecast(product_id, days)
        return {
            "product_id": product_id,
            "forecast_period": days,
            "predictions": forecast_data["predictions"],
            "confidence_intervals": forecast_data["confidence_intervals"],
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error fetching forecast for product {product_id}: {e}")
        raise HTTPException(status_code=404, detail=f"Forecast not found for product {product_id}")

@router.get("/trends/analysis", response_model=TrendAnalysis)
async def get_trend_analysis(
    product_ids: Optional[List[str]] = None,
    category: Optional[str] = None,
    time_period: str = "30d"
):
    """
    Get trend analysis for products or categories
    """
    try:
        trends = await forecasting_service.analyze_trends(
            product_ids=product_ids,
            category=category,
            time_period=time_period
        )
        return trends
    except Exception as e:
        logger.error(f"Error analyzing trends: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/signals/social")
async def get_social_signals(product_id: str):
    """
    Get social media signals for a product
    """
    try:
        signals = await forecasting_service.get_social_signals(product_id)
        return {
            "product_id": product_id,
            "sentiment_score": signals["sentiment"],
            "trending_score": signals["trending"],
            "mentions_count": signals["mentions"],
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error fetching social signals: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/signals/weather")
async def get_weather_signals(location: str, product_id: str):
    """
    Get weather signals for a location and product
    """
    try:
        weather_data = await forecasting_service.get_weather_signals(location, product_id)
        return {
            "location": location,
            "product_id": product_id,
            "weather_impact": weather_data["impact"],
            "forecast": weather_data["forecast"],
            "correlation_score": weather_data["correlation"]
        }
    except Exception as e:
        logger.error(f"Error fetching weather signals: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/accuracy/metrics")
async def get_forecast_accuracy():
    """
    Get forecast accuracy metrics
    """
    try:
        metrics = await forecasting_service.get_accuracy_metrics()
        return {
            "mape": metrics["mape"],
            "rmse": metrics["rmse"],
            "mae": metrics["mae"],
            "overall_accuracy": metrics["overall_accuracy"],
            "last_evaluation": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error fetching accuracy metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/models/retrain")
async def retrain_models(background_tasks: BackgroundTasks):
    """
    Trigger model retraining
    """
    try:
        background_tasks.add_task(forecasting_service.retrain_models)
        return {
            "message": "Model retraining started",
            "status": "processing",
            "estimated_completion": datetime.now() + timedelta(hours=2)
        }
    except Exception as e:
        logger.error(f"Error starting model retraining: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 