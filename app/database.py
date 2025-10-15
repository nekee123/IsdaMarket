from neomodel import config as neomodel_config
from .config import settings
from neo4j import GraphDatabase
import os

# Global driver instance
_driver = None


def init_database():
    """Initialize Neo4j database connection"""
    global _driver
    
    # Compose the full connection URL with credentials
    uri = settings.neo4j_uri
    
    # If credentials are not in URI, compose them
    if "@" not in uri:
        # Extract scheme and host
        if "://" in uri:
            scheme, host = uri.split("://", 1)
            uri = f"{scheme}://{settings.neo4j_user}:{settings.neo4j_password}@{host}"
    
    neomodel_config.DATABASE_URL = uri
    
    # Initialize Neo4j driver for direct queries
    _driver = GraphDatabase.driver(
        settings.neo4j_uri,
        auth=(settings.neo4j_user, settings.neo4j_password)
    )
    
    print(f"✓ Connected to Neo4j database")


def get_db():
    """Get Neo4j driver instance"""
    global _driver
    if _driver is None:
        _driver = GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password)
        )
    return _driver


def close_database():
    """Close database connection"""
    global _driver
    if _driver:
        _driver.close()
    # neomodel handles connection pooling automatically
    pass
