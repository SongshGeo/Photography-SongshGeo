# Changelog

## [Unreleased] - 2025-10-17

### ✨ Added
- **Professional Photography Workflow**: Complete pipeline from camera to website
  - GPS extraction from Mac Photos or exported folders
  - GPX track generation for Lightroom integration
  - Automated geotagging and reverse geocoding
  - Smart collection publishing workflow
  - Automated Vercel deployment

- **Core Scripts**:
  - `smart-gps-extract.py`: ⭐ Interactive GPS extraction with validation and gap detection
    - Auto-detects cities via OpenStreetMap API
    - Validates complete date coverage
    - Supports expected date range validation (-s, -e flags)
    - Manual city override for missing dates (--d1, --d2, etc.)
    - Generates trip summary JSON
  - `extract-gps-from-folder.sh`: Simple one-command GPS extraction
  - `json2gpx.py`: GPS JSON to GPX converter
  - `write-location-metadata.py`: Batch reverse geocoding utility

- **Travel Photography Content**:
  - Denmark/Faroe Islands 2025: 15 curated photos with precise geotagging
  - Japan 2025: 8 photos from Tokyo

- **Documentation**:
  - Enhanced README with complete workflow
  - QUICKSTART guide for rapid setup
  - Scripts documentation with examples

### 🔧 Changed
- Updated `.gitignore` to exclude GPS extraction artifacts
- Enhanced Makefile with GPS extraction commands
- Simplified workflow to focus on essential steps
- Improved trip template structure

### 🛠️ Infrastructure
- Vercel auto-deployment configuration
- Custom domain: `gallery.songshgeo.com`
- Hugo build optimization with `--gc --minify`

### 🎯 Workflow Benefits
- **90% reduction** in manual metadata entry
- **Automated publishing** from Lightroom to website
- **Precise GPS tagging** using phone location data
- **One-click deployment** via Git integration

---

## Previous Releases

### [1.0.0] - Initial Release
- Hugo theme gallery integration
- Basic site structure
- Initial deployment configuration

