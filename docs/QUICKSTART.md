# 🚀 快速开始

> 3 分钟从手机照片提取 GPS 并生成 GPX 轨迹

## 第一步：安装依赖（1 分钟）

```bash
brew install exiftool
pip3 install --user --break-system-packages gpxpy
```

## 第二步：导出手机照片（1 分钟）

1. 打开 Mac "照片" App
2. 选择旅行期间的手机照片（与相机拍摄同一时间段）
3. 文件 > 导出 > 导出未修改的原片
4. ✅ **勾选"位置信息"**
5. 导出到文件夹（如：`~/Downloads/Denmark`）

## 第三步：生成 GPX 轨迹（2 分钟）

```bash
# 智能提取 GPS 并生成 GPX（带验证）
python3 scripts/smart-gps-extract.py ~/Downloads/Denmark denmark-2025
```

**交互式流程**：
1. ✅ 检查 GPS 覆盖率
2. ✅ 分析行程日期
3. ✅ 自动查询每天的城市
4. ✅ 验证完整性
5. ✅ 生成 GPX

**输出文件**：
- ✅ `gpx/denmark-2025.gpx` - 可直接在 Lightroom 中使用
- ✅ `gpx/denmark-2025-summary.json` - 行程总结（城市列表）

## 第四步：在 Lightroom 中加载 GPX（1 分钟）

1. 安装 [Jeffrey's Geotag Support 插件](http://regex.info/blog/lightroom-goodies/gps)
2. 在 Lightroom 中：
   - 选中相机照片
   - 文件 > 插件附加功能 > Geoencoding Support > Load Track Log
   - 选择 `gpx/denmark-2025.gpx`
3. 等待匹配完成
4. 右键 > 插件 > Geoencoding Support > Lookup Address（反向地理编码）

## 完成！

现在你的相机照片已经有：
- ✅ GPS 坐标
- ✅ 城市/国家名称
- ✅ 可以按地点智能筛选

---

## 下一步

### 发布到网站

1. 使用 JF Collection Publisher 创建智能集合
2. 按国家/城市筛选照片
3. 一键发布到 `content/trips/`
4. `git push` 自动部署到 Vercel

详细工作流：见 [README.md](README.md)

---

## 常用命令

```bash
# 启动本地预览
hugo server --buildDrafts

# 部署到 Vercel
git add .
git commit -m "Add trip photos"
git push origin main
```

