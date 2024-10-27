
# Phishing Detection Using Machine Learning

This project focuses on identifying phishing websites by analyzing various URL and webpage features. By leveraging machine learning, we aim to predict whether a given website is legitimate or a phishing attempt based on features like IP address, SSL state, and URL structure. The project is containerized using Docker, with data versioning through DVC, and experiment tracking using MLflow. Additionally, DAGsHub is used as a remote repository for data storage and monitoring.

---

## Table of Contents

- [Overview](#overview)
- [Dataset Features](#dataset-features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Future Enhancements](#future-enhancements)


## Overview

Phishing attacks are a significant cybersecurity threat, with attackers attempting to trick users into visiting fraudulent websites. This project uses machine learning models to classify webpages as **phishing** or **legitimate** based on URL patterns and network-related features. Tools like **DVC**, **MLflow**, **Docker**, and **DAGsHub** were used to streamline the machine learning lifecycle, including data versioning, experiment tracking, and deployment.



## Technologies Used

- **Python**: Core programming language
- **Machine Learning**: Scikit-learn, Pandas, NumPy
- **Data Versioning**: DVC
- **Experiment Tracking**: MLflow
- **Containerization**: Docker
- **Remote Storage and Monitoring**: DAGsHub

## Project Structure

```plaintext
├── data/               # Dataset and DVC-managed data
├── src/                # Source code for data processing, feature engineering, and model training
├── experiments/        # MLflow experiment tracking directory
├── models/             # Saved model artifacts
├── Dockerfile          # Docker configuration file
├── requirements.txt    # Project dependencies
├── dvc.yaml            # DVC pipeline configuration
└── README.md           # Project documentation
```

## Setup Instructions

### Prerequisites

1. **Docker**: Install [Docker](https://docs.docker.com/get-docker/).
2. **DVC**: Install [DVC](https://dvc.org/doc/install).
3. **MLflow**: Install [MLflow](https://mlflow.org/docs/latest/quickstart.html).
4. **DAGsHub Account**: [DAGsHub](https://dagshub.com) for remote data storage.

### Step-by-Step Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Tafique-Hossain-khan/Network-security.git
   cd phishing-detection
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize DVC**
   ```bash
   dvc init
   dvc remote add -d origin <your-dagshub-dvc-url>
   ```

4. **Pull Data from DVC**
   ```bash
   dvc pull
   ```

5. **Start MLflow Server** (for local experiment tracking)
   ```bash
   mlflow ui
   ```

6. **Build and Run Docker Container**
   ```bash
   docker build -t phishing-detection .
   docker run -p 8501:8501 phishing-detection
   ```

### Environment Variables

Add a `.env` file to securely manage sensitive information like API keys, especially if using third-party services.

## Usage

1. **Data Versioning**: Track and manage dataset changes using DVC. Sync data with DAGsHub to maintain a record of data and transformations.
2. **Experiment Tracking**: Run experiments and track model performance with MLflow.
3. **Docker for Deployment**: Deploy the application via Docker for an efficient, dependency-free environment.
4. **DAGsHub for Remote Monitoring**: Store data and track experiments in DAGsHub for easy collaboration and monitoring.

## Future Enhancements

- **Enhanced Feature Engineering**: Explore additional features for improved accuracy.
- **Real-Time Prediction API**: Develop an API to classify URLs in real-time.
- **Automated CI/CD**: Integrate GitHub Actions or Jenkins for automated testing and deployment.

