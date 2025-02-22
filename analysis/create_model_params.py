import json
from Utility.Database import Database

"""
This script creates a database and table with the given schema for a given connection specified in config file.
"""

configs = json.load(open("C:/Users/MV_2/Documents/GitHub/lMS-monte-carlo/.venv/config.json", "r"))
db_params = configs.get("db_params")
db_name = "simulation_params"
table_schema = """
    date DATE,
    underlying_name VARCHAR(255) NOT NULL,
    bs_sigma DOUBLE,
    hs_sigma DOUBLE,
    hs_theta DOUBLE,
    hs_kappa DOUBLE,
    hs_rho DOUBLE,
    ts_sigma DOUBLE,
    ts_theta DOUBLE,
    ts_kappa DOUBLE,
    ts_rho DOUBLE,
    ts_time_horizon DOUBLE,
    ts_alpha0 DOUBLE,
    ts_alpha1 DOUBLE,
    ts_gamma DOUBLE,
    PRIMARY KEY (date, underlying_name)
"""
connection_instance = Database()
connection_instance.connect(db_params)
connection_instance.create_table(connection_instance.connection, "model_params", table_schema)
