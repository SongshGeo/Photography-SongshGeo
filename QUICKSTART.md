# 🚀 快速开始

> 5 分钟从 Mac 相册提取 GPS 并生成 GPX 轨迹

## 第一步：安装依赖（1 分钟）

```bash
make install
```

或者手动安装：

```bash
brew install exiftool
pip3 install --user gpxpy
```

## 第二步：授予终端访问权限（30 秒）

macOS 保护照片库，需要授权：

1. 打开"系统设置" > "隐私与安全性" > "完全磁盘访问权限"
2. 点击"+"添加你的终端应用（Terminal/iTerm2/VSCode）
3. 勾选启用
4. **重启终端**

**不想授权？** 见 [TROUBLESHOOTING.md](TROUBLESHOOTING.md) 的"方案 B：手动导出"

## 第三步：提取 GPS 并生成 GPX（3 分钟）

```bash
make extract-gps
```

或者手动执行：

```bash
./scripts/extract-mac-photos-gps.sh
python3 scripts/json2gpx.py mac-photos-gps.json mac-photos-track.gpx
python3 scripts/split-gpx-by-year.py mac-photos-track.gpx
```

**输出文件**：
- ✅ `mac-photos-track.gpx` - 完整轨迹
- ✅ `mac-photos-track-2015.gpx`, `mac-photos-track-2016.gpx` ... - 按年份分割

## 第四步：在 Lightroom 中使用（1 分钟）

1. 下载并安装 [Jeffrey's Geotag Support 插件](http://regex.info/blog/lightroom-goodies/gps)
2. 在 Lightroom 中：
   - 选中相机照片
   - 文件 > 插件附加功能 > Geoencoding Support > Load Track Log
   - 选择 `mac-photos-track.gpx`（或按年份的文件）
3. 等待匹配完成
4. 在元数据面板验证 GPS 字段

## 完成！

现在你的相机照片已经有 GPS 了，可以：
- ✅ 按国家/城市筛选
- ✅ 导出到网站
- ✅ 在地图上显示

---

## 下一步

查看详细工作流：
- 📖 [SETUP.md](SETUP.md) - 详细设置指南
- 📖 [WORKFLOW-SUMMARY.md](WORKFLOW-SUMMARY.md) - 完整工作流
- 📖 [scripts/README.md](scripts/README.md) - 脚本详细说明

---

## 常用命令

```bash
# 启动开发服务器
make server

# 清理生成的 GPS 文件
make clean

# 查看帮助
make help
```

---

## 需要帮助？

遇到问题？查看：
1. [WORKFLOW-SUMMARY.md](WORKFLOW-SUMMARY.md) 的"常见问题"章节
2. [scripts/README.md](scripts/README.md) 的"故障排查"章节
3. 或提交 Issue

