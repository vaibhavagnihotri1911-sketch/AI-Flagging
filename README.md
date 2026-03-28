# AI Flagging System 🚀

## 📌 Overview
AI Flagging System is an intelligent application designed to detect and flag suspicious or fraudulent activities using machine learning models.

## 🎯 Features
- Detects fraudulent transactions
- Uses trained ML models (.pkl files)
- Real-time prediction system
- Dashboard for monitoring results

## 🔥 Architecture
                    ┌────────────────────┐
                    │   QR Scanner Input │
                    └─────────┬──────────┘
                              ↓
                    ┌────────────────────┐
                    │  QR Parser Layer   │
                    │ (UPI / Account ID) │
                    └─────────┬──────────┘
                              ↓
          ┌────────────────────────────────────┐
          │        Feature Engineering        │
          │----------------------------------│
          │ - amount                         │
          │ - time of transaction           │
          │ - merchant / payee              │
          │ - user behavior profile         │
          └─────────┬────────────────────────┘
                              ↓
        ┌──────────────────────────────────────┐
        │        HYBRID RISK ENGINE            │
        │--------------------------------------│
        │ 1. Rule Engine (hard checks)        │
        │ 2. ML Model (Isolation Forest)      │
        │ 3. Behavioral Anomaly Scoring       │
        └─────────┬────────────────────────────┘
                              ↓
        ┌──────────────────────────────────────┐
        │     EXPLAINABILITY ENGINE (XAI)     │
        │--------------------------------------│
        │ Converts scores → human reasons      │
        └─────────┬────────────────────────────┘
                              ↓
        ┌──────────────────────────────────────┐
        │      STREAMLIT DASHBOARD UI         │
        │--------------------------------------│
        │ - Risk score                        │
        │ - Reason breakdown                  │
        │ - Trends + history                 │
        └──────────────────────────────────────┘


## 🛠️ Tech Stack
- Python
- Machine Learning (Scikit-learn)
- Flask / Streamlit
- Pandas, NumPy

## 🚀 How to Run
1. Install dependencies:
   pip install -r requirements.txt

2. Run the app:
   python app.py

## 📊 Future Scope
- Integration with real-time APIs
- Advanced NLP-based fraud detection
- Deployment on cloud

## 👨‍💻 Author
Vaibhav Agnihotri