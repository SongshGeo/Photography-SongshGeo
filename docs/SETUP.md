# Setup Guide

Detailed installation and configuration instructions.

## 📦 Prerequisites

### System Requirements

- **macOS** 12.0+ (for Photos.app integration)
- **Python** 3.9+
- **Node.js** 16+ (optional, for theme development)
- **Hugo Extended** 0.148.2+

### Required Software

1. **Hugo Extended**
   ```bash
   brew install hugo
   ```

2. **ExifTool**
   ```bash
   brew install exiftool
   ```

3. **Python packages**
   ```bash
   pip3 install --user --break-system-packages geopy gpxpy
   ```

### Lightroom Plugins

Download and install:

1. **[Jeffrey's Geotag Support Plugin](http://regex.info/blog/lightroom-goodies/gps)**
   - GPS track loading
   - Reverse geocoding
   - Map integration

2. **[JF Collection Publisher](https://regex.info/blog/lightroom-goodies/collection-publisher)**
   - Automated publishing
   - Smart collections
   - File naming templates

## 🚀 Installation

### 1. Clone Repository

```bash
git clone --recursive https://github.com/SongshGeo/Photography-SongshGeo.git
cd Photography-SongshGeo
```

**Note:** `--recursive` is important to include the Hugo theme submodule.

### 2. Install Dependencies

```bash
# Install production dependencies
make install

# Install development dependencies (for testing)
make install-dev
```

### 3. Verify Installation

```bash
# Check Hugo
hugo version

# Check Python packages
python3 -c "import gpxpy, geopy; print('OK')"

# Check ExifTool
exiftool -ver

# Run tests
make test
```

## ⚙️ Configuration

### Hugo Configuration

Edit `hugo.toml`:

```toml
baseURL = 'https://your-site.com/'
languageCode = 'en-us'
title = 'Your Photography Site'

[params]
  author = "Your Name"
  description = "Your photography description"
  
  [params.social]
    email = "your@email.com"
    github = "yourusername"
```

### Vercel Deployment

1. **Connect GitHub repository to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Configure project

2. **Build settings** (auto-detected from `vercel.json`):
   ```json
   {
     "build": {
       "command": "hugo --gc --minify"
     }
   }
   ```

3. **Environment variables** (if needed):
   - None required for basic setup

### GitHub Actions (Optional)

Tests run automatically. Configure in `.github/workflows/tests.yml`.

## 🔧 Lightroom Configuration

### Install Plugins

1. Download plugin ZIP files
2. Extract to folder
3. In Lightroom: `File > Plug-in Manager > Add`
4. Select plugin folder

### Configure Geotag Support

1. Open plugin settings
2. Configure timezone offset
3. Set default geocoding provider (OpenStreetMap)

### Configure Collection Publisher

1. Create publish service: `Library > Publish Services`
2. Choose "Hard Drive"
3. Set destination: `[Project]/content/trips/`
4. Configure export settings (see [Workflow Guide](WORKFLOW.md))

## 📁 Project Structure

```
Photography-SongshGeo/
├── content/              # Website content
│   ├── trips/           # Trip photo galleries
│   ├── nature/          # Nature photography
│   └── urban/           # Urban photography
├── docs/                # Documentation
├── gpx/                 # GPS tracks (git-ignored)
├── scripts/             # GPS extraction scripts
├── tests/               # Test suite
├── themes/gallery/      # Hugo theme (submodule)
├── hugo.toml            # Hugo configuration
├── Makefile             # Build commands
├── pytest.ini           # Test configuration
└── requirements-dev.txt # Development dependencies
```

## 🧪 Development Setup

### Running Tests

```bash
# Install development dependencies
make install-dev

# Run all tests
make test

# Run specific test
pytest tests/test_gps_extraction.py -v
```

### Local Development Server

```bash
# Start Hugo server
hugo server --buildDrafts

# Or use Makefile
make server
```

Open: http://localhost:1313

### Code Quality

```bash
# Format code
black scripts/ tests/

# Sort imports
isort scripts/ tests/

# Lint code
flake8 scripts/ tests/
```

## 🔐 Security & Privacy

### Git Ignore

The `.gitignore` includes:
- `gpx/` - GPS tracks (contains location data)
- Personal photo files
- Build artifacts
- Test coverage reports

### EXIF Data

- GPS coordinates embedded in published photos
- Consider privacy before publishing location data
- Use Lightroom's "Remove Location Data" if needed

## 🆘 Troubleshooting

### Hugo Theme Not Found

**Problem:** Theme files missing after clone.

**Solution:**
```bash
git submodule update --init --recursive
```

### Python Package Installation Fails

**Problem:** `externally-managed-environment` error on macOS.

**Solution:**
```bash
pip3 install --user --break-system-packages <package>
```

### ExifTool Permission Denied

**Problem:** Can't read Photos Library.

**Solution:**
1. System Preferences > Security & Privacy
2. Grant "Full Disk Access" to Terminal

### Vercel Build Failed

**Problem:** Deployment fails on Vercel.

**Check:**
1. Hugo version in `vercel.json`
2. Build command
3. Check Vercel build logs

## 📚 Next Steps

- Read [Workflow Guide](WORKFLOW.md) for complete photography workflow
- Check [Scripts Guide](SCRIPTS.md) for GPS extraction
- See [Testing Guide](TESTING.md) for development

---

**Need help?** Open an issue on [GitHub](https://github.com/SongshGeo/Photography-SongshGeo/issues).

