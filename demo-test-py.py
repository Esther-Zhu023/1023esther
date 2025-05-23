#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
智能研究助手 MCP 服务器演示测试脚本

这个脚本演示了如何使用智能研究助手的各种功能，包括：
1. 网络搜索
2. 文档获取和分析
3. 研究摘要生成
4. 知识库管理
5. 相关研究检索

运行方法:
python demo_test.py
"""

import os
import sys
import json
import time
import asyncio
from pathlib import Path
from typing import Dict, List, Any

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.mcp_server import ResearchAssistantMCPServer
from src.rag.vector_store import VectorStore
from src.agents.search_agent import SearchAgent
from src.agents.analysis_agent import AnalysisAgent
from src.agents.synthesis_agent import SynthesisAgent
from src.tools.knowledge_base import KnowledgeBase

# 设置环境变量（用于演示）
os.environ.setdefault("OPENAI_API_KEY", "your_openai_api_key_here")
os.environ.setdefault("GROQ_API_KEY", "your_groq_api_key_here")
os.environ.setdefault("SEARCH_API_KEY", "your_search_api_key_here")
os.environ.setdefault("LOCAL_STORAGE_PATH", "./demo_data/vector_store")
os.environ.setdefault("KB_INDEX_PATH", "./demo_data/knowledge_base_index.json")

class DemoTestRunner:
    """演示测试运行器"""
    
    def __init__(self):
        """初始化测试运行器"""
        print("🚀 初始化智能研究助手演示测试...")
        
        # 创建演示数据目录
        os.makedirs("./demo_data/vector_store", exist_ok=True)
        os.makedirs("./demo_data/logs", exist_ok=True)
        
        # 初始化组件
        self.vector_store = VectorStore()
        self.search_agent = SearchAgent(self.vector_store)
        self.analysis_agent = AnalysisAgent(self.vector_store)
        self.synthesis_agent = SynthesisAgent(self.vector_store)
        self.knowledge_base = KnowledgeBase(self.vector_store)
        
        print("✅ 初始化完成！")
    
    def run_all_tests(self):
        """运行所有演示测试"""
        print("\n" + "="*60)
        print("🧪 开始智能研究助手功能演示测试")
        print("="*60)
        
        # 测试列表
        tests = [
            ("搜索代理测试", self.test_search_agent),
            ("分析代理测试", self.test_analysis_agent),
            ("合成代理测试", self.test_synthesis_agent),
            ("知识库测试", self.test_knowledge_base),
            ("完整研究流程测试", self.test_complete_research_workflow)
        ]
        
        results = []
        
        for test_name, test_func in tests:
            print(f"\n📋 {test_name}")
            print("-" * 40)
            
            try:
                start_time = time.time()
                result = test_func()
                end_time = time.time()
                
                print(f"✅ {test_name} 完成 (耗时: {end_time - start_time:.2f}秒)")
                results.append({"test": test_name, "status": "success", "time": end_time - start_time})
                
            except Exception as e:
                print(f"❌ {test_name} 失败: {e}")
                results.append({"test": test_name, "status": "failed", "error": str(e)})
        
        # 显示测试结果摘要
        self.show_test_summary(results)
    
    def test_search_agent(self):
        """测试搜索代理"""
        print("🔍 测试网络搜索功能...")
        
        # 测试查询
        query = "人工智能在医疗领域的应用"
        
        # 执行搜索
        search_results = self.search_agent.search_web(query, max_results=3)
        
        print(f"搜索查询: {query}")
        print(f"找到 {len(search_results)} 条结果:")
        
        for i, result in enumerate(search_results, 1):
            print(f"  {i}. {result.get('title', '无标题')}")
            print(f"     URL: {result.get('url', '无URL')}")
            print(f"     摘要: {result.get('snippet', '无摘要')[:100]}...")
        
        # 测试文档获取
        if search_results:
            print(f"\n📄 测试文档获取功能...")
            first_url = search_results[0].get('url')
            if first_url:
                try:
                    document = self.search_agent.fetch_document(first_url)
                    print(f"成功获取文档: {first_url}")
                    print(f"内容长度: {len(document.get('content', ''))}")
                    print(f"内容预览: {document.get('content', '')[:200]}...")
                except Exception as e:
                    print(f"文档获取失败: {e}")
        
        return {"search_results": len(search_results)}
    
    def test_analysis_agent(self):
        """测试分析代理"""
        print("🔬 测试内容分析功能...")
        
        # 测试内容
        test_content = """
        人工智能（AI）在医疗领域的应用正在快速发展。主要应用包括：
        1. 医学影像诊断：AI可以帮助医生更准确地识别X光、CT和MRI图像中的异常。
        2. 药物发现：机器学习算法可以加速新药的发现和开发过程。
        3. 个性化治疗：AI可以根据患者的基因信息和医疗历史提供个性化的治疗方案。
        4. 预测性医疗：通过分析大量医疗数据，AI可以预测疾病的发生和进展。
        5. 智能诊断：AI助手可以帮助医生进行初步诊断和治疗建议。
        """
        
        query = "人工智能在医疗领域的应用"
        
        # 执行内容分析
        analysis_result = self.analysis_agent.analyze_content(test_content, query)
        
        print(f"分析查询: {query}")
        print(f"相关性分数: {analysis_result.get('relevance', 0):.2f}")
        print(f"推理: {analysis_result.get('reasoning', '无推理')}")
        
        insights = analysis_result.get('insights', [])
        print(f"提取的洞见 ({len(insights)}条):")
        for i, insight in enumerate(insights, 1):
            print(f"  {i}. {insight}")
        
        # 测试关键信息提取
        print(f"\n🔑 测试关键信息提取...")
        topics = ["医学影像", "药物发现", "个性化治疗"]
        key_info = self.analysis_agent.extract_key_information(test_content, topics)
        
        print("提取的关键信息:")
        for topic, info_points in key_info.items():
            print(f"  {topic}:")
            for point in info_points:
                print(f"    - {point}")
        
        return {"relevance": analysis_result.get('relevance', 0), "insights": len(insights)}
    
    def test_synthesis_agent(self):
        """测试合成代理"""
        print("📝 测试研究摘要生成功能...")
        
        # 模拟研究发现
        findings = [
            {
                "title": "AI在医学影像诊断中的应用",
                "content": "人工智能在医学影像诊断中展现出巨大潜力，特别是在X光、CT和MRI图像的分析方面。",
                "url": "https://example.com/ai-medical-imaging"
            },
            {
                "title": "机器学习加速药物发现",
                "content": "机器学习算法正在革命性地改变药物发现过程，显著缩短新药开发周期。",
                "url": "https://example.com/ml-drug-discovery"
            },
            {
                "title": "个性化医疗的AI应用",
                "content": "基于AI的个性化医疗正在成为现实，通过分析患者的基因和医疗历史提供定制化治疗。",
                "url": "https://example.com/ai-personalized-medicine"
            }
        ]
        
        query = "人工智能在医疗领域的应用现状"
        
        # 生成研究摘要
        summary_result = self.synthesis_agent.generate_research_summary(query, findings)
        
        print(f"研究查询: {query}")
        print(f"研究ID: {summary_result.get('research_id', '无ID')}")
        print(f"摘要:\n{summary_result.get('summary', '无摘要')}")
        
        key_points = summary_result.get('key_points', [])
        print(f"\n关键点 ({len(key_points)}条):")
        for i, point in enumerate(key_points, 1):
            print(f"  {i}. {point}")
        
        sources = summary_result.get('sources', [])
        print(f"\n来源 ({len(sources)}条):")
        for i, source in enumerate(sources, 1):
            print(f"  {i}. {source.get('title', '无标题')} - {source.get('url', '无URL')}")
        
        # 测试研究存储
        print(f"\n💾 测试研究结果存储...")
        store_result = self.synthesis_agent.store_research(query, summary_result)
        
        if store_result.get('success'):
            print(f"研究结果已存储，ID: {store_result.get('research_id')}")
        else:
            print(f"存储失败: {store_result.get('error')}")
        
        # 测试相关研究查找
        print(f"\n🔍 测试相关研究查找...")
        related_query = "AI医疗应用"
        related_research = self.synthesis_agent.find_related_research(related_query, limit=2)
        
        print(f"相关研究查询: {related_query}")
        print(f"找到 {len(related_research)} 条相关研究:")
        for i, research in enumerate(related_research, 1):
            print(f"  {i}. {research.get('query', '无查询')}")
            print(f"     相关性分数: {research.get('relevance_score', 0)}")
        
        return {"summary_length": len(summary_result.get('summary', '')), "key_points": len(key_points)}
    
    def test_knowledge_base(self):
        """测试知识库功能"""
        print("📚 测试知识库管理功能...")
        
        # 测试添加文本内容
        print("📝 测试添加文本内容...")
        test_content = """
        深度学习是机器学习的一个子领域，它模仿人脑神经网络的结构和功能。
        深度学习使用多层神经网络来学习数据的高级特征表示。
        
        主要特点：
        1. 多层结构：使用多个隐藏层来提取复杂特征
        2. 自动特征学习：无需手动设计特征，可以自动学习
        3. 大数据处理：能够处理大规模数据集
        4. 强大的表示能力：可以学习复杂的非线性关系
        
        应用领域：
        - 计算机视觉：图像识别、物体检测
        - 自然语言处理：机器翻译、文本分类
        - 语音识别：语音转文本、语音合成
        - 推荐系统：个性化推荐、内容过滤
        """
        
        add_result = self.knowledge_base.add_text_content(
            content=test_content,
            title="深度学习基础知识",
            category="machine_learning",
            tags=["深度学习", "神经网络", "人工智能"]
        )
        
        if add_result.get('success'):
            print(f"✅ 成功添加文本内容，文档ID: {add_result.get('doc_id')}")
            print(f"   分块数量: {add_result.get('chunk_count')}")
        else:
            print(f"❌ 添加文本内容失败: {add_result.get('error')}")
        
        # 测试知识库搜索
        print(f"\n🔍 测试知识库搜索...")
        search_results = self.knowledge_base.search_knowledge("深度学习的应用", top_k=3)
        
        print(f"搜索查询: 深度学习的应用")
        print(f"找到 {len(search_results)} 条结果:")
        for i, result in enumerate(search_results, 1):
            print(f"  {i}. 相关性分数: {result.score:.3f}")
            print(f"     内容预览: {result.page_content[:100]}...")
            print(f"     分类: {result.metadata.get('category', '未知')}")
            print(f"     标签: {result.metadata.get('tags', [])}")
        
        # 测试列出文档
        print(f"\n📋 测试文档列表...")
        documents = self.knowledge_base.list_documents()
        
        print(f"知识库中的文档 ({len(documents)}条):")
        for i, doc in enumerate(documents, 1):
            print(f"  {i}. {doc.get('title', '无标题')}")
            print(f"     分类: {doc.get('category', '未知')}")
            print(f"     标签: {doc.get('tags', [])}")
            print(f"     块数: {doc.get('chunk_count', 0)}")
        
        # 测试获取统计信息
        print(f"\n📊 测试统计信息...")
        stats = self.knowledge_base.get_statistics()
        
        print("知识库统计信息:")
        print(f"  总文档数: {stats.get('total_documents', 0)}")
        print(f"  总块数: {stats.get('total_chunks', 0)}")
        print(f"  总内容长度: {stats.get('total_content_length', 0)}")
        print(f"  分类: {stats.get('categories', {})}")
        print(f"  标签数: {stats.get('unique_tags', 0)}")
        
        return {"documents": len(documents), "search_results": len(search_results)}
    
    def test_complete_research_workflow(self):
        """测试完整的研究工作流程"""
        print("🔄 测试完整研究工作流程...")
        
        # 1. 定义研究主题
        research_topic = "区块链技术在供应链管理中的应用"
        print(f"研究主题: {research_topic}")
        
        # 2. 执行网络搜索
        print(f"\n🔍 步骤1: 网络搜索...")
        search_results = self.search_agent.search_web(research_topic, max_results=3)
        print(f"找到 {len(search_results)} 条搜索结果")
        
        # 3. 获取和分析文档
        print(f"\n📄 步骤2: 文档获取和分析...")
        analyzed_findings = []
        
        for i, result in enumerate(search_results[:2]):  # 只处理前2个结果以节省时间
            print(f"  处理结果 {i+1}: {result.get('title', '无标题')}")
            
            # 模拟文档内容（在真实环境中会获取实际内容）
            mock_content = f"""
            {result.get('title', '')}
            
            {result.get('snippet', '')}
            
            区块链技术为供应链管理提供了透明度、可追溯性和安全性。
            通过分布式账本技术，企业可以实时跟踪产品从原材料到最终消费者的整个流程。
            主要优势包括：减少欺诈、提高效率、降低成本、增强信任。
            """
            
            # 分析内容
            analysis = self.analysis_agent.analyze_content(mock_content, research_topic)
            
            finding = {
                "title": result.get('title', ''),
                "url": result.get('url', ''),
                "content": mock_content,
                "analysis": analysis,
                "relevance": analysis.get('relevance', 0)
            }
            
            analyzed_findings.append(finding)
            print(f"    相关性分数: {analysis.get('relevance', 0):.2f}")
        
        # 4. 生成研究摘要
        print(f"\n📝 步骤3: 生成研究摘要...")
        summary_result = self.synthesis_agent.generate_research_summary(
            research_topic, analyzed_findings
        )
        
        print(f"研究摘要已生成:")
        print(f"  摘要长度: {len(summary_result.get('summary', ''))}")
        print(f"  关键点数量: {len(summary_result.get('key_points', []))}")
        print(f"  来源数量: {len(summary_result.get('sources', []))}")
        
        # 显示摘要内容
        if summary_result.get('summary'):
            print(f"\n摘要内容:")
            print(summary_result['summary'][:300] + "..." if len(summary_result['summary']) > 300 else summary_result['summary'])
        
        # 5. 存储研究结果
        print(f"\n💾 步骤4: 存储研究结果...")
        store_result = self.synthesis_agent.store_research(research_topic, summary_result)
        
        if store_result.get('success'):
            print(f"✅ 研究结果已存储，ID: {store_result.get('research_id')}")
        else:
            print(f"❌ 存储失败: {store_result.get('error')}")
        
        # 6. 添加到知识库
        print(f"\n📚 步骤5: 添加到知识库...")
        kb_result = self.knowledge_base.add_text_content(
            content=summary_result.get('summary', ''),
            title=f"研究报告: {research_topic}",
            category="research_report",
            tags=["区块链", "供应链", "研究报告"],
            source="research_workflow"
        )
        
        if kb_result.get('success'):
            print(f"✅ 研究报告已添加到知识库，文档ID: {kb_result.get('doc_id')}")
        else:
            print(f"❌ 添加到知识库失败: {kb_result.get('error')}")
        
        # 7. 查找相关研究
        print(f"\n🔗 步骤6: 查找相关研究...")
        related_research = self.synthesis_agent.find_related_research("区块链供应链", limit=2)
        
        print(f"找到 {len(related_research)} 条相关研究:")
        for i, research in enumerate(related_research, 1):
            print(f"  {i}. {research.get('query', '无查询')}")
            if research.get('relevance_score'):
                print(f"     相关性: {research.get('relevance_score'):.2f}")
        
        return {
            "search_results": len(search_results),
            "analyzed_findings": len(analyzed_findings),
            "summary_generated": bool(summary_result.get('summary')),
            "stored_successfully": store_result.get('success', False),
            "added_to_kb": kb_result.get('success', False)
        }
    
    def show_test_summary(self, results: List[Dict[str, Any]]):
        """显示测试结果摘要"""
        print("\n" + "="*60)
        print("📊 测试结果摘要")
        print("="*60)
        
        total_tests = len(results)
        successful_tests = sum(1 for r in results if r["status"] == "success")
        failed_tests = total_tests - successful_tests
        total_time = sum(r.get("time", 0) for r in results if "time" in r)
        
        print(f"总测试数: {total_tests}")
        print(f"成功: {successful_tests} ✅")
        print(f"失败: {failed_tests} ❌")
        print(f"成功率: {(successful_tests/total_tests*100):.1f}%")
        print(f"总耗时: {total_time:.2f}秒")
        
        print(f"\n详细结果:")
        for result in results:
            status_icon = "✅" if result["status"] == "success" else "❌"
            test_name = result["test"]
            
            if result["status"] == "success":
                time_info = f" ({result.get('time', 0):.2f}s)" if "time" in result else ""
                print(f"  {status_icon} {test_name}{time_info}")
            else:
                error_info = result.get("error", "未知错误")
                print(f"  {status_icon} {test_name} - {error_info}")
        
        # 显示性能建议
        if total_time > 30:
            print(f"\n💡 性能建议:")
            print(f"   测试耗时较长，建议检查API响应速度和网络连接")
        
        if failed_tests > 0:
            print(f"\n🔧 故障排除建议:")
            print(f"   1. 检查API密钥是否正确设置")
            print(f"   2. 确保网络连接正常")
            print(f"   3. 检查依赖库是否正确安装")
            print(f"   4. 查看详细错误日志")
    
    def create_sample_mcp_config(self):
        """创建示例MCP配置文件"""
        print("\n📄 创建示例MCP配置文件...")
        
        config = {
            "mcpServers": {
                "intelligent-research-assistant": {
                    "command": "python",
                    "args": [str(project_root / "src" / "main.py")],
                    "env": {
                        "TRANSPORT": "stdio",
                        "OPENAI_API_KEY": "your_openai_api_key_here",
                        "GROQ_API_KEY": "your_groq_api_key_here",
                        "SEARCH_API_KEY": "your_search_api_key_here",
                        "EXA_API_KEY": "your_exa_api_key_here",
                        "LOCAL_STORAGE_PATH": "./data/vector_store",
                        "KB_INDEX_PATH": "./data/knowledge_base_index.json"
                    }
                }
            }
        }
        
        config_path = project_root / "claude_desktop_config_example.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ MCP配置文件已创建: {config_path}")
        print(f"   将此配置添加到Claude Desktop配置文件中以使用MCP服务器")
        
        return str(config_path)


def main():
    """主函数"""
    print("🎯 智能研究助手 MCP 服务器演示")
    print("=" * 60)
    
    try:
        # 检查基本环境
        print("🔧 检查运行环境...")
        
        # 检查Python版本
        if sys.version_info < (3, 8):
            print("❌ 需要Python 3.8或更高版本")
            return
        
        print(f"✅ Python版本: {sys.version}")
        
        # 检查必要的目录
        required_dirs = ["src", "src/agents", "src/rag", "src/tools"]
        for dir_path in required_dirs:
            full_path = project_root / dir_path
            if not full_path.exists():
                print(f"❌ 缺少必要目录: {dir_path}")
                return
        
        print("✅ 目录结构检查通过")
        
        # 创建演示运行器
        demo_runner = DemoTestRunner()
        
        # 运行所有测试
        demo_runner.run_all_tests()
        
        # 创建示例配置文件
        demo_runner.create_sample_mcp_config()
        
        print(f"\n🎉 演示测试完成！")
        print(f"如需在生产环境中使用，请：")
        print(f"1. 设置正确的API密钥在.env文件中")
        print(f"2. 安装所有依赖: pip install -r requirements.txt")
        print(f"3. 配置Claude Desktop以使用此MCP服务器")
        print(f"4. 运行: python src/main.py")
        
    except KeyboardInterrupt:
        print(f"\n⏹️  演示测试被用户中断")
    except Exception as e:
        print(f"\n❌ 演示测试出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()