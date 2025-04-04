from neo4j import GraphDatabase
from flask import current_app
import networkx as nx
import json

class KnowledgeGraphService:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            current_app.config['NEO4J_URI'],
            auth=(current_app.config['NEO4J_USER'], current_app.config['NEO4J_PASSWORD'])
        )
        self.max_related = current_app.config['MAX_RELATED_CONCEPTS']
        self.graph_depth = current_app.config['GRAPH_DEPTH']

    def get_concept_graph(self, concept):
        """获取概念的知识图谱"""
        try:
            with self.driver.session() as session:
                # 查询概念及其关联概念
                result = session.run("""
                    MATCH (c:Concept {name: $concept})-[r:RELATES_TO*1..2]-(related:Concept)
                    RETURN c, r, related
                    LIMIT $max_related
                """, concept=concept, max_related=self.max_related)
                
                # 构建NetworkX图
                G = nx.Graph()
                
                # 添加节点和边
                for record in result:
                    # 添加主概念节点
                    main_concept = record['c']
                    G.add_node(main_concept['name'], 
                             type='main',
                             description=main_concept.get('description', ''))
                    
                    # 添加关联概念节点和边
                    for rel in record['r']:
                        related = record['related']
                        G.add_node(related['name'],
                                 type='related',
                                 description=related.get('description', ''))
                        G.add_edge(main_concept['name'],
                                 related['name'],
                                 type=rel.type,
                                 weight=rel.get('weight', 1.0))
                
                # 转换为前端可用的格式
                return self._convert_to_frontend_format(G)
                
        except Exception as e:
            raise Exception(f"获取知识图谱失败: {str(e)}")

    def _convert_to_frontend_format(self, G):
        """将NetworkX图转换为前端可用的格式"""
        nodes = []
        edges = []
        
        for node in G.nodes(data=True):
            nodes.append({
                'id': node[0],
                'label': node[0],
                'type': node[1].get('type', 'unknown'),
                'description': node[1].get('description', '')
            })
        
        for edge in G.edges(data=True):
            edges.append({
                'from': edge[0],
                'to': edge[1],
                'type': edge[2].get('type', 'unknown'),
                'weight': edge[2].get('weight', 1.0)
            })
        
        return {
            'nodes': nodes,
            'edges': edges
        }

    def add_concept(self, concept, description, related_concepts=None):
        """添加新概念到知识图谱"""
        try:
            with self.driver.session() as session:
                # 创建主概念节点
                session.run("""
                    MERGE (c:Concept {name: $concept})
                    SET c.description = $description
                """, concept=concept, description=description)
                
                # 添加关联概念
                if related_concepts:
                    for related in related_concepts:
                        session.run("""
                            MATCH (c:Concept {name: $concept})
                            MERGE (r:Concept {name: $related})
                            MERGE (c)-[rel:RELATES_TO]->(r)
                            SET rel.weight = 1.0
                        """, concept=concept, related=related)
                        
        except Exception as e:
            raise Exception(f"添加概念失败: {str(e)}")

    def update_relationship(self, concept1, concept2, weight):
        """更新概念间的关系权重"""
        try:
            with self.driver.session() as session:
                session.run("""
                    MATCH (c1:Concept {name: $concept1})-[r:RELATES_TO]-(c2:Concept {name: $concept2})
                    SET r.weight = $weight
                """, concept1=concept1, concept2=concept2, weight=weight)
                
        except Exception as e:
            raise Exception(f"更新关系失败: {str(e)}")

    def get_related_concepts(self, concept, limit=5):
        """获取与概念最相关的其他概念"""
        try:
            with self.driver.session() as session:
                result = session.run("""
                    MATCH (c:Concept {name: $concept})-[r:RELATES_TO]-(related:Concept)
                    RETURN related.name as name, related.description as description, r.weight as weight
                    ORDER BY r.weight DESC
                    LIMIT $limit
                """, concept=concept, limit=limit)
                
                return [{
                    'name': record['name'],
                    'description': record['description'],
                    'weight': record['weight']
                } for record in result]
                
        except Exception as e:
            raise Exception(f"获取相关概念失败: {str(e)}")

    def __del__(self):
        """关闭数据库连接"""
        self.driver.close() 