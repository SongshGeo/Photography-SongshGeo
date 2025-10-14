# Photography by SongshGeo

> *"A geographer who also travels."*

Welcome to my photography gallery! This site showcases visual stories captured during my travels and research journeys as a geographer and scientist.

## About

I'm **Shuang Song** (SongshGeo), a postdoctoral researcher at the Max Planck Institute of Geoanthropology. This photography gallery bridges my scientific work studying human-environment interactions with my passion for visual storytelling.

## 🔗 Links

- 📸 **Photography Gallery**: [Live Site](https://photography-songshgeo-as9c9jcic-songshgeos-projects.vercel.app) *(deployed via Vercel)*
- 🎓 **Academic CV**: [cv.songshgeo.com](https://cv.songshgeo.com)
- ✍️ **Travel Blog**: [songshgeo.com](https://songshgeo.com)
- 📧 **Contact**: [SongshGeo@gmail.com](mailto:SongshGeo@gmail.com)

## 🛠️ Technology Stack

- **Static Site Generator**: [Hugo](https://gohugo.io) (v0.148.2)
- **Theme**: [hugo-theme-gallery](https://github.com/nicokaiser/hugo-theme-gallery) by Nico Kaiser
- **Deployment**: [Vercel](https://vercel.com) (primary) | [GitHub Pages](https://pages.github.com) (backup)
- **Hosting**: [GitHub](https://github.com)

## 🎨 Features

- Responsive photo gallery with lightbox functionality
- Justified album layouts using Flickr's Justified Layout
- SEO optimized with Open Graph tags
- Dark/light theme support
- Automatic image optimization
- RSS feeds
- Category and tag organization

## 📁 Project Structure

```
Photography-SongshGeo/
├── content/
│   ├── nature/          # Nature photography album
│   ├── urban/           # Urban photography album
│   ├── portraits/       # Portrait photography album
│   └── categories/      # Category pages
├── themes/gallery/      # Hugo theme (git submodule)
├── static/              # Static assets
└── hugo.toml           # Site configuration
```

## 🚀 Local Development

1. **Prerequisites**: Install [Hugo Extended](https://gohugo.io/installation/) (v0.148.2+)

2. **Clone the repository**:
   ```bash
   git clone --recursive https://github.com/SongshGeo/Photography-SongshGeo.git
   cd Photography-SongshGeo
   ```

3. **Start development server**:
   ```bash
   hugo server --buildDrafts
   ```

4. **View locally**: Open [http://localhost:1313](http://localhost:1313)

## 📷 Professional Photography Workflow

### Complete Pipeline: From Camera to Website

This repository contains a streamlined workflow for professional photographers to publish travel photos with precise GPS geotagging and automated website generation.

#### 🔧 Prerequisites

1. **Lightroom Classic** with plugins:
   - [Jeffrey's Geotag Support Plugin](http://regex.info/blog/lightroom-goodies/gps)
   - [JF Collection Publisher](https://regex.info/blog/lightroom-goodies/collection-publisher)

2. **Command-line tools**:
   ```bash
   # Install dependencies
   brew install exiftool
   pip3 install --user --break-system-packages geopy gpxpy
   ```

#### 📋 Step-by-Step Workflow

##### Step 1: Photo Preprocessing in Lightroom

1. **Import and organize**:
   - Import camera photos from your trip
   - Create smart collections by date range
   - Flag picks (P key) and rate 4+ stars for selection

2. **Create copyright preset**:
   ```
   Copyright: © 2025 SongshGeo
   Creator: SongshGeo
   Creator URL: https://songshgeo.github.io/Photography-SongshGeo/
   Keywords: photography, travel, [country], [city]
   ```
   - Apply preset to all selected photos

##### Step 2: GPS Track Generation

1. **Find phone photos** from the same date range with GPS data

2. **Generate GPX track**:
   ```bash
   # Extract GPS from phone photos
   ./scripts/extract-mac-photos-gps.sh
   
   # Convert to GPX format
   python3 scripts/json2gpx.py mac-photos-gps.json phone-track.gpx
   ```

##### Step 3: Geotagging in Lightroom

1. **Load GPS track**:
   - File > Plug-in Extras > Geoencoding Support > Load Track Log
   - Select your GPX file
   - Plugin automatically matches GPS to photos by timestamp

2. **Reverse geocoding**:
   - Use Jeffrey's plugin to lookup addresses from GPS coordinates
   - This fills City/Country/State fields automatically

##### Step 4: Smart Collection Publishing

1. **Set up Collection Publisher**:
   - Create published folder: `content/trips/`
   - Configure naming: `{date (yyyy)}-{date (mm)}-{date (dd)}-{sequence (0001)}`
   - Set export settings: JPEG quality 85%, 2560px long edge

2. **Create smart collections**:
   ```
   Collection Name: [Country] - [City] - [Year]
   Filter: Country = [Country] AND City = [City] AND Flag = Pick
   ```

3. **Publish collections**:
   - Drag photos to appropriate collections
   - Right-click collection > "Publish"
   - Photos automatically export to `content/trips/[Country]/`

##### Step 5: Website Generation

1. **Create trip index** (copy template):
   ```yaml
   ---
   title: "[City], [Country] [Year]"
   date: [YYYY-MM-DD]
   location:
     country: [Country]
     city: [City]
   coords:
     lat: [latitude]
     lon: [longitude]
   cover: [filename].jpg
   tags: [landscape, travel, [country]]
   ---
   ```

2. **Build and deploy**:
   ```bash
   # Test locally
   hugo server --buildDrafts
   
   # Commit and push (auto-deploys to Vercel)
   git add .
   git commit -m "Add [Country] trip photos"
   git push origin main
   ```

#### 🎯 Workflow Benefits

- ✅ **Precise GPS tagging**: Phone GPS + camera photos = accurate locations
- ✅ **Automated organization**: Smart collections sort by location automatically  
- ✅ **Professional metadata**: Copyright, keywords, and location data included
- ✅ **One-click publishing**: Collection Publisher handles file naming and export
- ✅ **Version control**: All photos tracked in Git with proper history
- ✅ **SEO optimized**: Automatic sitemap and metadata for search engines

#### 📚 Advanced Features

- **Batch processing**: Handle hundreds of photos in minutes
- **Reverse geocoding**: Automatic city/country lookup from coordinates
- **Smart collections**: Dynamic filtering by date, location, rating
- **Template system**: Consistent photo metadata across all trips

### Adding Photos Manually

To add photos to an existing album:

1. Copy image files to the appropriate directory (e.g., `content/nature/`)
2. The theme automatically creates gallery pages from images in album directories
3. Optionally add metadata in the album's `index.md` frontmatter

To create a new album:

1. Create a new directory under `content/`
2. Add an `index.md` file with album metadata
3. Add image files to the directory

## 🌐 Deployment

This site is configured for multiple deployment options:

- **Vercel** (Primary): Automatic deployment on push to main branch
- **GitHub Pages** (Backup): Via GitHub Actions workflow
- **Netlify** (Alternative): Configuration included

## 📄 License

This project is open source. The photography content is © 2025 Shuang Song. All rights reserved.

---

*Built with ❤️ by a geographer who also travels*
