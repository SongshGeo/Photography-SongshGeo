# 标签和文件夹结构设计文档

## 📋 设计原则

**核心原则**：所有照片都是旅行照片，不再使用 categories 分类系统。

**组织方式**：
- **文件夹结构**：按地理位置组织（国家/地区/城市）
- **标签系统**：使用 tags 进行分类，分为主题标签和地理标签

---

## 📁 文件夹结构

### 当前结构（保持不变）

```
content/trips/
├── _index.md                    # 旅行摄影主页
├── _template.md                  # 相册模板
├── Germany/                      # 国家/地区
│   ├── _index.md                # 德国主页
│   ├── Dresden/                 # 城市/区域
│   │   ├── _index.md
│   │   └── [照片文件]
│   ├── Frankfurt/
│   │   ├── _index.md
│   │   └── [照片文件]
│   └── [其他城市]
├── China/
│   ├── _index.md
│   ├── Hong Kong/
│   │   ├── _index.md
│   │   └── [照片文件]
│   └── Sichuan/
│       ├── _index.md
│       └── [照片文件]
├── Japan/
│   ├── _index.md
│   └── [照片文件]
├── Denmark/
│   ├── _index.md
│   └── [照片文件]
└── [其他国家/地区]
```

### 文件夹命名规范

- **一级目录**：国家/地区名称（英文，首字母大写）
  - 示例：`Germany`, `China`, `Japan`, `Denmark`, `United States`
  - 多词名称：使用空格，如 `United States`, `Faroe Islands`

- **二级目录**：城市/区域名称（英文，首字母大写）
  - 示例：`Dresden`, `Hong Kong`, `Sichuan`
  - 如果国家/地区下只有一个相册，可以直接使用 `index.md`，不需要子文件夹

---

## 🏷️ 标签系统设计

### 标签分类

标签分为两大类：

#### 1. 主题标签（Theme Tags）

描述照片的内容类型和主题：

**自然景观类**：
- `landscape` - 风景
- `nature` - 自然
- `coastline` - 海岸线
- `lake` - 湖泊
- `mountain` - 山脉

**建筑与城市类**：
- `architecture` - 建筑
- `urban` - 城市
- `cityscape` - 城市景观
- `street` - 街拍

**人文类**：
- `culture` - 文化
- `people` - 人物
- `portrait` - 肖像
- `history` - 历史

**其他**：
- `wildlife` - 野生动物
- `safari` - 野生动物园
- `biodiversity` - 生物多样性
- `road-trip` - 公路旅行

#### 2. 地理标签（Location Tags）

描述拍摄地点：

**国家/地区**：
- `germany` - 德国
- `china` - 中国
- `japan` - 日本
- `denmark` - 丹麦
- `italy` - 意大利
- `slovakia` - 斯洛伐克
- `ecuador` - 厄瓜多尔
- `zambia` - 赞比亚
- `united-states` / `usa` - 美国
- `faroe-islands` - 法罗群岛

**城市/区域**：
- `dresden` - 德累斯顿
- `frankfurt` - 法兰克福
- `tokyo` - 东京
- `hong-kong` - 香港
- `sichuan` - 四川
- `bavaria` - 巴伐利亚
- `bad-wiessee` - 巴特维塞
- `eisenach` - 爱森纳赫

**大洲/区域**：
- `europe` - 欧洲
- `asia` - 亚洲
- `africa` - 非洲
- `south-america` - 南美洲
- `scandinavia` - 斯堪的纳维亚
- `andes` - 安第斯山脉

**通用**：
- `travel` - 旅行（可选，因为所有照片都是旅行照片）

### 标签使用规范

#### 在相册的 `_index.md` 中使用：

```yaml
---
title: "Germany"
date: 2025-01-24
description: "Photography from various cities and regions across Germany"
tags: 
  # 地理标签
  - "germany"
  - "europe"
  # 主题标签
  - "architecture"
  - "landscape"
  - "culture"
  - "travel"  # 可选
---
```

#### 标签命名规范：

1. **使用小写字母**
2. **多词使用连字符**：`hong-kong`, `united-states`, `road-trip`
3. **避免空格**：使用连字符而不是空格
4. **使用英文**：所有标签使用英文
5. **保持一致性**：相同概念使用相同标签（如 `usa` 和 `united-states` 统一为一个）

---

## 🎨 前端展示设计

### 标签导航设计选项

#### 方案 A：统一标签列表（简单）

- 所有标签（主题+地理）混合显示
- 按使用频率排序（最常用的在前）
- 或按字母顺序排序
- 适合标签数量较少的情况

**视觉设计**：
- 标签云（Tag Cloud）：常用标签更大更突出
- 标签列表（Tag List）：统一大小，网格排列

