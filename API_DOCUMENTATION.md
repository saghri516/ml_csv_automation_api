# API Documentation

## Overview
Machine Learning CSV Automation API provides REST endpoints for:
- Training ML models on CSV files
- Making predictions on new data
- Validating CSV format
- Getting model information

## Base URL
```
http://localhost:5000
```

## Authentication
Currently no authentication required. For production, configure API_KEY in .env

## Endpoints

### 1. Health Check
Check if API is running.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-04T10:30:00.000000",
  "model_loaded": true
}
```

---

### 2. Get API Info
Get available endpoints and API version.

**Endpoint:** `GET /`

**Response:**
```json
{
  "name": "ML CSV Automation API",
  "version": "1.0",
  "endpoints": {
    "POST /predict": "Make predictions from CSV file",
    "POST /train": "Train new model from CSV file",
    "GET /model-info": "Get current model information",
    "POST /validate-csv": "Validate CSV format",
    "GET /health": "Health check"
  }
}
```

---

### 3. Validate CSV
Validate CSV format before uploading.

**Endpoint:** `POST /validate-csv`

**Request:**
```
Content-Type: multipart/form-data

file: <your_file.csv>
```

**Example using curl:**
```bash
curl -X POST -F "file=@data/train.csv" http://localhost:5000/validate-csv
```

**Response:**
```json
{
  "valid": true,
  "shape": [200, 15],
  "columns": ["Feature_1", "Feature_2", ..., "target"],
  "dtypes": {
    "Feature_1": "float64",
    "target": "int64"
  },
  "missing_values": {
    "Feature_1": 0,
    "Feature_2": 0
  },
  "duplicates": 5
}
```

---

### 4. Train Model
Train a new model on provided CSV file.

**Endpoint:** `POST /train`

**Request:**
```
Content-Type: multipart/form-data

file: <your_training_file.csv>
```

**CSV Requirements:**
- Must include target column (last column recommended)
- At least 30 rows for training
- Numeric and categorical data supported

**Example using curl:**
```bash
curl -X POST -F "file=@data/train.csv" http://localhost:5000/train
```

**Response:**
```json
{
  "status": "success",
  "message": "Model trained successfully",
  "accuracy": 0.85,
  "precision": 0.84,
  "recall": 0.86,
  "f1_score": 0.85,
  "model_saved": "models/model_20260204_103000.pkl",
  "timestamp": "2026-02-04T10:30:00.000000"
}
```

---

### 5. Make Predictions
Make predictions on new CSV data.

**Endpoint:** `POST /predict`

**Request:**
```
Content-Type: multipart/form-data

file: <your_test_file.csv>
```

**CSV Requirements:**
- Must have same features as training data
- Don't include target column
- Same column names and order

**Example using curl:**
```bash
curl -X POST -F "file=@data/test.csv" http://localhost:5000/predict
```

**Response:**
```json
{
  "status": "success",
  "total_predictions": 100,
  "predictions": [
    {
      "Feature_1": 45.5,
      "Feature_2": 23.1,
      "prediction": 1,
      "confidence": 0.92
    },
    {
      "Feature_1": 67.8,
      "Feature_2": 34.2,
      "prediction": 0,
      "confidence": 0.88
    }
  ],
  "saved_to": "output/predictions_20260204_103000.csv",
  "timestamp": "2026-02-04T10:30:00.000000"
}
```

---

### 6. Get Model Info
Get information about currently loaded model.

**Endpoint:** `GET /model-info`

**Response:**
```json
{
  "model_type": "random_forest",
  "metadata": {
    "trained_at": "2026-02-04T10:00:00.000000",
    "accuracy": 0.85,
    "precision": 0.84,
    "recall": 0.86,
    "f1_score": 0.85,
    "features": ["Feature_1", "Feature_2", ..., "Feature_14"],
    "target_column": "target",
    "training_samples": 160,
    "test_samples": 40
  },
  "features": ["Feature_1", "Feature_2", ...],
  "target": "target"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid request"
}
```

### 404 Not Found
```json
{
  "error": "Model not loaded. Train a model first."
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

---

## Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| "No file provided" | File not included in request | Include file in multipart form-data |
| "File must be CSV format" | Wrong file type | Use .csv files only |
| "Missing features" | Test data missing training features | Ensure same columns as training data |
| "Model not loaded" | No trained model exists | Train a model first using /train |

---

## Usage Examples

### Python
```python
import requests

# Train model
files = {'file': open('data/train.csv', 'rb')}
response = requests.post('http://localhost:5000/train', files=files)
print(response.json())

# Make predictions
files = {'file': open('data/test.csv', 'rb')}
response = requests.post('http://localhost:5000/predict', files=files)
predictions = response.json()
print(f"Made {predictions['total_predictions']} predictions")
```

### JavaScript/Node.js
```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

// Train model
const formData = new FormData();
formData.append('file', fs.createReadStream('data/train.csv'));

axios.post('http://localhost:5000/train', formData)
  .then(res => console.log(res.data))
  .catch(err => console.error(err));

// Make predictions
axios.post('http://localhost:5000/predict', formData)
  .then(res => console.log(res.data))
  .catch(err => console.error(err));
```

### cURL
```bash
# Health check
curl http://localhost:5000/health

# Validate CSV
curl -X POST -F "file=@data/train.csv" http://localhost:5000/validate-csv

# Train model
curl -X POST -F "file=@data/train.csv" http://localhost:5000/train

# Make predictions
curl -X POST -F "file=@data/test.csv" http://localhost:5000/predict

# Get model info
curl http://localhost:5000/model-info
```

---

## Rate Limiting
- No rate limiting implemented (configure in production)
- Max file size: 100 MB (configurable in config)
- Max rows per file: 1,000,000 (configurable)

---

## Support
For issues or questions, check logs at `logs/app.log`

## CI/CD (GitHub Actions) 🔧
A GitHub Actions workflow lives at `.github/workflows/ci-cd.yml`. It runs on `push`/`pull_request` to `main` and performs linting, testing (with junit coverage reports), and builds a Docker image artifact. Artifacts include the `flake8` report and test reports (JUnit and coverage XML). The build step produces an `image.tar` artifact using Docker Buildx (no registry push by default).
