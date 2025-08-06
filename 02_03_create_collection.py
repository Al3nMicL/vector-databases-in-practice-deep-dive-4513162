import utils
import weaviate.classes as wvc
from weaviate.classes.config import Configure, Property, DataType

client = utils.connect_to_my_db()  # Connect to our own database

client.collections.create(
    # Set the name of the collection
    name="Movie",

    # Set modules to be used
    # Create the collection with the Google AI Studio vectorizer
    vectorizer_config=Configure.Vectorizer.text2vec_google(
        model_id="models/embedding-001", # The 'text2vec_google' module uses 'model_id' to specify the model.
        api_endpoint="generative.googleapis.com",
    ), 
    generative_config=wvc.config.Configure.Generative.google(model="gemini-2.5-flash-lite"), # Set the generative module

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
