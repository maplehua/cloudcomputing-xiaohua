DEBUG = True
EXPLAIN = True
RESULT_SIZE = 10


SRF_ENABLED = True
SECRET_KEY = 'academi'

LANGUAGES = {
    'en': 'English'}

# MongoDB
MONGODB_HOST = '10.77.20.50'
MONGODB_PORT = 27017
MONGODB_SERVER = '%s:%s' % (MONGODB_HOST, MONGODB_PORT)
MONGODB_DB = 'academi_exp'
PAPER_COLLECTION = 'paper'



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
ES_HOST = '10.77.20.50'
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

