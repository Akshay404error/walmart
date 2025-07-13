import asyncio
import logging
from datetime import datetime, timedelta, date
from typing import List, Dict, Any, Optional
import numpy as np

from models.customer_models import (
    PreOrder, ComingSoonInterest, DemandLock, CustomerPreferences,
    CustomerEngagementMetrics
)

logger = logging.getLogger(__name__)

class CustomerService:
    def __init__(self):
        self.preorders = []
        self.coming_soon_interests = []
        self.demand_locks = []
        self.customer_preferences = {}
        
    async def create_preorder(
        self,
        customer_id: str,
        product_id: str,
        store_id: str,
        quantity: int,
        expected_availability: date
    ) -> Dict[str, Any]:
        """Create a pre-order for a customer"""
        try:
            logger.info(f"Creating pre-order for customer {customer_id}")
            
            # Generate pre-order ID
            preorder_id = f"PO_{len(self.preorders):06d}"
            
            # Create pre-order
            preorder = PreOrder(
                preorder_id=preorder_id,
                customer_id=customer_id,
                product_id=product_id,
                store_id=store_id,
                quantity=quantity,
                status="pending",
                created_at=datetime.now(),
                expected_availability=expected_availability
            )
            
            self.preorders.append(preorder)
            
            return {
                "preorder_id": preorder_id,
                "status": "created",
                "created_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error creating pre-order: {e}")
            raise
    
    async def get_customer_preorders(self, customer_id: str) -> List[Dict[str, Any]]:
        """Get all pre-orders for a customer"""
        try:
            customer_preorders = [
                p for p in self.preorders if p.customer_id == customer_id
            ]
            
            return [
                {
                    "preorder_id": p.preorder_id,
                    "product_id": p.product_id,
                    "store_id": p.store_id,
                    "quantity": p.quantity,
                    "status": p.status,
                    "created_at": p.created_at.isoformat(),
                    "expected_availability": p.expected_availability.isoformat(),
                    "fulfilled_at": p.fulfilled_at.isoformat() if p.fulfilled_at else None
                }
                for p in customer_preorders
            ]
            
        except Exception as e:
            logger.error(f"Error getting customer pre-orders: {e}")
            raise
    
    async def register_coming_soon_interest(
        self,
        customer_id: str,
        product_id: str,
        store_id: str
    ):
        """Register customer interest in coming soon products"""
        try:
            logger.info(f"Registering interest for customer {customer_id}")
            
            # Check if interest already exists
            existing_interest = next(
                (i for i in self.coming_soon_interests 
                 if i.customer_id == customer_id and i.product_id == product_id),
                None
            )
            
            if existing_interest:
                logger.info(f"Interest already registered for customer {customer_id}")
                return
            
            # Create new interest
            interest = ComingSoonInterest(
                interest_id=f"INT_{len(self.coming_soon_interests):06d}",
                customer_id=customer_id,
                product_id=product_id,
                store_id=store_id,
                registered_at=datetime.now(),
                notified=False
            )
            
            self.coming_soon_interests.append(interest)
            
        except Exception as e:
            logger.error(f"Error registering interest: {e}")
            raise
    
    async def get_coming_soon_interests(
        self,
        product_id: Optional[str] = None,
        store_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get customer interests for coming soon products"""
        try:
            interests = self.coming_soon_interests
            
            if product_id:
                interests = [i for i in interests if i.product_id == product_id]
            
            if store_id:
                interests = [i for i in interests if i.store_id == store_id]
            
            return [
                {
                    "interest_id": i.interest_id,
                    "customer_id": i.customer_id,
                    "product_id": i.product_id,
                    "store_id": i.store_id,
                    "registered_at": i.registered_at.isoformat(),
                    "notified": i.notified
                }
                for i in interests
            ]
            
        except Exception as e:
            logger.error(f"Error getting coming soon interests: {e}")
            raise
    
    async def lock_demand(
        self,
        customer_id: str,
        product_id: str,
        quantity: int,
        lock_duration_days: int = 7
    ) -> Dict[str, Any]:
        """Lock customer demand for a specific period"""
        try:
            logger.info(f"Locking demand for customer {customer_id}")
            
            # Generate lock ID
            lock_id = f"LOCK_{len(self.demand_locks):06d}"
            
            # Create demand lock
            demand_lock = DemandLock(
                lock_id=lock_id,
                customer_id=customer_id,
                product_id=product_id,
                quantity=quantity,
                created_at=datetime.now(),
                expires_at=datetime.now() + timedelta(days=lock_duration_days),
                status="active"
            )
            
            self.demand_locks.append(demand_lock)
            
            return {
                "lock_id": lock_id,
                "expires_at": demand_lock.expires_at.isoformat(),
                "quantity": quantity
            }
            
        except Exception as e:
            logger.error(f"Error locking demand: {e}")
            raise
    
    async def update_preferences(self, customer_id: str, preferences: CustomerPreferences):
        """Update customer notification preferences"""
        try:
            logger.info(f"Updating preferences for customer {customer_id}")
            
            self.customer_preferences[customer_id] = preferences
            
        except Exception as e:
            logger.error(f"Error updating preferences: {e}")
            raise
    
    async def get_preferences(self, customer_id: str) -> CustomerPreferences:
        """Get customer notification preferences"""
        try:
            return self.customer_preferences.get(customer_id, CustomerPreferences())
            
        except Exception as e:
            logger.error(f"Error getting preferences: {e}")
            raise
    
    async def get_engagement_analytics(
        self,
        start_date: str,
        end_date: str,
        store_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get customer engagement analytics"""
        try:
            # Mock engagement analytics
            total_preorders = len(self.preorders)
            active_customers = len(set(p.customer_id for p in self.preorders))
            engagement_rate = np.random.uniform(0.6, 0.9)
            conversion_rate = np.random.uniform(0.3, 0.6)
            
            details = {
                "new_customers": np.random.randint(10, 50),
                "returning_customers": np.random.randint(20, 80),
                "average_order_value": np.random.uniform(50, 150),
                "customer_satisfaction": np.random.uniform(0.7, 0.95)
            }
            
            return {
                "total_preorders": total_preorders,
                "active_customers": active_customers,
                "engagement_rate": engagement_rate,
                "conversion_rate": conversion_rate,
                "details": details
            }
            
        except Exception as e:
            logger.error(f"Error getting engagement analytics: {e}")
            raise 