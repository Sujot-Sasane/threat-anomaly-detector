# 🛡️ Threat Anomaly Detector

A machine learning web app that classifies network traffic as **Benign or Attack** in real-time.

## 🔗 Live Demo
[threat-anomaly-detector.streamlit.app](https://threat-anomaly-detector.streamlit.app)

## 📌 Project Overview
Built as a portfolio project combining cybersecurity domain knowledge with data engineering and ML.

## 🛠️ Tech Stack
- Python, Pandas, Scikit-learn
- Random Forest Classifier
- Streamlit (frontend + deployment)
- CICIDS2017 Dataset (2.3M network flow records)

## 📊 Dataset
- 2,313,810 rows of network traffic
- 14 attack types including DoS, DDoS, Brute Force, SQL Injection
- Source: Canadian Institute for Cybersecurity

## 🧠 ML Pipeline
1. Load 8 parquet files → merge into single dataset
2. Remove duplicates and infinite values
3. Feature selection → top 15 most important features
4. Train Random Forest → 99% accuracy
5. Deploy via Streamlit Cloud

## 👤 Author
Sujot Sasane — Data Engineer
