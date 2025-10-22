# 测试指南

GPS 提取脚本的完整测试套件文档。

## 🧪 测试概览

- **55 个测试** - 100% 通过率
- **8 个测试类** - 覆盖所有核心功能
- **9 个 Fixtures** - 共享测试数据
- **4 个测试工具** - 辅助测试开发

## 🚀 快速开始

```bash
# 安装测试依赖
make install-dev

# 运行所有测试
make test

# 快速测试（无覆盖率）
make test-fast

# 查看覆盖率报告
make test-cov
```

## 📊 测试类别

### 1. GPS 数据提取 (`TestGPSExtraction`)

测试 GPS 数据从照片中的提取功能。

**测试项目:**
- GPS 覆盖率验证（0%, 50%, 100%）
- 多种图片格式支持（jpg, jpeg, heic）
- 异常 GPS 坐标处理
- 空文件夹处理

**边缘情况:**
- 无 GPS 数据
- 格式错误的坐标
- 缺失经纬度

### 2. 日期范围分析 (`TestDateRangeAnalysis`)

测试旅行日期分析和分组。

**测试项目:**
- 单日旅行
- 多日旅行
- 预期日期范围验证
- 日期解析边缘情况

### 3. 反向地理编码 (`TestReverseGeocoding`)

测试 GPS 坐标到城市名称的转换。

**测试项目:**
- 已知坐标查询
- 坐标缓存机制
- API 请求限速
- 城市名称标准化

### 4. GPX 文件生成 (`TestGPXGeneration`)

测试 GPX 轨迹文件创建。

**测试项目:**
- GPX 格式验证
- 轨迹点排序
- 元数据保留
- 大小限制测试（0-10000 点）

### 5. 位置验证 (`TestLocationValidation`)

测试位置数据完整性验证。

**测试项目:**
- 完整覆盖检测
- 部分覆盖检测
- 多城市同一天检测

### 6. 手动覆盖 (`TestDayOverrides`)

测试用户手动指定城市功能。

**测试项目:**
- 单日覆盖
- 多日覆盖
- 覆盖优先级

### 7. 边缘情况 (`TestEdgeCases`)

测试各种异常情况。

**测试项目:**
- 不存在的文件夹
- 无图片文件夹
- GPS 和非 GPS 混合
- 时区处理

### 8. 集成测试 (`TestIntegration`)

测试完整工作流程。

**测试项目:**
- 端到端流程
- 幂等性测试
- 并发执行测试

## 🛠️ 测试工具

### TestDataGenerator

生成测试数据：

```python
from tests.test_helpers import TestDataGenerator

gen = TestDataGenerator()

# 简单 GPS 数据
data = gen.create_gps_photo_data(num_photos=10, ...)

# 多日旅行
trip = gen.create_multi_day_trip(days=5, ...)

# 带缺口的旅行
gapped = gen.create_trip_with_gaps(total_days=7, ...)
```

### MockGeocoder

模拟地理编码 API：

```python
from tests.test_helpers import MockGeocoder

geocoder = MockGeocoder()
result = geocoder.reverse((62.01, -6.77))
# 返回: {'city': 'Tórshavn', 'country': 'Faroe Islands'}
```

### GPXValidator

验证 GPX 文件：

```python
from tests.test_helpers import GPXValidator

validator = GPXValidator()
valid, errors = validator.validate_structure(gpx_xml)
```

### OutputValidator

验证输出文件：

```python
from tests.test_helpers import OutputValidator

validator = OutputValidator()
valid, errors = validator.validate_summary_json(path)
```

## 📝 编写新测试

### 测试类结构

```python
class TestFeatureName:
    """测试功能描述。"""
    
    def test_basic_case(self):
        """
        测试基本功能。
        
        场景:
            - 描述测试场景
            
        预期:
            - 描述预期结果
        """
        # Arrange
        input_data = ...
        
        # Act
        result = function_to_test(input_data)
        
        # Assert
        assert result == expected_value
    
    @pytest.mark.parametrize("input,expected", [
        (1, 2),
        (2, 4),
    ])
    def test_multiple_cases(self, input, expected):
        """使用参数化测试多种情况。"""
        result = function_to_test(input)
        assert result == expected
```

## 🎯 运行特定测试

```bash
# 运行特定文件
pytest tests/test_gps_extraction.py

# 运行特定类
pytest tests/test_gps_extraction.py::TestGPSExtraction

# 运行特定方法
pytest tests/test_gps_extraction.py::TestGPSExtraction::test_gps_coverage_validation

# 按名称匹配
pytest -k "test_gps"

# 运行标记的测试
pytest -m unit              # 只运行单元测试
pytest -m "not slow"        # 跳过慢速测试
pytest -m "not network"     # 跳过网络测试
```

## 📊 覆盖率报告

```bash
# 终端报告
pytest --cov=scripts --cov-report=term

# HTML 报告
pytest --cov=scripts --cov-report=html
open htmlcov/index.html

# XML 报告（用于 CI/CD）
pytest --cov=scripts --cov-report=xml
```

## 🐛 调试测试

```bash
# 失败时进入调试器
pytest --pdb

# 显示 print 输出
pytest -s

# 详细失败信息
pytest --tb=long -l

# 只运行上次失败的测试
pytest --lf
```

## ✅ 最佳实践

### 文档

- ✅ 每个测试有清晰的 docstring
- ✅ 描述测试场景
- ✅ 说明预期结果
- ✅ 标注边缘情况

### 组织

- ✅ 每个功能一个测试类
- ✅ 相关测试分组
- ✅ 使用 fixtures 复用数据
- ✅ 使用 parametrize 测试多种情况

### 质量

- ✅ 测试独立性
- ✅ 测试可重复性
- ✅ 清晰的断言消息
- ✅ 适当的错误处理

## 🔄 CI/CD 集成

### GitHub Actions

测试在以下情况自动运行：
- 推送到 main/dev 分支
- Pull Request
- Python 3.9, 3.10, 3.11, 3.12

### 本地预检

```bash
# 提交前运行所有检查
pytest && \
black --check scripts/ tests/ && \
isort --check scripts/ tests/ && \
flake8 scripts/ tests/
```

## 📚 相关文档

- [测试快速开始](TESTING_QUICKSTART.md) - 5 分钟上手
- [测试总结](TESTING_SUMMARY.md) - 测试套件概览
- [工作流指南](WORKFLOW_CN.md) - 完整工作流程

---

**测试是代码质量的保证！** 定期运行 `make test` 确保代码健壮性。

