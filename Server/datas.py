import datetime

# frequency_time_unit = 6 hours
frequency_time_unit = datetime.timedelta(hours=6)

# investment price coefficient
price_coefficient = 3
investment_coefficient = 3


# The first is the id the second is the value of reputation
standards = {
    "verra": 2000,
    "satba": 1000
}

standards_id_to_name = {
    0: "verra",
    1: "satba"
}

standards_name_to_id = {
    "verra": 0,
    "satba": 1
}

tokens = {}

weights = {
    "standard": 0.5,
    "carbon_type": 0.3,
    "issuance_year": 0.2
}

carbon_type_values = {
    "renewable energy": 1000
}

carbon_id_to_type = {
    0: "renewable energy"
}

carbon_type_to_id = {
    "renewable energy": 0
}

pools = {
    "verra": {
        "renewable energy": {
            2024: None,
        }
    },
    "satba": {
        "renewable energy": {
            2024: None,
        }
    }
}

