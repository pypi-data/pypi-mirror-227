import weaviate
from weaviate import Client


class VerbaQueryEngine:
    """
    An interface for Verba Query Engine.
    """

    client: Client = None

    def __init__(self, weaviate_url: str, weaviate_api_key: str, openai_key: str):
        VerbaQueryEngine.client = weaviate.Client(
            url=weaviate_url,
            auth_client_secret=weaviate.AuthApiKey(api_key=weaviate_api_key),
            additional_headers={"X-OpenAI-Api-Key": openai_key},
        )

    def query(self, query_string: str) -> tuple:
        """Execute a query to a receive specific chunks from Weaviate
        @parameter query_string : str - Search query
        @returns tuple - (system message, iterable list of results)
        """
        raise NotImplementedError("query must be implemented by a subclass.")

    def retrieve_document(self, doc_id: str) -> dict:
        """Return a document by it's ID (UUID format) from Weaviate
        @parameter doc_id : str - Document ID
        @returns dict - Document dict
        """
        raise NotImplementedError(
            "retrieve_document must be implemented by a subclass."
        )

    def retrieve_all_documents(self) -> list:
        """Return all documents from Weaviate
        @returns list - Document list
        """
        raise NotImplementedError(
            "retrieve_all_documents must be implemented by a subclass."
        )

    def get_client(self) -> Client:
        return VerbaQueryEngine.client
