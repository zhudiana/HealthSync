## Using PostgreSQL DB for our app

### Establishing Connectivity - the Engine

The engine is the core object that manages the connection to your databse.

```python
from sqlalchemy import create_engine

# The URL differs based on the DB type (Postgres, sqlite...)
engine = create_engine("sqlite:///example.db")
```

> Remember, the engine doesn't create a db. It only manages the connection to your db.

```python
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

- _SessionLocal_ is a factory of new sessions. When we want new session (interact with the db), we call **SessionLocal()**.

```python
#This creates a new session.
db = SessionLocal()
```

- After we create our session, we can interact with our db.

```python
user = db.query(User).filter(User.id == 1).first()  # query
user.name = "New Name"  # update
db.add(user)  # mark for update
db.commit()   # save changes to the database
db.close()    # close the session
```

- _Base_ is the base class for all SQLAlchemmy ORM models. We use it to define our db tables as Python classes.

```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
```

> When we define a model (table), we inherit from **_Base_**

### Pydantic Schemas

- Pydantic Schemas are Python classes used to define and validate the structure of data in FastAPI and other Python projects. They are data validation and serialization models, not database models.

- We use these schemas to:

  - Validate incoming request data (e.g., from JSON bodies)
  - Control what data is sent back in responses
  - Serialize/deserialize data between your API and your database models

```python
from pydantic import BaseModel

class UserSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True  # allows reading data from SQLAlchemy models
```
