"""
agent/nodes.py — LangGraph Node Definitions
=============================================
Responsibility: Define all processing nodes in the agent graph.

Three nodes in this agent:
    1. router_node     — Reads question, decides which tool to use
    2. tool_node       — Executes the selected tool, gets raw result
    3. llm_node        — Takes tool result, generates final polished answer

Node contract (LangGraph rule):
    - Every node receives the FULL AgentState
    - Every node returns a DICT with only the fields it wants to update
    - LangGraph merges the returned dict back into state automatically
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from agent.state import AgentState
from tools.csv_tool import run_csv_tool
from tools.sql_tool import run_sql_tool
from tools.rag_tool import run_rag_tool

load_dotenv()

# -------------------------------------------------------------------
# LLM — shared across all nodes
# -------------------------------------------------------------------
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# -------------------------------------------------------------------
# Router Prompt
# Tells LLM to classify the question into one of 4 tool categories
# Must return ONLY the tool name — no extra text
# -------------------------------------------------------------------
ROUTER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a routing agent. Classify the user question into exactly one of these tools:

csv_tool   — Use for: sales data, revenue totals, product performance,
             region analysis, salesperson stats from CSV data
             Examples: "total sales", "top products", "revenue by region"

sql_tool   — Use for: customer data, order counts, JOIN queries,
             structured database questions, city/industry filters
             Examples: "customers from Hyderabad", "top 5 customers by spend"

rag_tool   — Use for: TechNova company documents, annual report,
             HR policy, market research, product catalog
             Examples: "TechNova revenue", "WFH policy", "competitors"

llm_only   — Use for: general questions not related to any data source
             Examples: "what is AI?", "explain LangChain"

Return ONLY the tool name. Nothing else. No explanation. No punctuation.
Valid responses: csv_tool, sql_tool, rag_tool, llm_only"""),
    ("human", "{question}")
])

# Router chain — prompt | llm | parse to clean string
router_chain = ROUTER_PROMPT | llm | StrOutputParser()

# -------------------------------------------------------------------
# LLM Response Prompt
# Takes tool result + question, generates a clean final answer
# -------------------------------------------------------------------
RESPONSE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful data assistant.
Answer the user's question using the provided data.
Be clear, concise, and format numbers properly.
If the data is empty or irrelevant, say so honestly.

Conversation History:
{history}"""),
    ("human", """Question: {question}

Data Retrieved:
{tool_result}

Please provide a clear, well-formatted answer:""")
])

response_chain = RESPONSE_PROMPT | llm | StrOutputParser()


# -------------------------------------------------------------------
# NODE 1: Router Node
# Reads: state["question"]
# Writes: state["tool_to_use"]
# -------------------------------------------------------------------
def router_node(state: AgentState) -> dict:
    """
    Classify the question and decide which tool to use.

    Uses an LLM with a strict routing prompt to return exactly
    one of: csv_tool, sql_tool, rag_tool, llm_only

    Args:
        state: Current AgentState with question field set

    Returns:
        dict: {"tool_to_use": "<tool_name>"}
    """
    question = state["question"]
    print(f"\n[Router] Question: {question}")

    try:
        tool = router_chain.invoke({"question": question}).strip().lower()

        # Validate — if LLM returns unexpected value, default to llm_only
        valid_tools = {"csv_tool", "sql_tool", "rag_tool", "llm_only"}
        if tool not in valid_tools:
            print(f"[Router] Invalid tool '{tool}' — defaulting to llm_only")
            tool = "llm_only"

        print(f"[Router] Decision: {tool}")
        return {"tool_to_use": tool}

    except Exception as e:
        print(f"[Router] Error: {e}")
        return {"tool_to_use": "llm_only", "error": str(e)}


# -------------------------------------------------------------------
# NODE 2: Tool Node
# Reads: state["tool_to_use"], state["question"]
# Writes: state["tool_result"]
# -------------------------------------------------------------------
def tool_node(state: AgentState) -> dict:
    """
    Execute the tool selected by the router node.

    Routes to the correct tool function based on state["tool_to_use"].
    Captures and stores the raw result in state["tool_result"].

    Args:
        state: AgentState with tool_to_use and question set

    Returns:
        dict: {"tool_result": "<raw_tool_output>"}
    """
    tool = state["tool_to_use"]
    question = state["question"]

    print(f"\n[Tool] Executing: {tool}")

    try:
        if tool == "csv_tool":
            result = run_csv_tool(question)

        elif tool == "sql_tool":
            result = run_sql_tool(question)

        elif tool == "rag_tool":
            result = run_rag_tool(question)

        else:
            # llm_only — no tool needed, pass question as context
            result = f"No tool data needed. Answer from LLM knowledge."

        print(f"[Tool] Result preview: {result[:100]}...")
        return {"tool_result": result}

    except Exception as e:
        print(f"[Tool] Error: {e}")
        return {"tool_result": "", "error": str(e)}


# -------------------------------------------------------------------
# NODE 3: LLM Response Node
# Reads: state["question"], state["tool_result"], state["chat_history"]
# Writes: state["final_answer"], state["chat_history"]
# -------------------------------------------------------------------
def llm_node(state: AgentState) -> dict:
    """
    Generate a polished final answer using the tool result.

    Takes the raw tool result and formats it into a clear,
    well-structured response for the user. Also updates
    chat history for conversation memory.

    Args:
        state: AgentState with question and tool_result set

    Returns:
        dict: {"final_answer": "<answer>", "chat_history": ["Q: ... A: ..."]}
    """
    question = state["question"]
    tool_result = state["tool_result"]
    history = state.get("chat_history", [])

    print(f"\n[LLM] Generating final answer...")

    try:
        # Build history string for context
        history_str = "\n".join(history[-6:]) if history else "No previous conversation."

        answer = response_chain.invoke({
            "question": question,
            "tool_result": tool_result,
            "history": history_str
        })

        # Save this Q&A to chat history (appended via operator.add)
        new_memory = [f"Q: {question}\nA: {answer.strip()}"]

        print(f"[LLM] Answer generated successfully")
        return {
            "final_answer": answer.strip(),
            "chat_history": new_memory  # operator.add appends this
        }

    except Exception as e:
        print(f"[LLM] Error: {e}")
        return {
            "final_answer": f"Sorry, I encountered an error: {str(e)}",
            "error": str(e)
        }


# -------------------------------------------------------------------
# Conditional edge function — used by graph.py
# LangGraph calls this after router_node to decide next node
# -------------------------------------------------------------------
def decide_tool(state: AgentState) -> str:
    """
    Conditional edge function — tells LangGraph which node to go to next.

    Called after router_node. Returns the name of the next node.
    LangGraph uses this string to look up the edge mapping in graph.py.

    Args:
        state: AgentState after router_node has set tool_to_use

    Returns:
        str: One of "tool_node" or "llm_node"
    """
    tool = state.get("tool_to_use", "llm_only")

    if tool == "llm_only":
        # Skip tool_node — go directly to llm_node
        return "llm_node"
    else:
        # Go to tool_node first
        return "tool_node"