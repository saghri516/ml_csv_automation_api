"""
Main entry point for Machine Learning CSV Automation project
"""
import sys
from pathlib import Path
import config
from src.logger import logger
from src.utils import load_csv, validate_data
from src.train import train_model, load_model
from src.predict import make_predictions

def main():
    """Main execution function"""
    logger.info("=" * 50)
    logger.info("Machine Learning CSV Automation Started")
    logger.info("=" * 50)
    
    try:
        # Create necessary directories
        config.DATA_DIR.mkdir(exist_ok=True)
        config.MODELS_DIR.mkdir(exist_ok=True)
        config.OUTPUT_DIR.mkdir(exist_ok=True)
        config.LOGS_DIR.mkdir(exist_ok=True)
        
        logger.info("Directories verified/created")
        
        # Training phase
        if config.TRAIN_MODEL:
            logger.info("Starting training phase...")
            train_data_path = config.DATA_DIR / config.TRAIN_DATA_FILE
            
            if train_data_path.exists():
                # Load training data
                df = load_csv(train_data_path)
                
                if validate_data(df):
                    # Separate features and target
                    # Assuming last column is target - modify as needed
                    X = df.iloc[:, :-1]
                    y = df.iloc[:, -1]
                    
                    # Train model
                    model = train_model(X, y)
                    logger.info("Training completed successfully")
            else:
                logger.warning(f"Training data not found: {train_data_path}")
                logger.info("Place your training CSV in: data/train.csv")
        
        # Prediction phase
        logger.info("Starting prediction phase...")
        test_data_path = config.DATA_DIR / config.TEST_DATA_FILE
        
        if test_data_path.exists():
            results = make_predictions(config.TEST_DATA_FILE)
            if results is not None:
                logger.info("Predictions saved successfully")
        else:
            logger.warning(f"Test data not found: {test_data_path}")
            logger.info("Place your test CSV in: data/test.csv")
        
        logger.info("=" * 50)
        logger.info("Machine Learning CSV Automation Completed")
        logger.info("=" * 50)
        logger.info(f"Results saved to: {config.OUTPUT_DIR}")
        logger.info(f"Logs saved to: {config.LOGS_DIR}")
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}", exc_info=True)
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
print("")
