"""
agent/graph.py — LangGraph Graph Assembly
==========================================
Responsibility: Wire all nodes and edges together into a compiled graph.

This is the "blueprint" of the agent — defines:
    - Which nodes exist
    - How they connect (edges)
    - Where the flow starts (entry point)
    - Where the flow ends (END)

Graph Flow:
    START
      └→ router_node         (classifies question → decides tool)
              ↓ decide_tool() conditional edge
        ┌─────┴──────┐
    tool_node      llm_node   (tool_node if data needed)
        └─────┬──────┘
           llm_node           (always ends here)
              └→ END
"""

from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.nodes import router_node, tool_node, llm_node, decide_tool


def build_graph():
    """
    Build and compile the LangGraph agent graph.

    Steps:
        1. Create StateGraph with AgentState schema
        2. Add all nodes
        3. Set entry point
        4. Add normal edges (A always goes to B)
        5. Add conditional edges (A goes to B or C based on condition)
        6. Compile and return

    Returns:
        CompiledGraph: Ready-to-run agent graph
    """

    # Step 1: Create graph with our state schema
    graph = StateGraph(AgentState)

    # Step 2: Add all nodes
    # format: add_node("node_name", node_function)
    graph.add_node("router_node", router_node)
    graph.add_node("tool_node", tool_node)
    graph.add_node("llm_node", llm_node)

    # Step 3: Set entry point — first node to run
    graph.set_entry_point("router_node")

    # Step 4: Conditional edge from router_node
    # decide_tool() returns "tool_node" or "llm_node"
    # Graph uses that string to route to correct next node
    graph.add_conditional_edges(
        "router_node",   # from this node
        decide_tool,     # call this function to decide
        {
            "tool_node": "tool_node",   # if returns "tool_node" → go to tool_node
            "llm_node":  "llm_node"     # if returns "llm_node"  → go to llm_node
        }
    )

    # Step 5: Normal edge — tool_node always goes to llm_node
    graph.add_edge("tool_node", "llm_node")

    # Step 6: Normal edge — llm_node always ends the graph
    graph.add_edge("llm_node", END)

    # Step 7: Compile — validates graph, returns runnable
    compiled = graph.compile()
    print("Agent graph compiled successfully!")
    return compiled


# -------------------------------------------------------------------
# Global compiled graph instance
# Import this in app.py: from agent.graph import agent_graph
# -------------------------------------------------------------------
agent_graph = build_graph()


def run_agent(question: str) -> dict:
    """
    Run the agent graph for a single question.

    Args:
        question: Natural language question from user

    Returns:
        dict with keys:
            "answer"      → final polished answer
            "tool_used"   → which tool was selected
            "tool_result" → raw data from tool
    """
    # Build initial state
    initial_state = {
        "question":     question,
        "tool_to_use":  "",
        "tool_result":  "",
        "final_answer": "",
        "chat_history": [],
        "error":        ""
    }

    # Run the graph — returns final state
    final_state = agent_graph.invoke(initial_state)

    return {
        "answer":      final_state.get("final_answer", "No answer generated"),
        "tool_used":   final_state.get("tool_to_use", "unknown"),
        "tool_result": final_state.get("tool_result", "")
    }


# -------------------------------------------------------------------
# Quick test — run directly to verify full agent works end to end
# Usage: python -m agent.graph
# -------------------------------------------------------------------
if __name__ == "__main__":

    test_questions = [
        "What is the total sales revenue?",           # → csv_tool
        "How many customers are from Hyderabad?",     # → sql_tool
        "What is TechNova's work from home policy?",  # → rag_tool
        "What is 2 + 2?",                             # → llm_only
    ]

    for q in test_questions:
        print("\n" + "=" * 60)
        result = run_agent(q)
        print(f"Q: {q}")
        print(f"Tool used: {result['tool_used']}")
        print(f"A: {result['answer']}")