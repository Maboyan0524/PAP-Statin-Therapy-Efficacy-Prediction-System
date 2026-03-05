# PAP Statin Therapy Efficacy Prediction System

A machine learning platform for predicting statin therapy efficacy in Pulmonary Alveolar Proteinosis (PAP), featuring automated feature selection, stacking ensemble modelling, and SHAP interpretability analysis.

---

## Overview

This system provides a complete, automated machine learning workflow designed for clinical prediction research in PAP. It integrates six feature selection methods, eleven base classifiers, a stacking ensemble strategy, and SHAP-based model interpretability — all accessible through a clean graphical interface.

---

## Features

- **Adaptive Feature Selection** — Six methods (Lasso, RFE, Random Forest, XGBoost, Mutual Information, SelectKBest) with automatic early stopping and cross-validated AUC comparison
- **Stacking Ensemble** — Dynamic filtering of base learners by CV stability and performance; logistic regression meta-learner
- **SHAP Interpretability** — Feature importance bar charts, beeswarm summary plots, and dependence plots
- **Full Visualisation Output** — ROC curves, precision-recall curves, confusion matrices; export as PDF / PNG / SVG at up to 1200 DPI
- **Clean GUI** — Tab-based navigation, live run log, progress tracker, and data preview

---

## Screenshots

### Login
![Login](screenshots/login.png)

### Data Input & Configuration
![Data Input](screenshots/data_input.png)

### Run Analysis — Live Log
![Run Analysis](screenshots/run_analysis.png)

---

## Installation

**Requirements:** Python 3.8+

```bash
pip install pandas numpy scikit-learn xgboost lightgbm catboost shap matplotlib seaborn openpyxl
```

Run the application:

```bash
python "The PAP Statin Therapy Efficacy Prediction System.py"
```

> Default login — username: `1`, password: `1`

---

## Usage

| Step | Tab | Action |
|------|-----|--------|
| 1 | **Data Input** | Load training and test Excel files; set label column and output path |
| 2 | **Feature Selection** | Choose methods; configure CV folds and early stopping patience |
| 3 | **Model Config** | Select base classifiers; configure stacking thresholds |
| 4 | **Run Analysis** | Click **▶ Start Analysis** and monitor the live log |
| 5 | **Results** | Click **Refresh Results** to view the performance comparison table |
| 6 | **SHAP** | Select a target model and generate interpretability charts |

### Data Format

- Excel format (`.xlsx` / `.xls`); one sample per row, one feature per column
- Must include a binary label column (`0` = control, `1` = case)
- Feature columns must be numeric; missing values are handled automatically
- Training set ≥ 50 rows recommended; test set ≥ 20 rows
- Training and test sets must share identical feature column names

---

## Workflow

```
Data Load → Missing Value Imputation → Adaptive Feature Selection
    → Base Classifier Training → Stacking Ensemble → Visualisation → SHAP
```

**Feature Selection Strategy**
- Lasso: natural selection — retains all non-zero coefficients
- Other five methods: incremental search with early stopping; the method achieving the highest CV AUC supplies the final feature subset

**Stacking Strategy**
- Stage 1: each base learner generates out-of-fold predicted probabilities via cross-validation
- Stage 2: a logistic regression meta-learner combines base learner outputs
- Dynamic filtering excludes learners exceeding the CV std threshold or falling below the minimum CV AUC threshold

---

## Output Files

| File | Description |
|------|-------------|
| `model_comparison.xlsx` | CV AUC, test AUC, precision, recall, F1 for all models |
| `roc_test.pdf` | ROC curves on the test set |
| `pr_curves.pdf` | Precision-recall curves on the test set |
| `confusion_matrices.pdf` | Confusion matrices for all models |
| `shap_importance_*.pdf` | SHAP feature importance bar chart |
| `shap_summary_*.pdf` | SHAP beeswarm summary plot |
| `shap_dependence_*.pdf` | SHAP dependence plots for top 3 features |

---

## Dependencies

| Package | Purpose |
|---------|---------|
| scikit-learn | Core ML algorithms and evaluation |
| xgboost / lightgbm / catboost | Gradient boosting classifiers |
| shap | Model interpretability |
| pandas / numpy | Data processing |
| matplotlib / seaborn | Visualisation |
| tkinter | GUI framework (Python built-in) |

---

## Citation

If you use this system in your research, please cite the associated publication (details to be updated upon acceptance).

---

## License

This project is intended for academic and clinical research use.