#### 方案 B：分组显示（推荐）⭐

- **主题标签组**：显示所有主题标签
  - 标题："主题" 或 "Theme" 或 "内容类型"
  - 标签：landscape, architecture, nature, urban, cityscape, culture, wildlife, street, coastline, people, portrait 等
  
- **地理标签组**：显示所有地理标签
  - 标题："地点" 或 "Location" 或 "拍摄地点"
  - 标签：germany, china, japan, denmark, europe, asia, africa 等

**视觉设计**：
- 使用分组标题区分
- 可以使用不同的视觉样式（如不同颜色、图标）
- 主题标签：使用内容相关的图标（如 🏔️ landscape, 🏛️ architecture）
- 地理标签：使用地图/位置图标（如 📍）

#### 方案 C：仅显示主题标签

- 只显示主题标签（landscape, architecture, nature 等）
- 地理信息通过相册文件夹结构体现
- 在相册卡片上显示地理位置名称
- 适合希望导航更简洁的情况

### 标签筛选功能

**基础功能**：
- 点击标签后，筛选显示包含该标签的相册
- 显示当前激活的标签（高亮显示）
- 支持清除筛选（显示所有相册）

**高级功能**（可选）：
- 多标签筛选（AND 逻辑）：同时选择多个标签
- 标签组合筛选（OR 逻辑）：选择多个标签，显示包含任一标签的相册
- 标签计数：显示每个标签下的相册/照片数量

### 标签在相册卡片上的显示（可选）

- 在相册卡片上显示主要标签（1-3 个）
- 使用小标签图标或徽章样式
- 鼠标悬停显示所有标签

---

## 📝 实施建议

### 对于前端设计师

1. **设计标签导航组件**
   - 考虑使用方案 B（分组显示），用户体验更好
   - 设计标签的视觉样式（圆角、颜色、大小）
   - 设计激活状态的视觉反馈

2. **设计标签筛选交互**
   - 点击标签后的筛选动画
   - 筛选结果的展示方式
   - 清除筛选的交互

3. **响应式设计**
   - 移动端：标签可以横向滚动
   - 平板端：标签网格布局
   - 桌面端：标签完整展示

### 对于开发人员

1. **移除 Categories Navigation**
   - 从 `themes/gallery/layouts/_default/home.html` 中移除 `{{ partial "categories.html" }}`
   - 或修改 `categories.html` 为 `tags.html`

2. **创建 Tags Navigation 组件**
   - 新建 `themes/gallery/layouts/partials/tags.html`
   - 使用 `site.Taxonomies.tags` 访问标签数据
   - 实现标签分组（主题标签 vs 地理标签）

3. **实现标签筛选功能**
   - 使用 JavaScript 实现客户端筛选
   - 或使用 Hugo 的 taxonomy 页面实现服务端筛选

---

## 🔄 迁移计划

### 从 Categories 迁移到 Tags

1. **移除 categories 引用**
   - 从所有相册的 `_index.md` 中移除 `categories: ["trips"]`
   - 保留 `tags` 字段

2. **清理 categories 目录**
   - 可以保留 `content/categories/trips/_index.md` 作为备份
   - 或完全删除 `content/categories/` 目录

3. **更新标签**
   - 确保所有相册都有合适的主题标签和地理标签
   - 统一标签命名（如统一使用 `united-states` 而不是 `usa`）

---

## 📊 标签统计（参考）

基于当前内容，主要标签包括：

**主题标签**：
- landscape (风景) - 最常用
- architecture (建筑) - 常用
- nature (自然) - 常用
- urban (城市) - 常用
- cityscape (城市景观) - 常用
- culture (文化) - 常用
- street (街拍) - 较少
- wildlife (野生动物) - 较少
- coastline (海岸线) - 较少

**地理标签**：
- germany (德国) - 最常用
- china (中国) - 常用
- europe (欧洲) - 常用
- asia (亚洲) - 常用
- japan (日本) - 常用
- denmark (丹麦) - 常用

---

## ✅ Checklist

### 设计阶段
- [ ] 确定标签导航设计方案（A/B/C）
- [ ] 设计标签视觉样式
- [ ] 设计标签分组样式（如果使用方案 B）
- [ ] 设计标签筛选交互
- [ ] 设计响应式布局

### 开发阶段
- [ ] 移除 Categories Navigation
- [ ] 创建 Tags Navigation 组件
- [ ] 实现标签筛选功能
- [ ] 更新所有相册的标签
- [ ] 测试标签导航和筛选功能

---

## 📞 联系方式

如有任何问题，请随时联系：
- **项目负责人**：[你的名字]
- **项目仓库**：[GitHub 链接]
- **当前网站**：https://gallery.songshgeo.com/


