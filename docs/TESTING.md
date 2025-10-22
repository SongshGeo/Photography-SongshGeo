# GPS Extraction Test Suite

Comprehensive test suite for photography workflow scripts, following Google-style testing best practices.

## 🎯 Test Structure

```
tests/
├── __init__.py                 # Test package init
├── conftest.py                 # Shared pytest fixtures
├── test_gps_extraction.py      # GPS extraction tests
├── test_helpers.py             # Testing utilities
└── README.md                   # This file
```

## 🧪 Test Categories

### Unit Tests
Test individual functions and components:
- GPS data extraction
- Date range analysis
- Reverse geocoding
- GPX generation
- Location validation

### Integration Tests
Test complete workflows:
- End-to-end pipeline
- File I/O operations
- API interactions

### Edge Case Tests
Test boundary conditions:
- Empty inputs
- Invalid data
- Missing files
- API failures
- Timezone handling

## 🚀 Running Tests

### Basic Usage

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_gps_extraction.py

# Run specific test class
pytest tests/test_gps_extraction.py::TestGPSExtraction

# Run specific test method
pytest tests/test_gps_extraction.py::TestGPSExtraction::test_gps_coverage_validation
```

### Advanced Usage

```bash
# Run tests matching pattern
pytest -k "test_gps"

# Run tests with coverage report
pytest --cov=scripts --cov-report=html

# Run tests in parallel (faster)
pytest -n auto

# Run only failed tests from last run
pytest --lf

# Run tests with detailed output
pytest -vv --tb=long
```

### Test Markers

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"

# Skip network-dependent tests (offline mode)
pytest -m "not network"

# Run only edge case tests
pytest -m edge_case
```

## 📊 Test Coverage

Generate coverage report:

```bash
# Terminal report
pytest --cov=scripts --cov-report=term

# HTML report (opens in browser)
pytest --cov=scripts --cov-report=html
open htmlcov/index.html

# XML report (for CI/CD)
pytest --cov=scripts --cov-report=xml
```

## 🔧 Test Fixtures

### Shared Fixtures (conftest.py)

- `temp_dir`: Temporary directory for test files
- `gpx_dir`: GPX output directory
- `sample_gps_data`: Realistic GPS test data
- `sample_gps_no_coords`: Photos without GPS
- `sample_gps_single_day`: Single-day trip data
- `sample_gps_multi_city_per_day`: Multiple cities per day
- `sample_gps_with_gaps`: Trip with missing dates
- `mock_exiftool_output`: Mock exiftool JSON output

### Usage Example

```python
def test_example(sample_gps_data, temp_dir):
    """Test using fixtures."""
    # sample_gps_data is pre-loaded
    assert len(sample_gps_data) > 0
    
    # temp_dir is a clean temporary directory
    output_file = temp_dir / "output.gpx"
    output_file.write_text("test")
```

## 🛠️ Test Helpers

### TestDataGenerator

Generate realistic test data:

```python
from tests.test_helpers import TestDataGenerator

gen = TestDataGenerator()

# Generate simple GPS data
data = gen.create_gps_photo_data(
    num_photos=10,
    start_date=datetime(2025, 8, 15)
)

# Generate multi-day trip
trip = gen.create_multi_day_trip(
    days=5,
    photos_per_day=10,
    start_date=datetime(2025, 8, 15),
    cities=[(62.0, -6.77), (55.67, 12.56)]
)

# Generate trip with gaps
gapped = gen.create_trip_with_gaps(
    total_days=7,
    photo_days=[1, 3, 5, 7],
    start_date=datetime(2025, 8, 15)
)
```

### MockGeocoder

Mock geocoding without API calls:

```python
from tests.test_helpers import MockGeocoder

geocoder = MockGeocoder()
result = geocoder.reverse((62.01, -6.77))
print(result['city'])  # "Tórshavn"
```

### OutputValidator

Validate generated files:

```python
from tests.test_helpers import OutputValidator
from pathlib import Path

validator = OutputValidator()
valid, errors = validator.validate_summary_json(
    Path("gpx/trip-summary.json")
)

if not valid:
    print(f"Errors: {errors}")
```

## 📝 Writing New Tests

### Test Class Structure

Each feature should have its own test class:

```python
class TestFeatureName:
    """Test feature description."""
    
    def test_basic_case(self):
        """
        Test basic functionality.
        
        Scenario:
            - Describe the test scenario
            
        Expected:
            - Describe expected outcome
        """
        # Arrange
        input_data = ...
        
        # Act
        result = function_to_test(input_data)
        
        # Assert
        assert result == expected_value
    
    @pytest.mark.parametrize("input,expected", [
        (1, 2),
        (2, 4),
        (3, 6),
    ])
    def test_multiple_cases(self, input, expected):
        """
        Test multiple cases with parameterization.
        
        Args:
            input: Test input
            expected: Expected output
        """
        result = function_to_test(input)
        assert result == expected
    
    def test_edge_case_empty_input(self):
        """
        Test edge case: empty input.
        
        Edge Case:
            - Input is empty/None
            - Should handle gracefully
        """
        result = function_to_test([])
        assert result is not None
```

### Test Documentation

Each test should have a clear docstring:

```python
def test_function_name(self):
    """
    Brief description of what is being tested.
    
    Scenario:
        - Detailed description of test scenario
        - Initial conditions
        - Actions taken
        
    Expected:
        - Expected behavior
        - Expected outputs
        
    Edge Cases:
        - Special conditions tested
        - Boundary values
        
    Examples:
        >>> result = function(input)
        >>> assert result == expected
    """
```

## 🐛 Debugging Tests

### Run with debugger

```bash
# Drop into debugger on failure
pytest --pdb

# Drop into debugger at start of each test
pytest --trace
```

### Print debugging

```bash
# Show print statements
pytest -s

# Show print + verbose
pytest -sv
```

### Detailed failure info

```bash
# Long traceback format
pytest --tb=long

# Show local variables in traceback
pytest -l
```

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements-dev.txt
    
    - name: Run tests
      run: |
        pytest --cov=scripts --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

## 📚 Best Practices

### ✅ Do

- Write clear, descriptive test names
- Document test scenarios in docstrings
- Use fixtures for reusable test data
- Use parametrize for multiple similar cases
- Test edge cases and error conditions
- Keep tests independent and isolated
- Use appropriate markers for categorization

### ❌ Don't

- Write tests that depend on other tests
- Use hardcoded paths or dates
- Commit test output files
- Test implementation details (test behavior)
- Write overly complex tests
- Skip writing tests for edge cases
- Leave broken tests in the codebase

## 🎓 Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Python Testing Best Practices](https://docs.python-guide.org/writing/tests/)
- [Google Testing Blog](https://testing.googleblog.com/)

## 📊 Current Coverage

Run `pytest --cov=scripts` to see current test coverage.

Target: >80% code coverage for all core functions.

---

**Note**: Tests are designed to be fast and reliable. Network-dependent tests use mocks by default. Use `-m network` to run real API tests.

