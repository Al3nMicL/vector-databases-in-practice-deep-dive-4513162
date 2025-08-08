import utils
import weaviate.classes as wvc
import os
from weaviate.classes.config import Configure, Property, DataType

client = utils.connect_to_my_db()  # Connect to our own database
google_cloud_project_id = os.getenv("GCP_PROJECT_ID") # Define this in .env to match your Google Cloud project ID

print(f"Creating collection 'Movie' with Google AI Studio vectorizer... Project ID: {google_cloud_project_id}")
client.collections.create(
    # Set the name of the collection
    name="Movie",

    # Set modules to be used
    # Create the collection with the Google AI Studio vectorizer
    vectorizer_config=Configure.Vectorizer.text2vec_google(
        model_id="models/embedding-001", # The 'text2vec_google' module uses 'model_id' to specify the model.
        api_endpoint="generative.googleapis.com",
        project_id=google_cloud_project_id,
    ), 
    generative_config=wvc.config.Configure.Generative.google(model_id="gemini-2.5-flash-lite", project_id=google_cloud_project_id), # Set the generative module

    # Define the properties of the collection
    properties=[
        wvc.config.Property(
            # Set the name of the property
            name="title",
            # Set the data type of the property
            data_type=wvc.config.DataType.TEXT,
        ),
        wvc.config.Property(
            name="description",
            data_type=wvc.config.DataType.TEXT,
        ),
        wvc.config.Property(
            name="movie_id",
            data_type=wvc.config.DataType.INT,
        ),
        wvc.config.Property(
            name="year",
            data_type=wvc.config.DataType.INT,
        ),
        wvc.config.Property(
            name="rating",
            data_type=wvc.config.DataType.NUMBER,
        ),
        wvc.config.Property(
            name="director",
            data_type=wvc.config.DataType.TEXT,
            skip_vectorization=True,
        ),
    ],
)

client.close()
