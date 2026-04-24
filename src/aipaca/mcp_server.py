from fastmcp import FastMCP
import alpaca
from aipaca.schemas import alpcouplings_schema
import json

mcp = FastMCP(
    name = "AIPaca MCP Server",
    instructions="AIPaca MCP Server provides help with ALP-aca for the phenomenology of Axion-Like Particles (ALPs).",
)

@mcp.tool(
    name="aipaca-read-alp-couplings",
    description="Read an ALP couplings file and return the data as a structured object.",
    output_schema=alpcouplings_schema.ALPcouplingsBase.model_json_schema()
)
def read_file(file_path: str) -> alpcouplings_schema.ALPcouplingsBase:
    with open(file_path, "r") as f:
        data = json.load(f, cls=alpaca.ALPcouplingsDecoder)
    if isinstance(data, alpaca.ALPcouplings):
        return alpcouplings_schema.parse_ALPcouplings(data)
    else:
        raise ValueError("The provided file does not contain valid ALP couplings data.")
    
@mcp.tool(
    name="aipaca-write-alp-couplings",
    description="Write ALP couplings data to a file."
)
def write_file(file_path: str, data: alpcouplings_schema.ALPcouplingsBase):
    with open(file_path, "w") as f:
        json.dump(data.to_ALPcouplings(), f, cls=alpaca.ALPcouplingsEncoder)


@mcp.tool(
    name='aipaca-rgevolve-alp-couplings',
    description='Evolve ALP couplings to another energy scale (in GeV) using renormalization group equations (RGEs).',
    output_schema=alpcouplings_schema.ALPcouplingsBase.model_json_schema()
)
def rgevolve_alp_couplings(couplings: alpcouplings_schema.ALPcouplingsBase, final_scale: float, final_basis: str) -> alpcouplings_schema.ALPcouplingsBase:
    alp_couplings = couplings.to_ALPcouplings()
    evolved_couplings = alp_couplings.match_run(final_scale, final_basis)
    return alpcouplings_schema.parse_ALPcouplings(evolved_couplings)

def main():
    print("Welcome to the AIPaca MCP Server!")
    #mcp.run(transport='http', host='127.0.0.1', port=9000)
    mcp.run()


if __name__ == "__main__":
    main()
