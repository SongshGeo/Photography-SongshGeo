#!/usr/bin/env python3
"""
Interactive GPS extraction with validation and gap detection.

Usage:
    python3 scripts/smart-gps-extract.py /path/to/photos [output_name] [-s START] [-e END] [--d1 City1]

Examples:
    # Basic usage
    python3 scripts/smart-gps-extract.py ~/Downloads/Denmark denmark-2025
    
    # With expected date range
    python3 scripts/smart-gps-extract.py ~/Downloads/Denmark denmark-2025 -s 2025-08-12 -e 2025-08-23
    
    # With manual city overrides
    python3 scripts/smart-gps-extract.py ~/Downloads/Denmark denmark-2025 --d1 Copenhagen --d3 Aarhus
    
    # Combined: expected range + manual cities for missing dates
    python3 scripts/smart-gps-extract.py ~/Downloads/Trip trip-2025 -s 2025-07-01 -e 2025-07-10 --d1 Berlin --d8 Paris
"""

import json
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict, Counter

try:
    import gpxpy
    import gpxpy.gpx
    from geopy.geocoders import Nominatim
    from geopy.exc import GeocoderTimedOut
except ImportError as e:
    print(f"❌ 缺少依赖: {e}")
    print("请运行: pip3 install --user --break-system-packages gpxpy geopy")
    sys.exit(1)


# Color codes
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color


def print_header(text):
    """Print colored header."""
    print(f"\n{Colors.GREEN}{'='*60}{Colors.NC}")
    print(f"{Colors.GREEN}{text}{Colors.NC}")
    print(f"{Colors.GREEN}{'='*60}{Colors.NC}\n")


def print_step(step_num, total_steps, text):
    """Print step header."""
    print(f"\n{Colors.YELLOW}🔍 步骤 {step_num}/{total_steps}: {text}{Colors.NC}")


def print_success(text):
    """Print success message."""
    print(f"{Colors.GREEN}✅ {text}{Colors.NC}")


def print_error(text):
    """Print error message."""
    print(f"{Colors.RED}❌ {text}{Colors.NC}")


def print_warning(text):
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.NC}")


def print_info(text):
    """Print info message."""
    print(f"{Colors.BLUE}{text}{Colors.NC}")


def ask_continue(prompt="继续？"):
    """Ask user to continue."""
    response = input(f"\n{Colors.YELLOW}{prompt}{Colors.NC} (y/n): ")
    return response.lower() in ['y', 'yes', 'Y']


