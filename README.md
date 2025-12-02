# 🫁 PulmoScan: AI-Powered Lung Cancer Detection and Classification

Welcome to **PulmoScan**, a comprehensive deep learning project for automated detection and classification of pulmonary nodules from CT scans using **3D Convolutional Neural Networks** and **radiomics-based machine learning**. This work implements the approach described in:

> **"3D Deep Learning from CT Scans Predicts Tumor Invasiveness of Subcentimeter Pulmonary Adenocarcinomas"**
> Cancer Research, 2018 ([arXiv:1801.09555](https://arxiv.org/abs/1801.09555))

![Lung Cancer Detection](https://github.com/user-attachments/assets/36ba3b0f-900c-44f6-bbe8-9a2318d6e773)

---

## 🚀 Project Overview

PulmoScan offers a modular pipeline to detect, classify, and analyze pulmonary nodules using state-of-the-art 3D deep learning architectures and advanced radiomic feature extraction. The system processes CT scans through carefully tuned preprocessing pipelines, trains multi-stage detection and classification models, and validates improvements using comprehensive clinical metrics.

### 📋 Key Features

- **Advanced CT Preprocessing**: Lung segmentation with Sobel edge detection, Otsu thresholding, and morphological operations

- **3D Dual Path Network (DPN) Architecture**: Implements attention-enhanced 3D CNN with multi-scale feature extraction for nodule detection

- **Radiomics-Enhanced Classification**: PyRadiomics-based feature extraction with Random Forest, SVC, and KNN models for malignancy prediction

- **Multi-Dataset Support**: Works with LUNA16, LIDC-IDRI, and Chest CT-Scan datasets with standardized processing

- **VGG19-based Subtype Classification**: Validates cancer subtypes with transfer learning achieving 92% accuracy

- **Clinical-Grade Benchmarking**: Comprehensive metrics including AUC, sensitivity, specificity, and F1 scores

---

## 🏗️ Project Structure

```plaintext
📁 pulmoscan/
├── 📁 data/                      # Raw datasets
│   ├── 📁 luna16/
│   ├── 📁 lidc-idri/
│   └── 📁 chest-ct/
├── 📁 processed/                 # Preprocessed outputs
│   ├── 📁 segmented/
│   ├── 📁 normalized/
│   └── *.csv                     # Metadata and annotations
├── 📁 models/                    # Saved models
│   ├── 📁 nodule_detector/       # 3D DPN models
│   ├── 📁 malignancy_classifier/ # RF, SVC, KNN models
│   └── 📁 subtype_classifier/    # VGG19 models
├── 📁 experiments/               # Experimental logs and config
├── 📁 app/                       # Flask application
│   ├── 📁 static/
│   ├── 📁 templates/
│   ├── 📁 utils/
│   │   ├── preprocessing.py      # Segmentation and normalization
│   │   ├── feature_extraction.py # Radiomics and semantic features
│   │   └── visualization.py      # Result visualization
│   ├── routes.py
│   └── __init__.py
├── 📁 monitoring/                # Prometheus & Grafana
│   ├── 📁 prometheus/
│   └── 📁 grafana/
├── 📁 tests/                     # Unit and integration tests
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── main.py                       # Pipeline launcher
```

---

## Detailed Architecture

<img width="1063" height="462" alt="image" src="https://github.com/user-attachments/assets/b232e628-2bb0-4feb-bef0-c95b23b095ac" />


### Complete Pipeline Workflow

Our implementation follows a four-stage clinical pipeline:

1. **Data Preparation**: CT scan loading, lung segmentation, Hounsfield normalization, and 3D resampling
2. **Nodule Detection**: 3D DPN architecture with multi-scale feature extraction and region proposal
3. **Malignancy Classification**: Radiomic feature extraction followed by ensemble ML classification
4. **Subtype Identification**: Transfer learning with VGG19 for cancer subtype prediction

### 📐 Key Hyperparameters

| Parameter | Value | Purpose |
|-----------|-------|---------|
| BATCH_SIZE | 16 | Optimized for GPU memory with 3D volumes |
| LEARNING_RATE | 0.0001 | Fine-tuned for stable convergence in 3D CNNs |
| INPUT_SIZE | 64×64×64 | Voxel dimensions for nodule patches |
| HU_MIN / HU_MAX | -1000 / 400 | Hounsfield unit clipping for lung tissue |
| AUGMENTATION | Rotation, Flip, Elastic | Data augmentation for robust generalization |
| NUM_FEATURES | 107 | PyRadiomics features (first-order, shape, texture) |
| ENSEMBLE_MODELS | RF, SVC, KNN | Multi-model voting for classification |
| VGG19_LAYERS | 19 | Deep feature extraction with transfer learning |

### 3D Dual Path Network (DPN)

![3D DPN Architecture](https://github.com/user-attachments/assets/77dbc071-d435-44d6-894e-00db10c4177f)

Our nodule detection implementation uses a 3D DPN architecture specifically optimized for CT volumes:

- **Encoder**: Multi-scale 3D convolutional layers with residual connections
- **Dual Path Structure**: Combines high-resolution and high-level semantic features
- **Decoder**: 3D transposed convolutions with skip connections
- **Training**: Weighted cross-entropy loss with AdamW optimizer and ReduceLROnPlateau scheduler

This approach achieves **AUC ≈ 0.91** for nodule detection, outperforming traditional 2D approaches.

---

## Dataset Processing

<img width="1052" height="543" alt="image" src="https://github.com/user-attachments/assets/ec33443e-15c8-4001-b7f1-4faeac985ab2" />


All CT scans are processed with clinical-grade precision using carefully selected parameters:

### Preprocessing Pipeline

<img width="631" height="491" alt="image" src="https://github.com/user-attachments/assets/197b0a92-013e-4cb2-936e-909497231692" />

- **Lung Segmentation**: Sobel edge detection + Otsu thresholding + morphological operations
- **HU Normalization**: Clipping to [-1000, 400] and scaling to [0, 1]
- **Resampling**: Standardized voxel spacing of 1×1×1 mm³
- **Patch Extraction**: 64×64×64 voxel patches centered on nodule candidates
- **Augmentation**: 3D rotation, flipping, and elastic deformation

### Dataset Details

<img width="1165" height="565" alt="image" src="https://github.com/user-attachments/assets/1aa50754-eb54-43bc-9fb1-2a52e1a393a4" />

------

<img width="1163" height="504" alt="image" src="https://github.com/user-attachments/assets/f22273ac-a007-4904-bedb-ca63dc7f5901" />

------

<img width="1163" height="515" alt="image" src="https://github.com/user-attachments/assets/ee2615d7-78c9-42be-b252-8ef93761084a" />

-----


| Dataset | Scans | Annotations | Task | Notes |
|---------|-------|-------------|------|-------|
| LUNA16 | 888 CT scans | 1,186 nodules | Detection | Grand Challenge for nodule detection |
| LIDC-IDRI | 1,018 scans | ~2,600 nodules | Classification | 4 radiologist annotations per nodule |
| Chest CT-Scan | 1,000 images | 4 classes | Subtyping | Adenocarcinoma, Squamous, Large cell, Normal |

---

## Nodule Detection: 3D DPN Implementation

<img width="929" height="893" alt="image" src="https://github.com/user-attachments/assets/9e84126f-855f-4bbc-9d85-3f428201c4e2" />


Our 3D DPN implementation incorporates several architectural innovations:

- **Multi-Scale Feature Fusion**: Combines features from multiple resolution levels
- **Residual Connections**: Prevents gradient vanishing in deep networks
- **Weighted Loss Function**: Addresses class imbalance (nodule vs. non-nodule)
- **Early Stopping & LR Scheduling**: Ensures optimal convergence without overfitting

### Detection Performance

<img width="1399" height="435" alt="image" src="https://github.com/user-attachments/assets/733c5f98-bc6d-41fd-9e6a-ce95a5b01fa2" />

| Metric | Value | Clinical Significance |
|--------|-------|----------------------|
| AUC-ROC | 0.91 | Excellent discrimination capability |
| Sensitivity | 87.3% | High true positive rate |
| Specificity | 89.6% | Low false positive rate |
| Precision | 0.88 | Reliable positive predictions |
| F1 Score | 0.875 | Balanced performance |




---

## Malignancy Classification: Radiomics + ML


<img width="702" height="465" alt="image" src="https://github.com/user-attachments/assets/e03fe3ab-dc7c-41b7-b8d7-8c4a20b4e54a" />

----

The radiomics-based classification represents our interpretable ML approach:

- **Feature Extraction**: 107 PyRadiomics features (first-order statistics, shape, texture)
- **Semantic Features**: XML-based annotations from LIDC-IDRI using PyLIDC
- **Feature Selection**: Recursive feature elimination with cross-validation
- **Ensemble Classification**: Random Forest, SVC, and KNN with voting strategy
- **Validation**: 5-fold stratified cross-validation for robust evaluation

### Radiomics vs. Deep Learning Comparison

| Model | Accuracy | F1 Score | Notable Strength |
|-------|----------|----------|------------------|
| Random Forest | **91.2%** | **0.90** | Interpretable features & fast inference |
| SVC | 88.7% | 0.87 | Strong generalization with RBF kernel |
| KNN | 85.3% | 0.84 | Simple baseline with good performance |
| 3D CNN (End-to-end) | 89.8% | 0.89 | Automated feature learning |

---

## Cancer Subtype Classification

<img width="1294" height="317" alt="image" src="https://github.com/user-attachments/assets/a04bb57c-8f62-4bd8-b206-7304e6564a26" />

-----

Our subtype classification model identifies four key lung tissue categories:

### VGG19 Transfer Learning Results

| Subtype | Precision | Recall | F1 Score | Support |
|---------|-----------|--------|----------|---------|
| Adenocarcinoma | 0.94 | 0.91 | 0.92 | 250 |
| Squamous Cell | 0.91 | 0.93 | 0.92 | 250 |
| Large Cell | 0.89 | 0.90 | 0.89 | 250 |
| Normal | 0.95 | 0.94 | 0.94 | 250 |
| **Overall** | **0.92** | **0.92** | **0.92** | **1000** |




---

## Clinical Validation Results

<img width="1041" height="576" alt="image" src="https://github.com/user-attachments/assets/74433e61-47ef-49dd-b5e4-13339eca7981" />

------

The integrated pipeline demonstrates significant clinical value:

### Nodule Detection Performance (LUNA16)

| Metric | Baseline | PulmoScan | Improvement |
|--------|----------|-----------|-------------|
| Detection Rate | 82.4% | **91.3%** | +8.9% |
| False Positives | 4.2/scan | **2.1/scan** | -50% |
| AUC | 0.87 | **0.91** | +4.6% |

### Malignancy Classification (LIDC-IDRI)

| Approach | Accuracy | Sensitivity | Specificity | F1 Score |
|----------|----------|-------------|-------------|----------|
| Radiologist Average | 88.5% | 84.2% | 91.3% | 0.87 |
| **PulmoScan (RF)** | **91.2%** | **89.7%** | **92.8%** | **0.90** |
| Improvement | +2.7% | +5.5% | +1.5% | +0.03 |

---

## 🛠 Setup Instructions

```bash
# 1. Clone Repository
git clone https://github.com/dhouhameliane/PulmoScan
cd pulmoscan

# 2. Create Virtual Environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install Dependencies
pip install -r requirements.txt

# 4. Download Datasets
# LUNA16: https://luna16.grand-challenge.org/
# LIDC-IDRI: https://wiki.cancerimagingarchive.net/display/Public/LIDC-IDRI
# Place datasets in data/ directory

# 5. Run Preprocessing
python main.py --mode preprocess --dataset luna16

# 6. Train Models
python main.py --mode train --model nodule_detector


```

---

## 📡 API Reference

### Core Endpoints

```python
# Upload CT scan for analysis
POST /upload
Content-Type: multipart/form-data
Body: {file: CT_scan.mhd}

# Get prediction results
GET /report/<scan_id>
Response: {
  "nodules_detected": int,
  "malignancy_scores": [float],
  "subtypes": [string],
  "confidence": float
}

# Visualize 3D results
GET /visualize/<scan_id>
Response: Interactive 3D visualization

# Download diagnostic report
GET /download/<scan_id>
Response: PDF report with findings
```

---

## 🧪 Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test suites
pytest tests/test_preprocessing.py -v
pytest tests/test_models.py -v
pytest tests/test_api.py -v

# Generate coverage report
pytest --cov=app tests/
```

---

## 📊 Monitoring & Observability

PulmoScan includes comprehensive monitoring:

- **Prometheus Metrics**: Inference time, model accuracy, error rates
- **Grafana Dashboards**: Real-time visualization of system health
- **Custom Metrics**: Per-model performance tracking
- **Alerting**: Automated notifications for anomalies

---

## 🔬 Technical Implementation Details

### Preprocessing Pipeline

```python
# Key preprocessing steps
1. Load DICOM/MHD files
2. Resample to 1×1×1 mm³ spacing
3. Apply lung segmentation mask
4. Clip HU values to [-1000, 400]
5. Normalize to [0, 1]
6. Extract 64×64×64 patches
7. Apply data augmentation
```

### Feature Extraction

```python
# Radiomic features (107 total)
- First Order (19): Mean, Median, Std, Skewness, Kurtosis, etc.
- Shape (14): Volume, Surface Area, Sphericity, etc.
- Texture (74): GLCM, GLRLM, GLSZM, NGTDM, GLDM
```

### Model Training

```python
# Training configuration
- Optimizer: AdamW (weight_decay=1e-4)
- Loss: Weighted CrossEntropy
- LR Schedule: ReduceLROnPlateau (patience=5)
- Early Stopping: patience=10
- Batch Size: 16
- Epochs: 100 (with early stopping)
```

---

## 🚀 Future Improvements

- [ ] Integrate explainability with Grad-CAM and attention visualization
- [ ] Add multi-task learning for simultaneous detection and classification
- [ ] Enhance with transformer-based architectures (3D Vision Transformers)
- [ ] Develop real-time inference pipeline for clinical deployment
- [ ] Expand to multi-center validation with external datasets
- [ ] Implement uncertainty quantification for model predictions
- [ ] Web interface with PACS integration for clinical workflow

---

## 👥 Authors

**Project Team** (ESPRIT Data Science, 2024-2025):
- **Asser Aydi** - Lead Developer
- **Dhouha Meliane** - ML Engineer & Architecture
- **Harold Agbervo** - Data Preprocessing
- **Nouha Aouachri** - Model Evaluation
- **Ranim Souissi** - Web Development

**Supervisors**:
- **Ms. Sarah Zouari** - Academic Supervisor
- **Mr. Fares Khfecha** - Technical Advisor

---

## 📜 License

Licensed under **MIT License**.  
Created by **ESPRIT Data Science Team**  
📧 Contact: [dhouhameliane@esprit.tn](mailto:dhouhameliane@esprit.tn)

---

## 📬 References

### Scientific Papers
* Wang, S., et al. *"3D Deep Learning from CT Scans Predicts Tumor Invasiveness of Subcentimeter Pulmonary Adenocarcinomas"* [arXiv:1801.09555](https://arxiv.org/abs/1801.09555)
* Setio, A. A., et al. *"Validation, comparison, and combination of algorithms for automatic detection of pulmonary nodules in computed tomography images: The LUNA16 challenge"* Medical Image Analysis, 2017
* Armato III, S. G., et al. *"The Lung Image Database Consortium (LIDC) and Image Database Resource Initiative (IDRI)"* Medical Physics, 2011

### Datasets
* [LUNA16 Grand Challenge](https://luna16.grand-challenge.org/)
* [LIDC-IDRI (The Cancer Imaging Archive)](https://wiki.cancerimagingarchive.net/display/Public/LIDC-IDRI)
* [Chest CT-Scan Images Dataset (Kaggle)](https://www.kaggle.com/datasets/mohamedhanyyy/chest-ctscan-images)

### Tools & Libraries
* [PyRadiomics Documentation](https://pyradiomics.readthedocs.io/)
* [PyLIDC GitHub Repository](https://github.com/pylidc/pylidc)
* [VGG19 Architecture (Keras)](https://keras.io/api/applications/vgg/)

---

## 🙏 Acknowledgments

We thank ESPRIT for providing computational resources and the open-source community for maintaining the datasets and tools that made this project possible. Special thanks to the radiologists who contributed annotations to LIDC-IDRI and the LUNA16 challenge organizers.

---

**⭐ If you find this project helpful, please consider starring the repository!**
