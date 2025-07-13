# 🎯 FestAI - Intelligent Seasonal Demand Management Platform

## Overview
FestAI is an intelligent, fully-automated seasonal demand management platform that transforms supply chain efficiency for retail operations. This prototype demonstrates the core features outlined in the Walmart Idea proposal.

## 🚀 Key Features

- Multi-signal demand forecasting (sales, social, weather, events)
- Dynamic inventory and replenishment automation
- Customer engagement and pre-order simulation
- Supplier collaboration and sustainability analytics

## 🏗️ Architecture

```
├── backend/                 # FastAPI backend services
├── dashboard/               # Streamlit dashboard (main user interface)
├── ml_pipeline/             # ML model training and inference
├── data_ingestion/          # Data collection services
└── notifications/           # Communication services
```

## 🛠️ Tech Stack

- **FastAPI** (backend API)
- **Streamlit** (dashboard UI)
- **Prophet, XGBoost, Scikit-learn** (ML)
- **Plotly** (visualizations)

## 🚀 Quick Start (Streamlit Dashboard Only)

### Prerequisites
- Python 3.8+

### Installation

1. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Streamlit dashboard**
   ```bash
   streamlit run dashboard/main.py
   ```
   The dashboard will open in your browser (usually at http://localhost:8501 or http://localhost:8502).

---

## 📊 Demo Features

- Real-time demand forecasting (multi-signal)
- Inventory management simulation
- Customer engagement analytics
- Supplier collaboration tools
- Sustainability and waste reduction metrics

---