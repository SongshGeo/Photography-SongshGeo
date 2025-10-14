#!/usr/bin/env python3
"""
Reverse geocode GPS and write location metadata directly to photos.

Uses Nominatim (OpenStreetMap) API for free reverse geocoding,
then writes City/Country/State to IPTC metadata using exiftool.

Usage:
    python3 write-location-metadata.py photos_directory [--dry-run]
"""

import sys
import json
import time
import subprocess
from pathlib import Path

try:
    from geopy.geocoders import Nominatim
    from geopy.exc import GeocoderTimedOut, GeocoderServiceError
except ImportError:
    print("❌ 未安装 geopy")
    print("请运行: pip3 install --user --break-system-packages geopy")
    sys.exit(1)


def extract_gps_from_photos(directory):
    """Extract GPS data from photos."""
    
    print(f"📸 扫描照片: {directory}\n")
    
    cmd = [
        'exiftool',
        '-json', '-n', '-r',
        '-ext', 'jpg', '-ext', 'jpeg', '-ext', 'JPG',
        '-FileName', '-Directory', '-SourceFile',
        '-GPSLatitude', '-GPSLongitude',
        directory
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    
    photos_with_gps = [
        p for p in data 
        if 'GPSLatitude' in p and 'GPSLongitude' in p
    ]
    
    print(f"   找到 {len(photos_with_gps)} 张有 GPS 的照片\n")
    
    return photos_with_gps


def reverse_geocode(lat, lon, geolocator):
    """Query city/country from coordinates."""
    
    try:
        location = geolocator.reverse(f"{lat}, {lon}", language='en')
        
        if location and location.raw.get('address'):
            addr = location.raw['address']
            
            city = (addr.get('city') or 
                   addr.get('town') or 
                   addr.get('village') or 
                   addr.get('municipality') or
                   addr.get('county') or
                   'Unknown')
            
            state = (addr.get('state') or 
                    addr.get('region') or '')
            
            country = addr.get('country', 'Unknown')
            
            return city, state, country
        
    except (GeocoderTimedOut, GeocoderServiceError):
        pass
    
    return None, None, None


def write_metadata_to_photo(photo_path, city, state, country, dry_run=False):
    """Write location metadata to photo using exiftool."""
    
    cmd = ['exiftool', '-overwrite_original']
    
    if city and city != 'Unknown':
        cmd.extend(['-IPTC:City=' + city])
    if state:
        cmd.extend(['-IPTC:Province-State=' + state])
    if country and country != 'Unknown':
        cmd.extend(['-IPTC:Country-PrimaryLocationName=' + country])
    
    cmd.append(photo_path)
    
    if dry_run:
        print(f"      [DRY RUN] {' '.join(cmd)}")
        return True
    else:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0


def process_photos(photos, dry_run=False):
    """Process all photos with reverse geocoding and metadata writing."""
    
    print(f"🌍 反向地理编码并写入元数据...")
    print(f"   使用 OpenStreetMap Nominatim API")
    print(f"   API 限制: 每秒1次请求")
    
    if dry_run:
        print(f"   ⚠️  DRY RUN 模式 - 不会实际修改照片\n")
    else:
        print(f"   ✍️  将直接修改照片 IPTC 元数据\n")
    
    geolocator = Nominatim(user_agent="photography-site-songshgeo")
    cache = {}
    success = 0
    failed = 0
    
    for i, photo in enumerate(photos, 1):
        filename = photo['FileName']
        filepath = photo['SourceFile']
        lat = photo['GPSLatitude']
        lon = photo['GPSLongitude']
        
        # Round to 2 decimals for cache
        cache_key = (round(lat, 2), round(lon, 2))
        
        if cache_key in cache:
            city, state, country = cache[cache_key]
            print(f"   [{i}/{len(photos)}] {filename}")
            print(f"      📍 {city}, {country} (缓存)")
        else:
            city, state, country = reverse_geocode(lat, lon, geolocator)
            
            if city:
                cache[cache_key] = (city, state, country)
                print(f"   [{i}/{len(photos)}] {filename}")
                print(f"      📍 {city}, {state}, {country}" if state else f"      📍 {city}, {country}")
            else:
                failed += 1
                print(f"   [{i}/{len(photos)}] {filename}")
                print(f"      ❌ 查询失败")
                time.sleep(2)
                continue
            
            # Respect API rate limit
            time.sleep(1.1)
        
        # Write metadata
        if city and country:
            if write_metadata_to_photo(filepath, city, state, country, dry_run):
                success += 1
                if not dry_run:
                    print(f"      ✅ 已写入元数据")
            else:
                failed += 1
                print(f"      ❌ 写入失败")
    
    print(f"\n✅ 完成！")
    print(f"   成功: {success}")
    print(f"   失败: {failed}")
    
    if not dry_run:
        print(f"\n📖 在 Lightroom 中:")
        print(f"   1. 右键照片文件夹 > 同步文件夹")
        print(f"   2. 勾选 '从磁盘读取元数据'")
        print(f"   3. Lightroom 会自动导入 IPTC 元数据")
    else:
        print(f"\n💡 确认无误后，去掉 --dry-run 参数执行")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Reverse geocode and write location metadata to photos'
    )
    parser.add_argument('directory', help='Directory containing photos')
    parser.add_argument('--dry-run', action='store_true',
                       help='Preview without modifying photos')
    
    args = parser.parse_args()
    
    if not Path(args.directory).exists():
        print(f"❌ 目录不存在: {args.directory}")
        sys.exit(1)
    
    photos = extract_gps_from_photos(args.directory)
    
    if not photos:
        print("❌ 没有找到包含 GPS 的照片")
        sys.exit(1)
    
    process_photos(photos, dry_run=args.dry_run)

