def get_parameters():
    data = {
        "gross_base_rate": {
            "hull": 0.06,
            "liability": 0.02
        },
        "ilf": {
            "base_limit": 1000000,
            "z": 0.2
        },
        "max_take_off_weight" : {
            "0 - 5kg" : 1,
            "5 - 10kg" : 1.2,
            "10 - 20kg" : 1.6,
            "> 20" : 2.5
        }
    }
    return data
