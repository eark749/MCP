from dataclasses import field
from mcp.server.fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

# TODO: Write a tool to read a doc
@mcp.tool(
    name = "read_docs",
    description="it reads the document"
)

def read_docs(
    doc_id = Field(description="id of the document to read")
):
    if doc_id not in docs:
        raise ValueError (f"document with{doc_id} not found")
    else:
        return docs[doc_id]

# TODO: Write a tool to edit a doc
@mcp.tool(
    name="edit_docs",
    description="edits a document"
)

def edit_doc(
    doc_id:str = Field(description="id of the document tht will be edited"),
    old_str:str = Field(description="the text to replace. must match exaclty, including whitespace")
)

# TODO: Write a resource to return all doc id's
# TODO: Write a resource to return the contents of a particular doc
# TODO: Write a prompt to rewrite a doc in markdown format
# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
