import asyncio
import json
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from open_webui.retrieval.utils import query_doc_with_hybrid_search
from open_webui.retrieval.web.perplexity import search_perplexity
from open_webui.utils.chat import generate_chat_completion
from open_webui.env import SRC_LOG_LEVELS

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["RAG"])

@dataclass
class ResearchResult:
    source: str  # "perplexity" or "local_rag"
    content: str
    sources: List[Dict[str, Any]]
    confidence: float
    metadata: Dict[str, Any]

@dataclass
class DeepResearchConfig:
    primary_model: str
    secondary_model: str
    synthesis_model: str
    max_iterations: int
    rag_top_k: int
    perplexity_api_key: str
    perplexity_model: str
    perplexity_context_usage: str

class DeepResearchAgent:
    def __init__(self, config: DeepResearchConfig):
        self.config = config
        
    async def generate_research_queries(self, query: str, request, user) -> List[str]:
        """Generate multiple research queries for comprehensive coverage."""
        
        research_prompt = f"""Based on the user's question, generate 3-5 research queries that will provide comprehensive coverage of the topic. Consider:
1. Different aspects and perspectives
2. Recent developments and trends  
3. Expert opinions and analysis
4. Statistical data and studies
5. Historical context

User question: {query}

Return as JSON: {{"queries": ["query1", "query2", ...]}}"""

        try:
            res = await generate_chat_completion(
                request,
                {
                    "model": self.config.primary_model,
                    "messages": [{"role": "user", "content": research_prompt}],
                    "stream": False,
                },
                user,
                bypass_filter=True
            )
            
            response = res["choices"][0]["message"]["content"]
            
            # Extract JSON from response
            bracket_start = response.find("{")
            bracket_end = response.rfind("}") + 1
            
            if bracket_start != -1 and bracket_end != -1:
                response = response[bracket_start:bracket_end]
                queries_data = json.loads(response)
                return queries_data.get("queries", [query])
            else:
                return [query]
                
        except Exception as e:
            log.error(f"Error generating research queries: {e}")
            return [query]

    async def perplexity_research(self, queries: List[str], request) -> ResearchResult:
        """Perform Perplexity web search research."""
        
        all_results = []
        all_sources = []
        
        for query in queries:
            try:
                results = search_perplexity(
                    api_key=self.config.perplexity_api_key,
                    query=query,
                    count=3,
                    model=self.config.perplexity_model,
                    search_context_usage=self.config.perplexity_context_usage
                )
                
                for result in results:
                    all_results.append(result.snippet or "")
                    all_sources.append({
                        "url": result.link,
                        "title": result.title or "Perplexity Source",
                        "snippet": result.snippet or "",
                        "source_type": "web"
                    })
                    
            except Exception as e:
                log.error(f"Error in Perplexity research: {e}")
        
        content = "\n\n".join(all_results)
        
        return ResearchResult(
            source="perplexity",
            content=content,
            sources=all_sources,
            confidence=0.8,  # Perplexity is generally reliable
            metadata={"queries": queries, "result_count": len(all_results)}
        )

    async def local_rag_research(self, queries: List[str], request, user) -> ResearchResult:
        """Perform local RAG research on embedded data."""
        
        all_results = []
        all_sources = []
        
        # Get all available collections
        try:
            collections = request.app.state.VECTOR_DB_CLIENT.list_collections()
            collection_names = [col.name for col in collections]
        except Exception as e:
            log.error(f"Error getting collections: {e}")
            collection_names = []
        
        for query in queries:
            for collection_name in collection_names:
                try:
                    # Use hybrid search for better results
                    results = query_doc_with_hybrid_search(
                        collection_name=collection_name,
                        collection_result=request.app.state.VECTOR_DB_CLIENT.get_collection(collection_name),
                        query=query,
                        embedding_function=lambda q, prefix: request.app.state.EMBEDDING_FUNCTION(q, prefix=prefix, user=user),
                        k=self.config.rag_top_k,
                        reranking_function=request.app.state.RERANKING_FUNCTION,
                        k_reranker=5,
                        r=0.7,
                        hybrid_bm25_weight=0.5
                    )
                    
                    for doc, metadata in zip(results["documents"], results["metadatas"]):
                        all_results.append(doc)
                        all_sources.append({
                            "collection": collection_name,
                            "metadata": metadata,
                            "source_type": "local_rag"
                        })
                        
                except Exception as e:
                    log.error(f"Error in local RAG research: {e}")
        
        content = "\n\n".join(all_results)
        
        return ResearchResult(
            source="local_rag", 
            content=content,
            sources=all_sources,
            confidence=0.9,  # Local data is highly reliable
            metadata={"queries": queries, "collections": collection_names, "result_count": len(all_results)}
        )

    async def agentic_analysis(self, research_results: List[ResearchResult], original_query: str, request, user) -> str:
        """Perform agentic analysis where models discuss and refine the research."""
        
        # Prepare context for agentic discussion
        context = f"Original Query: {original_query}\n\n"
        
        for i, result in enumerate(research_results):
            context += f"Research Source {i+1} ({result.source}):\n{result.content[:1000]}...\n\n"
        
        # Agent 1: Primary analysis
        agent1_prompt = f"""You are a research analyst. Analyze the provided research and provide your findings.

{context}

Provide a comprehensive analysis focusing on:
1. Key findings and insights
2. Data quality and reliability
3. Gaps or missing information
4. Contradictions or inconsistencies

Your Analysis:"""

        try:
            agent1_response = await generate_chat_completion(
                request,
                {
                    "model": self.config.primary_model,
                    "messages": [{"role": "user", "content": agent1_prompt}],
                    "stream": False,
                },
                user,
                bypass_filter=True
            )
            
            agent1_analysis = agent1_response["choices"][0]["message"]["content"]
            
        except Exception as e:
            log.error(f"Error in agent1 analysis: {e}")
            agent1_analysis = "Primary analysis failed."
        
        # Agent 2: Critical review
        agent2_prompt = f"""You are a critical reviewer. Review the primary analysis and provide your assessment.

Original Query: {original_query}

Primary Analysis:
{agent1_analysis}

Provide your critical review focusing on:
1. Accuracy of the analysis
2. Missing perspectives
3. Potential biases
4. Recommendations for improvement

Your Critical Review:"""

        try:
            agent2_response = await generate_chat_completion(
                request,
                {
                    "model": self.config.secondary_model,
                    "messages": [{"role": "user", "content": agent2_prompt}],
                    "stream": False,
                },
                user,
                bypass_filter=True
            )
            
            agent2_review = agent2_response["choices"][0]["message"]["content"]
            
        except Exception as e:
            log.error(f"Error in agent2 analysis: {e}")
            agent2_review = "Critical review failed."
        
        return f"Primary Analysis:\n{agent1_analysis}\n\nCritical Review:\n{agent2_review}"

    async def synthesize_results(self, research_results: List[ResearchResult], agentic_analysis: str, original_query: str, request, user) -> Dict[str, Any]:
        """Synthesize all research results into a final answer."""
        
        synthesis_prompt = f"""You are a research synthesis expert. Combine all research findings into a comprehensive, well-structured answer.

Original Query: {original_query}

Research Results:
{agentic_analysis}

Additional Research Sources:
{chr(10).join([f"Source: {r.source} - {r.content[:500]}..." for r in research_results])}

Provide a final synthesized answer that:
1. Directly addresses the original query
2. Integrates insights from all sources
3. Highlights key findings and evidence
4. Acknowledges limitations or uncertainties
5. Provides clear, actionable information

Final Answer:"""

        try:
            synthesis_response = await generate_chat_completion(
                request,
                {
                    "model": self.config.synthesis_model,
                    "messages": [{"role": "user", "content": synthesis_prompt}],
                    "stream": False,
                },
                user,
                bypass_filter=True
            )
            
            final_answer = synthesis_response["choices"][0]["message"]["content"]
            
        except Exception as e:
            log.error(f"Error in synthesis: {e}")
            final_answer = "Synthesis failed."
        
        # Collect all sources
        all_sources = []
        for result in research_results:
            all_sources.extend(result.sources)
        
        return {
            "answer": final_answer,
            "sources": all_sources,
            "research_metadata": {
                "perplexity_results": len([r for r in research_results if r.source == "perplexity"]),
                "local_rag_results": len([r for r in research_results if r.source == "local_rag"]),
                "total_sources": len(all_sources)
            }
        }

    async def conduct_deep_research(self, query: str, request, user) -> Dict[str, Any]:
        """Main deep research orchestration method."""
        
        # Step 1: Generate research queries
        research_queries = await self.generate_research_queries(query, request, user)
        
        # Step 2: Parallel research execution
        perplexity_task = self.perplexity_research(research_queries, request)
        local_rag_task = self.local_rag_research(research_queries, request, user)
        
        research_results = await asyncio.gather(perplexity_task, local_rag_task)
        
        # Step 3: Agentic analysis
        agentic_analysis = await self.agentic_analysis(research_results, query, request, user)
        
        # Step 4: Synthesis
        final_result = await self.synthesize_results(research_results, agentic_analysis, query, request, user)
        
        return final_result