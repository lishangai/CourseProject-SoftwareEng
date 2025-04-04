# ConceptCraft

ConceptCraft是一个智能概念学习系统，旨在帮助用户更好地理解和掌握复杂概念。系统采用多种智能技术，提供个性化的学习体验。

## 功能特点

- 智能概念分析：深入解析概念的核心定义、原理和应用
- 多模态解释切换：提供文字、图表、代码等多种形式的解释
- 学习辅助：生成个性化学习路径和练习题
- 实践验证：通过案例分析和代码实践加深理解
- 差异化设计：根据用户水平提供不同深度的内容

## 技术栈

- 后端：Python Flask
- 前端：HTML5, CSS3, JavaScript
- AI：DeepSeek API
- 数据存储：Neo4j, Redis
- 可视化：Plotly, NetworkX

## 快速开始

1. 克隆项目
```bash
git clone https://github.com/yourusername/conceptcraft.git
cd conceptcraft
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
```bash
cp .env.example .env
# 编辑.env文件，填入必要的配置信息
```

4. 启动应用
```bash
flask run
```

5. 访问系统
打开浏览器访问 http://localhost:5000

## 项目结构

```
conceptcraft/
├── app/
│   ├── api/            # API接口
│   ├── services/       # 业务逻辑
│   ├── static/         # 静态资源
│   └── templates/      # 页面模板
├── tests/              # 测试文件
├── config.py           # 配置文件
├── requirements.txt    # 项目依赖
└── README.md          # 项目说明
```

## 主要功能模块

1. 概念解释
   - 核心定义提取
   - 费曼解释生成
   - 常见误解分析

2. 学习路径
   - 个性化学习计划
   - 进度追踪
   - 资源推荐

3. 知识图谱
   - 概念关联分析
   - 知识网络可视化
   - 学习路径规划

4. 记忆管理
   - 间隔复习提醒
   - 记忆强度分析
   - 学习效果评估

## 开发计划

- [ ] 用户认证系统
- [ ] 学习数据统计
- [ ] 社区讨论功能
- [ ] 移动端适配
- [ ] 离线学习模式

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

- 项目维护者：[Your Name]
- 邮箱：[your.email@example.com]
- 项目链接：[https://github.com/yourusername/conceptcraft](https://github.com/yourusername/conceptcraft) 