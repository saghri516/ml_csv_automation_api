import pandas as pd
import config
from .logger import logger
from .utils import load_csv, save_csv, save_report
from .train import load_model

def make_predictions(data_file):
    """Make predictions on new data"""
    logger.info(f"Making predictions on: {data_file}")
    
    # Load data
    df = load_csv(config.DATA_DIR / data_file)
    if df is None:
        logger.error("Failed to load data for predictions")
        return None
    
    # Load model
    model = load_model()
    if model is None:
        logger.error("Failed to load model for predictions")
        return None
    
    # Prepare features (exclude target column if present)
    X = df.drop(columns=[col for col in ['target', 'label', 'class'] if col in df.columns], errors='ignore')
    
    # Make predictions
    predictions = model.predict(X)
    logger.info(f"Generated {len(predictions)} predictions")
    
    # Create results dataframe
    results_df = X.copy()
    results_df['prediction'] = predictions
    
    # Save predictions
    predictions_path = config.OUTPUT_DIR / config.PREDICTIONS_FILE
    save_csv(results_df, predictions_path)
    
    # Generate summary report
    summary = f"""
PREDICTION SUMMARY
==================
Input File: {data_file}
Total Predictions: {len(predictions)}
Prediction Distribution:
{pd.Series(predictions).value_counts().to_string()}

Predictions saved to: {predictions_path}
"""
    save_report(summary, "prediction_summary.txt")
    logger.info("Predictions completed successfully")
    
    return results_df
