#!/bin/bash
# Extract GPS data from Mac Photos Library
# Usage: ./scripts/extract-mac-photos-gps.sh

set -e

PHOTOS_LIBRARY="$HOME/Pictures/Photos Library.photoslibrary/originals"
OUTPUT_JSON="mac-photos-gps.json"

echo "📸 从 Mac 相册提取 GPS 数据..."
echo "相册路径: $PHOTOS_LIBRARY"

# Check if exiftool is installed
if ! command -v exiftool &> /dev/null; then
    echo "❌ 未安装 exiftool"
    echo "请运行: brew install exiftool"
    exit 1
fi

# Check if Photos Library exists
if [ ! -d "$PHOTOS_LIBRARY" ]; then
    echo "❌ 相册库不存在: $PHOTOS_LIBRARY"
    echo "请检查路径或确保 iCloud 照片已下载到本机"
    exit 1
fi

# Extract GPS data
echo "正在扫描照片..."
exiftool -json -n -r -ext jpg -ext heic -ext jpeg \
  -FileName -GPSLatitude -GPSLongitude -GPSAltitude -DateTimeOriginal \
  "$PHOTOS_LIBRARY" > "$OUTPUT_JSON"

# Count results
TOTAL=$(cat "$OUTPUT_JSON" | grep -c "FileName" || echo "0")
WITH_GPS=$(cat "$OUTPUT_JSON" | grep -c "GPSLatitude" || echo "0")

echo "✅ 完成！"
echo "总照片数: $TOTAL"
echo "有 GPS 的: $WITH_GPS"
echo "输出文件: $OUTPUT_JSON"
echo ""
echo "下一步: python3 scripts/json2gpx.py $OUTPUT_JSON mac-photos-track.gpx"

