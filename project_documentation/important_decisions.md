## A list of import decisions

- For Python we use the docker image '3.11-slim-bookworm'.

- Use SQLite for the analytics. Motivation: 
    - It is part of the standard library, therefore valid given the Python Standard Library Constraint
    - SQL is suitable for analytics tasks
    - Given the queries in a separate module, one could swap SQLite with another library for the analytics, like for example PySpark.

- Prepare the data (bring them to suitable format) outside of SQLite, and have a separate pipeline. Motivation:
    - If we try to input invalid data to SQLite, we might end up not being able to either actual enter them or fix them later.

- Use unittest for the testing. Motivation:
    - It is part of the standard library, therefore valid given the Python Standard Library Constraint
    - The alternative would be to use plain assertions, but miss all the rest of the functionality, like test detection, provided by the library.