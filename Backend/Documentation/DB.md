## Using PostgreSQL DB for our app

### Establishing Connectivity - the Engine

The engine is the core object that manages the connection to your databse.

```python
from sqlalchemy import create_engine

engine = create_engine("sqlite:///example.db")  # or your database URL
```
