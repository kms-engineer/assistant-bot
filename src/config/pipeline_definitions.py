
PIPELINE_DEFINITIONS = {
    'add_contact': {
        'primary_command': 'add',
        'primary_required': ['name', 'phone'],
        'pipeline': [
            {
                'command': 'add-email',
                'entities': ['email'],
                'min_entities': 1
            },
            {
                'command': 'add-address',
                'entities': ['address'],
                'min_entities': 1
            },
            {
                'command': 'add-birthday',
                'entities': ['birthday'],
                'min_entities': 1
            }
        ]
    },
    'edit_phone': {
        'primary_command': 'change',
        'primary_required': ['name', 'phone'],
        'pipeline': [
            {
                'command': 'add-email',
                'entities': ['email'],
                'min_entities': 1,
                'condition': 'if_not_exists'
            },
            {
                'command': 'add-address',
                'entities': ['address'],
                'min_entities': 1,
                'condition': 'if_not_exists'
            },
            {
                'command': 'add-birthday',
                'entities': ['birthday'],
                'min_entities': 1,
                'condition': 'if_not_exists'
            }
        ]
    },
    'add_note': {
        'primary_command': 'add-note',
        'primary_required': ['note_text'],
        'pipeline': [
            {
                'command': 'add-tag',
                'entities': ['tag'],
                'min_entities': 1,
                'note_id_from_primary': True
            }
        ]
    },
    'search_contacts': {
        'primary_command': 'search',
        'primary_required': [],
        'pipeline': [
            {
                'command': 'show-phone',
                'entities': ['name'],
                'min_entities': 1,
                'condition': 'if_single_result'
            }
        ]
    }
}
