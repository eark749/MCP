from ast import Return
from dataclasses import field
import json
from mcp.server.fastmcp import FastMCP
from pydantic import Field
from mcp.server.fastmcp.prompts import base 

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

def edit_document(
    doc_id:str = Field(description="id of the document tht will be edited"),
    old_str:str = Field(description="the text to replace. must match exaclty, including whitespace"),
    new_str:str = Field(description="the new text to insert instead of old text")
):
    if doc_id not in docs:
        raise ValueError(f"doc id with {doc_id} not found")
    docs[doc_id] = docs[doc_id].replace(old_str, new_str)


@mcp.resource(
    "docs://documents",
    mime_type= "application/json"
)
def list_docs() -> list[str]:
    return list(docs.keys())

@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain"
)
def fetch_doc(doc_id:str) -> str:
    if doc_id not in docs:
        raise ValueError (f" doc with {doc_id} not found")
    return docs[doc_id]


@mcp.prompt(
    name = "format",
    description="rewrites the content of the document in the markdown format"
)
def format_document(
    doc_id=Field(description="id of the docuemnt to be formatted")
) -> list[base.Message]:
    prompt = f"""
        Your goal is to reformat a document to be written with markdown syntax.

        The id of the document you need to reformat is:
        <document_id>
        {doc_id}
        </document_id>

        Add in headers, bullet points, tables, etc as necessary. Feel free to add in structure.
        Use the 'edit_document' tool to edit the document. After the document has been reformatted...
        """
    return [base.UserMessage(prompt)]
    



if __name__ == "__main__":
    mcp.run(transport="stdio")
