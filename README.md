# 🫁 PulmoScan: AI-Powered Lung Cancer Detection and Classification
---

![Lung Cancer Detection](https://github.com/user-attachments/assets/36ba3b0f-900c-44f6-bbe8-9a2318d6e773)

---

Welcome to **PulmoScan**, an advanced AI-powered platform designed to automate the detection and classification of pulmonary nodules from CT scans. Developed as a Data Science Integrated Project at ESPRIT (2024-2025), PulmoScan combines robust preprocessing pipelines, advanced 3D CNN architectures, and radiomic features to assist healthcare professionals in diagnosing lung cancer early and accurately.

---

## 🚀 Project Overview

PulmoScan provides an end-to-end AI framework for:

- 🔍 **Nodule Detection**: Utilizing a 3D Dual Path Network (DPN) trained on LUNA16 dataset to detect pulmonary nodules with high precision.
- 🔬 **Malignancy Classification**: Leveraging radiomic and semantic features extracted from LIDC-IDRI dataset, followed by machine learning classification (Random Forest, SVC, KNN).
- 📊 **Subtype Prediction**: Identifying lung cancer subtypes including adenocarcinoma, squamous cell carcinoma, large cell carcinoma, and normal tissue using the Chest CT-Scan dataset.
- 🌐 **Web Interface**: Flask-based application for scan upload, analysis, and result visualization.
- 📈 **Monitoring**: Prometheus & Grafana dashboards for tracking inference performance and system health.

---

## 🧠 Key Features

✅ **3D DPN for Nodule Detection**: Accurate and efficient pulmonary nodule identification with AUC ≈ 0.91.  
✅ **Radiomics + ML for Classification**: Extracted features from CT images power interpretable ML models with F1 = 0.90 for malignancy detection.  
✅ **Subtype Classification**: Handles four key lung tissue types with 92% accuracy using pretrained VGG19.  
✅ **Flask Web Interface**: Lightweight UI for scan upload and result viewing.  
✅ **Containerized Deployment**: Docker and Docker Compose for easy deployment.  
✅ **Monitoring Tools**: Observability via Prometheus metrics and Grafana dashboards.

---

## 🏗️ Architecture

```
📦 pulmoscan/
├── 📂 app/
│   ├── static/
│   ├── templates/
│   ├── models/
│   │   ├── nodule_detector/      # 3D DPN model
│   │   ├── malignancy_classifier/ # RF, SVC, KNN models
│   │   └── subtype_classifier/   # VGG19 models
│   ├── utils/
│   │   ├── preprocessing/        # Segmentation, normalization
│   │   ├── feature_extraction/   # Radiomics, XML-based
│   │   └── visualization/        # Result visualization
│   ├── monitoring/
│   │   ├── prometheus/
│   │   └── grafana/
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

#### LUNA16 Dataset Preprocessing
- Lung segmentation using Sobel edge detection + Otsu thresholding + morphological operations
- Hounsfield unit normalization and 3D volumetric resampling
- Data augmentation techniques for balanced training

#### LIDC-IDRI Dataset Preprocessing
- Radiomic feature extraction with PyRadiomics (first-order statistics, shape features, texture features)
- XML-based feature extraction with PyLIDC for semantic annotations
- Feature preprocessing including normalization, missing data imputation, and feature selection
- Cross-validation for feature selection optimization

#### Chest CT-Scan Dataset Preprocessing
- Image preprocessing for VGG19 architecture compatibility
- Data augmentation to address class imbalance
- Normalization and standardization for transfer learning

---

### 🧠 Modeling Strategy

#### 🔍 Nodule Detection (LUNA16)
- **Architecture**: 3D Dual Path Network (DPN)
- **Optimizer**: AdamW with ReduceLROnPlateau scheduler
- **Loss Function**: Weighted cross-entropy to address class imbalance
- **Evaluation Metrics**: Accuracy, ROC-AUC (≈ 0.91), Confusion Matrix
- **Training Strategy**: Batch training with validation monitoring

#### 🔬 Malignancy Classification (LIDC-IDRI)
- **Models Evaluated**: 
  - Random Forest (Best performer: F1 = 0.90)
  - Support Vector Classifier (SVC)
  - K-Nearest Neighbors (KNN)
- **Features**: Combined radiomic and semantic features
- **Validation**: 5-fold stratified cross-validation
- **Hyperparameter Tuning**: Grid search for optimal parameters

#### 📑 Subtype Classification (Chest CT)
- **Architectures**:
  - VGG19 from scratch
  - Pretrained VGG19 (transfer learning) - Best performer
- **Performance**: 92% accuracy on test set
- **Comprehensive Metrics**: Precision, recall, F1-score per class

---

### 🌐 Web Application

- Upload CT scans in standard medical formats (.mhd/.raw)
- Interactive visualization of detected nodules
- Malignancy prediction with confidence scores
- Cancer subtype classification results
- Downloadable diagnostic reports in PDF format
- Flask-based backend with modular architecture

---

### 📉 Monitoring

- **Prometheus**: Track inference metrics, system performance
- **Grafana**: Visual dashboards for:
  - Model inference time
  - Prediction accuracy
  - System resource utilization
  - Error rates and exceptions
- Dashboards accessible on port 3000

---

### 🐳 Deployment

```bash
# Clone the repository
git clone https://github.com/yourusername/pulmoscan.git
cd pulmoscan

# Build and start all services
docker-compose up --build

# Access the application
# Web app: http://localhost:5000
# Grafana monitoring: http://localhost:3000
```

---

### 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific test modules
pytest tests/test_preprocessing.py
pytest tests/test_models.py
pytest tests/test_api.py
```

---

## 📡 API Endpoints

| Method | Endpoint              | Description                           |
|--------|----------------------|---------------------------------------|
| GET    | `/health`            | API health check                      |
| POST   | `/upload`            | Upload CT scan for prediction         |
| GET    | `/report/<id>`       | Retrieve scan analysis report         |
| GET    | `/visualize/<id>`    | Interactive 3D visualization          |
| GET    | `/download/<id>`     | Download PDF report                   |

---

## 🛠️ Makefile Commands

| Command               | Description                     |
|-----------------------|---------------------------------|
| `make install`        | Install dependencies            |
| `make run`            | Launch Flask server             |
| `make test`           | Run all tests                   |
| `make docker-build`   | Build Docker image              |
| `make docker-run`     | Start Docker container          |
| `make monitor`        | Start monitoring services       |
| `make clean`          | Clean temporary files           |

---

## 📈 Performance Summary

| Task                  | Model              | Best Metric        |
|-----------------------|--------------------|-------------------|
| Nodule Detection      | 3D DPN             | AUC ≈ 0.91        |
| Malignancy (Binary)   | Random Forest      | F1 = 0.90         |
| Subtype (Multi-class) | Pretrained VGG19   | Accuracy ≈ 92%    |

---

## 👥 Authors

Developed by ESPRIT Data Science Team – Academic Year 2024–2025  

**Asser Aydi** – **Dhouha Meliane** – **Harold Agbervo**  
 – **Nouha Aouachri** - **Ranim Souissi**

Supervised by:  
**Ms. Sarah Zouari** – **Mr. Fares khfecha**

---

## 📚 References

- ESPRIT Project Report (2025): "PulmoScan – AI-Powered Lung Cancer Detection and Classification"
- [LUNA16 Challenge Dataset](https://luna16.grand-challenge.org/)
- [LIDC-IDRI Dataset (TCIA)](https://wiki.cancerimagingarchive.net/display/Public/LIDC-IDRI)
- [PyRadiomics Documentation](https://pyradiomics.readthedocs.io/)
- [PyLIDC GitHub Repository](https://github.com/pylidc/pylidc)
- [VGG19 Architecture](https://keras.io/api/applications/vgg/)
