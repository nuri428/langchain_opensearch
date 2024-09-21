# langchain_opensearch

This repository contains 1 package with OpenSearch integrations with LangChain:

langchain-opensearch integrates Opensearch 

---

TODO 
1. OpensearchStore 구현 [X]
2. OpensearchRetriever 구현 [X]
3. 그외 langchain-elastic에서 제공하는 여러 기능 구현. [ ]
   3.1 추가할 기능 내역 목록화 [ ]

4. AWS 연동 [ ]
    4.1 계정부터 만들고.. 

---

example index
name is "news_article_embedding"
```json
{
  "properties": {
    "metadata": {
      "type": "object",
      "properties": {
        "created_date": {
          "type": "date"
        },
        "title": {
          "fields": {
            "nori_analyzer": {
              "type": "text",
              "analyzer": "nori_analyzer"
            }
          },
          "type": "text"
        },
      }
    },
    "text": {
      "fields": {
        "nori_analyzer": {
          "type": "text",
          "analyzer": "nori_analyzer"
        }
      },
      "type": "text"
    },
    "vector_field": {
      "dimension": 1024,
      "method": {
        "engine": "nmslib",
        "space_type": "l2",
        "name": "hnsw",
        "parameters": {
          "ef_construction": 512,
          "m": 16
        }
      },
      "type": "knn_vector"
    }
  }
}
```

set opensearch_url like "http://localhost:9200"

1. simple search
```python
from langchain_opensearch import OpenSearchRetriever

# define body function as below
def normal_query(search_query: str) -> t.Dict:
    return {
        "_source": ["text","metadata"], 
        "query": {
            "match_phrase":{
                "text.nori_analyzer":search_query
            }
        }
    }
# define retriever
retrieve3 = OpenSearchRetriever.from_os_params(
    index_name = "news_article_embedding",
    body_func=normal_query,
    opensearch_url = opensearch_url,
    content_field="text"
)
# invoke retriever
retrieve3.invoke(query)
```

2. knn search 
```python
from langchain_opensearch import OpenSearchRetriever
# define body function as below
def knn_query(search_query: str) -> t.Dict:
    vector = embeddings.embed_query(search_query)  # same embeddings as for indexing
    return {
        "_source":{"exclude":["vector_field"]},
             "query": {
                "script_score": {
                    "query": {
                    "match_all": {}
                    },
                    "script": {
                    "source": "knn_score",
                    "lang": "knn",
                    "params": {
                        "field": "vector_field",
                        "query_value": embeddings.embed_query(search_query),
                        "space_type": "cosinesimil"
                        }
                    }
                }
             }
    }
# define retriever
retrieve2 = OpenSearchRetriever.from_os_params(
    index_name = "news_article_embedding",
    body_func=knn_query,
    opensearch_url = opensearch_url,
    content_field="text"
)
# invoke retriever
retrieve2.invoke(query)
```

---

License
This project is developed by referencing the [langchain-elastic package](https://github.com/langchain-ai/langchain-elastic), which is licensed under the MIT License.
This project is also licensed under the MIT License - see the LICENSE file for details.

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
