import logging
from typing import Any, Sequence, Callable, Dict, List, Mapping, Optional, Union, cast

from opensearchpy import OpenSearch 
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

from langchain_opensearch.client import create_opensearch_client
logger = logging.getLogger(__name__)

class OpenSearchRetriever(BaseRetriever):
    """OpenSearch Retriever."""

    client: OpenSearch
    index_name: Union[str, Sequence[str]]
    body_func: Callable[[str], Dict]
    content_field: Optional[Union[str, Mapping[str,str]]] = None
    document_mapper : Optional[Callable[[Mapping], Document]] = None

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

        if self.content_field is None and self.document_mapper is None:
            raise ValueError("Either content_field or document_mapper must be provided")

        if self.content_field is not None and self.document_mapper is not None:
            raise ValueError("Only one of content_field or document_mapper can be provided")

        if not self.document_mapper:
            self.document_mapper = self._single_field_mapper
        elif isinstance(self.content_field, Mapping):
            self.document_mapper = self._multi_field_mapper
        else:
            raise ValueError("content_field must be a string or a mapping")

        # self.os_client = create_opensearch_client(**kwargs)

    @staticmethod
    def from_os_params(
        index_name: Union[str, Sequence[str]],
        body_func: Callable[[str], Dict],
        content_field: Optional[Union[str, Mapping[str,str]]] = None,
        document_mapper: Optional[Callable[[Mapping], Document]] = None,
        url : Optional[str] = None,
        cloud_id : Optional[str] = None,
        api_key : Optional[str] = None,
        username : Optional[str] = None,
        password : Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        ) -> "OpenSearchRetriever":
        client = create_opensearch_client(url=url, cloud_id=cloud_id, api_key=api_key, username=username, password=password, params=params)
        return OpenSearchRetriever(client=client, index_name=index_name, body_func=body_func, content_field=content_field, document_mapper=document_mapper)

    def _get_relevant_documents(self, query: str, *, run_manager: CallbackManagerForRetrieverRun) -> List[Document]:
        if not self.client or not self.document_mapper:
            raise ValueError("OpenSearch client or document mapper is not initialized")

        body = self.body_func(query)
        response = self.client.search(index=self.index_name, body=body)
        return [self.document_mapper(hit) for hit in response["hits"]["hits"]]

    def _single_field_mapper(self, hit: Mapping[str, Any]) -> Document:
        content = hit["_source"].pop(self.content_field)
        return Document(page_content=content, metadata=hit)

    def _multi_field_mapper(self, hit: Mapping[str, Any]) -> Document:
        self.content_field = cast(Mapping, self.content_field)
        field = self.content_field[hit["_index"]]
        content = hit["_source"].pop(field)
        return Document(page_content=content, metadata=hit)
