import os
from typing import List
from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
    TextLoader,
)
from langchain_core.documents import Document


def load_document(file_path: str) -> List[Document]:

    """ 
    
    Load a document from the specified file path with different loaders based on file type 
    and return it as a list of Document objects. 

    """

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return PyPDFLoader(file_path).load()

    elif ext in [".doc", ".docx"]:
        return UnstructuredWordDocumentLoader(file_path).load()

    elif ext == ".txt":
        return TextLoader(file_path, encoding="utf-8").load()

    else:
        raise ValueError(f"Unsupported file type: {ext}")
