# Introduction
Aclog is an automated log parsing tool that can parse unstructured, low-level logs into structured, compressed logs. At the same time, aclog can also automatically store the parsed logs in the database and easily query the logs in the database.

# Environment and Package
Required environment: python, mysql

Required Python packages: pyqt5, passlib, numpy, pandas, sqlalchemy

# configuration
Fill in the database link parameters (host, user, password, db) in MyApp_config.ini

Modify the function engine (user, password) in insert_db.py

Change line 198 in main.py to your own database name

Run the users table generation statement in app.sql
