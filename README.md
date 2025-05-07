# 🫁 PulmoScan: AI-Powered Lung Cancer Detection & Classification

Welcome to **PulmoScan**, a deep learning-based platform designed to automate the detection and classification of pulmonary nodules from CT scans. Developed as part of a data science engineering project at ESPRIT (2024–2025), PulmoScan combines robust preprocessing pipelines, advanced 3D CNN architectures, and radiomic features to assist healthcare professionals in diagnosing lung cancer early and accurately.

---

## 🚀 Project Overview

PulmoScan provides an end-to-end AI framework for:

- 🔍 **Nodule Detection**: Using a 3D Dual Path Network (DPN) trained on LUNA16 to detect pulmonary nodules.
- 🔬 **Classification**: Using radiomic and semantic features extracted from LIDC-IDRI and Chest CT-Scan datasets, followed by machine learning classification (Random Forest, SVC, KNN).
- 📊 **Subtype Prediction**: Identifying subtypes including adenocarcinoma, squamous cell carcinoma, large cell carcinoma, and normal tissue.
- 🌐 **Web Interface**: Flask-based app for scan upload, analysis, and result visualization.
- 📈 **Monitoring**: Prometheus & Grafana dashboards for tracking inference performance and system health.

---

## 🧠 Key Features

✅ **3D DPN for Detection**: Accurate and efficient pulmonary nodule identification.  
✅ **Radiomics + ML for Classification**: Extracted features from CT images power interpretable ML models.  
✅ **Subtype Support**: Handles four key lung tissue types for granular predictions.  
✅ **Flask Web Interface**: Lightweight UI for scan upload and result viewing.  
✅ **Containerized**: Docker and Docker Compose for easy deployment.  
✅ **Monitoring Tools**: Observability via Prometheus metrics and Grafana dashboards.

---

## 🏗️ Architecture

```
📦 pulmoscan/
├── 📂 app/
│   ├── static/
│   ├── templates/
│   ├── models/
│   ├── utils/
│   ├── monitoring/
│   ├── __init__.py
│   └── routes.py
├── 📂 tests/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── README.md
```

---

## 📌 Project Phases

### 📁 Data Sources

- **LUNA16**: For nodule detection (CT scans, annotated candidates).
- **LIDC-IDRI**: For radiomics, semantic features, malignancy scoring.
- **Chest CT-Scan Dataset**: Multi-class subtype classification (adenocarcinoma, large cell, squamous, normal).

---

### 🧹 Data Preparation

- Lung segmentation using Sobel + Otsu + morphological ops.
- Hounsfield normalization and 3D volumetric resampling.
- Radiomics extraction with PyRadiomics.
- XML-based feature extraction with PyLIDC.
- Label encoding, missing data imputation, and feature pruning.

---

### 🧠 Modeling Strategy

#### 🔍 Nodule Detection (LUNA16)
- Architecture: 3D Dual Path Network (DPN)
- Optimizer: AdamW + ReduceLROnPlateau
- Loss: Weighted cross-entropy
- Evaluation: Accuracy, ROC-AUC, Confusion Matrix

#### 🔬 Malignancy Classification (LIDC-IDRI)
- Models: Random Forest, SVC, KNN
- Features: Radiomic + semantic
- Cross-validation: 5-fold stratified
- Metric: F1-score (best: RF with 0.90 malignant class)

#### 📑 Subtype Classification (Chest CT)
- Architecture: VGG19 (from scratch & transfer learning)
- Best result from pretrained VGG19
- Metrics: Accuracy, precision, recall, F1

---

### 🌐 Web Application

- Upload scans (.mhd/.raw)
- Visualize prediction results and subtype probabilities
- Downloadable diagnostic reports
- Flask app with modular backend

---

### 📉 Monitoring

- **Prometheus**: Track inference metrics
- **Grafana**: Visual dashboards (response time, error rate)
- Dashboards exposed on port 3000

---

### 🐳 Deployment

```bash
docker-compose up --build
# Web app: http://localhost:5000
# Grafana: http://localhost:3000
```

---

### 🧪 Testing

```bash
pytest tests/
```

---

## 📡 API Endpoints

| Method | Endpoint         | Description                      |
|--------|------------------|----------------------------------|
| GET    | `/health`        | API health check                 |
| POST   | `/upload`        | Upload CT scan for prediction    |
| GET    | `/report/<id>`   | Retrieve scan report             |

---

## 🛠️ Makefile Commands

| Command             | Description               |
|---------------------|---------------------------|
| `make install`      | Install dependencies      |
| `make run`          | Launch Flask server       |
| `make test`         | Run all tests             |
| `make docker-build` | Build Docker image        |
| `make docker-run`   | Start Docker container    |
| `make monitor`      | Start monitoring services |

---

## 📈 Performance Summary

| Task                | Model            | Best Metric |
|---------------------|------------------|-------------|
| Nodule Detection    | 3D DPN           | AUC ≈ 0.91  |
| Malignancy (Binary) | Random Forest    | F1 = 0.90   |
| Subtype (Multi)     | Pretrained VGG19 | Acc ≈ 92%   |

---

## 👥 Authors

Developed by ESPRIT Data Science Team – Academic Year 2024–2025  
**Nouha Aouachri** – **Dhouha Meliane** – **Ranim Souissi**  
**Harold Agbervo** – **Asser Aydi**

---

## 📚 References

- ESPRIT Project Report (2025): “PulmoScan – AI-Powered Lung Cancer Detection and Classification”
- [LUNA16 Challenge Dataset](https://luna16.grand-challenge.org/)
- [LIDC-IDRI Dataset (TCIA)](https://wiki.cancerimagingarchive.net/display/Public/LIDC-IDRI)
- [PyRadiomics](https://pyradiomics.readthedocs.io/)
- [PyLIDC](https://github.com/pylidc/pylidc)
