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

## 📷 Adding Photos

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
