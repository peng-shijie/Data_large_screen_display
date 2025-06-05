# 项目简介

**Data_large_screen_display** 项目旨在通过结合 HTML 前端和 Python 后端并结合BI工具，实现数据可视化和大屏展示效果。该项目适用于数据大屏展示、监控面板、实时数据监控等场景。

## 项目结构

- `html/` 前端页面，使用 HTML/CSS/JavaScript 实现数据录入功能，为用户提供数据录入页面。
- `python/` 后端服务，负责数据的获取、处理与接口提供，将用户录入的数据存到数据库中。
- `BI/` 数据大屏展示。
- 其他文件和目录详见项目结构。

## 主要功能

- 实时数据采集/用户录入与展示
- 多种可视化图表（如折线图、柱状图、饼图等）
- 响应式页面布局，适配不同分辨率大屏
- 支持自定义数据源和展示模板

## 环境依赖

```python
# Python 依赖举例
flask
pandas
# 其他依赖请参考 requirements.txt
```

```mysql
mysql版本自行选择
```

```BI软件
BI软件可以自行选择，这里我使用的是免费开源的DataEase
```

## 快速开始

1. 克隆项目到本地：
   ```bash
   git clone https://github.com/shijiepeng/Data_large_screen_display.git
   ```
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 启动后端服务：
   ```bash
   python app.py
   ```
4. 安装mysql

5. 安装dataease

## 项目截图

（可在此处插入项目效果截图或 GIF 演示）

## 联系方式

- 作者：shijiepeng
- GitHub: [https://github.com/shijiepeng/Data_large_screen_display](https://github.com/shijiepeng/Data_large_screen_display)

---

如有建议或问题，欢迎提交 issue 或 pull request！
