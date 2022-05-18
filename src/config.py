config = {
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

criterion1 = {
    'cockroach': {
        'num_cockroaches': [5, 10, 25],
    },
}

criterion2 = {
    'cockroach': {
        'n_iterations': [1, 2],
    },
}