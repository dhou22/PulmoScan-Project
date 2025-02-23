# 🏥 Lung Cancer Detection and Classification (Pulmonary Nodules)

## 📌 Project Overview  
This project focuses on detecting and classifying **pulmonary nodules** in chest X-ray images using **deep learning**. The dataset used is **ChestX-ray8**, a **large-scale** hospital-based dataset containing:  
✅ **108,948 frontal-view X-ray images**  
✅ **32,717 unique patients**  
✅ **Labeled with 8 common thoracic diseases**, including:  
   - 🫁 **Atelectasis**  
   - ❤️ **Cardiomegaly**  
   - 💦 **Effusion**  
   - 🌫️ **Infiltration**  
   - 🦠 **Mass**  
   - 🔴 **Nodule**  
   - 🤒 **Pneumonia**  
   - ⚠️ **Pneumothorax**  

The goal is to leverage **deep learning** models to **analyze chest X-ray images, detect pulmonary nodules, and classify lung cancer-related findings**.

---

## 📂 Dataset Details  
### 🔍 1. Data Source  
- 📄 **Dataset Name:** ChestX-ray8  
- 📷 **Total Images:** 108,948 frontal X-ray scans  
- 👨‍⚕️ **Number of Patients:** 32,717  
- 🏷️ **Labels:** Multi-label dataset (each image can have multiple diseases)  
- 🖼️ **Format:** X-ray images in `.png` (extracted from DICOM files)  
- 🔬 **Annotations:**  
  - 📑 **Image-level disease labels** extracted from radiology reports using **Natural Language Processing (NLP)**  
  - 📌 A subset of **983 images with bounding boxes** for **pathology localization**  

### ⚙️ 2. Labeling and Preprocessing  
- 🏥 **Radiology reports were processed** using **DNorm** & **MetaMap** (NLP-based medical text mining).  
- 📝 **Negations and uncertain mentions were removed** to improve label accuracy.  
- 🖍️ **Bounding boxes were manually labeled** for **1,600 pathology instances** in 983 images to aid in disease localization.  

---

## 📊 Data Exploration Process  
### 🧐 1. Understanding the Dataset  
- 📌 **Inspect image distribution:** Check how many images correspond to each disease.  
- 🔗 **Analyze label co-occurrence:** Some diseases frequently appear together (e.g., Effusion & Atelectasis).  
- 📏 **Examine bounding box annotations:** Validate the labeled regions for accuracy.  

### 🔧 2. Image Preprocessing  
- 📏 **Rescaling:** Resize images to **1024×1024 pixels**.  
- 🎚️ **Normalization:** Adjust pixel intensity using DICOM window settings.  
- 🔄 **Augmentation (optional):** Apply transformations (rotation, flipping, contrast adjustments) for better model generalization.  

### 📈 3. Data Visualization  
- 📊 **Label distribution analysis:** Plot frequency of each disease.  
- 🔥 **Correlation heatmap:** Visualize how often diseases appear together.  
- 🖼️ **Sample X-ray images:** Display example scans with corresponding labels.  

### 📊 4. Statistical Analysis  
- ⚖️ **Class imbalance calculation:** Identify diseases with fewer samples (e.g., Pneumonia).  
- 🗂️ **Bounding box analysis:** Evaluate the size and position of labeled regions.  
- 🌈 **Pixel intensity distribution:** Assess variations in X-ray contrast levels.  

---

## 🚧 Key Challenges  
- 🤖 **Weakly-supervised learning:** Most images **only have image-level labels**, making precise disease localization challenging.  
- ⚠️ **Class imbalance:** Some diseases (**Mass, Pneumonia**) have fewer samples, leading to model bias.  
- 🧐 **Small pathology regions:** Nodules and masses can be **tiny**, requiring high precision in detection.  

---

## 🚀 Next Steps  
✅ Implement **deep learning models (CNN, ResNet, VGG)** for feature extraction.  
✅ Train **multi-label classification models** to detect thoracic diseases.  
✅ Develop a **weakly-supervised localization approach** for pulmonary nodule detection.  
✅ Experiment with **data augmentation** to handle class imbalance.  
✅ Evaluate performance using **AUC-ROC, precision-recall, and IoU metrics** for localization.  

---

📌 **This README serves as a reference for understanding the dataset and structuring the data exploration phase of the project.**  
💡 Feel free to contribute or suggest improvements!  

📧 **Contact:** Dhouha Meliane | 🌐 **GitHub:** [_Your Repo_]([https://github.com/dhou22/PulmoScan-Project])  

🚀 **Let's build AI-driven lung cancer detection!** 🏥💙  
