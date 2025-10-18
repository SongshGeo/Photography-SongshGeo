# Testing Quick Start Guide

快速上手测试套件。

## 🚀 快速开始

### 1. 安装依赖

```bash
# 安装测试依赖
make install-dev

# 或者手动安装
pip3 install --user --break-system-packages -r requirements-dev.txt
```

### 2. 运行测试

```bash
# 最简单的方式
make test

# 或者直接用 pytest
pytest
```

## 📊 常用命令

### 基础测试

```bash
# 运行所有测试
pytest

# 详细输出
pytest -v

# 非常详细的输出
pytest -vv

# 显示 print 输出
pytest -s
```

### 覆盖率

```bash
# 生成覆盖率报告
make test

# 打开 HTML 报告
make test-cov

# 快速测试（无覆盖率）
make test-fast
```

### 筛选测试

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
pytest -m unit           # 只运行单元测试
pytest -m "not slow"     # 跳过慢速测试
pytest -m "not network"  # 跳过网络测试
```

### 调试

```bash
# 失败时进入调试器
pytest --pdb

# 显示完整的错误信息
pytest --tb=long

# 显示局部变量
pytest -l

# 只运行上次失败的测试
pytest --lf

# 先运行失败的，再运行其他
pytest --ff
```

### 并行执行

```bash
# 使用所有 CPU 核心
pytest -n auto

# 指定核心数
pytest -n 4
```

## 📝 写新测试

### 测试模板

```python
import pytest

class TestMyFeature:
    """Test my feature description."""
    
    def test_basic_case(self):
        """
        Test basic functionality.
        
        Scenario:
            - What we're testing
            
        Expected:
            - What should happen
        """
        # Arrange
        input_data = ...
        
        # Act
        result = function_to_test(input_data)
        
        # Assert
        assert result == expected
    
    @pytest.mark.parametrize("input,expected", [
        (1, 2),
        (2, 4),
    ])
    def test_multiple_cases(self, input, expected):
        """Test with parameters."""
        result = function_to_test(input)
        assert result == expected
    
    def test_edge_case(self):
        """
        Test edge case.
        
        Edge Case:
            - Describe special condition
        """
        assert True
```

### 使用 Fixture

```python
def test_with_fixture(sample_gps_data, temp_dir):
    """Use shared fixtures from conftest.py."""
    # sample_gps_data 已经准备好了
    assert len(sample_gps_data) > 0
    
    # temp_dir 是临时目录
    output = temp_dir / "output.txt"
    output.write_text("test")
```

## 🎯 测试策略

### 优先级

1. **核心功能** - 必须有测试
   - GPS 数据提取
   - GPX 生成
   - 位置验证

2. **边缘情况** - 应该有测试
   - 空输入
   - 无效数据
   - 缺失文件

3. **集成测试** - 可选但推荐
   - 完整工作流
   - 文件 I/O
   - API 交互

### 测试覆盖率目标

- **核心脚本**: >80%
- **辅助函数**: >70%
- **整体项目**: >75%

## 🔍 查看覆盖率

```bash
# 生成报告
pytest --cov=scripts --cov-report=term

# HTML 报告（推荐）
pytest --cov=scripts --cov-report=html
open htmlcov/index.html

# 只看未覆盖的行
pytest --cov=scripts --cov-report=term-missing
```

## 🐛 常见问题

### 导入错误

```bash
# 问题：ImportError: No module named 'scripts'
# 解决：确保在项目根目录运行
cd /path/to/Photography-SongshGeo
pytest
```

### 文件权限错误

```bash
# 问题：Permission denied
# 解决：使用 --user 安装
pip3 install --user --break-system-packages pytest
```

### 测试发现失败

```bash
# 问题：No tests found
# 解决：检查文件名是否以 test_ 开头
ls tests/test_*.py

# 或者使用完整路径
pytest tests/test_gps_extraction.py
```

## 📚 更多资源

- 详细文档: [`tests/README.md`](README.md)
- Pytest 文档: https://docs.pytest.org/
- 项目主 README: [`../README.md`](../README.md)

## ✅ 检查清单

在提交代码前：

- [ ] 所有测试通过: `pytest`
- [ ] 覆盖率 >75%: `pytest --cov`
- [ ] 代码格式化: `black scripts/ tests/`
- [ ] 导入排序: `isort scripts/ tests/`
- [ ] 没有 linting 错误: `flake8 scripts/ tests/`

快速检查：

```bash
# 一键运行所有检查
pytest && black --check scripts/ tests/ && isort --check scripts/ tests/ && flake8 scripts/ tests/
```

---

**快速开始完成！** 🎉

现在你可以：
1. `make test` - 运行测试
2. `make test-cov` - 查看覆盖率
3. 开始写新测试！

