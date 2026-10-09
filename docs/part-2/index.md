---
title: MCP Lab Guide
description: "LTRCOL-2011 Part 2: connect Webex Messaging to an AI client with the Webex MCP server, Codex, a Webex Client Identity Token (WCIT) and MCP elicitation."
chip: "Part 2 of 3"
headline: "Webex MCP for AI Clients"
standfirst: "A step-by-step lab for Webex Messaging. Connect Webex to agentic workflows using Codex, a Webex Client Identity Token (WCIT) and MCP elicitation."
meta:
  - label: SESSION
    value: Delivered by Omer Ilyas
  - label: AI CLIENT
    value: Codex + WCIT
  - label: LAB TIME
    value: ~90 min
  - label: REVISION
    value: v1
links:
  - title: "Part 1 · Webex AI lab guide"
    url: ""
  - title: "Part 3 · GenAI lab guide"
    url: "part-3/"
  - title: "Token assignment tool"
    url: https://aibydesign-token-assignment.vercel.app/
  - title: "Collaboration Control Hub"
    url: https://admin.webex.com
  - title: "Webex MCP docs"
    url: https://developer.webex.com/mcp/docs/ai-in-webex
---

## About this lab { #about data-toc-label="About this lab" }

<p class="lede">Introducing Webex MCPs: bringing collaboration into the agentic era.</p>

Webex MCP servers provide a governed tool layer that lets an AI client discover and invoke Webex capabilities. Control Hub policy, granted scopes, and the signed-in user's existing Webex permissions still determine what a tool can do.

!!! note "Lab scope"
    Although Webex provides other MCP servers, this lab focuses only on **Webex Messaging MCP**. After completing the Messaging configuration, you can reuse the same general process for another Webex MCP server: confirm Control Hub access, configure the correct endpoint in the AI client, and review that server's tools, scopes, and content requirements. Always verify the product page for the server you choose.

