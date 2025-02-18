import os
class Config:
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'aftab_2')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'Qwerty12345')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'quiz_data')
