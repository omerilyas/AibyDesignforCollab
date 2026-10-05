---
title: GenAI Lab Guide
description: "LTRCOL-2011 Part 2: build AI-powered Webex messaging workflows with LangChain, the Webex APIs and Google Colab."
chip: "LTRCOL-2011 · Part 2 of 2"
headline: "Building AI-Powered Messaging with LangChain & Webex"
standfirst: "Go from using AI to building it. Read Webex messages through the API, then build Ask Me Anything, space summaries and a rewrite assistant with LangChain."
meta:
  - label: SESSION
    value: LTRCOL-2011
  - label: STACK
    value: Python · LangChain
  - label: LAB TIME
    value: ~120 min
  - label: RUNS IN
    value: Google Colab
links:
  - title: "Part 1 · Webex AI lab guide"
    url: ""
  - title: "Webex Developer Portal"
    url: https://developer.webex.com
  - title: "Google Colab"
    url: https://colab.research.google.com
  - title: "LangChain docs"
    url: https://python.langchain.com
---

## About this lab { #about data-toc-label="About this lab" }

In [Part 1](../index.md) of the Webex AI lab you explored how Cisco Webex uses Artificial Intelligence to enhance collaboration across Messaging, Calling, and Meetings. You experienced capabilities such as AI-powered message assistance, conversation summaries, smart rewrites, live translations, meeting intelligence, captions, transcriptions, and AI-generated insights.

While these features demonstrate what AI can do inside Webex, the next logical step is to understand how these experiences are actually built.

In this hands-on lab, we will take a step further and explore how modern AI frameworks (such as **LangChain**) can be used alongside the **Webex APIs** to build intelligent messaging workflows and agentic experiences.

You will learn how developers and architects can leverage AI models, orchestration frameworks, and APIs to create real-world conversational solutions within Webex Messaging.

Throughout this lab, you will explore:

- **Webex Messaging APIs:** Understanding how applications interact with Webex spaces, users, and messages programmatically.
- **LangChain Fundamentals:** Learning how LangChain orchestrates prompts, memory, tools, and workflows to power AI applications.
- **Building AI-Powered Messaging Workflows:** Creating logic that can read, process, and respond to Webex messages intelligently.
- **Introduction to AI Agents:** Understanding how agents can reason, make decisions, and perform actions based on context and instructions.
- **Prompt Engineering & LLM Integration:** Connecting Large Language Models (LLMs) to Webex workflows for intelligent responses.

By the end of this lab, you will not only understand how AI features appear inside Webex, but also gain insight into how AI-powered experiences are designed, orchestrated, and built using frameworks like LangChain and Webex APIs.

!!! tip "The shift in mindset"
    Think of this lab as moving from **"using AI"** to **"building AI."**

This lab is designed to provide a practical and approachable introduction to the foundations of **agentic AI**, helping you understand the core building blocks behind intelligent collaboration experiences.

### Lab at a glance { #glance data-toc-label="Lab at a glance" }

<div class="glance" markdown>

| | Module | Time |
|---|---|---|
| 1 | [Set up your lab environment](#module-1) | 30 min |
| 2 | [LangChain for Messaging Intelligence](#module-2) | 90 min |
| | **Total** | **~120 min** |

</div>

### How to use this guide { #how-to data-toc-label="How to use this guide" }

The whole lab lives on this one page. Scroll down and work through it in order.

- The **TREE** on the left shows where you are. The progress bar under it fills up as you scroll.
- Press <kbd>J</kbd> / <kbd>K</kbd> to jump to the next or previous section.
- When you finish a task, click **Mark complete** at the end of it. You get a ✓ in the tree, and your progress is saved in this browser.
- Every code block has a **copy** button in its top-right corner. Paste the code into a new Colab cell and run it.
- Click any screenshot to zoom in.

### Lab notes { #lab-notes data-toc-label="Lab notes" }

Click **Notes** (bottom-right) to open a scratchpad that stays with you on both parts of the lab guide. Use it to keep the things you'll need throughout the lab close at hand:

- your **Webex Bearer token** (so you don't have to re-grab it from the Developer Portal every time it expires)
- your **Webex Space (Room) ID**
- your **OpenAI API key**
- your **ngrok auth token**
- any **dCloud-assigned values** (the `cbXXX.dc-YY.com` domain, pod number, passwords)
- snippets, scratch notes, or anything else you want to remember

!!! warning "Where your notes live"
    Notes are saved **only in your browser** (localStorage on this device). They will be **lost** if you:

    - clear your browser data,
    - use a different browser or computer,
    - open the lab in a private/incognito window.

    Treat the notepad as a temporary scratchpad for the duration of the lab. If you need notes that survive long-term, copy them to a personal note-taking app at the end of the session.

!!! danger "Be mindful with secrets"
    Even though the notepad is local to your browser, treat any **API keys, tokens, or passwords** the way you would on any shared workstation. If you're on a shared/dCloud machine, **clear your notes** before logging out so the next user can't see them.

### Your lab proctors { #proctors data-toc-label="Your lab proctors" }

Need help? Raise your hand or reach out to any of us.

<div class="people" markdown>

<div class="person"><span class="nm">Omer Ilyas</span><span class="rl">Principal Technical Marketing Engineer</span><span class="em">oilyas@cisco.com</span></div>
<div class="person"><span class="nm">Kevin Ian Barrow</span><span class="rl">Technical Marketing Engineer</span><span class="em">kebarrow@cisco.com</span></div>
<div class="person"><span class="nm">Hussain Ali</span><span class="rl">Technical Marketing Engineer</span><span class="em">husali@cisco.com</span></div>
<div class="person"><span class="nm">Shane Long</span><span class="rl">Technical Marketing Engineer</span><span class="em">shalong@cisco.com</span></div>
<div class="person"><span class="nm">Venky Yechuri</span><span class="rl">Technical Projects Systems Engineer</span><span class="em">vyechuri@cisco.com</span></div>

</div>

<p class="eyebrow">Module 1 · ≈ 30 min</p>

## Set up your lab environment { #module-1 data-toc-label="Module 1 · Lab setup" }

Before you start building AI-powered messaging workflows, this module gets your foundation in place: a Webex API access token tied to your assigned account, a place to run Python notebooks, and an OpenAI API key for the LangChain pieces of the lab. Tasks 1d and 1e (Streamlit and ngrok) are optional background reading for future use; they are not used in this lab.

<div class="glance" markdown>

| | Task | Time |
|---|---|---|
| 1a | [Webex Developer Portal setup](#module-1a) | 10 min |
| 1b | [Google Colab setup](#module-1b) | 5 min |
| 1c | [Managing API keys in Colab](#module-1c) | 5 min |
| 1d | [Introduction to Streamlit](#module-1d) *(optional)* | 5 min |
| 1e | [Introduction to ngrok](#module-1e) *(optional)* | 5 min |

</div>
