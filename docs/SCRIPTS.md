# Photography Workflow Scripts

Essential scripts for GPS extraction and geotagging workflow.

## Quick Start

### Smart GPS Extraction (Recommended) ⭐

Interactive script with validation and gap detection:

```bash
# Basic usage
python3 scripts/smart-gps-extract.py ~/Downloads/Denmark denmark-2025

# With manual city specification
python3 scripts/smart-gps-extract.py ~/Downloads/Denmark denmark-2025 --d1 Copenhagen --d3 Aarhus
```

**Features**:
- ✅ Interactive validation at each step
- ✅ Automatic reverse geocoding (city detection)
- ✅ Gap detection and manual override support
- ✅ Detailed daily location summary
- ✅ Robust error handling

**Output**:
- `gpx/denmark-2025.gpx` - GPX track file
- `gpx/denmark-2025-summary.json` - Trip summary with cities
- `gpx/denmark-2025-gps.json` - Raw GPS data

---

## Core Scripts

### `smart-gps-extract.py` ⭐ Main Interactive Script

Intelligent GPS extraction with validation.

**Usage**:
```bash
python3 scripts/smart-gps-extract.py <photo_folder> [output_name] [--d1 City1] [--d2 City2]
```

**Interactive Steps**:
1. Scan photos and count GPS coverage
2. Analyze date range and photo distribution
3. Query city names via OpenStreetMap API
4. Validate all days have location data
5. Generate GPX track

**Advanced Examples**:

```bash
# Specify expected date range (validates coverage)
python3 scripts/smart-gps-extract.py ~/Downloads/Denmark denmark-2025 \
  -s 2025-08-12 -e 2025-08-23

# Manual city override for specific days
python3 scripts/smart-gps-extract.py ~/Downloads/Trip trip-2025 \
  --d1 "Copenhagen" --d5 "Aarhus"

# Combined: expected range + manual cities for missing dates
python3 scripts/smart-gps-extract.py ~/Downloads/Trip trip-2025 \
  -s 2025-07-01 -e 2025-07-10 \
  --d1 "Berlin" --d8 "Paris"
```

**Parameters**:
- `-s, --expected-start`: Expected trip start date (YYYY-MM-DD)
- `-e, --expected-end`: Expected trip end date (YYYY-MM-DD)  
- `--d1, --d2, ...`: Manually specify city for each day (d1=day 1, d2=day 2, etc.)

---

### `extract-gps-from-folder.sh`
Simple one-command GPS extraction (no validation).

**Usage**:
```bash
./scripts/extract-gps-from-folder.sh <photo_folder> [output_name]
```

**Output**:
- `gpx/[name]-gps.json` - GPS data
- `gpx/[name].gpx` - GPX track file

---

### `extract-mac-photos-gps.sh`
Alternative: Directly extracts from Mac Photos Library.

**Usage**:
```bash
./scripts/extract-mac-photos-gps.sh
```

**Requirements**: Terminal needs "Full Disk Access" permission.

**Output**: `mac-photos-gps.json`

---

### `json2gpx.py`
Converts GPS JSON to GPX format (used internally by extract-gps-from-folder.sh).

**Usage**:
```bash
python3 scripts/json2gpx.py input.json output.gpx
```

---

### `write-location-metadata.py`
Optional: Batch reverse geocoding to add city/country names to photo files.

**Usage**:
```bash
# Preview mode
python3 scripts/write-location-metadata.py /path/to/photos --dry-run

# Execute
python3 scripts/write-location-metadata.py /path/to/photos
```

**Note**: Usually Lightroom's reverse geocoding is sufficient; use this only for batch processing outside Lightroom.

---

## Typical Workflow

```bash
# 1. Extract GPS from exported phone photos
./scripts/extract-gps-from-folder.sh ~/Downloads/Trip-Photos trip-2025

# 2. Load gpx/trip-2025.gpx in Lightroom
# File > Plug-in Extras > Geoencoding Support > Load Track Log

# 3. Use Lightroom's reverse geocoding
# Right-click > Plug-in Extras > Geoencoding Support > Lookup Address

# 4. Publish via Collection Publisher
# Right-click collection > Publish
```

---

## Dependencies

```bash
# Install exiftool
brew install exiftool

# Install Python packages
pip3 install --user --break-system-packages gpxpy geopy
```

---

## Troubleshooting

**No GPS found in photos?**
- Ensure photos are from phone with GPS enabled
- Check file formats (JPG, HEIC supported)

**Permission denied on Mac Photos Library?**
- Grant terminal "Full Disk Access" in System Settings
- Or use `extract-gps-from-folder.sh` with exported photos instead

**GPX not matching in Lightroom?**
- Check camera/phone time synchronization
- Adjust camera time in Lightroom if needed
