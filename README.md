# AI-Powered Lead Qualification System

[![CI](https://github.com/your-repo/lead-qualification-system/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/your-repo/lead-qualification-system/actions/workflows/unit-tests.yml)
[![Integration Tests](https://github.com/your-repo/lead-qualification-system/actions/workflows/integration-tests.yml/badge.svg)](https://github.com/your-repo/lead-qualification-system/actions/workflows/integration-tests.yml)
[![Open in - LangGraph Studio](https://img.shields.io/badge/Open_in-LangGraph_Studio-00324d.svg?logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI4NS4zMzMiIGhlaWdodD0iODUuMzMzIiB2ZXJzaW9uPSIxLjAiIHZpZXdCb3g9IjAgMCA2NCA2NCI+PHBhdGggZD0iTTEzIDcuOGMtNi4zIDMuMS03LjEgNi4zLTYuOCAyNS43LjQgMjQuNi4zIDI0LjUgMjUuOSAyNC41QzU3LjUgNTggNTggNTcuNSA1OCAzMi4zIDU4IDcuMyA1Ni43IDYgMzIgNmMtMTIuOCAwLTE2LjEuMy0xOSAxLjhtMzcuNiAxNi42YzIuOCAyLjggMy40IDQuMiAzLjQgNy42cy0uNiA0LjgtMy40IDcuNkw0Ny4yIDQzSDE2LjhsLTMuNC0zLjRjLTQuOC00LjgtNC44LTEwLjQgMC0xNS4ybDMuNC0zLjRoMzAuNHoiLz48cGF0aCBkPSJNMTguOSAyNS42Yy0xLjEgMS4zLTEgMS43LjQgMi41LjkuNiAxLjcgMS44IDEuNyAyLjcgMCAxIC43IDIuOCAxLjYgNC4xIDEuNCAxLjkgMS40IDIuNS4zIDMuMi0xIC42LS42LjkgMS40LjkgMS41IDAgMi43LS41IDIuNy0xIDAtLjYgMS4xLS44IDIuNi0uNGwyLjYuNy0xLjgtMi45Yy01LjktOS4zLTkuNC0xMi4zLTExLjUtOS44TTM5IDI2YzAgMS4xLS45IDIuNS0yIDMuMi0yLjQgMS41LTIuNiAzLjQtLjUgNC4yLjguMyAyIDEuNyAyLjUgMy4xLjYgMS41IDEuNCAyLjMgMiAyIDEuNS0uOSAxLjItMy41LS40LTMuNS0yLjEgMC0yLjgtMi44LS44LTMuMyAxLjYtLjQgMS42LS41IDAtLjYtMS4xLS4xLTEuNS0uNi0xLjItMS42LjctMS43IDMuMy0yLjEgMy41LS41LjEuNS4yIDEuNi4zIDIuMiAwIC43LjkgMS40IDEuOSAxLjYgMi4xLjQgMi4zLTIuMy4yLTMuMi0uOC0uMy0yLTEuNy0yLjUtMy4xLTEuMS0zLTMtMy4zLTMtLjUiLz48L3N2Zz4=)](https://langgraph-studio.vercel.app/templates/open?githubUrl=https://github.com/your-repo/lead-qualification-system)

This project aims to solve the challenges of sales prospecting by creating an AI-powered lead qualification system. It leverages LangGraph's powerful agent frameworks to automate the enrichment and scoring of leads, ensuring a scalable and cost-effective solution for modern sales teams.

![Graph view in LangGraph studio UI](./static/studio_ui.png)

---

## Features

The lead qualification system:

1. Processes raw lead data from CSV or JSON files.
2. Enriches data using AI agents customized to analyze companies and personas.
3. Qualifies leads based on Ideal Customer Profiles (ICP) and buyer personas.
4. Outputs enriched and scored leads in JSON format for further use in sales outreach tools.

## Getting Started

### Prerequisites

1. Install [LangGraph Studio](https://github.com/langchain-ai/langgraph-studio).
2. Set up a `.env` file with the required API keys:

```bash
cp .env.example .env
```

### Steps

1. Define your ICP and buyer personas in the configuration file.
2. Provide the initial lead data in CSV or JSON format.
3. Customize and extend the agent logic in `src/agent/graph.py` to fit your specific requirements.
4. Open the project in LangGraph Studio and start processing leads.

---

## Customization

1. **Modify ICP and Buyer Personas**: Update the criteria for lead qualification in `src/configuration.py` to align with your sales strategy.
2. **Extend AI Agent Logic**: Modify `src/agent/graph.py` to include additional research nodes, enrich data further, or implement custom scoring logic.
3. **Integrate APIs**: Add APIs for additional data enrichment, such as social media or industry-specific insights.

---

## Development Workflow

- **Iterate and Debug**: Use LangGraph Studio to edit and test individual graph nodes.
- **Hot Reload**: Apply local changes and see results immediately.
- **Enhance Capabilities**: Add new tools or logic for dynamic lead handling and scoring.

---

## Challenges

- Customizing AI agents to meet specific qualification criteria.
- Ensuring data accuracy and relevance for enriched outputs.
- Integrating and harmonizing multiple data sources.

---

## Benefits

- **Increased Efficiency**: Automates lead qualification, saving time and resources.
- **Improved Accuracy**: Leverages data-driven approaches to prioritize high-value leads.
- **Scalable Solution**: Reduces reliance on expensive third-party tools and scales with lead volume.

---

## Conclusion

This project is designed to revolutionize lead qualification workflows by combining AI-powered agents with customizable logic. By automating data enrichment and scoring, it provides a scalable, efficient, and accurate solution tailored to your sales needs. Begin your journey by setting up the system and customizing it to your unique ICP and buyer personas!
