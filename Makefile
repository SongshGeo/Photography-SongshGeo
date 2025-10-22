# Photography Site Makefile
# Quick commands for common tasks

.PHONY: help install install-dev extract-gps server clean test test-cov test-fast

# Default target
help:
	@echo "📸 Photography Site - Available Commands:"
	@echo ""
	@echo "  make install      - Install production dependencies (exiftool, gpxpy, geopy)"
	@echo "  make install-dev  - Install development dependencies (pytest, etc.)"
	@echo "  make extract-gps  - Extract GPS from Mac Photos and generate GPX"
	@echo "  make server       - Start Hugo development server"
	@echo "  make test         - Run all tests with coverage"
	@echo "  make test-fast    - Run tests without coverage (faster)"
	@echo "  make test-cov     - Run tests and open coverage report"
	@echo "  make clean        - Clean generated GPS files"
	@echo ""
	@echo "See README.md for detailed workflow instructions"

# Install production dependencies
install:
	@echo "📦 Installing production dependencies..."
	@command -v exiftool >/dev/null 2>&1 || (echo "Installing exiftool..." && brew install exiftool)
	@command -v python3 >/dev/null 2>&1 || (echo "❌ Python 3 not found" && exit 1)
	@python3 -c "import gpxpy" 2>/dev/null || (echo "Installing gpxpy..." && pip3 install --user --break-system-packages gpxpy)
	@python3 -c "import geopy" 2>/dev/null || (echo "Installing geopy..." && pip3 install --user --break-system-packages geopy)
	@echo "✅ Production dependencies installed!"

# Install development dependencies
install-dev: install
	@echo "📦 Installing development dependencies..."
	@pip3 install --user --break-system-packages -r requirements-dev.txt
	@echo "✅ Development dependencies installed!"

# Extract GPS from Mac Photos
extract-gps:
	@echo "📸 Extracting GPS from Mac Photos..."
	@./scripts/extract-mac-photos-gps.sh
	@echo ""
	@echo "🔄 Converting to GPX..."
	@python3 scripts/json2gpx.py mac-photos-gps.json mac-photos-track.gpx
	@echo ""
	@echo "📅 Splitting by year..."
	@python3 scripts/split-gpx-by-year.py mac-photos-track.gpx
	@echo ""
	@echo "✅ Done! GPX files ready for Lightroom."
	@echo "Next: Load GPX in Lightroom using Jeffrey's Geotag Support plugin"

# Start Hugo development server
server:
	@echo "🚀 Starting Hugo server..."
	@hugo server --buildDrafts

# Run tests
test:
	@echo "🧪 Running tests with coverage..."
	@python3 -m pytest --cov=scripts --cov-report=term --cov-report=html
	@echo ""
	@echo "✅ Tests complete! Coverage report: htmlcov/index.html"

# Run tests without coverage (faster)
test-fast:
	@echo "🧪 Running tests (fast mode)..."
	@python3 -m pytest -v
	@echo "✅ Tests complete!"

# Run tests and open coverage report
test-cov: test
	@echo "📊 Opening coverage report..."
	@open htmlcov/index.html || xdg-open htmlcov/index.html

# Clean generated files
clean:
	@echo "🧹 Cleaning generated files..."
	@rm -f mac-photos-gps.json
	@rm -f mac-photos-track*.gpx
	@rm -rf gpx/*.json gpx/*.gpx
	@rm -rf htmlcov/
	@rm -rf .pytest_cache/
	@rm -rf .coverage
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Clean complete!"

