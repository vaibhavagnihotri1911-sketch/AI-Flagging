from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pickle
import os
from datetime import datetime
import logging

# ✅ FIX PATCH (ADDED - REQUIRED FOR YOUR v3 CODE)
from collections import defaultdict

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model = None
try:
    with open('models/fraud_detection_model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("✅ ML Model Loaded Successfully")
except Exception as e:
    print("❌ Model loading failed:", e)

reported_upi_ids = {}

user_behavior_db = {
    "default_user": {
        "avg_transaction": 2000,
        "max_transaction": 10000,
        "frequent_merchants": ["Amazon", "Swiggy", "Flipkart"],
        "usual_hours": (9, 22)
    }
}

# =====================================================
# 🧠 MAIN FRAUD DETECTOR CLASS
# =====================================================
class IndianFraudDetector:
    def __init__(self):
        self.load_models()

        self.indian_banks = ['SBI', 'HDFC Bank', 'ICICI Bank', 'Axis Bank', 'Kotak Mahindra', 'Punjab National Bank']
        self.indian_cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad']
        self.upi_apps = ['PhonePe', 'Google Pay', 'Paytm', 'BHIM UPI', 'Amazon Pay', 'WhatsApp Pay']
        self.merchant_categories = ['Grocery', 'Petrol_Pump', 'Restaurant', 'Online_Shopping', 'ATM', 'Entertainment']

    def load_models(self):
        logger.info("🔄 System initialized (ML + Rule-based hybrid)")

    def prepare_features(self, amount, hour, is_weekend, merchant_category):
        category_map = {
            'Grocery': 0,
            'Online_Shopping': 1,
            'ATM': 2,
            'Petrol_Pump': 3,
            'Restaurant': 4,
            'Entertainment': 5
        }
        category_encoded = category_map.get(merchant_category, 0)
        return np.array([[amount, hour, is_weekend, category_encoded]])

    def behavioral_score(self, amount, hour, merchant_category):
        score = 0
        reasons = []

        if 1 <= hour <= 4:
            score += 0.3
            reasons.append("Late night behavioral anomaly")

        if merchant_category == "ATM" and hour < 6:
            score += 0.2
            reasons.append("Unusual ATM usage time")

        if amount > 150000 and merchant_category == "Online_Shopping":
            score += 0.2
            reasons.append("Unusual high online purchase")

        return score, reasons

    def advanced_behavior_risk(self, amount, hour, merchant, user_id="default_user"):
        profile = user_behavior_db.get(user_id, user_behavior_db["default_user"])

        score = 0
        reasons = []

        if amount > profile["avg_transaction"] * 3:
            score += 0.4
            reasons.append("Amount significantly higher than user average")

        if merchant not in profile["frequent_merchants"]:
            score += 0.2
            reasons.append("New/unknown merchant detected")

        if hour < profile["usual_hours"][0] or hour > profile["usual_hours"][1]:
            score += 0.25
            reasons.append("Transaction outside usual active hours")

        return min(score, 1.0), reasons

    def generate_explanation(self, risk_score, base_reasons):
        label = "LOW RISK"
        if risk_score > 0.7:
            label = "HIGH RISK"
        elif risk_score > 0.4:
            label = "MEDIUM RISK"

        return {
            "risk_label": label,
            "summary": f"{label} transaction detected based on multiple risk signals",
            "reasons": base_reasons
        }

    def calculate_confidence(self, risk_score, ml_prediction):
        confidence = 0.5
        if ml_prediction == 1:
            confidence += 0.3
        if risk_score > 0.7:
            confidence += 0.2
        return round(min(confidence, 1.0), 2)

    def risk_breakdown(self, behavioral_risk, rule_risk):
        return {
            "behavioral_component": round(behavioral_risk, 2),
            "rule_based_component": round(rule_risk, 2),
            "total": round(min(behavioral_risk + rule_risk, 1.0), 2)
        }

    def predict_fraud(self, transaction_data):
        try:
            amount_inr = float(transaction_data.get('amount_inr', transaction_data.get('amount', 0)))
            bank = transaction_data.get('bank', 'Unknown')
            city = transaction_data.get('city', 'Unknown')
            merchant_category = transaction_data.get('merchant_category', 'Unknown')
            hour = int(transaction_data.get('hour', 12))
            is_weekend = int(transaction_data.get('is_weekend', 0))

            risk_score = 0.0
            explanation = []

            if amount_inr > 200000:
                risk_score += 0.3
                explanation.append("High transaction amount")

            if hour < 6 or hour > 23:
                risk_score += 0.25
                explanation.append("Unusual transaction time")

            if merchant_category == 'Online_Shopping':
                risk_score += 0.15
                explanation.append("Online transaction risk")

            if is_weekend:
                risk_score += 0.1
                explanation.append("Weekend activity anomaly")

            behavioral_risk, behavioral_reasons = self.behavioral_score(
                amount_inr, hour, merchant_category
            )

            risk_score += behavioral_risk
            explanation.extend(behavioral_reasons)

            risk_score = max(0, min(1, risk_score))

            if model:
                try:
                    input_data = self.prepare_features(amount_inr, hour, is_weekend, merchant_category)
                    ml_prediction = int(model.predict(input_data)[0])
                except:
                    ml_prediction = 0
            else:
                ml_prediction = 0

            rule_risk = risk_score - behavioral_risk

            return {
                'success': True,
                'prediction': ml_prediction,
                'fraud_probability': float(risk_score),
                'risk_level': 'HIGH' if risk_score > 0.6 else 'LOW',
                'confidence_score': self.calculate_confidence(risk_score, ml_prediction),
                'risk_breakdown': self.risk_breakdown(behavioral_risk, rule_risk),
                'explanation': explanation,
                'amount_inr': amount_inr,
                'bank': bank,
                'city': city,
                'timestamp': datetime.now().isoformat(),
                'market': 'India',
                'model_type': 'Hybrid ML + Behavioral + Explainable AI v3'
            }

        except Exception as e:
            logger.error(f"Error: {e}")
            return {'success': False, 'error': str(e)}

    def predict_upi_fraud(self, upi_data):
        try:
            amount_inr = float(upi_data.get('amount_inr', 0))
            is_new_payee = int(upi_data.get('is_new_payee', 0))

            risk_score = 0.0
            explanation = []

            upi_id = upi_data.get("upi_id", "")

            if not upi_id or "@" not in upi_id:
                risk_score += 0.5
                explanation.append("Invalid UPI ID format")

            if amount_inr > 50000:
                risk_score += 0.3
                explanation.append("High UPI amount")

            if is_new_payee:
                risk_score += 0.4
                explanation.append("New payee risk")

            hour = int(upi_data.get("hour", 12))
            if hour < 5:
                risk_score += 0.2
                explanation.append("Late-night UPI activity")

            prediction = 1 if risk_score > 0.5 else 0

            return {
                'success': True,
                'prediction': prediction,
                'fraud_probability': float(risk_score),
                'explanation': explanation,
                'timestamp': datetime.now().isoformat(),
                'model_type': 'UPI Risk Engine'
            }

        except Exception as e:
            return {'success': False, 'error': str(e)}


fraud_detector = IndianFraudDetector()

@app.route('/')
def home():
    return jsonify({
        'service': 'AI Flagging System - Indian Fraud Detection API',
        'status': 'running',
        'features': ['ML Prediction', 'Explainable AI', 'UPI Fraud Detection'],
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/v1/predict', methods=['POST'])
def predict():
    data = request.get_json()
    return jsonify(fraud_detector.predict_fraud(data))

@app.route('/api/v1/predict_upi', methods=['POST'])
def predict_upi():
    data = request.get_json()
    return jsonify(fraud_detector.predict_upi_fraud(data))


# =====================================================
# 🚀 APPENDED AI FLAGSHIP UPGRADE LAYER (NO CHANGES ABOVE)
# =====================================================

audit_logs = []
fraud_stats = {"total": 0, "high": 0, "low": 0}

def log_request(data, result):
    audit_logs.append({
        "input": data,
        "output": result,
        "time": datetime.now().isoformat()
    })

def update_stats(result):
    fraud_stats["total"] += 1
    if result.get("fraud_probability", 0) > 0.6:
        fraud_stats["high"] += 1
    else:
        fraud_stats["low"] += 1

@app.route("/api/v2/stats", methods=["GET"])
def stats():
    return jsonify({
        "stats": fraud_stats,
        "risk_ratio": fraud_stats["high"] / max(1, fraud_stats["total"])
    })

@app.route("/api/v2/audit", methods=["GET"])
def audit():
    return jsonify({"logs": audit_logs[-20:]})

@app.route("/api/v2/predict_enhanced", methods=["POST"])
def predict_enhanced():
    data = request.get_json()
    result = fraud_detector.predict_fraud(data)

    log_request(data, result)
    update_stats(result)

    result["version"] = "v2-enhanced"
    return jsonify(result)

@app.route("/api/v2/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "version": "v2-enhanced-system"
    })


# =====================================================
# 🔥 AI FLAGSHIP PRO UPGRADE LAYER (v3 - MULTI USER + TIME SERIES)
# =====================================================

# 🧠 FIX PATCH: missing import handled above (defaultdict added)

user_memory_db = defaultdict(lambda: {
    "transactions": [],
    "avg_amount": 0,
    "risk_history": []
})

def update_user_profile(user_id, transaction, risk_score):
    user_data = user_memory_db[user_id]

    user_data["transactions"].append(transaction)

    amounts = [t["amount"] for t in user_data["transactions"]]
    user_data["avg_amount"] = sum(amounts) / len(amounts)

    user_data["risk_history"].append({
        "time": datetime.now().isoformat(),
        "risk": risk_score,
        "amount": transaction["amount"]
    })

def behavioral_memory_risk(user_id, amount, hour):
    user_data = user_memory_db[user_id]

    score = 0
    reasons = []

    if len(user_data["transactions"]) > 0:
        avg = user_data["avg_amount"]

        if amount > avg * 2:
            score += 0.4
            reasons.append("Deviation from historical spending pattern")

        if len(user_data["transactions"]) > 5:
            last_txn = user_data["transactions"][-1]
            time_gap = abs(hour - last_txn.get("hour", hour))

            if time_gap < 1:
                score += 0.2
                reasons.append("Unusual rapid consecutive transactions")

    return min(score, 1.0), reasons


@app.route("/api/v3/user_history/<user_id>", methods=["GET"])
def get_user_history(user_id):
    data = user_memory_db[user_id]

    return jsonify({
        "user_id": user_id,
        "total_transactions": len(data["transactions"]),
        "avg_amount": data["avg_amount"],
        "risk_history": data["risk_history"]
    })


@app.route("/api/v3/predict", methods=["POST"])
def predict_v3():
    data = request.get_json()

    user_id = data.get("user_id", "default_user")
    amount = float(data.get("amount", 0))
    hour = int(data.get("hour", 12))

    result = fraud_detector.predict_fraud(data)

    mem_score, mem_reasons = behavioral_memory_risk(user_id, amount, hour)

    original_risk = result.get("fraud_probability", 0)
    final_risk = min(1.0, original_risk + mem_score)

    result["fraud_probability"] = final_risk
    result["explanation"].extend(mem_reasons)

    update_user_profile(user_id, {
        "amount": amount,
        "hour": hour,
        "merchant": data.get("merchant_category", "unknown")
    }, final_risk)

    result["user_id"] = user_id
    result["model_type"] = "AI Flagship PRO v3 (Memory + Time-Series + Behavioral AI)"

    return jsonify(result)


if __name__ == '__main__':
    logger.info("🚀 Starting AI Flagging System")
    app.run(debug=True)