def extract_gps_data(photo_folder, output_name):
    """Extract GPS data from photos using exiftool."""
    
    print_step(1, 5, "扫描照片并提取 GPS 数据")
    
    output_json = f"gpx/{output_name}-gps.json"
    
    cmd = [
        'exiftool',
        '-json', '-n', '-r',
        '-ext', 'jpg', '-ext', 'jpeg', '-ext', 'heic', 
        '-ext', 'HEIC', '-ext', 'JPG',
        '-FileName', '-GPSLatitude', '-GPSLongitude', 
        '-GPSAltitude', '-DateTimeOriginal',
        str(photo_folder)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print_error(f"exiftool 错误: {result.stderr}")
        sys.exit(1)
    
    with open(output_json, 'w') as f:
        f.write(result.stdout)
    
    data = json.loads(result.stdout)
    
    total = len(data)
    with_gps = len([p for p in data if 'GPSLatitude' in p and 'GPSLongitude' in p])
    
    print()
    print_success("扫描完成")
    print(f"   总照片数: {Colors.BLUE}{total}{Colors.NC}")
    print(f"   有 GPS 的: {Colors.GREEN}{with_gps}{Colors.NC}")
    print(f"   无 GPS 的: {Colors.YELLOW}{total - with_gps}{Colors.NC}")
    
    if with_gps == 0:
        print()
        print_error("没有找到包含 GPS 的照片")
        print("请确保:")
        print("  1. 照片是从手机拍摄的（带 GPS）")
        print('  2. 导出时勾选了"位置信息"')
        sys.exit(1)
    
    return data


def analyze_date_range(data, expected_start=None, expected_end=None):
    """Analyze date range and group photos by date."""
    
    print_step(2, 5, "分析行程时间范围")
    
    # Filter photos with GPS and date
    valid_photos = [
        p for p in data 
        if all(k in p for k in ['GPSLatitude', 'GPSLongitude', 'DateTimeOriginal'])
    ]
    
    if not valid_photos:
        print_error("没有包含完整 GPS 和时间信息的照片")
        sys.exit(1)
    
    # Group by date
    photos_by_date = defaultdict(list)
    
    for p in valid_photos:
        try:
            dt = datetime.strptime(p['DateTimeOriginal'], '%Y:%m:%d %H:%M:%S')
            date_str = dt.strftime('%Y-%m-%d')
            photos_by_date[date_str].append({
                'lat': p['GPSLatitude'],
                'lon': p['GPSLongitude'],
                'time': dt,
                'filename': p['FileName']
            })
        except ValueError:
            continue
    
    dates = sorted(photos_by_date.keys())
    
    print()
    print_success("时间范围分析完成")
    print(f"   开始日期: {Colors.BLUE}{dates[0]}{Colors.NC}")
    print(f"   结束日期: {Colors.BLUE}{dates[-1]}{Colors.NC}")
    print(f"   总天数: {Colors.BLUE}{len(dates)}{Colors.NC} 天")
    
    # Validate against expected range if provided
    missing_dates = []
    if expected_start or expected_end:
        print()
        print_info("📅 验证预期时间范围...")
        
        if expected_start:
            expected_start_dt = datetime.strptime(expected_start, '%Y-%m-%d')
            actual_start_dt = datetime.strptime(dates[0], '%Y-%m-%d')
            
            # Check for missing dates before start
            current = expected_start_dt
            while current < actual_start_dt:
                date_str = current.strftime('%Y-%m-%d')
                missing_dates.append(date_str)
                current = current + timedelta(days=1)
        
        if expected_end:
            expected_end_dt = datetime.strptime(expected_end, '%Y-%m-%d')
            actual_end_dt = datetime.strptime(dates[-1], '%Y-%m-%d')
            
            # Check for missing dates after end
            current = actual_end_dt + timedelta(days=1)
            while current <= expected_end_dt:
                date_str = current.strftime('%Y-%m-%d')
                missing_dates.append(date_str)
                current = current + timedelta(days=1)
        
        if missing_dates:
            print_warning(f"发现 {len(missing_dates)} 天没有 GPS 照片:")
            for date in sorted(missing_dates):
                print(f"   - {date}")
        else:
            print_success("时间范围完整！")
    
    return photos_by_date, dates, missing_dates if (expected_start or expected_end) else []


def reverse_geocode_locations(photos_by_date, dates, day_overrides=None):
    """Reverse geocode GPS to city names for each day."""
    
    print_step(3, 5, "查询每天的城市位置（OpenStreetMap API）")
    print_info("⏱  这可能需要几秒钟...\n")
    
    geolocator = Nominatim(user_agent="photography-songshgeo")
    locations_by_date = {}
    cache = {}
    
    for i, date in enumerate(dates, 1):
        coords_list = photos_by_date[date]
        
        # Check if manually overridden
        if day_overrides and str(i) in day_overrides:
            city = day_overrides[str(i)]
            locations_by_date[date] = {
                'primary': city,
                'all': [city],
                'count': len(coords_list),
                'manual': True
            }
            print(f"   第 {i:2d} 天 ({date}): {Colors.BLUE}{city}{Colors.NC} (手动指定)")
            continue
        
        cities = []
        
        # Sample up to 3 coordinates per day
        sample_size = min(3, len(coords_list))
        sample_indices = [0, len(coords_list)//2, len(coords_list)-1] if len(coords_list) > 2 else list(range(len(coords_list)))
        sample_coords = [coords_list[idx] for idx in sample_indices[:sample_size]]
        
        for coord in sample_coords:
            lat, lon = coord['lat'], coord['lon']
            cache_key = (round(lat, 2), round(lon, 2))
            
            if cache_key in cache:
                city = cache[cache_key]
            else:
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
                        cache[cache_key] = city
                    else:
                        city = 'Unknown'
                    time.sleep(1.1)  # API rate limit
                except (GeocoderTimedOut, Exception):
                    city = 'Unknown'
                    time.sleep(2)
            
            if city != 'Unknown':
                cities.append(city)
        
        # Count most common city
        if cities:
            city_counts = Counter(cities)
            primary_city = city_counts.most_common(1)[0][0]
            all_cities = list(city_counts.keys())
            locations_by_date[date] = {
                'primary': primary_city,
                'all': all_cities,
                'count': len(coords_list),
                'manual': False
            }
        else:
            locations_by_date[date] = {
                'primary': 'Unknown',
                'all': [],
                'count': len(coords_list),
                'manual': False
            }
        
        # Print result
        loc = locations_by_date[date]
        city_display = f"{Colors.GREEN}{loc['primary']}{Colors.NC}" if loc['primary'] != 'Unknown' else f"{Colors.RED}Unknown{Colors.NC}"
        print(f"   第 {i:2d} 天 ({date}): {city_display}")
        
        if len(loc['all']) > 1:
            others = ', '.join(loc['all'][1:])
            print(f"          {Colors.BLUE}其他: {others}{Colors.NC}")
        
        print(f"          照片数: {loc['count']} 张")
    
    return locations_by_date


def validate_coverage(locations_by_date, dates):
    """Validate that all days have location data."""
    
    print_step(4, 5, "验证地点覆盖完整性")
    
    missing_days = []
    for i, date in enumerate(dates, 1):
        loc = locations_by_date[date]
        if loc['primary'] == 'Unknown' and not loc.get('manual'):
            missing_days.append((i, date))
    
    if missing_days:
        print()
        print_error(f"发现 {len(missing_days)} 天无法确定地点:")
        for day_num, date in missing_days:
            print(f"   第 {day_num} 天: {date}")
        
        print()
        print_warning("请手动指定缺失日期的城市，然后重新运行:")
        print()
        
        # Generate example command
        manual_args = ' '.join([f'--d{day_num} "CityName"' for day_num, _ in missing_days])
        print(f'{Colors.BLUE}./scripts/smart-gps-extract.py "{sys.argv[1]}" "{sys.argv[2] if len(sys.argv) > 2 else "track"}" {manual_args}{Colors.NC}')
        print()
        
        return False
    
    print()
    print_success("所有日期都有地点信息！")
    
    # Display summary
    unique_cities = set(loc['primary'] for loc in locations_by_date.values())
    print(f"\n{Colors.BLUE}📊 行程总结:{Colors.NC}")
    print(f"   总天数: {len(dates)} 天")
    print(f"   访问城市: {', '.join(sorted(unique_cities))}")
    
    return True


def generate_gpx(photos_by_date, dates, locations_by_date, output_name):
    """Generate GPX track file."""
    
    print_step(5, 5, "生成 GPX 轨迹文件")
    
    gpx = gpxpy.gpx.GPX()
    gpx.creator = "Smart GPS Extractor - SongshGeo"
    
    track = gpxpy.gpx.GPXTrack()
    track.name = f"Trip {dates[0]} to {dates[-1]}"
    gpx.tracks.append(track)
    
    segment = gpxpy.gpx.GPXTrackSegment()
    track.segments.append(segment)
    
    # Collect all points sorted by time
    all_points = []
    for date in dates:
        all_points.extend(photos_by_date[date])
    
    all_points.sort(key=lambda x: x['time'])
    
    # Add track points
    for point in all_points:
        segment.points.append(gpxpy.gpx.GPXTrackPoint(
            point['lat'],
            point['lon'],
            elevation=point.get('alt'),
            time=point['time']
        ))
    
    # Write GPX
    output_gpx = f"gpx/{output_name}.gpx"
    with open(output_gpx, 'w') as f:
        f.write(gpx.to_xml())
    
    print()
    print_success("GPX 轨迹生成完成！")
    print(f"   轨迹点数: {Colors.BLUE}{len(segment.points)}{Colors.NC}")
    print(f"   时间跨度: {Colors.BLUE}{len(dates)}{Colors.NC} 天")
    
    return output_gpx


def save_location_summary(locations_by_date, dates, output_name):
    """Save location summary to JSON."""
    
    summary = {
        'trip_name': output_name,
        'start_date': dates[0],
        'end_date': dates[-1],
        'total_days': len(dates),
        'daily_locations': [
            {
                'day': i,
                'date': date,
                'primary_city': locations_by_date[date]['primary'],
                'all_cities': locations_by_date[date]['all'],
                'photo_count': locations_by_date[date]['count'],
                'manually_set': locations_by_date[date].get('manual', False)
            }
            for i, date in enumerate(dates, 1)
        ],
        'cities_visited': sorted(set(loc['primary'] for loc in locations_by_date.values()))
    }
    
    output_file = f"gpx/{output_name}-summary.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    return output_file


def main():
    """Main function."""
    
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Interactive GPS extraction with validation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/smart-gps-extract.py ~/Downloads/Denmark denmark-2025
  python3 scripts/smart-gps-extract.py ~/Downloads/Trip trip-2025 --d1 Copenhagen --d3 Aarhus
        """
    )
    
    parser.add_argument('photo_folder', help='Photo folder path')
    parser.add_argument('output_name', nargs='?', default='track', help='Output name (default: track)')
    
    # Expected date range
    parser.add_argument('-s', '--expected-start', metavar='DATE', 
                       help='Expected start date (YYYY-MM-DD)')
    parser.add_argument('-e', '--expected-end', metavar='DATE',
                       help='Expected end date (YYYY-MM-DD)')
    
    # Dynamic day arguments (d1, d2, d3, etc.)
    for i in range(1, 32):  # Support up to 31 days
        parser.add_argument(f'--d{i}', metavar='CITY', help=f'Manually specify city for day {i}')
    
    args = parser.parse_args()
    
    # Collect day overrides
    day_overrides = {}
    for i in range(1, 32):
        city = getattr(args, f'd{i}', None)
        if city:
            day_overrides[str(i)] = city
    
    # Validate photo folder
    photo_folder = Path(args.photo_folder)
    if not photo_folder.exists():
        print_error(f"文件夹不存在: {photo_folder}")
        sys.exit(1)
    
    # Create gpx directory if not exists
    Path('gpx').mkdir(exist_ok=True)
    
    # Print header
    print_header("📸 智能 GPS 提取与验证")
    print_info(f"📂 照片文件夹: {photo_folder}")
    print_info(f"📝 输出名称: {args.output_name}")
    
    if day_overrides:
        print()
        for day, city in sorted(day_overrides.items(), key=lambda x: int(x[0])):
            print_info(f"📍 手动指定第 {day} 天: {city}")
    
    # Step 1: Extract GPS data
    data = extract_gps_data(photo_folder, args.output_name)
    
    if not ask_continue("继续分析行程？"):
        print_warning("已取消")
        return
    
    # Step 2: Analyze date range
    result = analyze_date_range(data, args.expected_start, args.expected_end)
    photos_by_date, dates, missing_dates = result if len(result) == 3 else (*result, [])
    
    # Handle missing dates from expected range
    if missing_dates:
        print()
        print_error("时间范围不完整！")
        print()
        print_warning("请补充缺失日期的城市信息，然后重新运行:")
        print()
        
        # Calculate which day numbers these are
        if args.expected_start:
            start_dt = datetime.strptime(args.expected_start, '%Y-%m-%d')
        else:
            start_dt = datetime.strptime(dates[0], '%Y-%m-%d')
        
        manual_args = []
        for missing_date in sorted(missing_dates):
            missing_dt = datetime.strptime(missing_date, '%Y-%m-%d')
            day_num = (missing_dt - start_dt).days + 1
            manual_args.append(f'--d{day_num} "CityName"')
        
        cmd_args = ' '.join(manual_args)
        expected_range = ''
        if args.expected_start:
            expected_range += f' -s {args.expected_start}'
        if args.expected_end:
            expected_range += f' -e {args.expected_end}'
        
        print(f'{Colors.BLUE}python3 scripts/smart-gps-extract.py "{args.photo_folder}" "{args.output_name}"{expected_range} {cmd_args}{Colors.NC}')
        print()
        sys.exit(1)
    
    if not ask_continue("继续查询地点信息？"):
        print_warning("已取消")
        return
    
    # Step 3: Reverse geocode
    locations_by_date = reverse_geocode_locations(photos_by_date, dates, day_overrides)
    
    # Step 4: Validate coverage
    if not validate_coverage(locations_by_date, dates):
        sys.exit(1)
    
    if not ask_continue("地点验证通过，继续生成 GPX？"):
        print_warning("已取消")
        return
    
    # Step 5: Generate GPX
    output_gpx = generate_gpx(photos_by_date, dates, locations_by_date, args.output_name)
    
    # Save summary
    summary_file = save_location_summary(locations_by_date, dates, args.output_name)
    
    # Final summary
    print_header("✅ 处理完成！")
    
    print(f"{Colors.BLUE}📁 生成的文件:{Colors.NC}")
    print(f"   GPX 轨迹: {Colors.GREEN}gpx/{args.output_name}.gpx{Colors.NC}")
    print(f"   GPS 数据: gpx/{args.output_name}-gps.json")
    print(f"   行程总结: gpx/{args.output_name}-summary.json")
    
    print(f"\n{Colors.BLUE}📖 下一步:{Colors.NC}")
    print("   1. 在 Lightroom 中加载 GPX 文件")
    print("   2. File > Plug-in Extras > Geoencoding Support > Load Track Log")
    print(f"   3. 选择: {Colors.GREEN}gpx/{args.output_name}.gpx{Colors.NC}")
    print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        print_warning("用户中断")
        sys.exit(0)
    except Exception as e:
        print()
        print_error(f"发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

