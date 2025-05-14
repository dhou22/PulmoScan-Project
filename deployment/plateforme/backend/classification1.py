from flask import Blueprint, render_template, request, send_file, jsonify, send_from_directory
from flask_login import login_required
import joblib
import pydicom
import os
import SimpleITK as sitk
import numpy as np
import pandas as pd
from radiomics import featureextractor
import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import uuid
from reportlab.platypus import Table, TableStyle, Image as RLImage
from reportlab.lib import colors
from PIL import Image
# Blueprint setup
classification1 = Blueprint('classification1', __name__, template_folder='../frontend')

# Load model and PyRadiomics feature extractor
model_path = "C:/Users/user/Desktop/plateforme/backend/rf_lasso_model.pkl"
model = joblib.load(model_path)

UPLOAD_FOLDER = 'uploads'
REPORT_FOLDER = 'static/reports'  # Changed to match URL structure
params_path = "C:/Users/user/Desktop/plateforme/backend/Params.yaml"
extractor = featureextractor.RadiomicsFeatureExtractor(params_path)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

# UI page
@classification1.route('/classification1', methods=['GET'])
@login_required
def show():
    return render_template('classification1.html')

@classification1.route("/", methods=["GET"])
def index():
    return render_template("upload.html")

# Analyze route
@classification1.route("/analyze", methods=["POST"])
@login_required
def analyze():
    upload_dir = os.path.join(UPLOAD_FOLDER, str(uuid.uuid4()))
    os.makedirs(upload_dir, exist_ok=True)

    # Single file
    if 'file' in request.files:
        file = request.files['file']
        if file and file.filename.endswith('.dcm'):
            file_path = os.path.join(upload_dir, file.filename)
            file.save(file_path)
            result_path, label, y_proba, y_pred = process_dicom_file(file_path)
            report_url = f"/{result_path.replace(os.sep, '/')}"
            return jsonify({
                "label": label,
                "confidence": float(y_proba[0][y_pred[0]]),
                "report_url": report_url
            })

    # Folder (batch)
    if 'folder[]' in request.files:
        files = request.files.getlist('folder[]')
        if not files:
            return jsonify({"error": "No files uploaded."}), 400

        valid_files = []
        for file in files:
            if file.filename.endswith('.dcm'):
                file_path = os.path.join(upload_dir, os.path.basename(file.filename))
                file.save(file_path)
                valid_files.append(file_path)
        
        if not valid_files:
            return jsonify({"error": "No valid DICOM files found."}), 400

        try:
            report_path = process_dicom_folder(upload_dir)
            
            # If the result is an error tuple
            if isinstance(report_path, tuple):
                return jsonify({"error": report_path[0]}), report_path[1]
            
            # Ensure the report URL is properly formatted
            report_url = f"/{report_path}"  # Already includes static/reports
            
            return jsonify({
                "label": "Batch Classification Results",
                 "Result":"Please download the report to view the results",
                "report_url": report_url
            })
        except Exception as e:
            return jsonify({"error": f"Processing error: {str(e)}"}), 500

    return jsonify({"error": "Invalid request."}), 400

# Single DICOM - Unchanged
from datetime import datetime

