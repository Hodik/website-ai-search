from llama_index.core import Settings, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from transformers import AutoTokenizer
from llama_index.readers.file import UnstructuredReader
from llama_index.core.retrievers import VectorIndexRetriever
from html_reader import HTMLReader
from llama_index.core.schema import NodeWithScore

# set tokenizer to match LLM
Settings.tokenizer = AutoTokenizer.from_pretrained("NousResearch/Llama-2-7b-chat-hf")

# set the embed model
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")


def search(url: str, html: str, query: str) -> list[NodeWithScore]:
    documents = HTMLReader().load_data(html=html, url=url, split_documents=True)
    index = VectorStoreIndex.from_documents(
        documents,
    )

    # configure retriever
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=10,
    )

    retrieved_documents = retriever.retrieve(query)
    print(f"Retrieved {retrieved_documents} documents")
    for i, document in enumerate(retrieved_documents):
        original_text = document.get_text()
        print(f"{i=}, {document.score=}, {original_text=}")

    return retrieved_documents
