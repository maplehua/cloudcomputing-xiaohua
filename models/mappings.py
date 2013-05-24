paper_mapping = {
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
        'source': {
            'index': 'analyzed',
            'indexAnalyzer': 'ik',
            'searchAnalyzer': 'ik',
            'store': 'yes',
            'type': 'string',
            },
        'year': {
            'index': 'not_analyzed',
            'store': 'yes',
            'type': 'string',
            },
        'author': {
            'index': 'analyzed',
            'indexAnalyzer': 'ik',
            'searchAnalyzer': 'ik',
            'store': 'yes',
            'type': 'string',
            'term_vector': 'with_positions_offsets'
            },
        'content': {
            'index': 'analyzed',
            'indexAnalyzer': 'ik',
            'searchAnalyzer': 'ik',
            'store': 'yes',
            'type': 'string',
            'term_vector': 'with_positions_offsets'
            },
        'url': {
            'index': 'not_analyzed',
            'store': 'yes',
            'type': 'string'
            }
        }
