from pathlib import Path
from typing import Any, Dict, List, Optional

from llama_index.core.readers.base import BaseReader
from llama_index.core.schema import Document

from unstructured.partition.auto import partition
from unstructured.partition.html import partition_html


class HTMLReader(BaseReader):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Init params."""
        super().__init__(*args)  # not passing kwargs to parent bc it cannot accept it
        import nltk

        nltk.download("punkt")
        nltk.download("averaged_perceptron_tagger")

    def load_data(
        self,
        html: str | None = None,
        url: str | None = None,
        extra_info: Optional[Dict] = None,
        split_documents: Optional[bool] = True,
    ) -> List[Document]:

        if html:
            elements = partition_html(
                text=html,
                include_page_breaks=False,
                encoding=None,
                languages=None,
                detect_language_per_element=False,
            )
        elif url:
            elements = partition_html(
                url=url,
                include_page_breaks=False,
                encoding=None,
                languages=None,
                detect_language_per_element=False,
            )
        docs = []
        if split_documents:
            for node in elements:
                metadata = {}
                if hasattr(node, "metadata"):
                    """Load metadata fields"""
                    for field, val in vars(node.metadata).items():
                        if field == "_known_field_names":
                            continue
                        # removing coordinates because it does not serialize
                        # and dont want to bother with it
                        if field == "coordinates":
                            continue
                        # removing bc it might cause interference
                        if field == "parent_id":
                            continue
                        metadata[field] = val

                if extra_info is not None:
                    metadata.update(extra_info)

                docs.append(Document(text=node.text, extra_info=metadata))

        else:
            text_chunks = [" ".join(str(el).split()) for el in elements]

            metadata = {}

            if extra_info is not None:
                metadata.update(extra_info)

            # Create a single document by joining all the texts
            docs.append(Document(text="\n\n".join(text_chunks), extra_info=metadata))

        return docs
