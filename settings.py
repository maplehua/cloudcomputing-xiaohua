DEBUG = True
KEYWORD_EXPAND = False

LIB_PATH = './lib'

# number of qurey result on each pages
RESULT_SIZE = 10

# elasticsearch settings
ES_SETTING = {
        'server': '10.77.20.50:9200',
        'pre_tag': '<strong class="text-error">',
        'post_tag': '</strong>'
        }

ES_META = {
        'paper':{
            'index': 'dev_paper',
            'type': 'paper',
            'search': ['title', 'author', 'content'],
            'result': ['title', 'author', 'source', 'url', 'year']
            },
        'patent':{
            'index': 'dev_patent',
            'type': 'patent',
            'search': ['title', 'description'],
            'result': ['uuid', 'number', 'title', 'author', 'contributor', 'date', 'url']
            }
        }

REDIS_SERVER = '10.77.20.50'
MONGO_SERVER = '10.77.20.50'
MONGO_DB = 'academi'
DICTIONARY_COLLECTION = 'dictionary'
