#!/usr/bin/env python3
"""
Test runner script for Cloud Resume Challenge tests
"""

import unittest
import sys
import os

def run_unit_tests():
    """Run unit tests"""
    print("Running Unit Tests...")
    loader = unittest.TestLoader()
    suite = loader.discover('.', pattern='test_lambda_function.py')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()

def run_integration_tests():
    """Run integration tests"""
    print("\nRunning Integration Tests...")
    loader = unittest.TestLoader()
    suite = loader.discover('.', pattern='test_integration.py')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()

def run_e2e_tests():
    """Run end-to-end tests"""
    print("\nRunning End-to-End Tests...")
    loader = unittest.TestLoader()
    suite = loader.discover('.', pattern='test_e2e.py')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()

def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("Cloud Resume Challenge - Test Suite")
    print("=" * 50)
    
    all_passed = True
    
    # Run unit tests
    if not run_unit_tests():
        all_passed = False
    
    # Run integration tests
    if not run_integration_tests():
        all_passed = False
    
    # Run E2E tests (optional)
    try:
        if not run_e2e_tests():
            all_passed = False
    except Exception as e:
        print(f"E2E tests skipped: {e}")
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ ALL TESTS PASSED!")
        return 0
    else:
        print("❌ SOME TESTS FAILED!")
        return 1

if __name__ == '__main__':
    # Change to tests directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()
        if test_type == 'unit':
            success = run_unit_tests()
        elif test_type == 'integration':
            success = run_integration_tests()
        elif test_type == 'e2e':
            success = run_e2e_tests()
        else:
            print("Usage: python run_tests.py [unit|integration|e2e]")
            sys.exit(1)
        
        sys.exit(0 if success else 1)
    else:
        sys.exit(run_all_tests())