import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    db.execute("CREATE TABLE reviews(isbn VARCHAR NOT NULL, username VARCHAR NOT NULL, review VARCHAR NOT NULL, rating INTEGER NOT NULL)")
    db.commit()
if __name__ == "__main__":
    main()      
