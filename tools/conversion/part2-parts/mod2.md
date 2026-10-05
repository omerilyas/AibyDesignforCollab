<p class="eyebrow">Module 2 · ≈ 90 min</p>

## LangChain for Messaging Intelligence { #module-2 data-toc-label="Module 2 · LangChain" }

In Part 1 you explored Cisco AI Assistant features such as **Ask Me Anything**, **Space Summaries**, **Smart Rewrite**, and **Translation**. These features show how AI can help users understand conversations, catch up quickly, improve communication, and work across languages.

In this module, we will take a step further and explore how AI frameworks like **LangChain** can be used to build simplified versions of these experiences using the **Webex Messaging APIs**.

Rather than treating AI as magic or a black box, we will break the experience down into building blocks:

- how to connect to Webex
- how to authenticate using an API token
- how to retrieve messages from a Webex space
- how to convert those messages into LangChain documents
- how those documents can later be used for RAG, summaries, rewrite, and agents

By the end of this module, you will understand how prompts, chains, retrievers, vector databases, tools, and agents come together to create intelligent messaging experiences.

#### What you will build

You will build a simplified **Webex Messaging Intelligence Assistant** using LangChain. Each task stacks on the last, until you have a real, working AI assistant for your Webex spaces.

<div class="glance build" markdown>

| | Task | You'll learn | Time |
|---|---|---|---|
| 2a | [Read Webex messages](#module-2a) | API access, authentication, data ingestion, LangChain documents | 15 min |
| 2b | [Ask Me Anything for Webex spaces](#module-2b) | RAG, embeddings, vector database | 30 min |
| 2c | [Generate space summaries](#module-2c) | Prompt templates, chains | 20 min |
| 2d | [Rewrite Webex messages](#module-2d) | Prompt engineering | 25 min |

</div>

!!! warning "Use one Colab notebook for the whole module"
    Each task builds on variables created in the task before it (for example, `webex_documents` from Task 1). Work through 2a → 2d **in order, in the same Google Colab notebook**, and keep the runtime connected.
