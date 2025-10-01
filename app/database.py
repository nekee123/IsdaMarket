from neomodel import config as neomodel_config
from .config import settings


def init_database():
    """Initialize Neo4j database connection"""
    # Compose the full connection URL with credentials
    uri = settings.neo4j_uri
    
    # If credentials are not in URI, compose them
    if "@" not in uri:
        # Extract scheme and host
        if "://" in uri:
            scheme, host = uri.split("://", 1)
            uri = f"{scheme}://{settings.neo4j_user}:{settings.neo4j_password}@{host}"
    
    neomodel_config.DATABASE_URL = uri
    print(f"✓ Connected to Neo4j database")


def close_database():
    """Close database connection"""
    # neomodel handles connection pooling automatically
    pass
