# 脚本使用指南

GPS 提取和处理脚本的完整文档。

## 📋 脚本列表

### 核心脚本

1. **`smart-gps-extract.py`** ⭐ - 智能 GPS 提取（推荐）
2. **`extract-gps-from-folder.sh`** - 简单 GPS 提取
3. **`json2gpx.py`** - JSON 转 GPX
4. **`write-location-metadata.py`** - 批量地理编码

## ⭐ smart-gps-extract.py

交互式 GPS 提取，带自动验证和城市检测。

### 基本用法

```bash
python3 scripts/smart-gps-extract.py <照片文件夹> [输出名称]
```

### 示例

#### 1. 基础提取

```bash
python3 scripts/smart-gps-extract.py ~/Downloads/Denmark denmark-2025
```

**输出:**
```
📸 智能 GPS 提取与验证
━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 步骤 1/5: 扫描照片...
✅ 扫描完成
   总照片数: 124
   有 GPS 的: 17 (14%)

继续分析行程？ (y/n): y

🔍 步骤 2/5: 分析行程时间范围
✅ 时间范围分析完成
   开始日期: 2025-08-12
   结束日期: 2025-08-19
   总天数: 8 天

🔍 步骤 3/5: 查询每天的城市...
   第 1 天 (2025-08-12): Tórshavn
          照片数: 2 张
   第 2 天 (2025-08-13): Tórshavn, Vágar
          照片数: 5 张
   ...

✅ 所有日期都有地点信息！

地点验证通过，继续生成 GPX？ (y/n): y

✅ GPX 轨迹生成完成！
```

#### 2. 带日期范围验证

```bash
python3 scripts/smart-gps-extract.py ~/Downloads/Denmark denmark-2025 \
  -s 2025-08-12 -e 2025-08-23
```

如果有缺失日期，脚本会提示：

```
❌ 时间范围不完整！

⚠️  发现 3 天没有 GPS 照片:
   - 2025-08-20
   - 2025-08-21
   - 2025-08-22

请补充缺失日期的城市信息，然后重新运行:

python3 scripts/smart-gps-extract.py "~/Downloads/Denmark" "denmark-2025" \
  -s 2025-08-12 -e 2025-08-23 \
  --d9 "城市名" --d10 "城市名" --d11 "城市名"
```

#### 3. 手动指定城市

```bash
python3 scripts/smart-gps-extract.py ~/Downloads/Denmark denmark-2025 \
  --d1 "奥胡斯" --d2 "欧登塞" --d5 "哥本哈根"
```

适用于：
- 某天没有手机拍照
- 自动检测的城市不准确
- 需要指定特定位置

### 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `photo_folder` | 照片文件夹路径（必需） | `~/Downloads/Denmark` |
| `output_name` | 输出文件名（可选，默认: track） | `denmark-2025` |
| `-s, --expected-start` | 预期开始日期 | `-s 2025-08-12` |
| `-e, --expected-end` | 预期结束日期 | `-e 2025-08-23` |
| `--d1, --d2, ...` | 手动指定某天的城市 | `--d1 "哥本哈根"` |

### 输出文件

脚本生成 3 个文件：

```
gpx/
├── denmark-2025.gpx           # GPX 轨迹（用于 Lightroom）
├── denmark-2025-gps.json      # 原始 GPS 数据
└── denmark-2025-summary.json  # 行程总结
```

#### summary.json 示例

```json
{
  "trip_name": "denmark-2025",
  "start_date": "2025-08-12",
  "end_date": "2025-08-23",
  "total_days": 12,
  "daily_locations": [
    {
      "day": 1,
      "date": "2025-08-12",
      "primary_city": "Tórshavn",
      "all_cities": ["Tórshavn"],
      "photo_count": 2,
      "manually_set": false
    },
    ...
  ],
  "cities_visited": ["Aarhus", "Copenhagen", "Odense", "Tórshavn"]
}
```

## 📄 extract-gps-from-folder.sh

简单的一键 GPS 提取（无验证）。

### 用法

```bash
./scripts/extract-gps-from-folder.sh <照片文件夹> <输出名称>
```

### 示例

```bash
./scripts/extract-gps-from-folder.sh ~/Downloads/Denmark denmark
```

**输出:**
- `gpx/denmark-gps.json` - GPS 数据
- `gpx/denmark-track.gpx` - GPX 轨迹

## 🔄 json2gpx.py

将 exiftool JSON 转换为 GPX 格式。

### 用法

```bash
python3 scripts/json2gpx.py <输入JSON> <输出GPX>
```

### 示例

```bash
python3 scripts/json2gpx.py denmark-gps.json denmark.gpx
```

## 🌍 write-location-metadata.py

批量反向地理编码，将 GPS 坐标转换为城市/国家名称并写入 EXIF。

### 用法

```bash
python3 scripts/write-location-metadata.py <照片文件夹> [--dry-run]
```

### 示例

#### 1. 预览模式（不修改文件）

```bash
python3 scripts/write-location-metadata.py ~/Photos/Denmark --dry-run
```

#### 2. 实际写入

```bash
python3 scripts/write-location-metadata.py ~/Photos/Denmark
```

**注意:** 
- 使用 OpenStreetMap Nominatim API（免费）
- 自动限速（1 秒/请求）
- 缓存相近坐标以减少请求

## 🛠️ 工作流集成

### 推荐工作流

```bash
# 1. 从 Mac Photos 导出手机照片
# （文件 > 导出 > 导出未修改的原件，勾选"包含位置信息"）

# 2. 生成 GPX 轨迹（智能提取）
python3 scripts/smart-gps-extract.py ~/Downloads/Denmark denmark-2025

# 3. 在 Lightroom 中加载 GPX
# （文件 > 增效工具附加功能 > Geoencoding Support > Load Track Log）

# 4. 反向地理编码（可选，如果插件不可用）
python3 scripts/write-location-metadata.py /path/to/lightroom/photos

# 5. 发布到网站
# （使用 Lightroom Collection Publisher）
```

## 📊 性能提示

### GPS 覆盖率

- **理想**: >50% 的照片有 GPS
- **最低**: >10% 的照片有 GPS
- **不足**: <10% 可能导致日期缺失

### API 限速

OpenStreetMap Nominatim API:
- 限制: 1 请求/秒
- 脚本自动遵守限速
- 使用缓存减少重复请求

### 时区注意事项

- 确保 GPS 轨迹和照片时间戳时区一致
- EXIF 存储本地时间（无时区）
- 跨时区旅行时可能需要手动调整

## 🐛 故障排除

### 问题: GPS 覆盖率为 0%

**原因:** 导出照片时未包含位置信息

**解决:**
1. 重新从 Photos.app 导出
2. ✅ 勾选 "包含位置信息"

### 问题: 城市检测不准确

**原因:** OpenStreetMap 数据可能不精确

**解决:**
使用手动覆盖：
```bash
python3 scripts/smart-gps-extract.py ... --d3 "正确的城市名"
```

### 问题: 缺失某些日期

**原因:** 某天没有拍照或 GPS 数据

**解决:**
1. 使用 `-s` 和 `-e` 参数验证日期范围
2. 根据提示手动指定城市

## 📚 相关文档

- [工作流指南](WORKFLOW_CN.md) - 完整工作流程
- [测试指南](TESTING_CN.md) - 脚本测试
- [GitHub Issues](https://github.com/SongshGeo/Photography-SongshGeo/issues) - 报告问题

---

**需要帮助？** 在 [GitHub](https://github.com/SongshGeo/Photography-SongshGeo/issues) 上提出 issue。

