config = {
    'num_lines': 3,
    'num_buses': 20,
    'num_tests': 4, # number for option -t
    'generate': {
        'vertices': 20,
        'min_edges': 120,
        'num_passengers': 100
    },
    'cockroach': {
        'num_cockroaches': 10,
        'min_common': 8,
        'step_size': 2,
        'dispersing_update_ratio': .5,
        'n_iterations': 5,
        'num_to_test': 5
    },

    'bees': {
        'num_bees': 10,
        'num_transition': 2,
        'update_ratio': .3,
        'n_iterations': 5
    }
}

criterias = {
    '1': {
        'cockroach': {
            'num_cockroaches': [5], # array of values to compare
        },
    },
    '2': {
        'cockroach': {
            'n_iterations': [1, 2],
        },
    }
}
