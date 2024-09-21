from typing import Any, Dict, Optional

from opensearchpy import OpenSearch

def create_opensearch_client(
    hosts: Optional[str] = None,
    cloud_id: Optional[str] = None,
    api_key: Optional[int] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    params: Optional[Dict[str, Any]] = None,
) -> OpenSearch:
    """Create an OpenSearch client."""
    if hosts and cloud_id:
        raise ValueError("Both url and cloud_id are defined. Please provide only one")
    if not hosts and not cloud_id:
        raise ValueError("Must provide either url or cloud_id")

    connection_params: Dict[str, Any] = {}
    if hosts:
        connection_params["hosts"] = [hosts]
    if cloud_id:
        connection_params["cloud_id"] = cloud_id

    if api_key:
        connection_params["api_key"] = api_key
    elif username and password:
        connection_params["basic_auth"] = (username, password)

    if params is not None:
        connection_params.update(params)
    os_client = OpenSearch(**connection_params)
    os_client.info()
    return os_client

