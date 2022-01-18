from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base, registry

Base = declarative_base()


mapper_registry = registry()
metadata = MetaData()
