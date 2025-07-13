import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="FestAI - Intelligent Demand Management",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .alert-card {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
    }
    .success-card {
        background-color: #d1edff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🎯 FestAI Dashboard")
st.sidebar.markdown("---")

# Navigation
page = st.sidebar.selectbox(
    "Navigation",
    ["📊 Overview", "🔮 Forecasting", "📦 Inventory", "👥 Customers", "🏭 Suppliers", "🌱 Sustainability"]
)

# Mock API base URL
API_BASE_URL = "http://localhost:8000"

def mock_api_call(endpoint, method="GET", data=None):
    """Mock API calls for demo purposes"""
    try:
        # In real implementation, this would make actual HTTP requests
        if endpoint == "/dashboard":
            return {
                "forecasts": [
                    {"product_id": f"PROD_{i:03d}", "forecast_value": np.random.uniform(50, 200), 
                     "confidence": np.random.uniform(0.7, 0.95), "generated_at": datetime.now().isoformat()}
                    for i in range(10)
                ],
                "inventory_alerts": [
                    {"product_id": f"PROD_{i:03d}", "alert_type": "low_stock", "severity": "high", 
                     "message": f"Low stock alert for product {i+1}"}
                    for i in range(5)
                ],
                "pending_notifications": np.random.randint(10, 50),
                "system_status": "operational"
            }
        elif endpoint.startswith("/api/forecast"):
            return {
                "predictions": [np.random.uniform(80, 120) for _ in range(30)],
                "confidence_intervals": {
                    "lower": [np.random.uniform(60, 100) for _ in range(30)],
                    "upper": [np.random.uniform(100, 140) for _ in range(30)]
                }
            }
        elif endpoint.startswith("/api/inventory"):
            return {
                "items": [
                    {"product_id": f"PROD_{i:03d}", "current_quantity": np.random.randint(0, 100),
                     "status": np.random.choice(["in_stock", "low_stock", "out_of_stock"]),
                     "days_of_inventory": np.random.uniform(1, 30)}
                    for i in range(20)
                ]
            }
        else:
            return {"data": "Mock response"}
    except Exception as e:
        st.error(f"API Error: {e}")
        return None

# Overview Page
if page == "📊 Overview":
    st.markdown('<h1 class="main-header">FestAI Dashboard</h1>', unsafe_allow_html=True)
    
    # Get dashboard data
    dashboard_data = mock_api_call("/dashboard")
    
    if dashboard_data:
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Active Forecasts",
                value=len(dashboard_data["forecasts"]),
                delta="+5%"
            )
        
        with col2:
            st.metric(
                label="Critical Alerts",
                value=len(dashboard_data["inventory_alerts"]),
                delta="-2",
                delta_color="inverse"
            )
        
        with col3:
            st.metric(
                label="Pending Notifications",
                value=dashboard_data["pending_notifications"],
                delta="+12"
            )
        
        with col4:
            status_color = "🟢" if dashboard_data["system_status"] == "operational" else "🔴"
            st.metric(
                label="System Status",
                value=f"{status_color} {dashboard_data['system_status'].title()}"
            )
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Recent Forecasts")
            if dashboard_data["forecasts"]:
                df_forecasts = pd.DataFrame(dashboard_data["forecasts"])
                fig = px.bar(
                    df_forecasts.head(10),
                    x="product_id",
                    y="forecast_value",
                    color="confidence",
                    title="Top 10 Product Forecasts",
                    color_continuous_scale="viridis"
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("⚠️ Critical Alerts")
            if dashboard_data["inventory_alerts"]:
                df_alerts = pd.DataFrame(dashboard_data["inventory_alerts"])
                alert_counts = df_alerts["alert_type"].value_counts()
                fig = px.pie(
                    values=alert_counts.values,
                    names=alert_counts.index,
                    title="Alert Distribution by Type"
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        # Recent Activity
        st.subheader("🕒 Recent Activity")
        activity_data = [
            {"time": "2 min ago", "action": "Forecast generated for PROD_001", "user": "System"},
            {"time": "5 min ago", "action": "Reorder request sent to Supplier A", "user": "Auto"},
            {"time": "8 min ago", "action": "Customer pre-order created", "user": "Customer"},
            {"time": "12 min ago", "action": "Markdown triggered for perishable item", "user": "System"},
            {"time": "15 min ago", "action": "Weather signal updated", "user": "System"}
        ]
        
        for activity in activity_data:
            st.markdown(f"**{activity['time']}** - {activity['action']} (by {activity['user']})")

# Forecasting Page
elif page == "🔮 Forecasting":
    st.title("🔮 Demand Forecasting")
    
    # Forecast Generation
    st.subheader("Generate New Forecast")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        product_ids = st.multiselect(
            "Select Products",
            [f"PROD_{i:03d}" for i in range(1, 101)],
            default=["PROD_001", "PROD_002", "PROD_003"]
        )
    
    with col2:
        forecast_period = st.selectbox(
            "Forecast Period",
            ["week", "month", "quarter", "year"]
        )
    
    with col3:
        include_signals = st.checkbox("Include External Signals", value=True)
    
    if st.button("🚀 Generate Forecast", type="primary"):
        if product_ids:
            with st.spinner("Generating forecasts..."):
                # Simulate forecast generation
                progress_bar = st.progress(0)
                for i in range(100):
                    progress_bar.progress(i + 1)
                    st.empty()
                
                st.success(f"✅ Forecast generated for {len(product_ids)} products!")
                
                # Show forecast results
                st.subheader("Forecast Results")
                
                # Mock forecast data
                forecast_results = []
                for product_id in product_ids:
                    forecast_data = mock_api_call(f"/api/forecast/{product_id}")
                    if forecast_data:
                        forecast_results.append({
                            "product_id": product_id,
                            "predictions": forecast_data["predictions"],
                            "confidence_intervals": forecast_data["confidence_intervals"]
                        })
                
                if forecast_results:
                    # Plot forecasts
                    fig = make_subplots(
                        rows=len(forecast_results), cols=1,
                        subplot_titles=[f"Forecast for {r['product_id']}" for r in forecast_results],
                        vertical_spacing=0.1
                    )
                    
                    for i, result in enumerate(forecast_results):
                        dates = pd.date_range(start=datetime.now(), periods=len(result["predictions"]), freq="D")
                        
                        fig.add_trace(
                            go.Scatter(
                                x=dates,
                                y=result["predictions"],
                                mode="lines+markers",
                                name=f"{result['product_id']} - Predicted",
                                line=dict(color=f"rgb({50 + i*50}, {100 + i*30}, {150 + i*20})")
                            ),
                            row=i+1, col=1
                        )
                        
                        fig.add_trace(
                            go.Scatter(
                                x=dates,
                                y=result["confidence_intervals"]["upper"],
                                mode="lines",
                                line=dict(width=0),
                                showlegend=False,
                                fillcolor=f"rgba({50 + i*50}, {100 + i*30}, {150 + i*20}, 0.2)",
                                fill="tonexty"
                            ),
                            row=i+1, col=1
                        )
                        
                        fig.add_trace(
                            go.Scatter(
                                x=dates,
                                y=result["confidence_intervals"]["lower"],
                                mode="lines",
                                line=dict(width=0),
                                showlegend=False,
                                fillcolor=f"rgba({50 + i*50}, {100 + i*30}, {150 + i*20}, 0.2)",
                                fill="tonexty"
                            ),
                            row=i+1, col=1
                        )
                    
                    fig.update_layout(height=300 * len(forecast_results), showlegend=True)
                    st.plotly_chart(fig, use_container_width=True)

# Inventory Page
elif page == "📦 Inventory":
    st.title("📦 Inventory Management")
    
    # Inventory Status
    st.subheader("Current Inventory Status")
    
    inventory_data = mock_api_call("/api/inventory/status")
    
    if inventory_data and "items" in inventory_data:
        df_inventory = pd.DataFrame(inventory_data["items"])
        
        # Status distribution
        col1, col2 = st.columns(2)
        
        with col1:
            status_counts = df_inventory["status"].value_counts()
            fig = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                title="Inventory Status Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.scatter(
                df_inventory,
                x="current_quantity",
                y="days_of_inventory",
                color="status",
                size="current_quantity",
                hover_data=["product_id"],
                title="Inventory Levels vs Days of Inventory"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Inventory table
        st.subheader("Detailed Inventory View")
        st.dataframe(df_inventory, use_container_width=True)
        
        # Critical alerts
        st.subheader("🚨 Critical Alerts")
        critical_items = df_inventory[df_inventory["status"] == "out_of_stock"]
        
        if not critical_items.empty:
            for _, item in critical_items.iterrows():
                st.markdown(f"""
                <div class="alert-card">
                    <strong>⚠️ {item['product_id']}</strong><br>
                    Status: {item['status'].replace('_', ' ').title()}<br>
                    Current Quantity: {item['current_quantity']}<br>
                    Days of Inventory: {item['days_of_inventory']:.1f}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ No critical alerts at this time!")

# Customers Page
elif page == "👥 Customers":
    st.title("👥 Customer Engagement")
    
    # Pre-order System
    st.subheader("Pre-Order Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Create Pre-Order")
        
        customer_id = st.text_input("Customer ID", "CUST_001")
        product_id = st.selectbox("Product", [f"PROD_{i:03d}" for i in range(1, 21)])
        quantity = st.number_input("Quantity", min_value=1, value=1)
        expected_date = st.date_input("Expected Availability", value=datetime.now() + timedelta(days=7))
        
        if st.button("📝 Create Pre-Order"):
            st.success(f"✅ Pre-order created for {customer_id} - {product_id}")
    
    with col2:
        st.markdown("### Customer Analytics")
        
        # Mock customer analytics
        analytics_data = {
            "total_preorders": 156,
            "active_customers": 89,
            "engagement_rate": 0.73,
            "conversion_rate": 0.42
        }
        
        for metric, value in analytics_data.items():
            if isinstance(value, float):
                st.metric(metric.replace("_", " ").title(), f"{value:.2%}")
            else:
                st.metric(metric.replace("_", " ").title(), value)
    
    # Coming Soon Interest
    st.subheader("Coming Soon Interest")
    
    # Mock coming soon data
    coming_soon_data = [
        {"product_id": "PROD_101", "interests": 45, "category": "Electronics"},
        {"product_id": "PROD_102", "interests": 32, "category": "Clothing"},
        {"product_id": "PROD_103", "interests": 28, "category": "Home & Garden"},
        {"product_id": "PROD_104", "interests": 19, "category": "Sports"},
    ]
    
    df_coming_soon = pd.DataFrame(coming_soon_data)
    fig = px.bar(
        df_coming_soon,
        x="product_id",
        y="interests",
        color="category",
        title="Customer Interest in Coming Soon Products"
    )
    st.plotly_chart(fig, use_container_width=True)

# Suppliers Page
elif page == "🏭 Suppliers":
    st.title("🏭 Supplier Management")
    
    # Supplier Orders
    st.subheader("Supplier Orders")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Create Supplier Order")
        
        supplier_id = st.selectbox("Supplier", ["SUP_001", "SUP_002", "SUP_003"])
        products = st.multiselect("Products", [f"PROD_{i:03d}" for i in range(1, 21)])
        quantities = st.text_input("Quantities (comma-separated)", "10, 20, 15")
        delivery_date = st.date_input("Expected Delivery", value=datetime.now() + timedelta(days=14))
        
        if st.button("📋 Create Order"):
            st.success(f"✅ Order created for {supplier_id}")
    
    with col2:
        st.markdown("### Supplier Performance")
        
        # Mock performance metrics
        performance_data = {
            "on_time_delivery": 0.94,
            "quality_score": 0.87,
            "cost_efficiency": 0.91,
            "collaboration_score": 0.89
        }
        
        for metric, value in performance_data.items():
            st.metric(metric.replace("_", " ").title(), f"{value:.1%}")
    
    # Blockchain Transparency
    st.subheader("🔗 Blockchain Order Transparency")
    
    # Mock blockchain data
    blockchain_data = [
        {"order_id": "ORD_001", "supplier": "SUP_001", "status": "confirmed", "hash": "0x1234..."},
        {"order_id": "ORD_002", "supplier": "SUP_002", "status": "pending", "hash": "0x5678..."},
        {"order_id": "ORD_003", "supplier": "SUP_001", "status": "delivered", "hash": "0x9abc..."},
    ]
    
    df_blockchain = pd.DataFrame(blockchain_data)
    st.dataframe(df_blockchain, use_container_width=True)

# Sustainability Page
elif page == "🌱 Sustainability":
    st.title("🌱 Sustainability & Waste Reduction")
    
    # Waste Reduction Metrics
    st.subheader("Waste Reduction Analytics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Waste Reduced",
            "23.5%",
            delta="+5.2%",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            "Cost Savings",
            "$45,230",
            delta="+$2,100",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            "Carbon Footprint",
            "12.3 tons CO2",
            delta="-1.8 tons",
            delta_color="inverse"
        )
    
    # Perishable Item Management
    st.subheader("Perishable Item Management")
    
    # Mock perishable data
    perishable_data = [
        {"product_id": "PROD_001", "current_quantity": 45, "days_until_expiry": 2, "markdown_percentage": 0.3},
        {"product_id": "PROD_002", "current_quantity": 23, "days_until_expiry": 1, "markdown_percentage": 0.5},
        {"product_id": "PROD_003", "current_quantity": 67, "days_until_expiry": 5, "markdown_percentage": 0.2},
        {"product_id": "PROD_004", "current_quantity": 12, "days_until_expiry": 0, "markdown_percentage": 0.7},
    ]
    
    df_perishable = pd.DataFrame(perishable_data)
    
    fig = px.scatter(
        df_perishable,
        x="days_until_expiry",
        y="current_quantity",
        size="markdown_percentage",
        color="markdown_percentage",
        hover_data=["product_id"],
        title="Perishable Items - Expiry vs Quantity",
        color_continuous_scale="reds"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Sustainability Score
    st.subheader("🌍 Overall Sustainability Score")
    
    sustainability_score = 0.87
    st.progress(sustainability_score)
    st.markdown(f"**Current Score: {sustainability_score:.1%}**")
    
    if sustainability_score >= 0.8:
        st.success("🎉 Excellent sustainability performance!")
    elif sustainability_score >= 0.6:
        st.warning("⚠️ Good performance, room for improvement")
    else:
        st.error("❌ Needs immediate attention")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>🎯 FestAI - Intelligent Seasonal Demand Management Platform</p>
        <p>Powered by AI • Built for Sustainability • Designed for Efficiency</p>
    </div>
    """,
    unsafe_allow_html=True
) 