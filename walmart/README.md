# 🎯 FestAI - Intelligent Seasonal Demand Management Platform

## Overview
FestAI is an intelligent, fully-automated seasonal demand management platform that transforms supply chain efficiency for retail operations. This prototype demonstrates the core features outlined in the Walmart Idea proposal.

## 🚀 Key Features

### 1. Multi-Signal Forecasting
- Historical sales data analysis
- Social media trend integration
- Weather data correlation
- Event calendar impact assessment

### 2. Dynamic Replenishment Automation
- Real-time threshold calculations
- Automated purchase order generation
- Proactive supplier notifications

### 3. Customer Engagement
- Pre-order system
- "Coming Soon" notifications
- Demand locking mechanisms

### 4. Sustainability Optimization
- Perishable item management
- Automated markdown triggers
- Waste reduction analytics

## 🏗️ Architecture

```
├── backend/                 # FastAPI backend services
│   ├── api/                # API endpoints
│   ├── models/             # ML models and forecasting
│   ├── services/           # Business logic
│   └── utils/              # Utility functions
├── frontend/               # React.js dashboard
├── ml_pipeline/            # ML model training and inference
├── data_ingestion/         # Data collection services
└── notifications/          # Communication services
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** - High-performance web framework
- **SQLAlchemy** - Database ORM
- **Celery** - Task queue for background jobs
- **Redis** - Caching and message broker

### Machine Learning
- **Prophet** - Time series forecasting
- **XGBoost** - Gradient boosting
- **TensorFlow** - Deep learning models
- **Scikit-learn** - Traditional ML algorithms

### Frontend
- **React.js** - User interface
- **Streamlit** - Data visualization dashboard
- **Plotly** - Interactive charts

### External Services
- **Firebase** - Real-time database
- **BigQuery** - Data warehouse
- **Twilio** - SMS notifications
- **SendGrid** - Email services

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Redis server
- PostgreSQL database

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd festai-prototype
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Install Node.js dependencies**
```bash
cd frontend
npm install
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run the application**
```bash
# Start backend
uvicorn backend.main:app --reload

# Start frontend (in another terminal)
cd frontend
npm start

# Start ML pipeline
python ml_pipeline/main.py
```

## 📊 Demo Features

### 1. Demand Forecasting Dashboard
- Real-time demand predictions
- Multi-signal analysis visualization
- Historical vs predicted comparisons

### 2. Inventory Management
- Dynamic threshold monitoring
- Automated reorder suggestions
- Supplier communication logs

### 3. Customer Engagement
- Pre-order system simulation
- Notification management
- Customer preference tracking

### 4. Sustainability Metrics
- Waste reduction tracking
- Carbon footprint estimation
- Perishable item optimization

## 🔧 Configuration

### Environment Variables
```env
# Database
DATABASE_URL=postgresql://user:password@localhost/festai

# External APIs
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
SENDGRID_API_KEY=your_sendgrid_key

# ML Models
MODEL_STORAGE_PATH=./models
DATA_STORAGE_PATH=./data

# Firebase
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
```

## 📈 API Endpoints

### Forecasting
- `POST /api/forecast/generate` - Generate demand forecast
- `GET /api/forecast/{product_id}` - Get forecast for specific product
- `GET /api/forecast/trends` - Get trend analysis

### Inventory
- `GET /api/inventory/status` - Current inventory status
- `POST /api/inventory/reorder` - Generate reorder request
- `GET /api/inventory/thresholds` - Dynamic thresholds

### Customers
- `POST /api/customers/preorder` - Create pre-order
- `GET /api/customers/notifications` - Notification history
- `POST /api/customers/notify` - Send notifications

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions, please open an issue in the repository or contact the development team. 