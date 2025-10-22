# 安装指南

详细的安装和配置说明。

## 📦 前置要求

### 系统要求

- **macOS** 12.0+（用于 Photos.app 集成）
- **Python** 3.9+
- **Node.js** 16+（可选，用于主题开发）
- **Hugo Extended** 0.148.2+

### 必需软件

1. **Hugo Extended**
   ```bash
   brew install hugo
   ```

2. **ExifTool**
   ```bash
   brew install exiftool
   ```

3. **Python 包**
   ```bash
   pip3 install --user --break-system-packages geopy gpxpy
   ```

### Lightroom 插件

下载并安装：

1. **[Jeffrey's Geotag Support Plugin](http://regex.info/blog/lightroom-goodies/gps)**
   - GPS 轨迹加载
   - 反向地理编码
   - 地图集成

2. **[JF Collection Publisher](https://regex.info/blog/lightroom-goodies/collection-publisher)**
   - 自动发布
   - 智能合集
   - 文件命名模板

## 🚀 安装步骤

### 1. 克隆仓库

```bash
git clone --recursive https://github.com/SongshGeo/Photography-SongshGeo.git
cd Photography-SongshGeo
```

**注意:** `--recursive` 很重要，用于包含 Hugo 主题子模块。

### 2. 安装依赖

```bash
# 安装生产环境依赖
make install

# 安装开发依赖（用于测试）
make install-dev
```

### 3. 验证安装

```bash
# 检查 Hugo
hugo version

# 检查 Python 包
python3 -c "import gpxpy, geopy; print('OK')"

# 检查 ExifTool
exiftool -ver

# 运行测试
make test
```

## ⚙️ 配置

### Hugo 配置

编辑 `hugo.toml`:

```toml
baseURL = 'https://your-site.com/'
languageCode = 'zh-cn'
title = '你的摄影网站'

[params]
  author = "你的名字"
  description = "你的摄影描述"
  
  [params.social]
    email = "your@email.com"
    github = "yourusername"
```

### Vercel 部署

1. **连接 GitHub 仓库到 Vercel**:
   - 访问 [vercel.com](https://vercel.com)
   - 导入你的 GitHub 仓库
   - 配置项目

2. **构建设置**（从 `vercel.json` 自动检测）:
   ```json
   {
     "build": {
       "command": "hugo --gc --minify"
     }
   }
   ```

3. **环境变量**（如需要）:
   - 基本设置无需配置

### GitHub Actions（可选）

测试自动运行。在 `.github/workflows/tests.yml` 中配置。

## 🔧 Lightroom 配置

### 安装插件

1. 下载插件 ZIP 文件
2. 解压到文件夹
3. 在 Lightroom 中: `文件 > 增效工具管理器 > 添加`
4. 选择插件文件夹

### 配置 Geotag Support

1. 打开插件设置
2. 配置时区偏移
3. 设置默认地理编码提供商（OpenStreetMap）

### 配置 Collection Publisher

1. 创建发布服务: `图库 > 发布服务`
2. 选择 "硬盘"
3. 设置目标: `[项目]/content/trips/`
4. 配置导出设置（参见 [工作流指南](WORKFLOW_CN.md)）

## 📁 项目结构

```
Photography-SongshGeo/
├── content/              # 网站内容
│   ├── trips/           # 旅行照片画廊
│   ├── nature/          # 自然摄影
│   └── urban/           # 城市摄影
├── docs/                # 文档
├── gpx/                 # GPS 轨迹（git 忽略）
├── scripts/             # GPS 提取脚本
├── tests/               # 测试套件
├── themes/gallery/      # Hugo 主题（子模块）
├── hugo.toml            # Hugo 配置
├── Makefile             # 构建命令
├── pytest.ini           # 测试配置
└── requirements-dev.txt # 开发依赖
```

## 🧪 开发设置

### 运行测试

```bash
# 安装开发依赖
make install-dev

# 运行所有测试
make test

# 运行特定测试
pytest tests/test_gps_extraction.py -v
```

### 本地开发服务器

```bash
# 启动 Hugo 服务器
hugo server --buildDrafts

# 或使用 Makefile
make server
```

打开: http://localhost:1313

### 代码质量

```bash
# 格式化代码
black scripts/ tests/

# 排序导入
isort scripts/ tests/

# 代码检查
flake8 scripts/ tests/
```

## 🔐 安全与隐私

### Git 忽略

`.gitignore` 包含：
- `gpx/` - GPS 轨迹（包含位置数据）
- 个人照片文件
- 构建产物
- 测试覆盖率报告

### EXIF 数据

- GPS 坐标嵌入发布的照片中
- 发布位置数据前考虑隐私
- 如需要可使用 Lightroom 的 "移除位置数据"

## 🆘 故障排除

### Hugo 主题未找到

**问题:** 克隆后主题文件缺失。

**解决:**
```bash
git submodule update --init --recursive
```

### Python 包安装失败

**问题:** macOS 上出现 `externally-managed-environment` 错误。

**解决:**
```bash
pip3 install --user --break-system-packages <包名>
```

### ExifTool 权限被拒绝

**问题:** 无法读取照片库。

**解决:**
1. 系统偏好设置 > 安全性与隐私
2. 授予终端 "完全磁盘访问权限"

### Vercel 构建失败

**问题:** Vercel 上部署失败。

**检查:**
1. `vercel.json` 中的 Hugo 版本
2. 构建命令
3. 查看 Vercel 构建日志

## 📚 下一步

- 阅读 [工作流指南](WORKFLOW_CN.md) 了解完整摄影工作流程
- 查看 [脚本指南](SCRIPTS_CN.md) 了解 GPS 提取
- 参阅 [测试指南](TESTING_CN.md) 了解开发

---

**需要帮助?** 在 [GitHub](https://github.com/SongshGeo/Photography-SongshGeo/issues) 上提出 issue。

