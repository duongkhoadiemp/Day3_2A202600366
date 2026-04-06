# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- **Student Name**: DƯƠNG KHOA ĐIỀM
- **Student ID**: 2A202600366
- **Date**: 06/04/2026

---

## I. Technical Contribution (15 Points)

*Describe your specific contribution to the codebase (e.g., implemented a specific tool, fixed the parser, etc.).*

- **Modules Implemented**: `src/tools/oxford_tool.py`
- **Code Highlights**:

```python
def oxford_define(word: str):
    url = f"https://od-api-sandbox.oxforddictionaries.com/api/v2/entries/en-gb/{word.lower()}"
    headers = {
        "app_id": APP_ID,
        "app_key": APP_KEY
    }
    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        return f"API error: {res.status_code}"

    data = res.json()

    defs = []
    for r in data.get("results", []):
        for l in r.get("lexicalEntries", []):
            for e in l.get("entries", []):
                for s in e.get("senses", []):
                    defs.extend(s.get("definitions", []))

    return defs[0] if defs else "No definition found"
```

- **Documentation**: This tool is registered in the agent's tool inventory as `get_oxford_definition(word="<word>")` and integrates the Oxford Dictionary API as an external Action within the ReAct loop. When the agent needs a definition, it invokes `get_oxford_definition` as the **Action** step; the parsed API response is returned as the **Observation**, feeding back into the reasoning cycle (`Thought → Action → Observation → Final Answer`). In practice, this tool was chained with `add_card_to_set` for multi-step tasks — for example, the agent would first call `get_oxford_definition(word="address")` to retrieve the meaning, then immediately call `add_card_to_set(set_name="...", front="address", back="...")` using that result, which a stateless chatbot cannot do. One known limitation: the Oxford sandbox API returned `404` on certain words (e.g., `"address"`), so a fallback to the synonym tool or a static dictionary is recommended for production use.

---

## II. Debugging Case Study (10 Points)

*Analyze a specific failure event you encountered during the lab using the logging system.*

- **Problem Description**: Two errors were encountered while developing `oxford_tool.py`: a `401 Unauthorized` when calling the Oxford Dictionary API, and a `429 Too Many Requests` from the OpenAI API during repeated testing cycles.
- **Log Source**: The `401` surfaced as `"API error: 401"` returned from the `if res.status_code != 200` guard inside `oxford_define()`. The `429` appeared as an OpenAI exception in `logs/2026-04-06.log` during multi-step agent sessions. Additionally, the Oxford sandbox returned `404` on some valid words (e.g., `"address"`), causing the agent to receive `"API error: 404"` as an Observation and stall.
- **Diagnosis**: The `401` was caused by incorrect credentials — `APP_ID` and `APP_KEY` in `.env` were miscopied from the Oxford API dashboard. The `429` occurred because the agent looped toward `max_steps` with a growing context window each iteration, driving up token count and call frequency together. The `404` issue was a limitation of the Oxford sandbox API, which does not cover all common English words.
- **Solution**: The `401` was fixed by re-verifying and correcting the `.env` values. The `429` was mitigated by switching to a lighter model during development and relying on the `max_steps=5` hard cap to limit runaway loops. The `404` fallback was partially handled by the existing `"No definition found"` return value; a proper secondary API fallback remains a planned improvement.

---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

*Reflect on the reasoning capability difference.*

1. **Reasoning**: The `Thought` block significantly improved the agent's ability to handle multi-step problems. Instead of guessing directly, the agent explicitly reasoned about what it needed before acting — for example, deciding to call `get_oxford_definition` first, then chain the result into `add_card_to_set`. This made behavior transparent and traceable in a way a stateless chatbot cannot replicate.

2. **Reliability**: The agent performed *worse* than the Chatbot in simple or time-sensitive cases. For a basic greeting, the chatbot responded correctly in ~1.9s while the agent took ~3.2s for the same result. For "What date is today?", both failed — the chatbot hallucinated a date from training data, and the agent had no date tool to call. For stable factual questions already in the LLM's training data, the chatbot was faster and less error-prone.

3. **Observation**: The Observation step acted as a real-time correction mechanism. When `get_oxford_definition` returned `"API error: 404"`, the agent could re-evaluate in the next `Thought` step rather than blindly reporting a wrong answer. This self-healing behavior — driven by real environment feedback — is the clearest structural advantage of ReAct over a plain chatbot.

---

## IV. Future Improvements (5 Points)

*How would you scale this for a production-level AI agent system?*

- **Scalability**: Introduce an asynchronous task queue (e.g., Celery or asyncio) to handle multiple tool calls concurrently, reducing latency when the agent needs to invoke several tools in parallel.
- **Safety**: Add a Supervisor LLM layer that audits each Action before execution, flagging potentially harmful or out-of-scope tool calls and preventing runaway loops by enforcing strict step budgets.
- **Performance**: Implement a Vector DB (e.g., Chroma or Pinecone) to cache tool descriptions and previous Observations, enabling fast semantic retrieval in systems with a large number of available tools.
