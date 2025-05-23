# 智能研究助手 MCP 服务器

一个功能强大的Model Context Protocol (MCP)服务器，集成了三个协作代理（搜索、分析、合成）和RAG系统，为AI助手提供深度研究功能。

## 🌟 特性

### 核心功能
- **🔍 搜索代理**: 执行网络搜索，获取和处理文档内容
- **🔬 分析代理**: 分析内容相关性，提取关键信息和洞见
- **📝 合成代理**: 生成研究摘要，存储和检索研究结果
- **📚 知识库管理**: 本地文档处理和向量存储
- **🧠 RAG系统**: 检索增强生成，支持混合搜索和重排序

### 技术特色
- **多代理协作**: 三个专门代理协同工作，提供完整研究流程
- **灵活的向量存储**: 支持Qdrant云服务和本地文件存储
- **多种搜索引擎**: 支持Exa API、Brave Search和DuckDuckGo
- **高速推理**: 优先使用Groq API实现毫秒级响应
- **文档处理**: 支持PDF、Word、CSV、JSON、XML等多种格式
- **智能分块**: 自动文档分块和重叠处理
- **元数据过滤**: 支持基于分类、标签等的精确检索

## 🏗️ 架构设计

```
智能研究助手 MCP 服务器
├── 搜索代理 (Search Agent)
│   ├── 网络搜索 (Exa API / Brave Search / DuckDuckGo)
│   ├── 文档获取 (HTML/PDF/多格式处理)
│   └── 内容存储 (向量化存储)
├── 分析代理 (Analysis Agent)
│   ├── 相关性计算 (语义相似度)
│   ├── 洞见提取 (LLM驱动分析)
│   └── 信息结构化 (主题信息提取)
├── 合成代理 (Synthesis Agent)
│   ├── 摘要生成 (多来源内容整合)
│   ├── 研究存储 (持久化存储)
│   └── 相关性检索 (历史研究关联)
└── RAG系统 (Retrieval-Augmented Generation)
    ├── 向量存储 (Qdrant / 本地存储)
    ├── 混合检索 (语义+关键词)
    ├── 智能重排序 (相关性优化)
    └── 知识库管理 (文档生命周期)
```

## 🚀 快速开始

### 1. 环境准备

**Python版本要求**: Python 3.8+

```bash
# 克隆项目
git clone <repository-url>
cd intelligent-research-assistant

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 环境配置

复制环境变量模板并配置：

```bash
cp .env.example .env
```

编辑`.env`文件，配置必要的API密钥：

```env
# 必需的API密钥
OPENAI_API_KEY=your_openai_api_key_here
GROQ_API_KEY=your_groq_api_key_here          # 可选，用于高速推理
SEARCH_API_KEY=your_search_api_key_here      # Brave Search API
EXA_API_KEY=your_exa_api_key_here           # 可选，增强搜索

# 向量数据库配置（可选）
QDRANT_URL=https://your-cluster.qdrant.tech:6333
QDRANT_API_KEY=your_qdrant_api_key_here

# 本地存储路径
LOCAL_STORAGE_PATH=./data/vector_store
KB_INDEX_PATH=./data/knowledge_base_index.json
```

### 3. 运行演示测试

```bash
python demo_test.py
```

这将运行完整的功能演示，测试所有核心组件。

### 4. 启动MCP服务器

```bash
# 使用stdio传输（推荐用于Claude Desktop）
python src/main.py --transport stdio

# 或使用SSE传输（用于Web应用）
python src/main.py --transport sse --host 127.0.0.1 --port 8080
```

## 🔧 Claude Desktop集成

### 配置Claude Desktop

将以下配置添加到Claude Desktop的配置文件中：

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "intelligent-research-assistant": {
      "command": "python",
      "args": ["/path/to/project/src/main.py"],
      "env": {
        "TRANSPORT": "stdio",
        "OPENAI_API_KEY": "your_openai_api_key_here",
        "GROQ_API_KEY": "your_groq_api_key_here",
        "SEARCH_API_KEY": "your_search_api_key_here",
        "LOCAL_STORAGE_PATH": "./data/vector_store"
      }
    }
  }
}
```

重启Claude Desktop后，您将看到🔌图标，表示MCP服务器已连接。

## 🛠️ MCP工具说明

本服务器提供以下MCP工具：

### 搜索相关工具
- **`search_web`**: 在网络上搜索特定查询
- **`fetch_document`**: 获取并处理文档内容

### 分析相关工具
- **`analyze_content`**: 分析内容与查询的相关性
- **`extract_key_information`**: 从内容中提取关键信息

### 合成相关工具
- **`generate_research_summary`**: 生成研究摘要
- **`store_research`**: 存储研究结果
- **`related_research`**: 查找相关研究

## 📖 使用示例

### 基本研究流程

```python
# 1. 网络搜索
search_results = search_web("人工智能在医疗领域的应用", max_results=5)

# 2. 获取文档内容
document = fetch_document(search_results[0]["url"])

# 3. 分析内容
analysis = analyze_content(document["content"], "人工智能医疗应用")

# 4. 提取关键信息
key_info = extract_key_information(
    document["content"], 
    ["诊断", "治疗", "药物发现"]
)

# 5. 生成研究摘要
summary = generate_research_summary(
    "人工智能在医疗领域的应用", 
    [{"content": document["content"], "url": document["url"]}]
)

# 6. 存储研究结果
store_research("人工智能医疗应用", summary)

# 7. 查找相关研究
related = related_research("AI医疗技术", limit=3)
```

### 高级功能

