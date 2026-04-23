#!/usr/bin/env python3
"""
Unit tests for Veggie Magic web application
Tests meal data integrity, filter functionality, and CSV generation
"""

import json
import unittest
import os
import tempfile
import csv
from unittest.mock import patch, MagicMock
import sys

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestVeggieMagic(unittest.TestCase):
    """Test suite for Veggie Magic functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.meals_file = 'meals.json'
        self.test_meals = {
            "meals": [
                {"name": "Lemon Herb Pasta", "miracleFruitCompatible": True},
                {"name": "Spinach Salad", "miracleFruitCompatible": False},
                {"name": "Pickled Beets", "miracleFruitCompatible": True},
                {"name": "Roasted Vegetables", "miracleFruitCompatible": False}
            ]
        }
    
    def test_meals_json_exists(self):
        """Test that meals.json file exists and is valid JSON"""
        self.assertTrue(os.path.exists(self.meals_file), "meals.json file should exist")
        
        with open(self.meals_file, 'r') as f:
            data = json.load(f)
        
        self.assertIn('meals', data, "meals.json should contain 'meals' key")
        self.assertIsInstance(data['meals'], list, "meals should be a list")
    
    def test_meal_data_structure(self):
        """Test that each meal has required fields"""
        with open(self.meals_file, 'r') as f:
            data = json.load(f)
        
        for meal in data['meals']:
            self.assertIn('name', meal, f"Meal {meal} should have 'name' field")
            self.assertIn('miracleFruitCompatible', meal, f"Meal {meal} should have 'miracleFruitCompatible' field")
            self.assertIsInstance(meal['name'], str, f"Meal name should be string")
            self.assertIsInstance(meal['miracleFruitCompatible'], bool, f"miracleFruitCompatible should be boolean")
            self.assertTrue(meal['name'].strip(), f"Meal name should not be empty")
    
    def test_miracle_fruit_filter_logic(self):
        """Test miracle fruit filter logic"""
        with open(self.meals_file, 'r') as f:
            data = json.load(f)
        
        all_meals = data['meals']
        compatible_meals = [meal for meal in all_meals if meal['miracleFruitCompatible']]
        incompatible_meals = [meal for meal in all_meals if not meal['miracleFruitCompatible']]
        
        # Test that filter works correctly
        self.assertTrue(len(compatible_meals) > 0, "Should have at least one miracle fruit compatible meal")
        self.assertTrue(len(incompatible_meals) > 0, "Should have at least one incompatible meal")
        self.assertEqual(len(compatible_meals) + len(incompatible_meals), len(all_meals), "Filtered meals should equal total meals")
        
        # Test that compatible meals contain expected keywords
        sour_keywords = ['lemon', 'pickled', 'kimchi', 'sauerkraut', 'yogurt', 'tamarind', 'grapefruit']
        found_sour = any(any(keyword in meal['name'].lower() for keyword in sour_keywords) 
                       for meal in compatible_meals)
        self.assertTrue(found_sour, "Compatible meals should contain sour-related keywords")
    
    def test_csv_generation_format(self):
        """Test CSV generation format"""
        with open(self.meals_file, 'r') as f:
            data = json.load(f)
        
        # Simulate CSV generation
        headers = ['Recipe Name', 'Miracle Fruit Compatible']
        csv_content = [
            ','.join(headers),
            *[f'"{meal["name"]}",{"Yes" if meal["miracleFruitCompatible"] else "No"}' 
              for meal in data['meals']]
        ]
        csv_string = '\n'.join(csv_content)
        
        # Test CSV format
        lines = csv_string.split('\n')
        self.assertEqual(lines[0], 'Recipe Name,Miracle Fruit Compatible', "CSV should have correct headers")
        self.assertEqual(len(lines), len(data['meals']) + 1, "CSV should have header + one line per meal")
        
        # Test CSV parsing
        reader = csv.reader(csv_string.split('\n'))
        csv_headers = next(reader)
        self.assertEqual(csv_headers, ['Recipe Name', 'Miracle Fruit Compatible'])
        
        # Count rows
        row_count = sum(1 for row in reader)
        self.assertEqual(row_count, len(data['meals']))
    
    def test_html_file_exists(self):
        """Test that index.html exists and contains required elements"""
        self.assertTrue(os.path.exists('index.html'), "index.html should exist")
        
        with open('index.html', 'r') as f:
            content = f.read()
        
        # Test for required React components
        self.assertIn('useState', content, "Should contain useState hook")
        self.assertIn('getRandomMeal', content, "Should contain getRandomMeal function")
        self.assertIn('downloadCSV', content, "Should contain downloadCSV function")
        self.assertIn('miracleFruitFilter', content, "Should contain miracle fruit filter")
        
        # Test for required UI elements
        self.assertIn('Get New Idea', content, "Should contain Get New Idea button")
        self.assertIn('Download CSV', content, "Should contain Download CSV button")
        self.assertIn('Miracle Fruit Compatible', content, "Should contain filter checkbox")
    
    def test_no_empty_meal_names(self):
        """Test that no meal names are empty or just whitespace"""
        with open(self.meals_file, 'r') as f:
            data = json.load(f)
        
        for meal in data['meals']:
            self.assertTrue(meal['name'].strip(), f"Meal name should not be empty: {meal}")
            self.assertNotEqual(meal['name'].lower(), 'null', f"Meal name should not be 'null': {meal}")
            self.assertNotEqual(meal['name'].lower(), 'undefined', f"Meal name should not be 'undefined': {meal}")

def run_tests():
    """Run all tests and return results"""
    print("🥬 Running Veggie Magic Unit Tests...")
    print("=" * 50)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestVeggieMagic)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)
    
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✅ All tests passed! Ready to commit.")
        return True
    else:
        print("❌ Some tests failed. Fix issues before committing.")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        return False

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
