# 专业摄影工作流程

从相机到网站的完整 GPS 地理标记流程。

## 📋 目录

- [前置要求](#前置要求)
- [流程概览](#流程概览)
- [分步指南](#分步指南)
- [高级功能](#高级功能)
- [故障排除](#故障排除)

## 前置要求

### 必需软件

1. **Lightroom Classic** 及插件:
   - [Jeffrey's Geotag Support Plugin](http://regex.info/blog/lightroom-goodies/gps)
   - [JF Collection Publisher](https://regex.info/blog/lightroom-goodies/collection-publisher)

2. **命令行工具**:
   ```bash
   brew install exiftool
   pip3 install --user --break-system-packages geopy gpxpy
   ```

3. **Hugo Extended** (v0.148.2+):
   ```bash
   brew install hugo
   ```

## 流程概览

```
📷 相机照片 → 🎨 Lightroom → 🗺️ GPS轨迹 → 📍 地理标记 → 📂 导出 → 🚀 部署
   (无GPS)     (后期处理)   (手机GPS)    (匹配)     (网站)    (Vercel)
```

### 时间投入

- **初次设置**: ~30 分钟（一次性）
- **单次旅行处理**: ~15 分钟（100 张照片）
- **日常发布**: ~5 分钟每个合集

## 分步指南

### 步骤 1: Lightroom 照片预处理

#### 1.1 导入和组织

```
导入 → 智能合集 → 标记精选 → 评4+星级
```

**操作:**
- 导入旅行中的所有相机照片
- 按日期范围创建智能合集
- 按 `P` 键标记最佳照片
- 评 4+ 星级用于发布

#### 1.2 创建版权预设

导航至: `元数据 > 编辑元数据预设`

**设置:**
```yaml
版权: © 2025 SongshGeo
创建者: SongshGeo
创建者 URL: https://songshgeo.github.io/Photography-SongshGeo/
关键字: photography, travel, [国家], [城市]
```

**应用到所有选中的照片。**

### 步骤 2: GPS 轨迹生成

#### 2.1 导出手机照片

从 **照片 App**:
1. 选择同一日期范围的照片
2. `文件 > 导出 > 导出未修改的原件`
3. ✅ **勾选**: "包含位置信息"
4. 保存到文件夹（例如 `~/Downloads/Denmark`）

#### 2.2 生成 GPX 轨迹

**基本用法:**
```bash
python3 scripts/smart-gps-extract.py ~/Downloads/Denmark denmark-2025
```

**带日期范围验证:**
```bash
python3 scripts/smart-gps-extract.py ~/Downloads/Denmark denmark-2025 \
  -s 2025-08-12 -e 2025-08-23
```

**手动指定城市:**
```bash
python3 scripts/smart-gps-extract.py ~/Downloads/Denmark denmark-2025 \
  --d1 "奥胡斯" --d2 "欧登塞" --d5 "哥本哈根"
```

**交互式输出:**
```
📸 智能 GPS 提取与验证
━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 检查 GPS 覆盖率: 17/124 张照片 (14%)
✅ 分析行程日期: 2025-08-12 至 2025-08-23 (12 天)
✅ 查询城市信息:
   第 1 天 (2025-08-12): 托尔斯港
   第 2 天 (2025-08-13): 托尔斯港, 沃格
   ...
✅ 验证完整性: 所有日期都已覆盖
✅ 生成 GPX: gpx/denmark-2025.gpx
```

### 步骤 3: Lightroom 地理标记

#### 3.1 加载 GPS 轨迹

1. `文件 > 增效工具附加功能 > Geoencoding Support > Load Track Log`
2. 选择: `gpx/denmark-2025.gpx`
3. 插件自动按时间戳匹配 GPS 到照片
4. 查看地图视图验证准确性

#### 3.2 反向地理编码

1. `文件 > 增效工具附加功能 > Geoencoding Support > Reverse Geocode`
2. 选择有 GPS 的照片
3. 插件查询城市/国家/州名称
4. 元数据字段自动填充

**结果:** 所有照片现在都有 GPS 坐标 + 位置名称

### 步骤 4: 智能合集发布

#### 4.1 设置合集发布器

**首次设置:**

1. **创建发布服务**:
   - `图库 > 发布服务 > 设置...`
   - 选择: "硬盘"
   - 目标: `[项目根目录]/content/trips/`

2. **配置导出设置**:
   ```
   图像格式: JPEG
   质量: 85
   色彩空间: sRGB
   图像调整: 长边 2560px
   锐化: 屏幕，数量: 标准
   ```

3. **文件命名模板**:
   ```
   {date (yyyy)}{date (mm)}{date (dd)}-{sequence (0001)}
   示例: 20250812-0001.jpg
   ```

#### 4.2 创建智能合集

**合集结构:**
```
已发布文件夹: Trips
├── Denmark/Faroe Islands 2025
│   └── 过滤器: 国家 = 法罗群岛, 旗标 = 精选
├── Japan/Tokyo 2025
│   └── 过滤器: 国家 = 日本 AND 城市 = 东京, 旗标 = 精选
└── ...
```

**智能合集设置:**
```
名称: [国家] - [城市] - [年份]
匹配: 满足以下所有规则
  - 旗标为精选
  - 评级 ≥ 4 星
  - 国家包含 [国家]
  - 城市包含 [城市]
  - 拍摄日期在 [开始] 到 [结束] 范围内
```

#### 4.3 发布照片

1. 右键点击合集 → `发布`
2. 照片导出到 `content/trips/[国家]/`
3. 文件命名遵循模板
4. 元数据嵌入到 JPEG

### 步骤 5: 网站生成

#### 5.1 创建旅行索引

**创建文件:** `content/trips/Denmark/index.md`

```yaml
---
title: "法罗群岛与丹麦 2025"
date: 2025-08-12
location:
  country: 丹麦与法罗群岛
  city: 托尔斯港, 哥本哈根, 奥胡斯
coords:
  lat: 62.0104
  lon: -6.7719
cover: 20250812-0001.jpg
tags:
  - 风景
  - 旅行
  - 欧洲
  - 丹麦
  - 法罗群岛
  - 海岸线
categories:
  - trips
  - nature
---

一次夏日之旅，穿越法罗群岛壮丽的风景和丹麦充满活力的城市。
```

#### 5.2 本地测试

```bash
hugo server --buildDrafts
```

打开: http://localhost:1313

**验证:**
- ✅ 照片显示在画廊中
- ✅ 灯箱效果正常
- ✅ 元数据正确显示
- ✅ 地图显示 GPS 位置

#### 5.3 部署到生产环境

```bash
# 提交更改
git add content/trips/Denmark/
git add gpx/denmark-2025.gpx
git commit -m "添加丹麦与法罗群岛 2025 旅行照片 (15 张)"

# 推送到 GitHub
git push origin main
```

**Vercel** 在推送时自动部署（约 2 分钟）。

## 高级功能

### 批量处理

处理多次旅行:

```bash
# 为每次旅行生成 GPX
python3 scripts/smart-gps-extract.py ~/Photos/Japan japan-2025
python3 scripts/smart-gps-extract.py ~/Photos/Iceland iceland-2025

# 在 Lightroom 中加载所有轨迹
# 使用日期范围将正确的轨迹应用到每次旅行
```

### 自定义元数据

添加旅行特定的元数据:

```yaml
# content/trips/Japan/index.md
---
title: "东京街头摄影 2025"
trip_duration: "7 天"
camera: "Olympus OM-1"
lens: "M.Zuiko 12-40mm f/2.8"
highlights:
  - 涩谷十字路口
  - 浅草寺
  - 东京晴空塔
---
```

### SEO 优化

Hugo 自动生成:
- ✅ 站点地图: `/sitemap.xml`
- ✅ RSS 订阅: `/index.xml`
- ✅ Open Graph 标签
- ✅ Schema.org 标记

## 故障排除

### GPS 轨迹不匹配

**问题:** 加载轨迹后照片没有获得 GPS 坐标。

**解决方案:**
1. 检查时区: GPS 轨迹和照片必须匹配
2. 验证日期范围: 轨迹必须覆盖照片日期
3. 使用 `--expected-start` 和 `--expected-end` 进行验证
4. 使用 `--d1`、`--d2` 等手动指定缺失日期

### Lightroom 地图模块显示为灰色

**问题:** 地图模块不可用（中国区账号）。

**解决方案:** 改用 Jeffrey's 插件:
- GPS 坐标: Jeffrey's Geotag Support
- 反向地理编码: 使用插件内置查询

### 导出文件命名问题

**问题:** 文件命名不正确。

**检查:**
1. Lightroom 导出/发布设置中的文件命名模板
2. 使用: `{date (yyyy)}{date (mm)}{date (dd)}-{sequence (0001)}`
3. 避免空格和特殊字符

### Vercel 部署失败

**问题:** 推送到 GitHub 但网站未更新。

**步骤:**
1. 检查 Vercel 控制面板的构建日志
2. 验证 `hugo.toml` 配置
3. 确保 Hugo 版本匹配 (`0.148.2`)
4. 检查 `vercel.json` 中的构建命令

## 下一步

- 📚 阅读 [脚本指南](SCRIPTS_CN.md) 了解 GPS 提取详情
- 🧪 查看 [测试指南](TESTING_CN.md) 了解测试套件
- ⚙️ 参阅 [安装指南](SETUP_CN.md) 了解高级配置

---

**有疑问?** 在 [GitHub](https://github.com/SongshGeo/Photography-SongshGeo/issues) 上提出 issue。

