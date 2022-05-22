config = {
    'num_lines': 4,
    'num_buses': 20,
    'num_tests': 4, # number for option -t
    'generate': {
        'vertices': 20,
        'min_edges': 30,
        'num_passengers': 80
    },
    'cockroach': {
        'num_cockroaches': 10,
        'min_common': 8,
        'step_size': 2,
        'dispersing_update_ratio': .5,
        'n_iterations': 10,
        'num_to_test': 5
    },

    'bees': {
        'num_bees': 10,
        'num_transition': 2,
        'update_ratio': .4,
        'n_iterations': 10
    }
}

criterias = {
    '1': {
        'cockroach': {
            'num_cockroaches': [5, 10, 15, 20],
        },
    },
    '2': {
        'cockroach': {
            'min_common': [1, 4, 7, 10],
        },
    },
    '3': {
        'cockroach': {
            'step_size': [1, 2, 4, 8],
        },
    },
    '4': {
        'cockroach': {
            'dispersing_update_ratio': [0.2, 0.3, 0.4, 0.5],
        },
    },
    '5': {
        'bees': {
            'num_bees': [5, 10, 15, 20],
        },
    },
    '6': {
        'bees': {
            'num_transition': [1, 2, 3, 4],
        },
    },
    '7': {
        'bees': {
            'update_ratio': [.3, .4, .5, .6],
        },
    }
}
