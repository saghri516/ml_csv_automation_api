import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"
CONFIGS_DIR = BASE_DIR / "configs"

# Data configuration
TRAIN_DATA_FILE = "train.csv"
TEST_DATA_FILE = "test.csv"
TEST_SIZE = 0.2
RANDOM_STATE = 42

# Model configuration
MODEL_TYPE = "random_forest"  # Options: random_forest, svm, neural_network, etc.
MODEL_NAME = "model.pkl"
TRAIN_MODEL = True

# Prediction configuration
PREDICTIONS_FILE = "predictions.csv"
REPORT_FILE = "report.txt"

# Logging
LOG_FILE = LOGS_DIR / "execution.log"
LOG_LEVEL = "INFO"
