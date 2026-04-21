from fastmcp import FastMCP
import alpaca
from aipaca.schemas import alpcouplings_schema
import json

mcp = FastMCP(
    name = "AIPaca MCP Server",
    instructions="AIPaca MCP Server provides help with ALP-aca for the phenomenology of Axion-Like Particles (ALPs).",
)

@mcp.tool(description="Read an ALP couplings file and return the data as a structured object.")
def read_file(file_path: str) -> alpcouplings_schema.ALPcouplingsBase:
    with open(file_path, "r") as f:
        data = json.load(f, cls=alpaca.ALPcouplingsDecoder)
    if isinstance(data, alpaca.ALPcouplings):
        return alpcouplings_schema.parse_ALPcouplings(data)


if __name__ == "__main__":
    mcp.run(transport='http', host='127.0.0.1', port=9000)