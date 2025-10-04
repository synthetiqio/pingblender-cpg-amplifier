# Pingblender CPG Models (Graffiti)
Commercial Consumer Packaged Goods (CPG) RAG based agents and agentic framework components. 
PB CPG handles diverse ingest of data for a variety of case and purposes. 

## Setting Pingblender Up:
- Create a .env file and use the example set from the base repo to get started. 
- When the subscription kicks in for licensed users, you'll need to leverage the vault.

### Running Individual Components

To run the Anthropic MCP Server
```bash 
    cd /signals/module/mcp
    uv run mcp --port=9001
```
This will create a virtual environment with a working MCP pattern server for any individual MCP conforming agent, assistant, or A2A workflow which you would like to enable. Once available, you should be able to mount and run several types of integrated AI units for a variety of purposes. 

#### This MFE unit is intended to run in the SynthetIQ Signals&reg; Graffiti AI Amplifier.
The frontend application can be run here or build/run as a MFE in single-spa style. 
When deploying, the files and pipeline are set up to make a version of the script available for testing and running. It will be published within the operational mfe path:

<strong>Example structure:</strong> <url>/mfe/<package.name>

*Local MFE or MCP testing*

You need:
A version of the application or another application running in the parent MFE setup:

```bash 
    npm run dev:parent 
```

You can run another versino of the app as a child:
```bash 
    npm run watch:child
```
