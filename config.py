DEBUG = True
DEV = False
EXPLAIN = True
RESULT_SIZE = 10

if DEV:
    HOST = '127.0.0.1'
else:
    HOST = '10.77.20.50'


SRF_ENABLED = True
SECRET_KEY = 'academi'

LANGUAGES = {
    'en': 'English'}

# Redis
REDIS_HOST = HOST
REDIS_PORT = 6379
REDIS_DB = 0

# MongoDB
MONGODB_HOST = HOST
MONGODB_PORT = 27017
MONGODB_SERVER = '%s:%s' % (MONGODB_HOST, MONGODB_PORT)
MONGODB_DB = 'academi_exp'
PAPER_COLLECTION = 'paper'
PAPER_EN_COLLECTION = 'paper_en'
SCHOLAR_COLLECTION = 'scholar'


# Translate Service
TRANSLATOR = 'youdao'
TRANSLATE_SERVICE = {
        'youdao':{
            'endpoint':'http://fanyi.youdao.com/openapi.do',
            'username' :'academi',
            'key' :'1179509028'
            },
        }

# Elasticsearch
ES_HOST = HOST
ES_PORT = '9200'
ES_SERVER = '%s:%s' % (ES_HOST, ES_PORT)
PAPER_INDEX = 'paper_index_exp'
PAPER_TYPE = 'paper_type'
PAPER_MAPPING = {
        'uuid': {
            'index': 'not_analyzed',
            'store': 'yes',
            'type': 'string'
            },
        'title': {
            'index': 'analyzed',
            'indexAnalyzer': 'ik',
            'searchAnalyzer': 'ik',
            'store': 'yes',
            'type': 'string',
            'term_vector': 'with_positions_offsets'
            },
        'body': {
            'index': 'analyzed',
            'indexAnalyzer': 'ik',
            'searchAnalyzer': 'ik',
            'store': 'yes',
            'type': 'string',
            'term_vector': 'with_positions_offsets'
            }
        }

PAPER_EN_INDEX = 'paper_en_index_exp'
PAPER_EN_TYPE = 'paper_en_type'
PAPER_EN_MAPPING = {
        'uuid': {
            'index': 'not_analyzed',
            'store': 'yes',
            'type': 'string'
            },
        'title': {
            'index': 'analyzed',
            'indexAnalyzer': 'ik',
            'searchAnalyzer': 'ik',
            'store': 'yes',
            'type': 'string',
            'term_vector': 'with_positions_offsets'
            },
        'body': {
            'index': 'analyzed',
            'indexAnalyzer': 'ik',
            'searchAnalyzer': 'ik',
            'store': 'yes',
            'type': 'string',
            'term_vector': 'with_positions_offsets'
            }
        }
