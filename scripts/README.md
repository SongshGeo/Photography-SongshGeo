# Scripts

Essential scripts for the photography workflow.

## Core Scripts

### `extract-mac-photos-gps.sh`
Extracts GPS coordinates from Mac Photos Library.

```bash
./scripts/extract-mac-photos-gps.sh
```

Output: `mac-photos-gps.json`

### `json2gpx.py`
Converts GPS JSON data to GPX format for Lightroom.

```bash
python3 scripts/json2gpx.py input.json output.gpx
```

### `write-location-metadata.py`
Reverse geocodes GPS coordinates to city/country names.

```bash
python3 scripts/write-location-metadata.py /path/to/photos [--dry-run]
```

## Workflow

1. Extract GPS: `./scripts/extract-mac-photos-gps.sh`
2. Convert to GPX: `python3 scripts/json2gpx.py mac-photos-gps.json phone-track.gpx`
3. Load GPX in Lightroom for geotagging
4. Use Lightroom's reverse geocoding for location names
