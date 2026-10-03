# Customer Persona Segmenter

## 📌 Project Overview

Customer Persona Segmenter is an **Unsupervised Machine Learning project** that groups customers into meaningful behavioural segments based on their **annual income** and **spending score**.

The project uses the **K-Means Clustering algorithm** to discover customer groups. The resulting clusters are analyzed and mapped to meaningful customer personas.

The trained machine learning model is integrated with a **FastAPI backend**, while **Streamlit** provides an interactive dashboard for prediction, analytics, visualization, and CSV-based customer segmentation.

---

## 🎯 Objectives

- Analyze customer income and spending behaviour.
- Group similar customers using K-Means clustering.
- Standardize features using StandardScaler.
- Determine a suitable number of clusters using the Elbow Method and Silhouette Score.
- Analyze and interpret the resulting clusters.
- Convert numerical clusters into meaningful customer personas.
- Provide customer persona prediction through an API.
- Build an interactive Streamlit dashboard.
- Support CSV upload for batch customer segmentation.
- Allow users to download the segmented customer data.

---

## 🧠 Machine Learning Approach

This project uses **Unsupervised Learning**, because the customer dataset does not contain predefined persona labels.

### Algorithm

**K-Means Clustering**

K-Means groups customers based on the similarity of their selected features.

### Features Used

- `annual_income_k` — Annual income in thousands
- `spending_score` — Customer spending score

### Preprocessing

The selected features are standardized using:

```text
StandardScaler
