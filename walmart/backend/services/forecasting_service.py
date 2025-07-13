import asyncio
import logging
from datetime import datetime, timedelta, date
from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np
from prophet import Prophet
import xgboost as xgb
from sklearn.metrics import mean_absolute_error, mean_squared_error
import json

from models.forecast_models import (
    ForecastData, SocialSignal, WeatherSignal, EventSignal,
    MultiSignalForecast, ModelAccuracy, TrendAnalysis
)

logger = logging.getLogger(__name__)

class ForecastingService:
    def __init__(self):
        self.models = {}
        self.signal_weights = {
            'pos': 0.4,
            'social': 0.2,
            'weather': 0.2,
            'events': 0.2
        }
        self.model_versions = {
            'prophet': '1.0.0',
            'xgboost': '1.0.0',
            'ensemble': '1.0.0'
        }
        
    async def generate_forecast_async(
        self,
        product_ids: List[str],
        forecast_period: str,
        include_external_signals: bool = True
    ):
        """Generate forecasts asynchronously for multiple products"""
        try:
            logger.info(f"Starting async forecast generation for {len(product_ids)} products")
            
            # Generate forecasts for each product
            forecasts = []
            for product_id in product_ids:
                forecast = await self._generate_single_forecast(
                    product_id, forecast_period, include_external_signals
                )
                forecasts.append(forecast)
                
            # Store forecasts
            await self._store_forecasts(forecasts)
            
            logger.info(f"Completed forecast generation for {len(product_ids)} products")
            return forecasts
            
        except Exception as e:
            logger.error(f"Error in async forecast generation: {e}")
            raise
    
    async def _generate_single_forecast(
        self,
        product_id: str,
        forecast_period: str,
        include_external_signals: bool
    ) -> MultiSignalForecast:
        """Generate forecast for a single product"""
        try:
            # Get historical data
            historical_data = await self._get_historical_data(product_id)
            
            # Generate base forecast using Prophet
            base_forecast = await self._generate_prophet_forecast(historical_data, forecast_period)
            
            # Apply external signals if requested
            social_adjustment = 0.0
            weather_adjustment = 0.0
            event_adjustment = 0.0
            
            if include_external_signals:
                social_adjustment = await self._calculate_social_adjustment(product_id)
                weather_adjustment = await self._calculate_weather_adjustment(product_id)
                event_adjustment = await self._calculate_event_adjustment(product_id)
            
            # Calculate final forecast
            final_forecast = (
                base_forecast * (1 + social_adjustment + weather_adjustment + event_adjustment)
            )
            
            # Calculate confidence intervals
            confidence_interval = self._calculate_confidence_interval(
                base_forecast, social_adjustment, weather_adjustment, event_adjustment
            )
            
            return MultiSignalForecast(
                product_id=product_id,
                base_forecast=base_forecast,
                social_adjustment=social_adjustment,
                weather_adjustment=weather_adjustment,
                event_adjustment=event_adjustment,
                final_forecast=final_forecast,
                signal_weights=self.signal_weights,
                confidence_interval=confidence_interval,
                generated_at=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Error generating forecast for product {product_id}: {e}")
            raise
    
    async def _get_historical_data(self, product_id: str) -> pd.DataFrame:
        """Get historical sales data for a product"""
        # Mock data - in real implementation, this would fetch from database
        dates = pd.date_range(start='2023-01-01', end=datetime.now().date(), freq='D')
        np.random.seed(hash(product_id) % 2**32)
        
        # Generate realistic sales data with seasonality
        base_sales = 100
        seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * dates.dayofyear / 365)
        trend_factor = 1 + 0.001 * np.arange(len(dates))
        noise = np.random.normal(0, 0.1, len(dates))
        
        sales = base_sales * seasonal_factor * trend_factor * (1 + noise)
        sales = np.maximum(sales, 0)  # Ensure non-negative sales
        
        return pd.DataFrame({
            'ds': dates,
            'y': sales
        })
    
    async def _generate_prophet_forecast(self, data: pd.DataFrame, forecast_period: str) -> float:
        """Generate forecast using Prophet model"""
        try:
            # Initialize and fit Prophet model
            model = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=True,
                daily_seasonality=False,
                seasonality_mode='multiplicative'
            )
            
            model.fit(data)
            
            # Create future dataframe
            if forecast_period == 'week':
                periods = 7
            elif forecast_period == 'month':
                periods = 30
            elif forecast_period == 'quarter':
                periods = 90
            else:  # year
                periods = 365
                
            future = model.make_future_dataframe(periods=periods)
            forecast = model.predict(future)
            
            # Return the average forecast for the period
            return forecast['yhat'].tail(periods).mean()
            
        except Exception as e:
            logger.error(f"Error in Prophet forecast: {e}")
            # Return simple moving average as fallback
            return data['y'].tail(30).mean()
    
    async def _calculate_social_adjustment(self, product_id: str) -> float:
        """Calculate adjustment based on social media signals"""
        try:
            # Mock social signals - in real implementation, fetch from social media APIs
            sentiment_score = np.random.uniform(-0.5, 0.5)
            trending_score = np.random.uniform(0, 1)
            mentions_count = np.random.randint(0, 1000)
            
            # Calculate adjustment factor
            adjustment = (
                sentiment_score * 0.3 +
                trending_score * 0.4 +
                min(mentions_count / 1000, 1) * 0.3
            ) * 0.2  # Scale factor
            
            return adjustment
            
        except Exception as e:
            logger.error(f"Error calculating social adjustment: {e}")
            return 0.0
    
    async def _calculate_weather_adjustment(self, product_id: str) -> float:
        """Calculate adjustment based on weather signals"""
        try:
            # Mock weather data - in real implementation, fetch from weather APIs
            temperature = np.random.uniform(0, 100)
            humidity = np.random.uniform(0, 100)
            precipitation = np.random.uniform(0, 10)
            
            # Simple weather impact model
            temp_impact = (temperature - 50) / 100  # Normalize temperature
            humidity_impact = (humidity - 50) / 100  # Normalize humidity
            precip_impact = -precipitation / 10  # Negative impact of precipitation
            
            adjustment = (temp_impact + humidity_impact + precip_impact) / 3 * 0.15
            
            return adjustment
            
        except Exception as e:
            logger.error(f"Error calculating weather adjustment: {e}")
            return 0.0
    
    async def _calculate_event_adjustment(self, product_id: str) -> float:
        """Calculate adjustment based on event signals"""
        try:
            # Mock event data - in real implementation, fetch from event calendars
            upcoming_events = np.random.randint(0, 5)
            event_impact = np.random.uniform(-0.3, 0.3)
            
            adjustment = upcoming_events * event_impact * 0.1
            
            return adjustment
            
        except Exception as e:
            logger.error(f"Error calculating event adjustment: {e}")
            return 0.0
    
    def _calculate_confidence_interval(
        self,
        base_forecast: float,
        social_adjustment: float,
        weather_adjustment: float,
        event_adjustment: float
    ) -> Dict[str, float]:
        """Calculate confidence intervals for the forecast"""
        # Calculate uncertainty based on signal adjustments
        total_adjustment = abs(social_adjustment) + abs(weather_adjustment) + abs(event_adjustment)
        uncertainty_factor = 1 + total_adjustment
        
        confidence_level = 0.95
        z_score = 1.96  # 95% confidence interval
        
        margin_of_error = base_forecast * 0.1 * uncertainty_factor * z_score
        
        return {
            'lower_bound': max(0, base_forecast - margin_of_error),
            'upper_bound': base_forecast + margin_of_error,
            'confidence_level': confidence_level
        }
    
    async def get_product_forecast(self, product_id: str, days: int = 30) -> Dict[str, Any]:
        """Get forecast for a specific product"""
        try:
            # Generate forecast
            forecast = await self._generate_single_forecast(
                product_id, 'month', include_external_signals=True
            )
            
            # Generate daily predictions
            historical_data = await self._get_historical_data(product_id)
            model = Prophet(yearly_seasonality=True, weekly_seasonality=True)
            model.fit(historical_data)
            
            future = model.make_future_dataframe(periods=days)
            predictions = model.predict(future)
            
            return {
                'predictions': predictions['yhat'].tail(days).tolist(),
                'confidence_intervals': {
                    'lower': predictions['yhat_lower'].tail(days).tolist(),
                    'upper': predictions['yhat_upper'].tail(days).tolist()
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting product forecast: {e}")
            raise
    
    async def analyze_trends(
        self,
        product_ids: Optional[List[str]] = None,
        category: Optional[str] = None,
        time_period: str = "30d"
    ) -> TrendAnalysis:
        """Analyze trends for products or categories"""
        try:
            # Mock trend analysis
            trends = []
            for i in range(5):
                trends.append({
                    'trend_name': f'Trend {i+1}',
                    'direction': np.random.choice(['increasing', 'decreasing', 'stable']),
                    'strength': np.random.uniform(0.1, 0.9),
                    'confidence': np.random.uniform(0.7, 0.95)
                })
            
            seasonality = {
                'weekly': np.random.uniform(0.8, 1.2),
                'monthly': np.random.uniform(0.9, 1.1),
                'yearly': np.random.uniform(0.7, 1.3)
            }
            
            anomalies = [
                {
                    'date': (datetime.now() - timedelta(days=i)).isoformat(),
                    'severity': np.random.uniform(0.1, 0.9),
                    'description': f'Anomaly {i+1}'
                }
                for i in range(3)
            ]
            
            return TrendAnalysis(
                product_ids=product_ids or [],
                category=category,
                time_period=time_period,
                trends=trends,
                seasonality=seasonality,
                anomalies=anomalies,
                confidence_score=np.random.uniform(0.7, 0.95),
                generated_at=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Error analyzing trends: {e}")
            raise
    
    async def get_social_signals(self, product_id: str) -> Dict[str, Any]:
        """Get social media signals for a product"""
        try:
            # Mock social signals
            return {
                'sentiment': np.random.uniform(-0.5, 0.5),
                'trending': np.random.uniform(0, 1),
                'mentions': np.random.randint(0, 1000)
            }
        except Exception as e:
            logger.error(f"Error getting social signals: {e}")
            raise
    
    async def get_weather_signals(self, location: str, product_id: str) -> Dict[str, Any]:
        """Get weather signals for a location and product"""
        try:
            # Mock weather data
            return {
                'impact': np.random.uniform(-0.3, 0.3),
                'forecast': {
                    'temperature': np.random.uniform(0, 100),
                    'humidity': np.random.uniform(0, 100),
                    'precipitation': np.random.uniform(0, 10)
                },
                'correlation': np.random.uniform(0.1, 0.8)
            }
        except Exception as e:
            logger.error(f"Error getting weather signals: {e}")
            raise
    
    async def get_accuracy_metrics(self) -> Dict[str, float]:
        """Get forecast accuracy metrics"""
        try:
            # Mock accuracy metrics
            return {
                'mape': np.random.uniform(5, 15),
                'rmse': np.random.uniform(10, 30),
                'mae': np.random.uniform(8, 25),
                'overall_accuracy': np.random.uniform(0.8, 0.95)
            }
        except Exception as e:
            logger.error(f"Error getting accuracy metrics: {e}")
            raise
    
    async def get_recent_forecasts(self) -> List[Dict[str, Any]]:
        """Get recent forecasts for dashboard"""
        try:
            # Mock recent forecasts
            return [
                {
                    'product_id': f'PROD_{i:03d}',
                    'forecast_value': np.random.uniform(50, 200),
                    'confidence': np.random.uniform(0.7, 0.95),
                    'generated_at': (datetime.now() - timedelta(hours=i)).isoformat()
                }
                for i in range(10)
            ]
        except Exception as e:
            logger.error(f"Error getting recent forecasts: {e}")
            raise
    
    async def retrain_models(self):
        """Retrain all forecasting models"""
        try:
            logger.info("Starting model retraining...")
            
            # Simulate retraining process
            await asyncio.sleep(2)
            
            # Update model versions
            for model_name in self.model_versions:
                version_parts = self.model_versions[model_name].split('.')
                version_parts[2] = str(int(version_parts[2]) + 1)
                self.model_versions[model_name] = '.'.join(version_parts)
            
            logger.info("Model retraining completed")
            
        except Exception as e:
            logger.error(f"Error retraining models: {e}")
            raise
    
    async def _store_forecasts(self, forecasts: List[MultiSignalForecast]):
        """Store forecasts in database"""
        try:
            # Mock storage - in real implementation, save to database
            logger.info(f"Storing {len(forecasts)} forecasts")
            await asyncio.sleep(0.1)  # Simulate storage time
            
        except Exception as e:
            logger.error(f"Error storing forecasts: {e}")
            raise 