def process_dicom_file(file_path):
    try:
                # Save DICOM image as PNG and add it to the report
        try:
            img = Image.fromarray(image_array)
            if img.mode != "L":
                img = img.convert("L")  # Ensure grayscale
            temp_img_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}.png")
            img.save(temp_img_path)

            c.drawImage(temp_img_path, 380, 610, width=150, height=150)  # Adjust position/size if needed
        except Exception as e:
            print(f"⚠️ Could not add image to PDF: {e}")

        ds = pydicom.dcmread(file_path)
        image_array = ds.pixel_array
        image = sitk.GetImageFromArray(image_array.astype(np.float32))

        try:
            spacing = (float(ds.PixelSpacing[0]), float(ds.PixelSpacing[1]), float(ds.SliceThickness))
            image.SetSpacing(spacing)
        except:
            pass

        # Generate dummy binary mask
        mask_array = np.zeros_like(image_array)
        center_x, center_y = mask_array.shape[1] // 2, mask_array.shape[0] // 2
        mask_size = 30
        mask_array[
            center_y - mask_size // 2:center_y + mask_size // 2,
            center_x - mask_size // 2:center_x + mask_size // 2
        ] = 1
        mask = sitk.GetImageFromArray(mask_array.astype(np.uint8))
        mask.CopyInformation(image)

        features = extractor.execute(image, mask, label=1)
        filtered = {k: v for k, v in features.items() if not k.startswith("diagnostics")}
        X_radiomics = pd.DataFrame([filtered])

        semantic_features = {
            'Subtlety': 0, 'Internalstructure': 0, 'Calcification': 0,
            'Sphericity': 0, 'Margin': 0, 'Lobulation': 0,
            'Spiculation': 0, 'Texture': 0
        }
        X_semantic = pd.DataFrame([semantic_features])
        X_combined = pd.concat([X_semantic, X_radiomics], axis=1)

        expected_features = model.feature_names_in_
        for col in expected_features:
            if col not in X_combined.columns:
                X_combined[col] = 0
        X_input = X_combined[expected_features]

        y_pred = model.predict(X_input)
        y_proba = model.predict_proba(X_input)
        label = "Malignant" if y_pred[0] == 1 else "Benign"
        confidence = float(y_proba[0][y_pred[0]]) * 100

        # Create the PDF report
        output_path = f"{REPORT_FOLDER}/{uuid.uuid4()}.pdf"
        c = canvas.Canvas(output_path, pagesize=letter)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(200, 770, "PulmoScan Clinical Report")

        c.setFont("Helvetica", 10)
        c.drawString(50, 750, f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        c.drawString(50, 735, f"Model Used: Random Forest with Lasso-selected features")
        c.drawString(50, 720, "-" * 80)

        # Patient Information (if available)
        c.drawString(50, 705, "Patient Information:")
        patient_id = getattr(ds, 'PatientID', 'N/A')
        study_date = getattr(ds, 'StudyDate', 'N/A')
        modality = getattr(ds, 'Modality', 'N/A')
        c.drawString(70, 690, f"Patient ID: {patient_id}")
        c.drawString(70, 675, f"Study Date: {study_date}")
        c.drawString(70, 660, f"Modality: {modality}")

        # Prediction
        c.drawString(50, 640, "Prediction Results:")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(70, 625, f"Diagnosis: {label}")
        c.drawString(70, 610, f"Confidence: {confidence:.2f}%")
        c.setFont("Helvetica", 10)

        # Feature Summary (Top 5 important features if desired)
        top_features = X_input.iloc[0].sort_values(ascending=False).head(5)
        c.drawString(50, 590, "Top 5 Radiomic Feature Values:")
        y_offset = 575
        for feat, val in top_features.items():
            c.drawString(70, y_offset, f"{feat}: {val:.4f}")
            y_offset -= 15

        # Disclaimer
        c.setFont("Helvetica-Oblique", 8)
        c.drawString(50, 100, "Disclaimer: This report is generated by AI and is not a substitute for professional clinical evaluation.")
        c.drawString(50, 85, "Please consult a licensed physician for a final diagnosis.")

        c.save()
        return output_path, label, y_proba, y_pred

    except Exception as e:
        return f"❌ Error: {str(e)}", 500
    

def process_dicom_folder(folder_path):
    try:
        semantic_features_list = []
        radiomic_features_list = []
        filenames = []

        # Extract features for each file
        for root, _, files in os.walk(folder_path):
            for fname in files:
                if not fname.endswith('.dcm'):
                    continue
                file_path = os.path.join(root, fname)
                try:
                    ds = pydicom.dcmread(file_path)
                    image_array = ds.pixel_array
                    image = sitk.GetImageFromArray(image_array.astype(np.float32))

                    try:
                        spacing = (float(ds.PixelSpacing[0]), float(ds.PixelSpacing[1]), float(ds.SliceThickness))
                        image.SetSpacing(spacing)
                    except:
                        pass

                    # Dummy mask
                    mask_array = np.zeros_like(image_array)
                    cx, cy = mask_array.shape[1]//2, mask_array.shape[0]//2
                    size = 30
                    mask_array[cy-size//2:cy+size//2, cx-size//2:cx+size//2] = 1
                    mask = sitk.GetImageFromArray(mask_array.astype(np.uint8))
                    mask.CopyInformation(image)

                    features = extractor.execute(image, mask, label=1)
                    filtered = {k: v for k, v in features.items() if not k.startswith('diagnostics')}
                    radiomic_features_list.append(filtered)
                    semantic_features_list.append({
                        'Subtlety': 0, 'Internalstructure': 0, 'Calcification': 0,
                        'Sphericity': 0, 'Margin': 0, 'Lobulation': 0,
                        'Spiculation': 0, 'Texture': 0
                    })
                    filenames.append(fname)
                except Exception as e:
                    print(f"⚠️ Skipping {fname}: {e}")

        if not radiomic_features_list:
            return ("No valid DICOM files processed.", 400)

        # Build DataFrame
        X_semantic = pd.DataFrame(semantic_features_list)
        X_radiomics = pd.DataFrame(radiomic_features_list).fillna(0)
        X_combined = pd.concat([X_semantic.reset_index(drop=True), X_radiomics.reset_index(drop=True)], axis=1)

        expected_features = model.feature_names_in_
        for col in expected_features:
            if col not in X_combined.columns:
                X_combined[col] = 0
        X_input = X_combined[expected_features]

        # Predictions
        y_pred = model.predict(X_input)
        y_proba = model.predict_proba(X_input)
        confidences = [prob[pred] * 100 for pred, prob in zip(y_pred, y_proba)]
        avg_confidence = sum(confidences) / len(confidences)

        # Prepare report
        report_filename = f"{uuid.uuid4()}.pdf"
        report_path = os.path.join(REPORT_FOLDER, report_filename)
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        c = canvas.Canvas(report_path, pagesize=letter)

        # Header
        c.setFont("Helvetica-Bold", 16)
        c.drawString(200, 770, "PulmoScan Batch Classification Report")
        c.setFont("Helvetica", 10)
        c.drawString(50, 750, f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        c.drawString(50, 735, f"Total Processed Files: {len(filenames)}")
        c.drawString(50, 720, f"Average Confidence: {avg_confidence:.2f}%")
        c.drawString(50, 705, f"Malignant Nodules: {sum(1 for p in y_pred if p==1)}")
        c.drawString(50, 690, f"Benign Nodules: {sum(1 for p in y_pred if p==0)}")
        c.drawString(50, 675, "-" * 80)

        # Detailed results with top features
        y_offset = 660
        for i, (fname, pred, prob) in enumerate(zip(filenames, y_pred, y_proba)):
            label = "Malignant" if pred == 1 else "Benign"
            confidence = prob[pred] * 100
            line = f"{i+1}. {fname}: {label} ({confidence:.2f}%)"
            if y_offset < 100:
                c.showPage()
                y_offset = 770
            c.setFont("Helvetica-Bold", 10)
            c.drawString(50, y_offset, line)
            y_offset -= 15
            # Top 3 features for this file
            top_feats = X_input.iloc[i].sort_values(ascending=False).head(3)
            feat_line = "Top features: " + ", ".join([f"{f}: {v:.3f}" for f, v in top_feats.items()])
            c.setFont("Helvetica", 9)
            if y_offset < 100:
                c.showPage()
                y_offset = 770
            c.drawString(70, y_offset, feat_line)
            y_offset -= 20

        # Disclaimer
        if y_offset < 120:
            c.showPage()
            y_offset = 770
        c.setFont("Helvetica-Oblique", 8)
        c.drawString(50, 100, "Disclaimer: This report is generated by AI and is not a substitute for professional clinical evaluation.")
        c.drawString(50, 85, "Please consult a licensed physician for a final diagnosis.")

        c.save()
        return report_path

    except Exception as e:
        print(f"Error in batch processing: {e}")
        return (f"❌ Error processing folder: {e}", 500)

# Route: download reports
@classification1.route('/static/reports/<filename>')
@login_required
def download_report(filename):
    return send_from_directory(directory='static/reports', path=filename, as_attachment=True)