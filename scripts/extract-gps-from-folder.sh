#!/bin/bash
# Extract GPS from exported photo folder and generate GPX track
# Usage: ./scripts/extract-gps-from-folder.sh /path/to/photos output-name

set -e

if [ $# -lt 1 ]; then
    echo "Usage: ./scripts/extract-gps-from-folder.sh <photo_folder> [output_name]"
    echo "Example: ./scripts/extract-gps-from-folder.sh ~/Downloads/Denmark denmark-2025"
    exit 1
fi

PHOTO_FOLDER="$1"
OUTPUT_NAME="${2:-track}"

echo "📸 从照片文件夹提取 GPS 数据..."
echo "照片路径: $PHOTO_FOLDER"
echo "输出名称: $OUTPUT_NAME"

# Check if exiftool is installed
if ! command -v exiftool &> /dev/null; then
    echo "❌ 未安装 exiftool"
    echo "请运行: brew install exiftool"
    exit 1
fi

# Check if folder exists
if [ ! -d "$PHOTO_FOLDER" ]; then
    echo "❌ 文件夹不存在: $PHOTO_FOLDER"
    exit 1
fi

# Extract GPS data
echo ""
echo "🔍 正在扫描照片..."
exiftool -json -n -r -ext jpg -ext jpeg -ext heic -ext HEIC -ext JPG \
  -FileName -GPSLatitude -GPSLongitude -GPSAltitude -DateTimeOriginal \
  "$PHOTO_FOLDER" > "gpx/${OUTPUT_NAME}-gps.json"

# Count results
TOTAL=$(cat "gpx/${OUTPUT_NAME}-gps.json" | grep -c "FileName" || echo "0")
WITH_GPS=$(cat "gpx/${OUTPUT_NAME}-gps.json" | grep -c "GPSLatitude" || echo "0")

echo "✅ GPS 数据提取完成！"
echo "   总照片数: $TOTAL"
echo "   有 GPS 的: $WITH_GPS"
echo "   输出文件: gpx/${OUTPUT_NAME}-gps.json"

# Convert to GPX
echo ""
echo "🔄 转换为 GPX 格式..."
python3 scripts/json2gpx.py "gpx/${OUTPUT_NAME}-gps.json" "gpx/${OUTPUT_NAME}.gpx"

echo ""
echo "🎉 完成！"
echo "📍 生成的 GPX 文件: gpx/${OUTPUT_NAME}.gpx"
echo ""
echo "📖 下一步:"
echo "   在 Lightroom 中加载: gpx/${OUTPUT_NAME}.gpx"
echo "   File > Plug-in Extras > Geoencoding Support > Load Track Log"

