#!/usr/bin/env python3
"""
Convert exiftool JSON output to GPX track file.

Usage:
    python3 json2gpx.py input.json output.gpx
"""

import json
import sys
from datetime import datetime

try:
    import gpxpy
    import gpxpy.gpx
except ImportError:
    print("❌ 未安装 gpxpy")
    print("请运行: pip3 install --user gpxpy")
    sys.exit(1)


def json_to_gpx(input_json: str, output_gpx: str):
    """Convert exiftool JSON to GPX track."""
    
    print(f"📖 读取 {input_json}...")
    with open(input_json, 'r') as f:
        data = json.load(f)
    
    # Create GPX object
    gpx = gpxpy.gpx.GPX()
    gpx.creator = "Mac Photos GPS Extractor"
    
    track = gpxpy.gpx.GPXTrack()
    track.name = "Mac Photos Track"
    gpx.tracks.append(track)
    
    segment = gpxpy.gpx.GPXTrackSegment()
    track.segments.append(segment)
    
    # Filter valid points with GPS
    valid_points = [
        p for p in data 
        if all(k in p for k in ['GPSLatitude', 'GPSLongitude', 'DateTimeOriginal'])
    ]
    
    if not valid_points:
        print("❌ 未找到包含 GPS 和时间的照片")
        sys.exit(1)
    
    # Sort by time
    valid_points.sort(key=lambda x: x['DateTimeOriginal'])
    
    print(f"✨ 找到 {len(valid_points)} 个有效轨迹点")
    
    # Add track points
    skipped = 0
    for item in valid_points:
        try:
            # Parse datetime (EXIF format: "2025:07:24 14:23:45")
            time_str = item['DateTimeOriginal']
            time = datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S')
            
            lat = float(item['GPSLatitude'])
            lon = float(item['GPSLongitude'])
            alt = float(item.get('GPSAltitude', 0)) if 'GPSAltitude' in item else None
            
            segment.points.append(gpxpy.gpx.GPXTrackPoint(
                lat, lon, elevation=alt, time=time
            ))
            
        except Exception as e:
            skipped += 1
            if skipped <= 3:  # Only print first few errors
                filename = item.get('FileName', 'unknown')
                print(f"⚠️  跳过 {filename}: {e}")
    
    # Write GPX
    print(f"💾 写入 {output_gpx}...")
    with open(output_gpx, 'w') as f:
        f.write(gpx.to_xml())
    
    print(f"✅ 成功生成 GPX 轨迹！")
    print(f"   轨迹点数: {len(segment.points)}")
    if skipped > 0:
        print(f"   跳过: {skipped} 个")
    print(f"\n📍 时间范围:")
    if segment.points:
        print(f"   开始: {segment.points[0].time}")
        print(f"   结束: {segment.points[-1].time}")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 json2gpx.py input.json output.gpx")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    json_to_gpx(input_file, output_file)

