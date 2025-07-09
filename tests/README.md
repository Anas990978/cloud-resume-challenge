# Cloud Resume Challenge - Test Suite

This directory contains comprehensive tests for the Cloud Resume Challenge project.

## Test Structure

```
tests/
├── test_lambda_function.py    # Unit tests for Lambda function
├── test_integration.py        # Integration tests for API and website
├── test_e2e.py               # End-to-end tests
├── run_tests.py              # Test runner script
├── requirements.txt          # Test dependencies
└── README.md                 # This file
```

## Test Types

### 1. Unit Tests (`test_lambda_function.py`)
- Tests Lambda function logic in isolation
- Uses mocked DynamoDB for testing
- Validates response format and CORS headers
- Tests visitor counter increment logic

### 2. Integration Tests (`test_integration.py`)
- Tests actual API Gateway endpoints
- Validates API response format and performance
- Tests website accessibility
- Verifies CORS configuration

### 3. End-to-End Tests (`test_e2e.py`)
- Tests complete user journey
- Browser-based testing with Selenium
- Mobile responsiveness testing
- Validates all website sections

## Running Tests

### Install Dependencies
```bash
cd tests
pip install -r requirements.txt
```

### Run All Tests
```bash
python run_tests.py
```

### Run Specific Test Types
```bash
# Unit tests only
python run_tests.py unit

# Integration tests only
python run_tests.py integration

# End-to-end tests only
python run_tests.py e2e
```

### Run Individual Test Files
```bash
# Unit tests
python -m unittest test_lambda_function.py

# Integration tests
python -m unittest test_integration.py

# E2E tests
python -m unittest test_e2e.py
```

## Test Coverage

### Lambda Function Tests
- ✅ New visitor handling
- ✅ Existing visitor increment
- ✅ Response format validation
- ✅ CORS headers verification
- ✅ DynamoDB interaction mocking

### API Integration Tests
- ✅ Endpoint accessibility
- ✅ Response format validation
- ✅ CORS headers verification
- ✅ Counter increment functionality
- ✅ Performance testing

### Website Tests
- ✅ Website accessibility
- ✅ Visitor counter presence
- ✅ All sections validation
- ✅ Social links verification
- ✅ Mobile responsiveness

## CI/CD Integration

Tests are automatically run in GitHub Actions:
- **Unit tests** run on every push/PR
- **Integration tests** run after unit tests pass
- **E2E tests** can be run manually or on schedule

## Test Environment Variables

For E2E tests with Selenium:
```bash
export RUN_SELENIUM_TESTS=true
```

## Dependencies

- `boto3`: AWS SDK for Python
- `moto`: AWS service mocking
- `requests`: HTTP library for API testing
- `selenium`: Browser automation (optional)
- `unittest-xml-reporting`: XML test reports

## Best Practices

1. **Isolation**: Each test is independent
2. **Mocking**: External dependencies are mocked in unit tests
3. **Real Testing**: Integration tests use real endpoints
4. **Error Handling**: Tests handle network failures gracefully
5. **Documentation**: Each test has clear docstrings