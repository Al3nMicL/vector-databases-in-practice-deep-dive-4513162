import os
import weaviate
from dotenv import load_dotenv
from weaviate.client import WeaviateClient
from weaviate.connect.helpers import connect_to_weaviate_cloud

# Load environment variables (`DEMO_WEAVIATE_URL` and `DEMO_WEAVIATE_RO_KEY`)
# From the provided `.env` file
load_dotenv()


def connect_to_demo_db() -> WeaviateClient:
    """
    Helper function to connect to the demo Weaviate database.
    For queries only.
    This database instance has the necessary data loaded.
    """
    # OpenAI API key for queries that require it
    openai_api_key = os.getenv("OPENAI_APIKEY")
    # Be sure to set `OPENAI_APIKEY` in your environment variables
    headers = {"X-OpenAI-Api-Key": openai_api_key} if openai_api_key else None
    client = weaviate.connect_to_wcs(
        cluster_url=os.getenv("DEMO_WEAVIATE_URL"),                                     # Demo server URL,
        auth_credentials=weaviate.auth.AuthApiKey(os.getenv("DEMO_WEAVIATE_RO_KEY")),   # Demo server read-only API key
        headers=headers
    )  
    return client
    


def connect_to_my_db():
    """
    Connect to your Weaviate Cloud instance using environment variables.
    Ensure you set WEAVIATE_CLUSTER_URL and WEAVIATE_API_KEY in your .env or environment.
    For Google modules, GOOGLE_APIKEY (or PALM_APIKEY) should also be set as an environment variable.
    """
    # Ensure env vars are loaded if using python-dotenv
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass  # Not required, just helpful for .env support

    cluster_url = os.getenv("WEAVIATE_CLUSTER_URL")
    api_key = os.getenv("WEAVIATE_API_KEY")

    if not cluster_url or not api_key:
        raise ValueError("WEAVIATE_CLUSTER_URL and WEAVIATE_API_KEY must be set in the environment.")

    client = connect_to_weaviate_cloud(
        cluster_url=cluster_url,
        auth_credentials=api_key,
        # headers parameter omitted, as generative modules need env vars for keys.
    )
    return client


def main():

    # Connect to Weaviate
    client = connect_to_demo_db()
    # client = connect_to_my_db()  # Could also use this to connect to your own Weaviate instance

    try:
        # Check whether the client is ready
        assert client.is_ready()  # Check connection status (i.e. is the Weaviate server ready)

        # Try a query
        movies = client.collections.get("Movie")
        response = movies.query.near_text(query="time travel", limit=1)
        assert len(response.objects) == 1
        print("Success! You appear to be correctly set up.")
    finally:
        # Close the connection
        client.close()


if __name__ == "__main__":
    main()