!!! note "Note"
    This part continues from [Part 1](../index.md). Use the same dCloud session and the same credentials from `Session_Info.txt` that you saved on your physical/attendee workstation (or in the **Notes** panel) during [Accessing your lab](../index.md#access). Whenever this part asks you to sign in to **Collaboration Control Hub** or Webex, use the **Charles Holland** credentials.

!!! info "Client and authentication used in this lab"
    For the hands-on exercises, we use **Codex** with a **Webex Client Identity Token (WCIT)**. Webex MCP can also be connected through other AI clients, such as Claude Code, but that setup is not part of this lab. The OAuth Integration workflow is included for reference only and is not required to complete the lab. During WCIT elicitation, Webex may still open an OAuth authorization page when a tool requires an additional scope.

![Webex MCP servers bring Webex Meetings, Messaging, Workspaces, Vidcast and Slido into agentic workflows](img/mcp-02.png){ loading=lazy }

/// caption
Webex MCP servers bring Webex Meetings, Messaging, Workspaces, Vidcast and Slido into agentic workflows.
///

### Lab at a glance { #glance data-toc-label="Lab at a glance" }

<div class="glance time" markdown>

| | Module | Time |
|---|---|---|
| — | [Start here in Control Hub](#start) | 5 min |
| 1 | [Understand MCP and enable a Webex MCP server](#module-1) | 10 min |
| 2 | [Create credentials](#module-2) | 20 min |
| 3 | [Understanding OAuth and elicitation](#module-3) *(optional)* | 10 min |
| 4 | [Configure Codex](#module-4) | 15 min |
| 5 | [Messaging prompts](#module-5) | 20 min |
| 6 | [Summary and next steps](#module-6) | 5 min |
| 7 | [Troubleshooting and cleanup](#module-7) | 10 min |
| | **Total** (including the optional reference module) | **~90 min** |

</div>

<div class="glance" markdown>

| Lab profile | Details |
|---|---|
| Primary path | Webex Messaging MCP with Codex and WCIT |
| Audience | Developers, administrators, technical instructors, and solution engineers |
| Revision | v1 |

</div>

### Learning outcomes { #outcomes data-toc-label="Learning outcomes" }

- [ ] Explain how an AI client discovers and calls Webex MCP tools.
- [ ] Enable the Cisco Webex Messaging MCP server in Control Hub.
- [ ] Generate a WCIT and explain how elicitation requests additional Webex scopes.
- [ ] Connect Codex without exposing the WCIT.
- [ ] Run read-only prompts, interpret a scope request, and perform a controlled write action.

### Before you begin { #before data-toc-label="Before you begin" }

<div class="glance" markdown>

| Requirement | What the lab users need |
|---|---|
| Webex | An active account in the organization used for the lab |
| Control Hub | An administrator account so you can enable the selected MCP server |
| Developer Portal | An account able to generate a WCIT. Creating an OAuth Integration is covered for reference only. |
| AI client | **Codex** installed and signed in. Use your existing Codex account. If you don't have one, create your own free account with the email address provided for the lab, or select **Continue with Google** and use your Gmail account. Sign in and confirm that you can start a new task before continuing. The instructor will not provide shared AI-client credentials. Sign up: [chatgpt.com](https://chatgpt.com){:target="_blank" rel="noopener"} |

</div>

### How to use this guide { #how-to data-toc-label="How to use this guide" }

The whole lab lives on this **one page**. Scroll down and work through it in order.

- The **TREE** on the left shows where you are. The progress bar under it fills up as you scroll.
- Press <kbd>J</kbd> / <kbd>K</kbd> to jump to the next or previous section.
- When you finish a module, click **Mark complete** at the end of it. You get a ✓ in the tree, and your progress is saved in this browser.
- Every prompt and configuration block has a **copy** button in its top-right corner.
- Click **Notes** (bottom-right) to keep lab values close at hand. Never paste your WCIT or any other secret into shared notes, prompts or screenshots.
- Click any screenshot to zoom in.

### Your lab proctor { #proctors data-toc-label="Your lab proctor" }

Need help? Raise your hand or reach out to me.

<div class="people" markdown>

<div class="person"><span class="nm">Omer Ilyas</span><span class="rl">Principal Technical Marketing Engineer</span><span class="em">oilyas@cisco.com</span></div>

</div>

<p class="eyebrow">Before you start · ≈ 5 min</p>

## Start here in Collaboration Control Hub { #start data-toc-label="Start here in Control Hub" data-task="start" }

##### Step 1: Sign in

Open [admin.webex.com](https://admin.webex.com){:target="_blank" rel="noopener"} using an administrator account for your assigned lab.

![The Collaboration Control Hub sign-in page](img/mcp-03.png){ loading=lazy }

/// caption
The Collaboration Control Hub sign-in page.
///

!!! note "Note"
    The account shown in the screenshot, **omer.ilyas@boldbetz.com**, is for demo purposes only. Sign in with the credentials provided for your lab session: the same **Charles Holland** credentials from `Session_Info.txt` that you used in [Part 1](../index.md#access). If you have any questions, ask your proctor.

##### Step 2: Open the Webex inventory

Select **Apps**, then **Agentic Apps**, then the **Webex** tab.

![Apps > Agentic apps > Webex lists the Webex MCP servers and their access state](img/mcp-04.png){ loading=lazy }

/// caption
Apps > Agentic apps > Webex lists the Webex MCP servers and their access state.
///

!!! note
    The MCP servers available in your lab environment may differ from those shown above, but for this lab, confirm that **Webex Messaging** is available before continuing.

!!! success "Checkpoint"
    The class begins only after the administrator confirms the selected server is visible. Module 1 completes the policy and tool review.

<p class="eyebrow">Overview · the servers</p>

## Webex MCP servers at a glance { #servers data-toc-label="MCP servers at a glance" }

### How Webex connects AI agents { #how-it-works data-toc-label="How Webex connects AI" }

Agents use approved tools, work with context, and take bounded actions toward a user's goal. MCP is one of four ways Webex connects to AI, not the whole Webex AI strategy.

#### Four ways to connect

<div class="models">
<div><b>REST APIs and SDKs</b><span>Direct requests and deterministic app logic</span></div>
<div><b>Webhooks and events</b><span>Event-driven workflows and notifications</span></div>
<div class="on"><b>Model Context Protocol (MCP)</b><span>Agents discover and use approved tools and context</span><em>This lab</em></div>
<div><b>Agent-to-Agent (A2A)</b><span>Specialized agents hand work to each other</span><em>Beta</em></div>
</div>

MCP connects an agent to **capabilities**, A2A connects an agent to **another agent**. Behind the scenes, an MCP server often calls the same Webex REST APIs.

#### Two directions for MCP

**1. Webex MCP servers → external AI clients** (what you do in this lab)

<ol class="flow">
<li><b>You</b><span>Ask for something in plain language</span></li>
<li><b>AI client</b><span>The MCP client, for example Codex</span></li>
<li><b>Webex MCP server</b><span>Offers approved tools, for example Messaging</span></li>
<li><b>Webex services</b><span>Spaces, messages, meetings and more</span></li>
</ol>

The MCP server supplies the tools, the agent lives in the AI client. Example tasks: search messages, post a space update, or find a meeting and pull its transcript.

**2. External MCP servers → Webex AI** (context only)

<ol class="flow">
<li><b>Caller</b><span>Talks to the contact center</span></li>
<li><b>Webex AI Agent</b><span>The MCP client, in Webex Contact Center</span></li>
<li><b>External MCP server</b><span>Your company's tools</span></li>
<li><b>Business system</b><span>Orders, shipping, CRM and more</span></li>
</ol>

Here Webex is the client: the Webex AI Agent calls your own MCP server during a live customer conversation, for example to look up an order.

#### Who controls what

- **Tools:** each MCP server exposes a set of approved actions. The agent can only use those tools.
- **Scopes and permissions:** a tool works only within the signed-in user's Webex permissions and the scopes they granted.
- **Administrators:** in **Collaboration Control Hub**, admins enable or block each server for users, choose which tools are allowed, and review changes. Webex calls this governance layer **Agentic Apps**.

### Security: trust before you connect { #mcp-security data-toc-label="MCP security" }

An MCP server gives an AI agent real tools. Some tools only read information, others can create, update, delete, send or publish data on behalf of a user or an organization. That is why Webex's guidance is simple: **connect only to MCP servers you know and trust.**

#### The risk with external MCP servers

When you add an MCP server that isn't the provider's official one, for example a community or third-party version, you are trusting whoever runs it with your data and your users' actions. Before connecting, you need to know:

- **What its tools can do:** read data only, or also send messages, change records, or act in other services.
- **Where your data goes:** which systems it connects to, and whether it stores data outside Webex.
- **Who runs it:** who owns and supports it, how they handle data, and whether it's meant for production use.
- **What it asks for:** whether the permissions it requests match what you actually need.

If any answer is unclear, don't connect yet. Whenever possible, use the **official MCP server hosted by the service provider**, such as the Webex MCP servers in this lab.

#### Control Hub as your orchestration layer

Webex MCP servers are managed in **Collaboration Control Hub** as **Agentic Apps**, so an administrator decides what agents can reach before any user connects:

<div class="models">
<div><b>Enable or block</b><span>Turn each MCP server on or off for your users</span></div>
<div><b>Choose the tools</b><span>Allow only the tools your use case needs</span></div>
<div><b>Inspect schemas</b><span>See exactly what each tool accepts and does</span></div>
<div><b>Reauthorize changes</b><span>Review again when a server's tools change</span></div>
</div>

Every request still runs within the signed-in user's Webex permissions and the scopes they granted. With Control Hub in front of your MCP servers, you get one place to set policy for every AI client, instead of trusting each client or server separately.

!!! tip "Quick checklist before connecting any MCP server"
    Is it hosted by the official provider? If not, do you trust who hosts it? Do you understand its tools? Are the permissions appropriate? Could it access or store sensitive data? Is it meant for production? Do you know who owns and supports it?

### Webex Messaging MCP capabilities { #messaging-caps data-toc-label="Messaging MCP" }

Webex Messaging MCP lets an authorised AI client work with spaces, messages, memberships, and files. Control Hub policy, granted scopes, and the signed-in user's Webex permissions determine which operations are available.

![Webex Messaging MCP: bringing messaging intelligence to AI agents](img/mcp-05.png){ loading=lazy }

/// caption
Webex Messaging MCP: bringing messaging intelligence to AI agents.
///

#### Capabilities used in this lab

- **Space management.** Create, discover, and manage Webex spaces from an AI client.
- **Messaging actions.** Send, retrieve, edit, and delete messages through MCP tools.
- **Membership control.** Add, remove, and manage users within spaces and conversations.
- **File collaboration.** Access and share files in Webex spaces as part of an agent workflow.

!!! info "Access state shown"
    The slide shows Webex Messaging **blocked for all users**. This is an example tenant state, not an instruction. An administrator must allow the intended lab users before they can connect.

### Webex Meetings MCP capabilities (context only) { #meetings-caps data-toc-label="Meetings MCP (context)" }

Webex Meetings MCP lets an authorised AI client work with meeting administration and available post-meeting content. The meeting configuration and the signed-in user's Webex permissions still control access.

![Webex Meetings MCP: bringing meeting intelligence to AI agents](img/mcp-06.png){ loading=lazy }

/// caption
Webex Meetings MCP: bringing meeting intelligence to AI agents.
///

#### Capabilities shown for context

- **Meeting lifecycle.** Schedule, update, retrieve, and cancel meetings from an AI client.
- **Meeting intelligence.** Access available AI-generated summaries, action items, and meeting insights.
- **Transcript access.** Search and retrieve transcripts or transcript snippets from completed meetings.
- **Recording management.** Discover recordings and retrieve available playback information for analysis and follow-up.
- **Standards-based access.** Webex Meetings MCP is shown for context only and is not configured in this lab.

!!! info "Availability and access"
    Summaries, recordings, and transcripts depend on the meeting settings and the user's access. Webex Meetings MCP is included for context only and is not covered in the hands-on exercises. Once you have configured Messaging MCP, you can use the same general approach to configure Meetings MCP separately.

<p class="eyebrow">Module 1 · ≈ 10 min</p>

## Understand MCP and enable a Webex MCP server { #module-1 data-toc-label="Module 1 · Understand & enable" data-task="1" }

Before you configure Webex, take a minute to understand what MCP is doing. MCP is not another AI model and it does not replace the Webex API. It is a common way for an AI application to discover approved capabilities and call them in a structured way. In this lab, your AI client connects to a Webex MCP server, and the server works with Webex on behalf of the signed-in user.

### How MCP fits together { #m1-parts data-toc-label="How MCP fits together" }

The diagram below separates the main parts. They may feel like one experience when you use Codex, but each part has a different job.

![Model Context Protocol key components: MCP host, MCP client, MCP server and tools, linked by the MCP protocol](img/mcp-07.png){ loading=lazy }

/// caption
Model Context Protocol key components: MCP host, MCP client, MCP server and tools, linked by the MCP protocol.
///

- **MCP host.** The application you work in. In this lab, the MCP host is Codex, it manages the conversation and the user experience.
- **MCP client.** The connection component inside the host. It reads the server's capability information, sends tool requests, and returns results to the host.
- **MCP server.** The service that publishes capabilities in a standard format. In this lab, Cisco hosts the Webex Messaging and Webex Meetings MCP servers.
- **Tools.** The actions the server makes available, such as finding a space, listing meetings, retrieving a transcript, or sending a message. Each tool describes the information it needs.
- **MCP protocol.** The agreed format the client and server use to describe capabilities, make requests, return results, and report errors.

MCP can also expose resources and reusable prompts. This lab concentrates on tools because those are the capabilities you will discover and call from the AI client.

### How a Webex MCP tool call works { #m1-call data-toc-label="How a tool call works" }

The language model helps choose a suitable tool and prepares its inputs, but it does not bypass Webex. The MCP client carries the request, and the Webex MCP server applies authentication, granted scopes, Control Hub policy, enabled tools, and the signed-in user's existing Webex permissions.

![From a natural-language request to a Webex tool result](img/mcp-08.png){ loading=lazy }

/// caption
From a natural-language request to a Webex tool result.
///

1. **You ask.** Enter a natural-language request in the AI application, for example asking it to find a Webex space or list recent meetings.
2. **The host interprets the request.** The application gives the model the conversation and information about the connected MCP servers.
3. **The client discovers capabilities.** The MCP client reads the tools and their input definitions from the selected Webex MCP server.
4. **The model chooses a tool.** The model selects the tool that matches your request and prepares the required parameters. The client can ask you to clarify a missing or ambiguous value.
5. **Webex runs the allowed action and returns the result.** The client sends the structured tool call to the server. Webex checks access, calls the underlying Webex service, and sends the result back through the client for the application to present.

!!! tip "The key point"
    The model can **propose** a tool call, but the Webex MCP server **decides** whether that call is allowed. This is why the server must be enabled in Control Hub and why scopes and user permissions matter.

### Servers used in this lab { #m1-servers data-toc-label="Servers used in this lab" }

Use **Webex Messaging** for all hands-on exercises in this guide. Webex Meetings is included only as portfolio context. Other Webex MCP servers follow the same overall pattern: confirm Control Hub access, configure the correct endpoint, review the available tools and scopes, and begin with a read-only request.

<div class="glance" markdown>

| Server | Endpoint | Use in this lab |
|---|---|---|
| Webex Messaging | `https://mcp.webexapis.com/mcp/webex-messaging` | **Primary path:** spaces, messages, memberships, files, and related tools |
| Webex Meetings | `https://mcp.webexapis.com/mcp/webex-meeting` | Context only: schedules, participants, recordings, transcripts, and summaries |

</div>

### What scopes control { #m1-scopes data-toc-label="What scopes control" }

!!! danger "Note"
    **Where do these scopes come from?** The scopes listed in this section are the ones published by Webex for the **Webex Messaging MCP server**. You don't need to create or look them up yourself. You can find the same list in the **Scopes** section of the [Messaging MCP Server page](https://developer.webex.com/mcp/docs/messaging-mcp-server){:target="_blank" rel="noopener"} on developer.webex.com. Other Webex MCP servers, such as Meetings, use their own scopes.

A scope is a named permission carried by the user's authorization. A tool describes an action, the scope decides whether the signed-in identity may perform that type of action. The required `spark:mcp` scope opens the MCP connection, but it does not by itself allow the client to read a message, find a space, or make a change.

Scopes work together with the Control Hub tool policy and the user's existing Webex permissions. **All three checks must pass.** A tool may therefore be visible in the client but still fail if its required scope was not granted or the signed-in user cannot access the target space.

<div class="glance" markdown>

| Scope | What it permits | Use in this lab |
|---|---|---|
| `spark:mcp` | Connect to the Webex MCP server. It is required before any MCP tool can run. | **Required** |
| `spark:messages_read` | Get and search messages, read thread content, and retrieve file details or downloads. | Read exercises |
| `spark:messages_write` | Create, edit, or delete messages, upload or share files, and reply in a thread. | Controlled write only |
| `spark:rooms_read` | Get and search Webex spaces. | Find the lab space |
| `spark:rooms_write` | Create, update, or delete Webex spaces. | Not required |
| `spark:memberships_read` | Read space membership information. | Optional |
| `spark:memberships_write` | Add, update, or remove space memberships. | Not required |
| `spark:webhooks_read` | Read Webex webhook subscriptions. | Out of scope |
| `spark:webhooks_write` | Create, update, or delete Webex webhook subscriptions. | Out of scope |

</div>

In this lab, a Webex Client Identity Token (WCIT) lets Codex begin with `spark:mcp` and request extra service scopes through **elicitation** when a selected tool needs them. For reference, a client that does not support elicitation can use a Webex OAuth Integration with its required scopes registered in advance. Grant only the scopes required for the task, and add a write scope only when you are ready for the controlled write exercise. You'll set up the WCIT in [Module 2](#module-2), and [Module 3](#module-3) explains how elicitation and OAuth work, so don't worry if these terms are new for now.

Reference: [Cisco Webex Messaging MCP server and scope list](https://developer.webex.com/mcp/docs/messaging-mcp-server){:target="_blank" rel="noopener"}

### Administrator task in Control Hub { #m1-admin data-toc-label="Administrator task in Control Hub" }

##### Step 1: Open Agentic Apps

Sign in to Control Hub at [admin.webex.com](https://admin.webex.com){:target="_blank" rel="noopener"}. In the left navigation, select **Apps**, then select the **Agentic Apps** tab.

![Control Hub > Apps > Agentic apps](img/mcp-09.png){ loading=lazy }

/// caption
Control Hub > Apps > Agentic apps.
///

##### Step 2: Choose the Webex tab

Open **Webex Messaging** for the main lab.

![The Webex tab lists Webex Messaging and the other Webex MCP servers](img/mcp-10.png){ loading=lazy }

/// caption
The Webex tab lists Webex Messaging and the other Webex MCP servers.
///

##### Step 3: Review the General tab and allow access

!!! warning "Lab starting state"
    By default, Webex Messaging is shown as **Blocked for all users**. This is the safe starting point. The **Allowed for all users** option stays greyed out until you turn on automatic server data updates and save, so follow the steps below in order. Allowing the server does not bypass OAuth scopes or the signed-in user's normal Webex permissions.

![Webex Messaging > General: blocked for all users by default](img/mcp-11.png){ loading=lazy }

/// caption
Webex Messaging > General: blocked for all users by default.
///

1. **Turn on Authorise automatic server data updates.** This switch is off at the start of the lab. When enabled, updates such as the server name, description, same-domain URL, transport type, or related server metadata can take effect without a fresh authorization. The administrator still receives an indication of the change and can reauthorize the server.
2. **Click Save.** This unlocks the access options.
3. **Select Allowed for all users,** which is no longer greyed out, and click **Save** again.

![Allowed for all users, with automatic server data updates authorised](img/mcp-12.png){ loading=lazy }

/// caption
Allowed for all users, with automatic server data updates authorised.
///

##### Step 4: Review the Authentication tab

!!! warning "Review, do not edit"
    Open the **Authentication** tab. Cisco-official servers are automatically configured. Do not enter or replace the authorization endpoint, token endpoint, token authentication method, client ID, scopes, registration endpoint, or custom headers unless Cisco documentation or your organization explicitly instructs you to change the default authentication.

![The Authentication tab: Cisco-official servers are configured automatically](img/mcp-13.png){ loading=lazy }

/// caption
The Authentication tab: Cisco-official servers are configured automatically.
///

**What this tab means.** It defines how the MCP server authenticates clients. It is not where students paste their token or client secret. The required WCIT and elicitation steps appear later in this guide, the OAuth Integration method is included there for reference only. For this step, leave the official values unchanged.

##### Step 5: Review tools and their schemas

Open the **Tools** tab. This page controls which Webex actions an approved client can discover and request. For this lab, **enable the tools exactly as shown in the image below**: turn on **Allow tool** and **Allow signature change** for **Create Webex Message**, **Edit Webex Message**, **Delete Webex Message**, **Get Webex Messages** and **Create Webex Space**, and leave the rest off. A tool still remains subject to its scope, Control Hub policy, and the signed-in user's Webex access.

![The Tools tab: Allow tool, Allow signature change and Review for each tool](img/mcp-14.png){ loading=lazy }

/// caption
The Tools tab: Allow tool, Allow signature change and Review for each tool.
///

!!! note "Note"
    You're welcome to explore the other tools and enable any of them to try your own use cases. Just leave **Get Webex Space** and **Search Webex Spaces** off for now: a later step in [Module 4](#module-4) shows what happens when Codex has no tool to find spaces, and you'll turn **Get Webex Space** on there.

<div class="glance" markdown>

| Control | What it does | Lab decision |
|---|---|---|
| Allow tool | **On** makes the tool available and discoverable to approved client users. **Off** removes it from the client-side tool list. | Enable only the tools required by the exercise. |
| Allow signature change | **On** keeps the tool available if its input or output schema changes after authorization and marks the drift for review. **Off** withholds a changed tool until an administrator reviews and reauthorizes it. | Keep **On** for this lab. |
| Details / Review | Opens the tool description, input schema, output schema, and annotations so the administrator can see what data the tool accepts, returns, or changes. | Review before enabling the tool and again after any reported schema change. |

</div>

#### Webex Messaging tools available

The Webex Messaging MCP server currently publishes **24 tools**. Control Hub may display friendly names, while the Developer Portal uses the protocol tool names shown below. The tool catalogue describes what the server can offer, attendees can use only the tools that the administrator has allowed and for which their authorization includes the required scope.

<div class="glance tools" markdown>

| Area | Tool | What it does |
|---|---|---|
| Messages | `webex-create-message` | Send a message to a space or directly to a person, supports text, markdown, HTML, file URLs, and adaptive cards. |
| | `webex-edit-message` | Edit an existing message using its message and space IDs, supports text or markdown. |
| | `webex-delete-message` | Delete a message from a direct or group space. The deletion is irreversible. |
| | `webex-get-message` | Retrieve one message by ID or list messages in a space with optional filters. |
| | `webex-search-messages` | Search a space using keywords, dates, mentions, thread parent, or file filters. |
| Spaces | `webex-create-space` | Create a Webex space with a title and optional team, lock, or announcement settings. |
| | `webex-get-space` | Retrieve one space or list spaces by type, team, or sort order. |
| | `webex-update-space` | Change a space title, locked state, or announcement-only setting. |
| | `webex-delete-space` | Delete a space or remove the caller from it, depending on role. A deleted space cannot be recovered. |
| | `webex-search-spaces` | Search spaces with type, team, and sort filters. |
| Memberships | `webex-add-membership` | Add a person to a space by ID or email, with optional moderator privileges. |
| | `webex-get-membership` | Retrieve one membership or list memberships by space or person. |
| | `webex-update-membership` | Change membership properties, including moderator role or hidden-space state. |
| | `webex-remove-membership` | Remove a member from a space using the membership ID. |
| Webhooks | `webex-create-webhook` | Create a real-time event subscription with optional filters and an HMAC secret. |
| | `webex-get-webhook` | Retrieve one webhook or list the authenticated user's webhooks. |
| | `webex-update-webhook` | Change a webhook name, target URL, secret, or active status. |
| | `webex-delete-webhook` | Delete a webhook subscription using its webhook ID. |
| Files | `webex-share-file` | Share one or more publicly reachable file URLs through a Webex message. |
| | `webex-upload-file` | Upload base64-encoded file content to a space with a file name and content type. |
| | `webex-get-file-details` | Read file metadata such as type, size, and disposition from a message file URL. |
| | `webex-download-file` | Download message-file content and return it as base64-encoded data. |
| Threading | `webex-create-thread-reply` | Reply to a parent message using the space ID, parent message ID, and text or markdown. |
| | `webex-get-thread` | Retrieve the replies associated with a parent message in a space. |

</div>

!!! note "Meetings and other Webex MCP servers"
    Each server has its own tool catalogue, schemas, prerequisites, and OAuth scopes. The same review method used in this lab applies, but do not assume that the Messaging tool names or scopes apply to another server. For the current Meetings list, see [Webex Meetings MCP server](https://developer.webex.com/mcp/docs/meetings-mcp-server){:target="_blank" rel="noopener"}.

#### What the Review details page shows

Select **Review** beside a tool to inspect the contract that the AI client uses. The example below shows **Create Webex Message**. Always scroll through the complete schema, the screenshot shows only part of the JSON definition.

![Select Review beside a tool on the Tools tab](img/mcp-15.png){ loading=lazy }

/// caption
Select Review beside a tool on the Tools tab.
///

![Review details for Create Webex Message: description, input schema and output schema](img/mcp-16.png){ loading=lazy }

/// caption
Review details for Create Webex Message: description, input schema and output schema.
///

#### How to review a tool schema

1. **Select Review beside the tool.** Read the description first and identify whether the tool only reads data or can send, edit, delete, or otherwise change Webex content.
2. **Inspect the input schema.** Note required fields, data types, target identifiers such as a space ID, optional fields, and any request for sensitive or unexpected data.
3. **Inspect the output schema.** Check what identifiers, message content, file details, or other data can be returned to the AI client.
4. **Read the annotations** for side-effect and safety hints. Treat tools that send, edit, delete, manage membership, or manage webhooks as higher risk than read-only lookups.
5. **Choose the Allow tool and Allow signature change settings.** If Control Hub reports a schema change, review it and reauthorize the server to establish a new approved baseline, even if the tool was allowed to remain available during the change.

##### Step 6: Validate the administrator configuration

![Webex Messaging allowed, with the lab tools enabled. Select Save](img/mcp-17.png){ loading=lazy }

/// caption
Webex Messaging allowed, with the lab tools enabled. Select Save.
///

!!! success "Before continuing"
    Confirm that Webex Messaging is **allowed for all users**, the automatic server update setting matches the lab policy, the Cisco-official authentication settings remain unchanged, and the tools are enabled. When these checks are complete, select **Save**.

<p class="eyebrow">Module 2 · ≈ 20 min</p>

## Create credentials { #module-2 data-toc-label="Module 2 · Create credentials" data-task="2" }

!!! note "Note"
    As covered in [How Webex connects AI agents](#how-it-works), MCP in Webex works in two directions:

    - **Outbound:** use Cisco's own **Webex MCP servers** in external AI tools, such as Codex.
    - **Inbound:** bring **external MCP servers** into Webex AI, for example so the Webex AI Agent in Contact Center can use your company's tools.

    This lab follows the **outbound** direction. You'll connect the **Webex Messaging MCP server**, built and hosted by Cisco, to **Codex**. The credentials you create in this module are for that connection.

Before Codex can call the Webex Messaging MCP server, it needs a credential that Webex can validate. This lab follows **Path A: WCIT with elicitation**. Path B explains an OAuth Integration **for reference only**, students do not need to complete it.

!!! success "Required lab path: WCIT with elicitation"
    The WCIT starts with the `spark:mcp` scope. When a tool requires another Webex scope, the server asks the user to approve it during the tool call. Codex uses this path throughout the hands-on exercises.

!!! note "Reference only: OAuth 2.0 Integration"
    A client that does not support elicitation may require a Webex Integration with `spark:mcp`, the scopes required by the selected MCP server, and the exact redirect URI supplied by that client. This workflow is included to explain the alternative approach, it is not required for this lab.

!!! info "Important distinction"
    Elicitation is not a separate credential type. It is the MCP interaction used to request missing authorization at runtime, the credential used to start this path is the WCIT.

<div class="glance" markdown>

| Client scenario | Credential | Runtime behavior |
|---|---|---|
| Hands-on lab: Codex | **WCIT** | Starts with `spark:mcp`, Webex requests additional scopes through elicitation when a tool needs them |
| Reference only: client without elicitation | OAuth Integration | Uses browser sign-in and consent with the exact redirect URI supplied by that client |

</div>

![Webex MCP supports two authentication methods: token-based (WCIT) and OAuth 2.0](img/mcp-18.png){ loading=lazy }

/// caption
Webex MCP supports two authentication methods: token-based (WCIT) and OAuth 2.0.
///

!!! warning "Lab note"
    Path A is the required hands-on path. Generate a WCIT from the token page shown below, **do not create an Agentic App**.

### Path A · Generate a WCIT (required for this lab) { #m2-path-a data-toc-label="Path A · Generate a WCIT" }

##### Step 1: Open the token page

Sign in to the Webex Developer Portal as **Charles Holland**, using the same credentials from `Session_Info.txt` that you used in [Part 1](../index.md#access). Then open [https://developer.webex.com/agentic-token](https://developer.webex.com/agentic-token){:target="_blank" rel="noopener"}. Select **Generate now**.

![Manage Webex Agentic MCP App token: select Generate now](img/mcp-19.png){ loading=lazy }

/// caption
Manage Webex Agentic MCP App token: select Generate now.
///

##### Step 2: Name the token

Enter a recognisable, temporary token name such as **Omer MCP**. Do not include a password or secret in the name. If the optional **MCP server** field is available, select **Webex Messaging** for this lab or leave it unchanged.

![Generate token: enter a token name](img/mcp-20.png){ loading=lazy }

/// caption
Generate token: enter a token name.
///

!!! note "Note"
    Once the token is created in the next step, keep it safe: Webex shows it only once. For convenience, you can paste it into this guide's **Notes** panel (the **NOTES** button in the bottom-right corner) so it's ready when you configure Codex later. Notes are saved only in this browser, so don't use the Notes panel on a shared computer.

##### Step 3: Create and copy the token

Select **Create token**. Copy the token and store it in a password manager or a temporary environment variable. **The token is shown only once.** The WCIT starts with the `spark:mcp` scope, additional tool scopes are requested later through elicitation.

![Token generated successfully. Copy it now, you won't see it again](img/mcp-21.png){ loading=lazy }

/// caption
Token generated successfully. Copy it now, you won't see it again.
///

### Path B · Create an OAuth Integration (reference only) { #m2-path-b data-toc-label="Path B · OAuth (reference)" }

<div class="ref-banner" markdown>
<span class="ref-tag">Optional · reference only</span>
**You do not need to do this.** Path A (WCIT) is the lab path. Do not create an OAuth Integration unless your instructor specifically asks you to test this alternative method.<br>
[Skip to the credentials summary →](#m2-summary){ .ref-skip }
</div>

<div class="reference-only" markdown>

##### Step 1: Start an Integration

Open [https://developer.webex.com/my-apps/new/integration](https://developer.webex.com/my-apps/new/integration){:target="_blank" rel="noopener"} and select **Create an Integration**.

![Create a New App: choose Integration](img/mcp-22.png){ loading=lazy }

/// caption
Create a New App: choose Integration.
///

##### Step 2: Complete the Integration details

Complete the following fields:

- **Mobile SDK:** select **No**.
- **Integration name:** enter a recognisable name such as **Webex MCP Lab**.
- **Icon:** choose one of the default icons.
- **App Hub Description:** enter a short description, such as **Webex MCP laboratory client**.

![The New Integration form](img/mcp-23.png){ loading=lazy }

/// caption
The New Integration form.
///

##### Step 3: Enter the exact redirect URI

Copy the redirect URI from the OAuth configuration page in the client being reviewed and register it exactly as shown. The Integration and client values must match, including the scheme, host, port, path, and trailing slash. Because this is a reference-only path, do not invent or reuse a redirect URI, use the value supplied by that client.

##### Step 4: Select scopes

For a Messaging OAuth Integration, select `spark:mcp` plus the complete scope set required by the server. To verify the latest scopes, open **Agentic Apps**, choose **Webex Messaging**, and select **Learn More**. The scope lists below are reference information and are not required for the WCIT lab path. Do not add unrelated Webex scopes.

**Messaging scope set**

```text
spark:mcp spark:messages_read spark:messages_write
spark:rooms_read spark:rooms_write
spark:memberships_read spark:memberships_write
spark:webhooks_read spark:webhooks_write
```

**Meetings scope set**

```text
spark:mcp meeting:schedules_read meeting:schedules_write
meeting:participants_read meeting:summaries_read
meeting:recordings_read meeting:transcripts_read
```

##### Step 5: Create and protect credentials

Select **Add Integration**. On the next page, copy the **Client ID** and **Client Secret** and store them securely. The Client Secret cannot be viewed again after you leave the page. Do not place either credential in a prompt, screenshot, repository, slide, or shared notes.

</div>

### Summary { #m2-summary data-toc-label="Credentials summary" }

**Required lab path: Path A, WCIT and elicitation**

<ol class="flow">
<li><b>Developer Portal</b><span>Sign in to Webex</span></li>
<li><b>WCIT page</b><span>Open the agentic-token page</span></li>
<li><b>Create token</b><span>Name and generate the WCIT</span></li>
<li><b>Store token</b><span>Copy it once and protect it</span></li>
</ol>

Initial scope: `spark:mcp`. Webex can request additional scopes through elicitation.

**Reference only: Path B, OAuth Integration**

<ol class="flow">
<li><b>My Apps</b><span>Create an Integration</span></li>
<li><b>App details</b><span>Set Mobile SDK to No</span></li>
<li><b>URI and scopes</b><span>Enter the exact URI and select <code>spark:mcp</code></span></li>
<li><b>Credentials</b><span>Copy the Client ID and Client Secret</span></li>
</ol>

Redirect URI: the callback registered in Webex must match the AI client exactly.

!!! success "Validation"
    **Required lab path:** students have a WCIT stored outside the document. **Reference only:** Path B describes the Client ID, Client Secret, redirect URI, and scope requirements of an OAuth Integration, those credentials are not required for the hands-on exercises.

<p class="eyebrow">Module 3 · ≈ 10 min · optional</p>

## Understanding OAuth and elicitation { #module-3 data-toc-label="Module 3 · OAuth & elicitation" data-task="3" }

This optional reference module explains the two authorization flows. **There is nothing to configure in this module:** you'll connect Codex to Webex Messaging with the WCIT from Module 2, Path A, in [Module 4](#module-4). When a tool needs another Webex scope, WCIT elicitation may still open a Webex OAuth authorization page for consent. Creating your own OAuth Integration, as shown in Path B, remains reference information only.

!!! tip "Authentication vs authorization"
    **Authentication** proves who is connecting. **Authorization** controls what the connection can do. Effective access is the intersection of Control Hub policy, granted scopes, enabled tools, and the signed-in user's existing Webex permissions.

### Elicitation with a WCIT { #m3-elicitation data-toc-label="Elicitation with a WCIT" }

<ol class="flow">
<li><b>AI client</b><span>Connects using the WCIT</span></li>
<li><b>Webex MCP</b><span>Detects a missing tool scope</span></li>
<li><b>Consent</b><span>User reviews and approves the scope</span></li>
<li><b>Tool call</b><span>Continues with the granted scope</span></li>
</ol>

1. **Connect.** Codex sends the WCIT and establishes the MCP session with `spark:mcp`.
2. **Trigger a scoped tool.** A prompt calls a Webex Messaging tool that needs an additional Webex scope.
3. **Review the request.** Webex returns an elicitation request with an authorization link. Verify the Webex domain, organization, account, and scope before approving.
4. **Return and retry.** Return to Codex after approval. Retry the same prompt, the tool can now continue with the newly authorized scope.

### OAuth authorization code flow (reference only) { #m3-oauth data-toc-label="OAuth code flow (reference)" }

<ol class="flow">
<li><b>AI client</b><span>Starts OAuth using the Client ID</span></li>
<li><b>Webex sign-in</b><span>User signs in and approves scopes</span></li>
<li><b>Redirect URI</b><span>Receives the authorization code</span></li>
<li><b>MCP call</b><span>Uses the resulting access token</span></li>
</ol>

1. **Start authentication.** The client uses the Integration's Client ID and exact redirect URI to begin sign-in.
2. **Sign in and consent.** Webex authenticates the user and displays requested permissions. Approve only the expected organization and scopes.
3. **Complete callback.** Webex returns an authorization code to the registered redirect URI. A mismatch stops the flow.
4. **Use the access token.** The client exchanges the code and sends the resulting bearer token when it calls the Webex MCP server.

<p class="eyebrow">Module 4 · ≈ 15 min</p>

## Configure Codex { #module-4 data-toc-label="Module 4 · Configure Codex" data-task="4" }

This module uses the WCIT generated and stored securely in Module 2, Path A. This is the required hands-on path, you do not need OAuth Integration credentials. Generating the WCIT was Step 1, so continue here with Step 2. Codex supports MCP elicitation, which allows tools to request additional Webex scopes at runtime.

!!! warning "Before you start"
    In Control Hub, confirm that **Webex Messaging** is allowed for all users and that the Messaging tools required for this lab are enabled. If the server or a required tool is disabled, Codex cannot use it even when the local configuration is correct.

### Step 2 · Add the Webex Messaging MCP server { #m4-add data-toc-label="Add the MCP server" }

Codex provides two ways to add the Webex Messaging MCP server. **Choose one option only**: both methods update the same Codex configuration, so you do not need to complete both.

=== "Option 1 · Edit config.toml manually"

    Open or create the user-level Codex configuration file for your platform. Replace `<username>` with your own username.

    <div class="glance" markdown>

    | Platform | Configuration file | Open in a text editor |
    |---|---|---|
    | macOS | `/Users/<username>/.codex/config.toml` (lab example: `/Users/omer/.codex/config.toml`) | `open -e ~/.codex/config.toml` |
    | Windows | `C:\Users\<username>\.codex\config.toml` | `notepad "$env:USERPROFILE\.codex\config.toml"` |

    </div>

    Add the Webex Messaging server block below. Replace `YOUR_WCIT_TOKEN_FROM_PATH_A` with the WCIT you saved in Module 2. Keep the `Bearer` prefix and save the file.

    ```toml title="config.toml"
    [mcp_servers.webex-messaging]
    enabled = true
    url = "https://mcp.webexapis.com/mcp/webex-messaging"
    http_headers = { "Authorization" = "Bearer YOUR_WCIT_TOKEN_FROM_PATH_A" }
    ```

    !!! warning "Important"
        Replace `YOUR_WCIT_TOKEN_FROM_PATH_A` with the WCIT saved in Module 2. Keep the word `Bearer` followed by one space.

    !!! danger "Security note"
        This method stores the WCIT in plain text inside `config.toml`.

=== "Option 2 · Add the MCP server in Codex Settings"

    1. **Open the MCP settings.** In Codex Desktop, open **Settings**, select **Plugins**, and then select the **MCPs** tab.
    2. **Start adding the server.** Select **Add**, then select **Add MCP server**.

        ![Codex Settings > Plugins > MCPs > Add > Add MCP server](img/mcp-24.png){ loading=lazy }

        /// caption
        Codex Settings > Plugins > MCPs > Add > Add MCP server.
        ///

    3. **Enter the connection details.** Use the following values:
        - **Name:** `webex-messaging`
        - **Server type:** Streamable HTTP
        - **URL:** `https://mcp.webexapis.com/mcp/webex-messaging`
        - **Bearer token env var:** leave blank for this lab method.
        - **Header key:** `Authorization`
        - **Header value:** `Bearer YOUR_WCIT_TOKEN_FROM_PATH_A`

        !!! warning "Important"
            Replace `YOUR_WCIT_TOKEN_FROM_PATH_A` with the WCIT saved in Module 2. Keep the word `Bearer` followed by one space.

        ![The Codex MCP server form with the Webex Messaging URL and Authorization header](img/mcp-25.png){ loading=lazy }

        /// caption
        The Codex MCP server form with the Webex Messaging URL and Authorization header.
        ///

    4. **Save and confirm.** Select **Save**, return to the MCPs list, and confirm that the Webex Messaging server is present and enabled.

        ![The Codex MCP server list with Webex Messaging enabled. Your list may contain different entries](img/mcp-26.png){ loading=lazy }

        /// caption
        The Codex MCP server list with Webex Messaging enabled. Your list may contain different entries.
        ///

    !!! danger "Security note for the Settings option"
        The static Authorization header is stored in your local Codex configuration. Use only the temporary lab WCIT, do not include it in screenshots or submitted work, and remove or revoke it after the lab.

### Step 3 · Restart Codex { #m4-restart data-toc-label="Restart Codex" }

After completing either option, restart the Codex app, or fully quit and reopen Codex. This reloads the local MCP configuration.

### Step 4 · Verify discovery { #m4-verify data-toc-label="Verify discovery" }

Confirm that `webex-messaging` is enabled and available. In Codex, run the command below:

```bash
codex mcp list
```

![codex mcp list shows the Webex Messaging server enabled with a bearer token](img/mcp-27.png){ loading=lazy }

/// caption
codex mcp list shows the Webex Messaging server enabled with a bearer token.
///

!!! note "Note"
    If `codex mcp list` doesn't show the list of configured MCP servers, you can ask Codex directly in the chat instead, for example:

    ```text
    Which MCP servers are configured, and is webex-messaging available?
    ```

    You can also type `/mcp` in the Codex chat to see the configured MCP servers and their tools. If `webex-messaging` still isn't listed, check your configuration in [Step 2](#m4-add) and restart Codex again.

### Step 5 · Complete WCIT elicitation { #m4-elicit data-toc-label="Complete WCIT elicitation" }

Run the first read-only prompt. When the WCIT connection needs an additional Webex scope, Webex opens an authorization step as part of elicitation. Verify the Webex domain and requested scope, approve the expected request, return to Codex, and retry the same prompt.

#### Lab example: enable a missing read-only tool

This short exercise shows the difference between connecting an MCP server and allowing a specific tool. The server can be connected correctly while a tool required by the prompt is still disabled in Control Hub.

1. **Run the read-only prompt.** In Codex, enter the following prompt exactly as shown:

    ```text
    Use the `webex-messaging` MCP server. List up to five Webex spaces that I can access.
    Return the space title and space ID only. This is a read-only request.
    Do not create, update, delete, or send anything.
    ```

    !!! note "Note"
        `webex-messaging` is the MCP server name you added in [Step 2](#m4-add). If you gave the server a different name there, in `[mcp_servers.<name>]` in `config.toml` or in the **Name** field in the Codex app, replace `webex-messaging` in this prompt (and the prompts that follow) with your name. This is the server name, not the name of your WCIT token.

2. **Review the result.** In the example below, Codex cannot complete the request because the connected server does not expose a tool for retrieving or searching spaces. No Webex data is changed.

    ![Codex can't list spaces yet: no space-listing tool is enabled](img/mcp-28.png){ loading=lazy }

    /// caption
    Codex can't list spaces yet: no space-listing tool is enabled.
    ///

3. **Check the Control Hub tool policy.** In Control Hub, open **Apps > Agentic apps > Webex Messaging > Tools**, and locate **Get Webex Space**. In the example below, **Allow tool** for "Get Webex Space" is disabled, hence the warning above.

    ![Get Webex Space is disabled in the Tools tab](img/mcp-29.png){ loading=lazy }

    /// caption
    Get Webex Space is disabled in the Tools tab.
    ///

4. **Enable the tool.** Turn on **Allow tool** for "Get Webex Space". For this lab, also turn on **Allow signature change** so approved changes to the tool input or output schema can be accepted.

    ![Get Webex Space enabled, with Allow signature change on](img/mcp-30.png){ loading=lazy }

    /// caption
    Get Webex Space enabled, with Allow signature change on.
    ///

5. **Save.** Select **Save** in Control Hub.
6. **Restart Codex and run the prompt again.** If Webex requests an additional scope, complete the elicitation and authorization flow below.

    !!! danger "Important: don't run Codex in Full access mode"
        Before you run the prompt again, make sure Codex is set to **Ask for approval**, not **Full access** (approval policy *never*). In Full access mode, Codex can't show you the Webex authorization request, so it cancels it automatically, and you'll see an error like:

        ```text
        I couldn't list the spaces because Webex OAuth authorization was cancelled.
        ```

        **To fix it:** in the Codex app, click the approval button at the bottom left of the message box (it shows the current mode) and select **Ask for approval**, as shown below. In the Codex CLI, type `/approvals` and choose an option that asks, or start Codex with `codex -a on-request`. Then run the prompt again: this time Codex shows the **OAuth Authorization Required** request so you can approve it.

        ![Codex approval modes: select Ask for approval, not Full access](img/mcp-37.png){ loading=lazy }

        /// caption
        Codex approval modes: select Ask for approval, not Full access.
        ///

7. **Review the elicitation request.** Codex displays an **OAuth Authorization Required** request. Confirm that the tool is `webex-get-space` and that the requested scope is `spark:rooms_read`.

    ![Codex shows OAuth Authorization Required for webex-get-space and spark:rooms_read](img/mcp-31.png){ loading=lazy }

    /// caption
    Codex shows OAuth Authorization Required for webex-get-space and spark:rooms_read.
    ///

8. **Open the Webex authorization page.** Codex displays an **Authorize access through Webex** link. Select the link. A browser page opens, if you are asked to sign in, enter the lab administrator credentials provided for your environment.

    ![Codex links to Authorize access through Webex](img/mcp-32.png){ loading=lazy }

    /// caption
    Codex links to Authorize access through Webex.
    ///

9. **Review and accept the requested permissions.** After sign-in, Webex shows the permissions requested by the MCP tool. Confirm that the request is for listing the titles of spaces you can access and for accessing MCP servers, then select **Accept**.

    ![The Webex consent page lists the requested permissions](img/mcp-33.png){ loading=lazy }

    /// caption
    The Webex consent page lists the requested permissions.
    ///

10. **Complete the browser flow.** When the **You're all set!** confirmation appears, select **Return to Agent**. If the browser does not return automatically, close the browser tab and return to Codex.

    ![You're all set! Select Return to Agent](img/mcp-34.png){ loading=lazy }

    /// caption
    You're all set! Select Return to Agent.
    ///

11. **Continue in Codex.** In the same Codex task, follow the instructions or enter `authorization done` and submit it.

    ![Tell Codex the authorization is done](img/mcp-35.png){ loading=lazy }

    /// caption
    Tell Codex the authorization is done.
    ///

12. **Confirm the result.** Codex can now use Webex Messaging to list up to five spaces available to the signed-in lab account and return only each space title and space ID. This remains a read-only operation.

    ![Codex lists space titles and space IDs](img/mcp-36.png){ loading=lazy }

    /// caption
    Codex lists space titles and space IDs.
    ///

!!! note
    The space titles and space IDs shown in this example are from a different environment. Your results and IDs will be different.

<p class="eyebrow">Module 5 · ≈ 20 min</p>

## Messaging prompts { #module-5 data-toc-label="Module 5 · Messaging prompts" data-task="5" }

Now that the Webex Messaging MCP is configured and authorized, use the prompts below to test some common messaging tasks. These are only examples, you can also create your own prompts to explore the MCP. **Start with read-only requests**, and use only the dedicated lab space for prompts that create, edit, delete, or send content.

!!! note "Use your own space name"
    In every prompt, replace `MCP Lab - <your name>` with the exact title of a Webex space you can access that contains messages. It can be a space you created for the lab or another existing space.

### Exercise 1 · Find the space { #m5-ex1 data-toc-label="Ex 1 · Find the space" }

```text
Use Webex Messaging. Find the space named "MCP Lab - <your name>".
Return the exact space title and its ID. Do not send, edit, or delete anything.
```

**Expected result:** one matching lab space is identified. If several spaces match, the client asks you to choose, it must not guess.

### Exercise 2 · Summarize recent messages { #m5-ex2 data-toc-label="Ex 2 · Summarize messages" }

```text
In the Webex space "MCP Lab - <your name>", list the 10 most recent messages.
Summarize the discussion in five bullets and show author and timestamp for each source message.
Do not send, edit, or delete anything.
```

**Expected result:** a grounded summary using only messages returned by the MCP tool.

### Exercise 3 · Search for a decision { #m5-ex3 data-toc-label="Ex 3 · Search for a decision" }

```text
Search the Webex space "MCP Lab - <your name>" for messages containing "decision"
from the last 30 days. State the decision, owner, due date, and any ambiguity.
Include message IDs or timestamps. Do not modify Webex.
```

**Expected result:** an evidence-backed answer or a clear statement that no matching message was found.

### Exercise 4 · Draft only { #m5-ex4 data-toc-label="Ex 4 · Draft only" }

```text
Draft a concise reply to the latest message in "MCP Lab - <your name>".
Show the target space and exact draft. Do not send it.
```

**Expected result:** the client returns text only and does not call a message creation tool.

### Exercise 5 · Controlled write { #m5-ex5 data-toc-label="Ex 5 · Controlled write" }

```text
Prepare to send exactly this message to "MCP Lab - <your name>":
"Webex MCP lab validation complete."
Before sending, show the resolved space title, space ID, and exact message, then ask for my confirmation.
Do not send until I explicitly confirm.
```

!!! warning "Write actions"
    This is the only exercise that changes Webex. Make sure **Create Webex Message** is enabled in Control Hub, check the resolved space and message, and confirm only when they are correct.

<p class="eyebrow">Module 6 · ≈ 5 min</p>

## Summary and next steps { #module-6 data-toc-label="Module 6 · Summary" data-task="6" }

This concludes the Webex Messaging MCP lab. You have approved the server in Control Hub, connected Codex with a WCIT, completed an elicitation request, and tested messaging tools. The connection is straightforward: enable the server, choose the tools, add its URL and credential to the client, then approve the scopes needed for the action you request.

Control Hub is the **governance and control layer** for this MCP orchestration. Administrators decide who can use a server, which tools are available, and whether changes to tool definitions need review. Codex handles the conversation and invokes the approved tools, Webex still checks the granted scopes and the signed-in user's permissions.

To explore Webex Meetings MCP, follow the same setup pattern with the Webex Meeting server: allow it in Control Hub, review and enable the Meeting tools you need, and use the Meeting server URL in your Codex MCP entry. When a tool needs another scope, complete the authorization request. Use the same approach for other Webex MCP servers, checking each server's own URL, tools, scopes, and prerequisites.

For current server details, see the [Webex Meetings MCP Server guide](https://developer.webex.com/mcp/docs/meetings-mcp-server){:target="_blank" rel="noopener"} and the [AI in Webex overview](https://developer.webex.com/mcp/docs/ai-in-webex){:target="_blank" rel="noopener"} on the Webex Developer Portal.

<p class="eyebrow">Module 7 · ≈ 10 min</p>

## Troubleshooting and cleanup { #module-7 data-toc-label="Module 7 · Troubleshoot & clean up" data-task="7" }

### Troubleshooting decision table { #m7-table data-toc-label="Troubleshooting table" }

<div class="glance" markdown>

| Symptom | Likely cause | Check and recovery |
|---|---|---|
| Server does not connect | Wrong endpoint, blocked HTTPS, or server not enabled | Compare the endpoint character for character, test network access, ask the Control Hub administrator to verify Agentic Apps policy |
| 401 or not authenticated | Missing, expired, revoked, or malformed credential | Verify the WCIT in the configured Authorization header, never paste it into chat, restart Codex |
| Tool asks for permission | Expected WCIT elicitation | Verify the Webex URL and requested scope, approve only the expected scope, return and retry |
| "Webex OAuth authorization was cancelled" | Codex is in **Full access** mode (approval policy *never*), so it cancels the Webex authorization request automatically | Switch Codex to **Ask for approval** (the approval button at the bottom left of the message box in the app, or `/approvals` / `codex -a on-request` in the CLI), then run the prompt again and approve the request |
| Tools are missing | Tool disabled, scope absent, or user outside policy | Check Control Hub Tools, granted scopes, and signed-in account, reconnect after changes |
| OAuth Integration redirect mismatch (reference only) | Integration URI differs from client callback | For the optional reference path, make the scheme, hostname, port, path, and trailing slash identical, then authenticate again |
| Wrong space selected | Ambiguous name resolved incorrectly | Stop. Display the exact space ID, use a unique lab space, require confirmation |

</div>

### Cleanup checklist { #m7-cleanup data-toc-label="Cleanup checklist" }

- [ ] Remove the WCIT from the Authorization header in `config.toml`, or remove the temporary `webex-messaging` server block if your instructor does not want it retained.
- [ ] Revoke the lab WCIT in the Webex Developer Portal when instructed, and delete any temporary local copy of the token.
- [ ] Remove a temporary connector or MCP server entry.

<p class="eyebrow">Appendix A</p>

## Quick reference { #appendix data-toc-label="Appendix A · Quick reference" }

<div class="glance" markdown>

| Item | Messaging | Meetings |
|---|---|---|
| Endpoint | `https://mcp.webexapis.com/mcp/webex-messaging` | `https://mcp.webexapis.com/mcp/webex-meeting` |
| Primary use | Spaces, messages, memberships, files, webhooks | Schedules, participants, summaries, recordings, transcripts |
| Codex auth | WCIT plus elicitation | WCIT plus elicitation |
| Content prerequisite | Dedicated space with sample messages | Eligible meeting, recording, transcript, and AI Assistant as needed |

</div>

#### Guide scope

The hands-on exercises use Webex Messaging in Codex with a WCIT. Other AI clients and the OAuth Integration path are included for reference only. Screens may look slightly different depending on the account, operating system, Codex release, and organization policy.

<p class="eyebrow">Up next · Part 3</p>

## What's next { #next data-toc-label="Next · Part 3 (GenAI lab)" }

You've connected Webex Messaging to an AI client through MCP. In Part 3 you go one level deeper and build AI-powered messaging workflows yourself, with LangChain and the Webex APIs.

<a class="next-card" href="../part-3/">
  <span class="nc-k">Part 3 · Lab guide</span>
  <span class="nc-t">Building AI-Powered Messaging with LangChain &amp; Webex</span>
  <span class="nc-u">Part 3 →</span>
</a>
