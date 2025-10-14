---
# Trip information template
# Copy this file to create a new trip: content/trips/<Country>/<City-YYYY>/index.md

title: "City, Country YYYY"
date: 2025-01-01  # Trip start date

# Location metadata
location:
  country: CountryName
  city: CityName

# GPS coordinates for map marker (Google: "city name coordinates")
coords:
  lat: 0.0000
  lon: 0.0000

# Cover image filename (from this directory)
cover: YYYYMMDD-filename.jpg

# Tags for categorization
tags: [street, landscape, portrait, nature, cityscape, architecture]

# Optional: Trip summary
summary: A brief description of this trip.

# Optional: Photo count limit (defaults to all)
# maxphotos: 24
---

# Optional trip description

You can add markdown content here to describe the trip, but it's not required.
The gallery theme will automatically generate a photo gallery from all images in this directory.

## Tips

- Keep 12-24 photos per trip for best loading performance
- Name photos with date prefix for chronological sorting: `YYYYMMDD-*.jpg`
- Use sequence numbers if needed: `01_YYYYMMDD-*.jpg`
- Supported formats: JPG, JPEG, PNG, WebP
- Recommended size: 2560px long edge, JPEG quality 85

