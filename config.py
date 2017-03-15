import os
SQLALCHEMY_POOL_RECYCLE = 30
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI =  os.environ.get('DATABASE_URL')

COMPRESS_MIMETYPES = ['text/html',
                      'text/css',
                      'text/xml',
                      'application/json',
                      'application/javascript']
COMPRESS_LEVEL = 9
COMPRESS_MIN_SIZE = 500
