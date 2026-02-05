import pandas as pd
import numpy as np
from pathlib import Path
import config
from .logger import logger

def load_csv(file_path):
    """Load CSV file and return dataframe"""
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Loaded CSV: {file_path} with shape {df.shape}")
        return df
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return None
    except Exception as e:
        logger.error(f"Error loading CSV: {str(e)}")
        return None

def save_csv(df, file_path, index=False):
    """Save dataframe to CSV file"""
    try:
        df.to_csv(file_path, index=index)
        logger.info(f"Saved CSV: {file_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving CSV: {str(e)}")
        return False

def validate_data(df):
    """Validate data quality"""
    if df is None:
        logger.warning("DataFrame is None")
        return False
    
    if df.empty:
        logger.warning("DataFrame is empty")
        return False
    
    logger.info(f"Data shape: {df.shape}")
    logger.info(f"Missing values:\n{df.isnull().sum()}")
    return True

def save_report(content, filename=None):
    """Save report to output folder"""
    if filename is None:
        filename = config.REPORT_FILE
    
    report_path = config.OUTPUT_DIR / filename
    try:
        with open(report_path, 'w') as f:
            f.write(content)
        logger.info(f"Report saved: {report_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving report: {str(e)}")
        return False
