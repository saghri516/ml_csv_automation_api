import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import config
from .logger import logger
from .utils import load_csv, save_report

def train_model(X, y):
    """Train machine learning model"""
    logger.info("Training model...")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=config.TEST_SIZE, random_state=config.RANDOM_STATE
    )
    
    logger.info(f"Training set size: {X_train.shape[0]}, Test set size: {X_test.shape[0]}")
    
    # Train model
    model = RandomForestClassifier(random_state=config.RANDOM_STATE)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    logger.info(f"Model accuracy: {accuracy:.4f}")
    
    # Save model
    model_path = config.MODELS_DIR / config.MODEL_NAME
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    logger.info(f"Model saved: {model_path}")
    
    # Generate report
    report = classification_report(y_test, y_pred)
    logger.info(f"Classification Report:\n{report}")
    save_report(f"Model Accuracy: {accuracy}\n\n{report}")
    
    return model

def load_model():
    """Load trained model"""
    model_path = config.MODELS_DIR / config.MODEL_NAME
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        logger.info(f"Model loaded: {model_path}")
        return model
    except FileNotFoundError:
        logger.error(f"Model not found: {model_path}")
        return None
