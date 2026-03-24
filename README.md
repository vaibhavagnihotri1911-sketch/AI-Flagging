# Fraud Detection Ensemble Hackathon Project

## Overview

This project presents an ensemble of machine learning models aimed at detecting fraudulent financial transactions across multiple banking and credit card datasets. The goal is to build a robust, adaptable fraud detection system leveraging diverse datasets and model architectures.

## Datasets Used

We trained models on the following publicly available datasets:

- **ULB Credit Card Fraud Dataset**

  - Target column: Class (fraudulent or legitimate transactions)
  - Used XGBoost, Random Forest, and Logistic Regression models.

- **IEEE-CIS Credit Card Fraud Dataset**

  - Target column: isFraud
  - Used XGBoost and Random Forest models.

- **Sparkov Credit Card Fraud Dataset**

  - Target column: is_fraud
  - Used Logistic Regression and Random Forest models.

- **BAF (Bank Account Fraud) Dataset**

  - Target column: fraud_bool
  - Used XGBoost and Random Forest models.

- **Bank Transaction Dataset (Unlabeled)**
  - Fraud labels generated via anomaly detection techniques (Isolation Forest, DBSCAN)
  - Used Random Forest model trained on generated fraud labels.

## What We Have Done So Far

- Data preprocessing and feature engineering tailored to each dataset.
- Trained multiple models (XGBoost, Random Forest, Logistic Regression) on each dataset individually for fraud classification.
- Generated pseudo-labels on the unlabeled Bank Transaction dataset using unsupervised anomaly detection to enable supervised learning.
- Implemented SMOTE oversampling where applicable to address class imbalance.
- Evaluated models with key performance metrics: Accuracy, Precision, Recall, F1-score, AUC-ROC.
- Saved all trained models as pickled files for reproducibility and future use.

## Future Work and Roadmap

- Train on the PaySim dataset, currently pending due to time constraints, to further improve generalizability.
- Develop an ensemble model combining predictions from all trained models for improved accuracy and robustness.
- Build real-time prediction APIs and interactive dashboards (e.g., Streamlit apps) for demo and deployment.
- Enhance model explainability using techniques like SHAP values to interpret fraud indicators.
- Extend anomaly detection methods and incorporate more advanced feature engineering.
- Explore deep learning architectures and sequence models for improved temporal fraud detection.

## How to Use

1. Clone or download this repository.
2. Install required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Use notebooks in the `notebooks/` folder to preprocess data and train models.
4. Load pickled models from the `models/` folder for inference or ensemble building.
5. See `demo.py` for a simple command-line interface for fraud prediction on sample transactions.
6. For an interactive UI, run the Streamlit app (`app.py`) after installing dependencies.

## Repository Structure

```
fraud-ensemble/
│
├── data/                # Sample datasets and input files
├── models/              # Pickled trained models (*.pkl)
├── notebooks/           # Jupyter notebooks for training, evaluation, demo
├── demo.py              # Command-line fraud prediction script
├── app.py               # Streamlit demo app (interactive UI)
├── requirements.txt     # Python dependencies
├── README.md            # Project overview and instructions
```
