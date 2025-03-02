import os

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:f894c0087e04d8e7@srv-captain--fleet-mgt-pg:5432/postgres')
SQLALCHEMY_TRACK_MODIFICATIONS = False