```python
# 混合检索（语义+关键词）
results = retriever.retrieve_hybrid(
    query="区块链供应链管理",
    namespaces=["research_results", "documents"],
    top_k=5
)

# 元数据过滤搜索
filtered_results = retriever.retrieve_with_metadata_filter(
    query="机器学习算法",
    filter_dict={"category": "technology", "tags": ["ML"]},
    top_k=3
)

# 知识库管理
kb_result = knowledge_base.add_document(
    file_path="./research_paper.pdf",
    category="academic",
    tags=["深度学习", "计算机视觉"]
)
```

## 🎯 适用场景

### 学术研究
- 文献调研和综述撰写
- 跨领域知识整合
- 研究趋势分析

### 商业分析
- 市场调研和竞品分析
- 行业报告生成
- 技术方案评估

### 内容创作
- 深度文章写作
- 多源信息整合
- 事实核查和验证

### 知识管理
- 企业知识库构建
- 文档智能分类
- 历史信息检索

## 🔍 项目结构

```
intelligent-research-assistant/
├── src/                          # 源代码目录
│   ├── __init__.py
│   ├── main.py                   # 主入口文件
│   ├── mcp_server.py            # MCP服务器实现
│   ├── agents/                   # 代理模块
│   │   ├── search_agent.py      # 搜索代理
│   │   ├── analysis_agent.py    # 分析代理
│   │   └── synthesis_agent.py   # 合成代理
│   ├── rag/                     # RAG系统
│   │   ├── vector_store.py      # 向量存储
│   │   ├── embedding.py         # 嵌入处理
│   │   └── retrieval.py         # 检索逻辑
│   └── tools/                   # 工具模块
│       ├── web_search.py        # 网络搜索
│       ├── document_processor.py # 文档处理
│       └── knowledge_base.py    # 知识库管理
├── tests/                       # 测试目录
├── data/                        # 数据存储目录
├── demo_test.py                 # 演示测试脚本
├── requirements.txt             # 项目依赖
├── .env.example                 # 环境变量示例
└── README.md                    # 项目文档
```

## ⚙️ 配置选项

### 环境变量

| 变量名 | 描述 | 默认值 | 必需 |
|--------|------|--------|------|
| `OPENAI_API_KEY` | OpenAI API密钥 | - | ✅ |
| `GROQ_API_KEY` | Groq API密钥 | - | ❌ |
| `SEARCH_API_KEY` | 搜索API密钥 | - | ❌ |
| `EXA_API_KEY` | Exa API密钥 | - | ❌ |
| `QDRANT_URL` | Qdrant服务URL | - | ❌ |
| `QDRANT_API_KEY` | Qdrant API密钥 | - | ❌ |
| `LOCAL_STORAGE_PATH` | 本地存储路径 | `./data/vector_store` | ❌ |
| `HOST` | 服务器主机 | `127.0.0.1` | ❌ |
| `PORT` | 服务器端口 | `8080` | ❌ |
| `TRANSPORT` | 传输协议 | `stdio` | ❌ |

### 性能优化

- **嵌入模型**: 默认使用`text-embedding-3-small`，可在环境变量中修改
- **分块大小**: 默认1000字符，重叠200字符
- **并发限制**: 默认最大10个并发请求
- **缓存**: 支持工具列表缓存和结果缓存

## 🔨 开发指南

### 添加新的代理

1. 在`src/agents/`目录创建新代理文件
2. 继承基础代理类（如果有）
3. 实现必要的方法
4. 在`mcp_server.py`中注册新工具

### 扩展搜索引擎

1. 在`src/tools/web_search.py`中添加新的搜索函数
2. 更新`perform_web_search`函数的逻辑
3. 添加相应的环境变量配置

### 支持新的文档格式

1. 在`src/tools/document_processor.py`中添加处理函数
2. 更新`process_document`函数的分发逻辑
3. 添加必要的依赖库

## 🐛 故障排除

### 常见问题

**Q: MCP服务器无法连接**
- 检查API密钥是否正确设置
- 确保Python路径和依赖正确
- 查看Claude Desktop日志

**Q: 搜索功能不工作**
- 验证搜索API密钥
- 检查网络连接
- 尝试不同的搜索引擎

**Q: 向量存储错误**
- 检查Qdrant配置
- 确保本地存储目录权限
- 验证嵌入API密钥

**Q: 文档处理失败**
- 检查文件格式支持
- 安装额外的处理库
- 验证文件权限

### 调试技巧

1. 启用调试模式：设置`DEBUG_MODE=true`
2. 查看详细日志：设置`LOG_LEVEL=DEBUG`
3. 使用演示测试：运行`python demo_test.py`
4. 检查MCP连接：查看Claude Desktop的🔌图标

## 🤝 贡献指南

1. Fork项目仓库
2. 创建功能分支：`git checkout -b feature/new-feature`
3. 提交更改：`git commit -am 'Add new feature'`
4. 推送分支：`git push origin feature/new-feature`
5. 创建Pull Request

## 📄 许可证

本项目采用MIT许可证。详见[LICENSE](LICENSE)文件。

## 🙏 致谢

- [Anthropic](https://anthropic.com) - Model Context Protocol
- [OpenAI](https://openai.com) - 嵌入和语言模型
- [Groq](https://groq.com) - 高速推理引擎
- [Qdrant](https://qdrant.tech) - 向量数据库
- 开源社区的所有贡献者

## 📞 支持

如有问题或建议，请：
1. 查看[常见问题](#故障排除)
2. 提交[Issue](../../issues)
3. 参与[讨论](../../discussions)

---

**智能研究助手 MCP 服务器** - 让AI研究更智能、更高效！ 🚀