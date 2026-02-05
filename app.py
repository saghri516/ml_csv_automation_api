"""
FastAPI for Machine Learning CSV Automation
Enables predictions via REST API with automatic documentation
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pathlib import Path
from datetime import datetime
from models.autom_model import AutomatedMLModel
from src.logger import logger
import traceback
import uvicorn
from io import BytesIO

app = FastAPI(
    title="ML CSV Automation API",
    description="Automated Machine Learning for CSV files",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model instance
model = None

@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    global model
    model_path = Path('models/trained_model.pkl')
    if model_path.exists():
        model = AutomatedMLModel()
        model.load_model(str(model_path))
        logger.info("Model loaded on startup")
    else:
        logger.info("No pre-trained model found")

@app.get("/", tags=["Info"])
async def root():
    """Get API information and available endpoints"""
    return {
        "name": "ML CSV Automation API",
        "version": "1.0",
        "framework": "FastAPI",
        "endpoints": {
            "GET /": "API information",
            "GET /docs": "Swagger UI documentation",
            "GET /redoc": "ReDoc documentation",
            "GET /health": "Health check",
            "POST /validate-csv": "Validate CSV format",
            "POST /train": "Train new model",
            "POST /predict": "Make predictions",
            "GET /model-info": "Get model information"
        },
        "docs_url": "http://localhost:5000/docs",
        "redoc_url": "http://localhost:5000/redoc"
    }

@app.get("/health", tags=["Monitoring"])
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "model_loaded": model is not None
    }

@app.get("/model-info", tags=["Model"])
async def model_info():
    """Get model information"""
    if model is None:
        raise HTTPException(status_code=404, detail="Model not loaded. Train a model first.")
    
    try:
        summary = model.get_model_summary()
        return summary
    except Exception as e:
        logger.error(f"Error getting model info: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/validate-csv", tags=["Utilities"])
async def validate_csv(file: UploadFile = File(...)):
    """Validate CSV format"""
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="File must be CSV format")
        
        # Read CSV
        contents = await file.read()
        df = pd.read_csv(BytesIO(contents))
        
        validation_result = {
            "valid": True,
            "shape": list(df.shape),
            "columns": list(df.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "missing_values": df.isnull().sum().to_dict(),
            "duplicates": int(df.duplicated().sum())
        }
        
        logger.info(f"CSV validation successful: {df.shape}")
        return validation_result
        
    except Exception as e:
        logger.error(f"CSV validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid CSV: {str(e)}")

@app.post("/predict", tags=["Prediction"])
async def predict(file: UploadFile = File(...)):
    """Make predictions from uploaded CSV"""
    try:
        if model is None:
            raise HTTPException(status_code=404, detail="Model not loaded. Train a model first.")
        
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="File must be CSV format")
        
        # Read CSV
        contents = await file.read()
        df = pd.read_csv(BytesIO(contents))
        
        # Check if CSV is empty
        if df.empty:
            raise HTTPException(status_code=400, detail="CSV file is empty")
        
        # Validate features only if model has trained features
        if model.feature_columns:
            missing_features = set(model.feature_columns) - set(df.columns)
            if missing_features:
                raise HTTPException(
                    status_code=400,
                    detail=f"Missing features: {list(missing_features)}. Expected: {model.feature_columns}"
                )
        
        # Make predictions with DataFrame (not filename)
        predictions_df = model.predict(df)
        
        # Save predictions
        output_file = Path('output') / f"predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        predictions_df.to_csv(output_file, index=False)
        
        # Return results
        result = {
            "status": "success",
            "total_predictions": len(predictions_df),
            "predictions": predictions_df.to_dict('records')[:10],
            "saved_to": str(output_file),
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Predictions made successfully: {len(predictions_df)} samples")
        return result
        
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/train", tags=["Training"])
async def train(file: UploadFile = File(...)):
    """Train new model from uploaded CSV"""
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="File must be CSV format")
        
        # Save temporary file
        temp_path = Path('data') / 'temp_train.csv'
        contents = await file.read()
        with open(temp_path, 'wb') as f:
            f.write(contents)
        
        # Train model
        global model
        model = AutomatedMLModel()
        results = model.train(str(temp_path))
        
        if not results.get('success'):
            return {"status": "error", "error": results.get('error', 'Training failed')}
        
        # Save model
        model_path = Path('models') / f"model_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"
        model.save_model(str(model_path))
        
        # Clean temp file
        temp_path.unlink()
        
        # Prepare response
        response = {
            "status": "success",
            "message": "Model trained successfully",
            "accuracy": float(results['accuracy']),
            "precision": float(results['precision']),
            "recall": float(results['recall']),
            "f1_score": float(results['f1_score']),
            "model_saved": str(model_path),
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Model trained: Accuracy={results['accuracy']:.4f}")
        return response
        
    except Exception as e:
        logger.error(f"Training error: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}", tags=["Utilities"])
async def download_file(filename: str):
    """Download prediction file"""
    try:
        file_path = Path('output') / filename
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type='text/csv'
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Create necessary directories
    Path('data').mkdir(exist_ok=True)
    Path('models').mkdir(exist_ok=True)
    Path('output').mkdir(exist_ok=True)
    Path('logs').mkdir(exist_ok=True)


if __name__ == "__main__":
    """Run the server only when app.py is executed directly"""
    logger.info("Starting FastAPI server...")
    
    # Run with uvicorn
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=5000,
        reload=False,
        log_level="info"
    )
