from collections import defaultdict
from time import sleep
import os
from dotenv import load_dotenv
import json
import httpx
import requests
from rag_sdk.core import RAGCore

load_dotenv()


class ESGAIChat:
    VECTORDB_URI = f'{os.environ.get("VECTORDB_HOST")}:{os.environ.get("VECTORDB_PORT")}'
    RAG_CORE = RAGCore(vector_database_uri=VECTORDB_URI, collection_list=["greenhousegas"])

    def __init__(self):
        self.default_custom_topk = 2
        self.default_temperature = 0.1
        self.default_max_tokens = 4096
        self.default_streaming = True
        self.default_retries = 3
        self.default_timeout = 90
        self.default_wait_seconds = 0.5

    def chat(self, query, **kwargs) -> object:
        kwargs = defaultdict(lambda: None, kwargs)
        request_data = {
            "vector_database_uri": kwargs["vector_database_uri"] or self.VECTORDB_URI,
            "chain_category": "qa",
            "custom_topk": kwargs["custom_topk"] or self.default_custom_topk, 
            "temperature": kwargs["temperature"] or self.default_temperature,
            "max_tokens": kwargs["max_tokens"] or self.default_max_tokens,
            "streaming": kwargs.get("streaming", self.default_streaming)
        }
        return self.RAG_CORE.chat(query=query, **request_data)
