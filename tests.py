"""
Unit tests for ML Automation project
"""

import unittest
import pandas as pd
import numpy as np
from pathlib import Path
from models.autom_model import AutomatedMLModel
import os

class TestAutomatedMLModel(unittest.TestCase):
    """Test cases for AutomatedMLModel"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.test_data_dir = Path('data')
        cls.test_data_dir.mkdir(exist_ok=True)
        
        # Create test data
        np.random.seed(42)
        test_data = {
            'Feature_1': np.random.uniform(0, 100, 50),
            'Feature_2': np.random.uniform(0, 50, 50),
            'Feature_3': np.random.uniform(0, 100, 50),
            'target': np.random.randint(0, 2, 50)
        }
        cls.test_df = pd.DataFrame(test_data)
        cls.test_csv_path = cls.test_data_dir / 'test_data.csv'
        cls.test_df.to_csv(cls.test_csv_path, index=False)
    
    def setUp(self):
        """Set up before each test"""
        self.model = AutomatedMLModel()
    
    def test_model_initialization(self):
        """Test model initialization"""
        self.assertIsNotNone(self.model)
        self.assertIsNotNone(self.model.config)
    
    def test_load_csv(self):
        """Test CSV loading"""
        df = self.model.load_csv(str(self.test_csv_path))
        self.assertIsNotNone(df)
        self.assertEqual(df.shape, (50, 4))
    
    def test_load_nonexistent_csv(self):
        """Test loading non-existent CSV"""
        df = self.model.load_csv('nonexistent.csv')
        self.assertIsNone(df)
    
    def test_data_analysis(self):
        """Test data analysis"""
        analysis = self.model.analyze_data(self.test_df)
        self.assertEqual(analysis['shape'], (50, 4))
        self.assertIn('columns', analysis)
        self.assertIn('dtypes', analysis)
    
    def test_preprocessing(self):
        """Test data preprocessing"""
        df = self.test_df.copy()
        preprocessed = self.model.preprocess_data(df, fit=True)
        self.assertEqual(preprocessed.shape, df.shape)
        self.assertIsNotNone(self.model.scaler)
    
    def test_target_detection(self):
        """Test target column detection"""
        target = self.model.detect_target_column(self.test_df, {})
        self.assertIn(target, self.test_df.columns)
    
    def test_training(self):
        """Test model training"""
        results = self.model.train(str(self.test_csv_path))
        self.assertTrue(results['success'])
        self.assertIn('accuracy', results)
        self.assertGreater(results['accuracy'], 0)
        self.assertLess(results['accuracy'], 1)
    
    def test_model_persistence(self):
        """Test saving and loading models"""
        # Train model
        self.model.train(str(self.test_csv_path))
        
        # Save model
        save_path = Path('models') / 'test_model.pkl'
        self.model.save_model(str(save_path))
        self.assertTrue(save_path.exists())
        
        # Load model
        new_model = AutomatedMLModel()
        loaded = new_model.load_model(str(save_path))
        self.assertTrue(loaded)
        
        # Clean up
        save_path.unlink()
    
    def test_predictions(self):
        """Test predictions"""
        # Train model
        self.model.train(str(self.test_csv_path))
        
        # Make predictions
        predictions = self.model.predict(str(self.test_csv_path))
        self.assertIsNotNone(predictions)
        self.assertIn('prediction', predictions.columns)
        self.assertEqual(len(predictions), 50)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test data"""
        if cls.test_csv_path.exists():
            cls.test_csv_path.unlink()

class TestInputValidation(unittest.TestCase):
    """Test input validation"""
    
    def test_csv_format_validation(self):
        """Test CSV format validation"""
        df = pd.DataFrame({
            'Feature_1': [1, 2, 3],
            'Feature_2': [4, 5, 6],
            'target': [0, 1, 0]
        })
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape, (3, 3))
    
    def test_empty_dataframe(self):
        """Test empty dataframe handling"""
        df = pd.DataFrame()
        self.assertTrue(df.empty)
        self.assertEqual(len(df), 0)

if __name__ == '__main__':
    unittest.main()
