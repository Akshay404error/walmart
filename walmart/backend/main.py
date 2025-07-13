from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from datetime import datetime, timedelta
import logging

from api.forecast import router as forecast_router
from api.inventory import router as inventory_router
from api.customers import router as customers_router
from api.suppliers import router as suppliers_router
from services.forecasting_service import ForecastingService
from services.inventory_service import InventoryService
from services.notification_service import NotificationService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="FestAI - Intelligent Seasonal Demand Management",
    description="AI-powered supply chain optimization platform for retail operations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(forecast_router, prefix="/api/forecast", tags=["Forecasting"])
app.include_router(inventory_router, prefix="/api/inventory", tags=["Inventory"])
app.include_router(customers_router, prefix="/api/customers", tags=["Customers"])
app.include_router(suppliers_router, prefix="/api/suppliers", tags=["Suppliers"])

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "FestAI Backend",
        "version": "1.0.0"
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "message": "Welcome to FestAI - Intelligent Seasonal Demand Management Platform",
        "docs": "/docs",
        "health": "/health",
        "version": "1.0.0"
    }

# Dashboard endpoint
@app.get("/dashboard")
async def dashboard():
    """Dashboard overview endpoint"""
    try:
        # Initialize services
        forecasting_service = ForecastingService()
        inventory_service = InventoryService()
        notification_service = NotificationService()
        
        # Get dashboard data
        dashboard_data = {
            "forecasts": await forecasting_service.get_recent_forecasts(),
            "inventory_alerts": await inventory_service.get_critical_alerts(),
            "pending_notifications": await notification_service.get_pending_count(),
            "system_status": "operational",
            "last_updated": datetime.now().isoformat()
        }
        
        return dashboard_data
    except Exception as e:
        logger.error(f"Error fetching dashboard data: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch dashboard data")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 