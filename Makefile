# Photography Site Makefile
# Quick commands for common tasks

.PHONY: help install extract-gps server clean

# Default target
help:
	@echo "📸 Photography Site - Available Commands:"
	@echo ""
	@echo "  make install      - Install dependencies (exiftool, gpxpy)"
	@echo "  make extract-gps  - Extract GPS from Mac Photos and generate GPX"
	@echo "  make server       - Start Hugo development server"
	@echo "  make clean        - Clean generated GPS files"
	@echo ""
	@echo "See SETUP.md for detailed workflow instructions"

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	@command -v exiftool >/dev/null 2>&1 || (echo "Installing exiftool..." && brew install exiftool)
	@command -v python3 >/dev/null 2>&1 || (echo "❌ Python 3 not found" && exit 1)
	@python3 -c "import gpxpy" 2>/dev/null || (echo "Installing gpxpy..." && pip3 install --user --break-system-packages gpxpy)
	@echo "✅ All dependencies installed!"

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

# Clean generated files
clean:
	@echo "🧹 Cleaning generated GPS files..."
	@rm -f mac-photos-gps.json
	@rm -f mac-photos-track*.gpx
	@echo "✅ Clean complete!"

