# create_tables.py
from sqlalchemy import create_engine, MetaData, Table, Column, String, Numeric, Date
import os
import sys

DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    print('Please set DATABASE_URL environment variable')
    sys.exit(1)

engine = create_engine(DATABASE_URL)
meta = MetaData()

contract_state = Table(
    'contract_state', meta,
    Column('contract_id', String, primary_key=True),
    Column('last_interest_date', Date),
    Column('acc_interest', Numeric),
    Column('balance', Numeric),
)

meta.create_all(engine)
print('Tables created')
