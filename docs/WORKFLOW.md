# Professional Photography Workflow

Complete pipeline from camera to website with GPS geotagging.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Workflow Overview](#workflow-overview)
- [Step-by-Step Guide](#step-by-step-guide)
- [Advanced Features](#advanced-features)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software

1. **Lightroom Classic** with plugins:
   - [Jeffrey's Geotag Support Plugin](http://regex.info/blog/lightroom-goodies/gps)
   - [JF Collection Publisher](https://regex.info/blog/lightroom-goodies/collection-publisher)

2. **Command-line tools**:
   ```bash
   brew install exiftool
   pip3 install --user --break-system-packages geopy gpxpy
   ```

3. **Hugo Extended** (v0.148.2+):
   ```bash
   brew install hugo
   ```

## Workflow Overview

```
📷 Camera Photos → 🎨 Lightroom → 🗺️ GPS Track → 📍 Geotagging → 📂 Export → 🚀 Deploy
     (No GPS)      (Processing)   (Phone GPS)   (Matching)    (Website)   (Vercel)
```

### Time Investment

- **Initial setup**: ~30 minutes (one-time)
- **Per trip processing**: ~15 minutes for 100 photos
- **Ongoing publishing**: ~5 minutes per collection

## Step-by-Step Guide

### Step 1: Photo Preprocessing in Lightroom

#### 1.1 Import and Organize

```
Import → Smart Collection → Flag Picks → Rate 4+ Stars
```

**Actions:**
- Import all camera photos from trip
- Create smart collection by date range
- Press `P` to flag best photos
- Rate 4+ stars for publication

#### 1.2 Create Copyright Preset

Navigate to: `Metadata > Edit Metadata Presets`

**Settings:**
```yaml
Copyright: © 2025 SongshGeo
Creator: SongshGeo
Creator URL: https://songshgeo.github.io/Photography-SongshGeo/
Keywords: photography, travel, [country], [city]
```

**Apply to all selected photos.**

### Step 2: GPS Track Generation

#### 2.1 Export Phone Photos

From **Photos.app**:
1. Select photos from same date range
2. `File > Export > Export Unmodified Originals`
3. ✅ **Check**: "Include location information"
4. Save to folder (e.g., `~/Downloads/Denmark`)

#### 2.2 Generate GPX Track

**Basic usage:**
```bash
python3 scripts/smart-gps-extract.py ~/Downloads/Denmark denmark-2025
```

**With date range validation:**
```bash
python3 scripts/smart-gps-extract.py ~/Downloads/Denmark denmark-2025 \
  -s 2025-08-12 -e 2025-08-23
```

**With manual city overrides:**
```bash
python3 scripts/smart-gps-extract.py ~/Downloads/Denmark denmark-2025 \
  --d1 "Aarhus" --d2 "Odense" --d5 "Copenhagen"
```

**Interactive output:**
```
📸 Smart GPS Extraction
━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 检查 GPS 覆盖率: 17/124 photos (14%)
✅ 分析行程日期: 2025-08-12 to 2025-08-23 (12 days)
✅ 查询城市信息:
   Day 1 (2025-08-12): Tórshavn
   Day 2 (2025-08-13): Tórshavn, Vágar
   ...
✅ 验证完整性: All days covered
✅ 生成 GPX: gpx/denmark-2025.gpx
```

### Step 3: Geotagging in Lightroom

#### 3.1 Load GPS Track

1. `File > Plug-in Extras > Geoencoding Support > Load Track Log`
2. Select: `gpx/denmark-2025.gpx`
3. Plugin automatically matches GPS to photos by timestamp
4. Review map view to verify accuracy

#### 3.2 Reverse Geocoding

1. `File > Plug-in Extras > Geoencoding Support > Reverse Geocode`
2. Select photos with GPS
3. Plugin queries city/country/state names
4. Metadata fields auto-populate

**Result:** All photos now have GPS coordinates + location names

### Step 4: Smart Collection Publishing

#### 4.1 Set Up Collection Publisher

**First-time setup:**

1. **Create Publish Service**:
   - `Library > Publish Services > Set Up...`
   - Choose: "Hard Drive"
   - Destination: `[ProjectRoot]/content/trips/`

2. **Configure Export Settings**:
   ```
   Image Format: JPEG
   Quality: 85
   Color Space: sRGB
   Image Sizing: Long Edge 2560px
   Sharpening: Screen, Amount: Standard
   ```

3. **File Naming Template**:
   ```
   {date (yyyy)}{date (mm)}{date (dd)}-{sequence (0001)}
   Example: 20250812-0001.jpg
   ```

#### 4.2 Create Smart Collections

**Collection structure:**
```
Published Folder: Trips
├── Denmark/Faroe Islands 2025
│   └── Filter: Country = Faroe Islands, Flag = Pick
├── Japan/Tokyo 2025
│   └── Filter: Country = Japan AND City = Tokyo, Flag = Pick
└── ...
```

**Smart Collection Settings:**
```
Name: [Country] - [City] - [Year]
Match: All of the following rules
  - Flag is Picked
  - Rating ≥ 4 stars
  - Country contains [Country]
  - City contains [City]
  - Capture Date is in the range [start] to [end]
```

#### 4.3 Publish Photos

1. Right-click collection → `Publish`
2. Photos export to `content/trips/[Country]/`
3. File naming follows template
4. Metadata embedded in JPEG

### Step 5: Website Generation

#### 5.1 Create Trip Index

**Create file:** `content/trips/Denmark/index.md`

```yaml
---
title: "Faroe Islands & Denmark 2025"
date: 2025-08-12
location:
  country: Denmark & Faroe Islands
  city: Tórshavn, Copenhagen, Aarhus
coords:
  lat: 62.0104
  lon: -6.7719
cover: 20250812-0001.jpg
tags:
  - landscape
  - travel
  - europe
  - denmark
  - faroe-islands
  - coastline
categories:
  - trips
  - nature
---

A summer journey through the dramatic landscapes of the Faroe Islands and the vibrant cities of Denmark.
```

#### 5.2 Test Locally

```bash
hugo server --buildDrafts
```

Open: http://localhost:1313

**Verify:**
- ✅ Photos appear in gallery
- ✅ Lightbox works
- ✅ Metadata displays correctly
- ✅ Map shows GPS locations

#### 5.3 Deploy to Production

```bash
# Commit changes
git add content/trips/Denmark/
git add gpx/denmark-2025.gpx
git commit -m "Add Denmark & Faroe Islands 2025 trip (15 photos)"

# Push to GitHub
git push origin main
```

**Vercel** automatically deploys on push (~2 minutes).

## Advanced Features

### Batch Processing

Process multiple trips:

```bash
# Generate GPX for each trip
python3 scripts/smart-gps-extract.py ~/Photos/Japan japan-2025
python3 scripts/smart-gps-extract.py ~/Photos/Iceland iceland-2025

# Load all tracks in Lightroom
# Use date ranges to apply correct track to each trip
```

### Custom Metadata

Add trip-specific metadata:

```yaml
# content/trips/Japan/index.md
---
title: "Tokyo Street Photography 2025"
trip_duration: "7 days"
camera: "Olympus OM-1"
lens: "M.Zuiko 12-40mm f/2.8"
highlights:
  - Shibuya Crossing
  - Senso-ji Temple
  - Tokyo Skytree
---
```

### SEO Optimization

Hugo automatically generates:
- ✅ Sitemap: `/sitemap.xml`
- ✅ RSS feed: `/index.xml`
- ✅ Open Graph tags
- ✅ Schema.org markup

## Troubleshooting

### GPS Track Not Matching

**Problem:** Photos don't get GPS coordinates after loading track.

**Solutions:**
1. Check timezone: GPS track and photos must match
2. Verify date range: Track must cover photo dates
3. Use `--expected-start` and `--expected-end` for validation
4. Manually specify missing dates with `--d1`, `--d2`, etc.

### Lightroom Map Module Grayed Out

**Problem:** Map module unavailable (China region account).

**Solution:** Use Jeffrey's plugins instead:
- GPS coordinates: Jeffrey's Geotag Support
- Reverse geocoding: Use plugin's built-in lookup

### Export File Naming Issues

**Problem:** Files not named correctly.

**Check:**
1. File Naming template in Lightroom Export/Publish settings
2. Use: `{date (yyyy)}{date (mm)}{date (dd)}-{sequence (0001)}`
3. Avoid spaces and special characters

### Vercel Deployment Failed

**Problem:** Push to GitHub but site doesn't update.

**Steps:**
1. Check Vercel dashboard for build logs
2. Verify `hugo.toml` configuration
3. Ensure Hugo version matches (`0.148.2`)
4. Check build command in `vercel.json`

## Next Steps

- 📚 Read [Scripts Guide](SCRIPTS.md) for GPS extraction details
- 🧪 Check [Testing Guide](TESTING.md) for test suite
- ⚙️ See [Setup Guide](SETUP.md) for advanced configuration

---

**Questions?** Open an issue on [GitHub](https://github.com/SongshGeo/Photography-SongshGeo/issues).

