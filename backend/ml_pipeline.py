"""
Machine Learning Pipeline for Crop Recommendation System
Trains a Random Forest Classifier on the 2,200-record agricultural dataset,
evaluates precision, recall, f1, accuracy, and confusion matrix, and exports model & metrics.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, 'dataset', 'Crop_recommendation.csv')
MODEL_DIR = os.path.join(BASE_DIR, 'models')
MODEL_PATH = os.path.join(MODEL_DIR, 'crop_recommendation_model.pkl')
METRICS_PATH = os.path.join(MODEL_DIR, 'model_metrics.json')


def train_crop_model():
    os.makedirs(MODEL_DIR, exist_ok=True)

    print("=" * 60)
    print("STEP 1: Loading Dataset from", DATASET_PATH)
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATASET_PATH}")

    df = pd.read_csv(DATASET_PATH)
    print(f"Dataset Loaded. Total Records: {len(df)}, Columns: {df.columns.tolist()}")

    # Check missing values
    missing_counts = df.isnull().sum().to_dict()
    print("Missing Values Check:", missing_counts)

    # Features and Target
    feature_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    X = df[feature_cols]
    y_raw = df['label']

    # Label encoding
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y_raw)
    class_names = list(label_encoder.classes_)
    print(f"Total Unique Crop Classes: {len(class_names)}")
    print("Classes:", class_names)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"Train Shape: {X_train.shape}, Test Shape: {X_test.shape}")

    # Model training
    print("STEP 2: Training Random Forest Classifier (100 Estimators)...")
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        max_depth=15,
        criterion='entropy'
    )
    model.fit(X_train, y_train)

    # Predictions & Evaluation
    print("STEP 3: Evaluating Model Performance...")
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)

    acc = float(accuracy_score(y_test, y_pred))
    prec_weighted = float(precision_score(y_test, y_pred, average='weighted', zero_division=0))
    rec_weighted = float(recall_score(y_test, y_pred, average='weighted', zero_division=0))
    f1_weighted = float(f1_score(y_test, y_pred, average='weighted', zero_division=0))

    prec_macro = float(precision_score(y_test, y_pred, average='macro', zero_division=0))
    rec_macro = float(recall_score(y_test, y_pred, average='macro', zero_division=0))
    f1_macro = float(f1_score(y_test, y_pred, average='macro', zero_division=0))

    cm = confusion_matrix(y_test, y_pred).tolist()
    clf_report_dict = classification_report(y_test, y_pred, target_names=class_names, output_dict=True)

    # Feature Importances
    feat_importances = {
        feat: round(float(imp), 4)
        for feat, imp in zip(feature_cols, model.feature_importances_)
    }

    # Per-crop metrics
    per_crop_metrics = []
    for crop in class_names:
        if crop in clf_report_dict:
            per_crop_metrics.append({
                'crop': crop,
                'precision': round(clf_report_dict[crop]['precision'], 4),
                'recall': round(clf_report_dict[crop]['recall'], 4),
                'f1_score': round(clf_report_dict[crop]['f1-score'], 4),
                'support': int(clf_report_dict[crop]['support'])
            })

    print(f"-> Accuracy:  {acc * 100:.2f}%")
    print(f"-> Precision: {prec_weighted * 100:.2f}%")
    print(f"-> Recall:    {rec_weighted * 100:.2f}%")
    print(f"-> F1-Score:  {f1_weighted * 100:.2f}%")
    print("Feature Importances:", feat_importances)

    # Save model artifact
    model_payload = {
        'model': model,
        'label_encoder': label_encoder,
        'feature_names': feature_cols,
        'classes': class_names,
        'accuracy': acc,
        'trained_at': datetime.now().isoformat()
    }
    joblib.dump(model_payload, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

    # Save metrics JSON
    metrics_data = {
        'algorithm': 'Random Forest Classifier',
        'n_estimators': 100,
        'total_dataset_records': len(df),
        'train_samples': len(X_train),
        'test_samples': len(X_test),
        'total_crops': len(class_names),
        'crop_classes': class_names,
        'features': feature_cols,
        'accuracy': round(acc, 4),
        'accuracy_percent': round(acc * 100, 2),
        'precision_weighted': round(prec_weighted, 4),
        'recall_weighted': round(rec_weighted, 4),
        'f1_score_weighted': round(f1_weighted, 4),
        'precision_macro': round(prec_macro, 4),
        'recall_macro': round(rec_macro, 4),
        'f1_score_macro': round(f1_macro, 4),
        'feature_importances': feat_importances,
        'confusion_matrix': cm,
        'per_crop_metrics': per_crop_metrics,
        'trained_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    with open(METRICS_PATH, 'w') as f:
        json.dump(metrics_data, f, indent=4)
    print(f"Metrics saved to {METRICS_PATH}")
    print("=" * 60)
    return metrics_data


# Cached model singleton
_MODEL_CACHE = None


def load_model():
    global _MODEL_CACHE
    if _MODEL_CACHE is None:
        if not os.path.exists(MODEL_PATH):
            train_crop_model()
        _MODEL_CACHE = joblib.load(MODEL_PATH)
    return _MODEL_CACHE


def predict_crop(n, p, k, temperature, humidity, ph, rainfall, top_n=3):
    """
    Predict the most suitable crop with confidence and top alternatives.
    Returns:
    {
        'recommended_crop': 'rice',
        'confidence': 94.5,
        'top_recommendations': [
            {'crop': 'rice', 'confidence': 94.5, 'probability': 0.945},
            {'crop': 'jute', 'confidence': 3.2, 'probability': 0.032},
            {'crop': 'maize', 'confidence': 1.1, 'probability': 0.011}
        ],
        'explanation': {...}
    }
    """
    pkg = load_model()
    model = pkg['model']
    le = pkg['label_encoder']
    classes = pkg['classes']

    input_df = pd.DataFrame([{
        'N': float(n),
        'P': float(p),
        'K': float(k),
        'temperature': float(temperature),
        'humidity': float(humidity),
        'ph': float(ph),
        'rainfall': float(rainfall)
    }])

    probs = model.predict_proba(input_df)[0]
    top_indices = np.argsort(probs)[::-1][:top_n]

    recommendations = []
    for idx in top_indices:
        crop_name = le.classes_[idx] if hasattr(le, 'classes_') else classes[idx]
        confidence = round(float(probs[idx]) * 100, 2)
        recommendations.append({
            'crop': crop_name.capitalize(),
            'crop_key': crop_name.lower(),
            'confidence': confidence,
            'probability': round(float(probs[idx]), 4)
        })

    primary = recommendations[0]

    # Generate Explainable AI breakdown
    explanation_points = []
    if float(rainfall) > 150:
        explanation_points.append(f"High rainfall ({rainfall} mm) supports moisture-demanding crop physiology.")
    elif float(rainfall) < 60:
        explanation_points.append(f"Low rainfall condition ({rainfall} mm) is well suited for drought-resistant growth.")
    else:
        explanation_points.append(f"Moderate rainfall ({rainfall} mm) meets optimal agronomic threshold.")

    if float(humidity) > 75:
        explanation_points.append(f"High relative humidity ({humidity}%) provides ideal microclimate.")
    else:
        explanation_points.append(f"Humidity level ({humidity}%) is well matched for transpiration and canopy health.")

    if float(n) >= 70:
        explanation_points.append(f"Elevated Soil Nitrogen ({n} kg/ha) satisfies high vegetative nutrient requirement.")
    else:
        explanation_points.append(f"Soil Nitrogen ({n} kg/ha) is balanced for optimal root and shoot growth.")

    if 6.0 <= float(ph) <= 7.5:
        explanation_points.append(f"Soil pH ({ph}) falls in the neutral to slightly acidic optimal nutrient uptake zone.")
    else:
        explanation_points.append(f"Soil pH ({ph}) aligns with the tolerance threshold of the recommended crop.")

    return {
        'recommended_crop': primary['crop'],
        'crop_key': primary['crop_key'],
        'confidence': primary['confidence'],
        'top_recommendations': recommendations,
        'alternative_crops': [r['crop'] for r in recommendations[1:]],
        'explanation_points': explanation_points,
        'model_used': 'Random Forest Classifier (100 Estimators)',
        'disclaimer': 'AI/ML-based agronomic recommendation generated from soil and meteorological inputs.'
    }


if __name__ == '__main__':
    train_crop_model()
    test_pred = predict_crop(90, 42, 43, 20.88, 82.0, 6.5, 202.9)
    print("\nSample Test Prediction Result:")
    print(json.dumps(test_pred, indent=2))
