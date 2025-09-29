# Pingblender CPG&copy; [A2A Workflows] - Analytics, Marketing, Advertising
Full stack application to present a ready infrastructure for use with evolving AI and pattern standards. The broad field controls and human-in-the-loop layout assures that the 23Controls Agents carry out management and control of the data it uses throughout the profile lifetime. 

## CURRENT UNIT [TRL3]
<div align="center">
<strong>Pingblender CPG - Running DEMO</strong>
[![PyPI][pypi-badge]][pypi-url]
[![MIT licensed][mit-badge]][mit-url]
[![Python Version][python-badge]][python-url]
[![Documentation][docs-badge]][docs-url]
[![Specification][spec-badge]][spec-url]
[![GitHub Discussions][discussions-badge]][discussions-url]
</div>

### Case 1: CPG Brand Coverage for Marketing Collateral Workflows &amp; Personalization
Pingblender CPG is the solution to the complex mess of transformation and coordination that takes place over the lifecycle of the message economy surrounding popular products and incentives. Quickly handle approval via workflow agents and leverage capacities of expertise informed ‘Agents’ to carry out functions interpreting the CPG economy in one or many product flagships, across the world. Make personalization relevant nuancing messaging with regional dialects, while targeting attributes to hydrate the RAG.


### Demonstration Link (Video)
HERE:  https://www.loom.com/share/1116236865044bb7b690d39de4b1b167?sid=fa7a561a-8a5d-45aa-8b9a-9cefde57217a


## Containerized/Dockerized LOCAL Installation

### Core Signals Container Stack 
The local interface for Pingblender is built on the SynthetIQ Signals framework and our 23Controls&reg;
From a Docker enabled command line you can deploy the stack which includes:
- Python 3.13 | FastAPI Endpoint 
- Anthropic MCP SDK (integrated)
- PGVector (Deployed as PGV16 - with POSTGRESQL)
- OpenAI, Groq &amp; Federal Reserve Bank of St. Louis
- N8N Canvas for workflow deployments/orchestration
- MCP Auth &amp; Chat units for running from CMD
- NEO4j Composite Graph DB 
- Hashicorp Terraform INFRA Deployment (Commercial License Required)

### Configure AWS & Docker Access
If you intend to use the platform deployment in some commercial capacity, you'll need to use the licensed version of the technology which relies on having access to DockerHUb and a private IAM for the endpoint. In these cases, you can supply a AWS token in your ENV file. 

### Run Local with Dock
```bash
docker-compose up -d --build 
```

The OOTB Pingblender containierized platform is enhanced with a series of upgradeable functions. The deployment is slow during first builds, as it covers a body of extendable features to expedite access and accelerate dev cycles for those who are just jumping in. 

## Separately Activate MCP Server for AUTH/Chat
In order to run Agents within N8N, they need to be started manually in the instructions set below for any purpose. 

### Start MCP Server (Generic)
```bash
cd signals/module/mcp/server
uv run mcp
```

### Start individual services
```bash
uv run [service] --[port=####] #name in pyproject.toml
```


