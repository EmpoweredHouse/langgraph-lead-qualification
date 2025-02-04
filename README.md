# AI-Powered Lead Qualification System

[![Open in - LangGraph Studio](https://img.shields.io/badge/Open_in-LangGraph_Studio-00324d.svg?logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI4NS4zMzMiIGhlaWdodD0iODUuMzMzIiB2ZXJzaW9uPSIxLjAiIHZpZXdCb3g9IjAgMCA2NCA2NCI+PHBhdGggZD0iTTEzIDcuOGMtNi4zIDMuMS03LjEgNi4zLTYuOCAyNS43LjQgMjQuNi4zIDI0LjUgMjUuOSAyNC41QzU3LjUgNTggNTggNTcuNSA1OCAzMi4zIDU4IDcuMyA1Ni43IDYgMzIgNmMtMTIuOCAwLTE2LjEuMy0xOSAxLjhtMzcuNiAxNi42YzIuOCAyLjggMy40IDQuMiAzLjQgNy42cy0uNiA0LjgtMy40IDcuNkw0Ny4yIDQzSDE2LjhsLTMuNC0zLjRjLTQuOC00LjgtNC44LTEwLjQgMC0xNS4ybDMuNC0zLjRoMzAuNHoiLz48cGF0aCBkPSJNMTguOSAyNS42Yy0xLjEgMS4zLTEgMS43LjQgMi41LjkuNiAxLjcgMS44IDEuNyAyLjcgMCAxIC43IDIuOCAxLjYgNC4xIDEuNCAxLjkgMS40IDIuNS4zIDMuMi0xIC42LS42LjkgMS40LjkgMS41IDAgMi43LS41IDIuNy0xIDAtLjYgMS4xLS44IDIuNi0uNGwyLjYuNy0xLjgtMi45Yy01LjktOS4zLTkuNC0xMi4zLTExLjUtOS44TTM5IDI2YzAgMS4xLS45IDIuNS0yIDMuMi0yLjQgMS41LTIuNiAzLjQtLjUgNC4yLjguMyAyIDEuNyAyLjUgMy4xLjYgMS41IDEuNCAyLjMgMiAyIDEuNS0uOSAxLjItMy41LS40LTMuNS0yLjEgMC0yLjgtMi44LS44LTMuMyAxLjYtLjQgMS42LS41IDAtLjYtMS4xLS4xLTEuNS0uNi0xLjItMS42LjctMS43IDMuMy0yLjEgMy41LS41LjEuNS4yIDEuNi4zIDIuMiAwIC43LjkgMS40IDEuOSAxLjYgMi4xLjQgMi4zLTIuMy4yLTMuMi0uOC0uMy0yLTEuNy0yLjUtMy4xLTEuMS0zLTMtMy4zLTMtLjUiLz48L3N2Zz4=)](https://langgraph-studio.vercel.app/templates/open?githubUrl=https://github.com/your-repo/lead-qualification-system)

## **Overview**

🚧 **Project Status: In Progress** 🚧

This project aims to solve a critical challenge in sales prospecting: **time loss during lead qualification**. The idea is simple – given some initial lead information collected from another process, the system uses AI-powered agents to evaluate whether the lead is worth pursuing. It applies techniques like **BANT (Budget, Authority, Need, Timing)** and **SPIN (Situation, Problem, Implication, Need-payoff)** to assess whether the lead fits the Ideal Customer Profile (ICP) and buyer persona. Leads receive a score along with a reasoning summary, helping sales teams prioritize efficiently.

The scenario where this AI agent shines is **scraping content from technical conferences** to identify relevant people or companies to engage with. This bot not only saves time but also **reduces costs** by allowing the sales team to focus primarily on high-potential leads.

In the future, the system will be extended beyond structured lead data. The idea is to **leverage tools like Apollo** to enrich and qualify leads before scoring them and generating a personalized message for outreach.

**Current Capabilities:**

- Automated lead enrichment
- AI-based lead qualification
- Assigns lead scores with reasoning

**Planned Features:**

- Full research from minimal input (name or company)
- Automated outreach message generation
- CRM and real-time data integrations



---

## **System Architecture**

### **How It Works**

1. **Input Data**: The system ingests **Company Research Data (JSON format)** containing all information retrieved from other tools, as well as ICP and Buyer Persona details.
2. **Lead Qualification Agent**: Based on the provided data, the agent checks if it can perform qualification. If some information is missing, it attempts additional web research to retrieve the missing parts. This process repeats until it reaches a satisfactory answer or a configurable loop limit.
3. **Lead Scoring and Reasoning**: Once all necessary data is gathered, the system scores the lead and provides reasoning for the decision.

### **Current AI Agents**

- **Lead Qualification Agent** – The primary agent responsible for scoring leads based on ICP and persona criteria.
- **Company Researcher Agent** – A copy of [Langchain-AI's company researcher](https://github.com/langchain-ai/company-researcher), responsible for fetching company-related data. It will be merged with other agents in the future to enhance capabilities.
- **People Researcher Agent** – A copy of [Langchain-AI's people researcher](https://github.com/langchain-ai/people-researcher), gathering professional details about individuals. It will also be integrated into a unified agent for more advanced research.

### **Flowchart**

![Graph view in LangGraph studio UI](./static/studio_ui.png)

---

## **Lead Scoring Breakdown**

| Score | Qualification Level | Description                                   |
| ----- | ------------------- | --------------------------------------------- |
| 1-3   | Low Fit             | Minimal alignment with ICP and buyer persona. |
| 4-6   | Medium Fit          | Partial alignment; further review needed.     |
| 7-10  | High Fit            | Strong alignment; ideal lead for outreach.    |

---

## **Roadmap**

✔️ **Current Features:**

- Automated lead enrichment
- AI-based lead qualification
- LangGraph Studio support

🚀 **Planned Features:**

- CRM auto-sync
- Real-time lead scoring dashboard
- Multi-language support
