import json
import os
from typing import Dict, Any
from datetime import date, datetime
from webbrowser import Error  # TODO: is this the right error category for fetching data from mysql?
from logging import error

import mysql.connector
from mysql.connector import Error as mysqlError

from MarketDataContainer.MkdContainer import MkdContainer
from PortfolioEvaluation.Params.BlackScholesParams import BlackScholesParams
from PortfolioEvaluation.Params.CIRParams import CIRParams
from PortfolioEvaluation.Params.HestonCIRParams import HestonCIRParams
from PortfolioEvaluation.Params.HestonCKLSParams import HestonCKLSParams
from PortfolioEvaluation.Params.GeneralSimConfigParams import GeneralSimConfigParams
from PortfolioEvaluation.Params.SimulationKernelParams import SimulationKernelParams
from PortfolioEvaluation.Params.StockOptionParams import StockOptionParams
from PortfolioEvaluation.Params.TrolleSchwartzParams import TrolleSchwartzParams
from PortfolioEvaluation.PortfolioParams import PortfolioParams
from PortfolioEvaluation.SimulationKernel import SimulationKernel


class RunPortfolioEvaluation:
    """
    Current design: read portfolio
    Process portfolio: get params from the json. Trades -> List of dicts will be converted to list of class instances
    with all parameters

    """
    def __init__(self, portfolio_name: str):
        self.portfolio_str = portfolio_name
        self.portfolio_des = None
        self.underlying_list = []
        self.currency_list = []
        self.request_profile = None
        self.result_profile = None
        self.job_requests_new = SimulationKernelParams()
        self.job_requests = {}
        self.job_results = {}
        self.trades = None
        self.__portfolio_value = None
        self.config = None

        self.portfolio_params = PortfolioParams()
        self.portfolio_raw = None
        self.sim_config_params = GeneralSimConfigParams()  # TODO
        self.trade_params = {}  # Structure that contains simulation parameters for each trade
        self.default_params = {}

        self.trade_params_str = "trade_params"
        self.simulation_params_str = "simulation_params"

        self.today = date.today()
        self.mkd_container = MkdContainer()
        self.db_params = None
        self.db_connection = None
        self.db_status = None
        self.db_result: Dict[int, Dict[str, Any]] = {}

    def run(self):
        self.setup_functionality()
        self.read_portfolio()
        self.convert_portfolio()
        self.process_params()
        self.mkd_and_db_fetch()
        self.fill_up_params()
        self.run_simulation()
        self.aggregate_results()

    def read_portfolio(self):
        # Loading the portfolio json
        try:
            with open(self.portfolio_str, 'r') as file:
                data = json.load(file)
            self.__validate_portfolio(data)
            self.portfolio_raw = data
        except Exception as e:
            raise FileNotFoundError(f"Portfolio json could not be loaded due to Error: {e}")

    def setup_functionality(self):
        a = self.__get_project_root()
        config_path = os.path.join(a, ".venv", "config.json")
        # Loading the config json
        try:
            with open(config_path, 'r') as file:
                self.config = json.load(file)
        except Exception as e:
            raise FileNotFoundError(f"Config could not be loaded due to: {e}")

        # Get database params
        try:
            self.db_params = self.config.get("db_params")
        except Exception as e:
            self.db_status = False
            print(f"Database params could not be loaded due to Error: {e}, continuing without database")
        # Get default parameters for each mathematical model (path should be specified in config json)
        try:
            self.__load_and_set_default("BlackScholes")
            self.__load_and_set_default("TrolleSchwartz")
            self.__load_and_set_default("HestonCir")
            self.__load_and_set_default("HestonCev")
        except Exception as e:
            raise FileNotFoundError(f"Default parameters could not be loaded due to: {e}")

        # establish database connection for model parameters
        if self.db_status is None:
            self.db_connection, self.db_status = self.connect_to_database(self.db_params)
        pass

    def convert_portfolio(self):
        """
        This method converts the portfolio dict to a class instances (with potentially nested dicts of other class
        instances).
        """
        self.job_requests_new.pull_from_input(self.portfolio_raw)

    def mkd_and_db_fetch(self):
        # MARKET DATA LOADING
        # Get underlying list and currency list
        underlying_list = []
        currency_list = []
        for trade_id in self.job_requests_new.get_all().keys():
            underlying_list.append(self.job_requests_new.get(trade_id).get_trade_params().get_underlying())
            currency_list.append(self.job_requests_new.get(trade_id).get_trade_params().get_notional_currency())
        self.underlying_list = list(set(underlying_list))  # convert to set to get unique values
        # Get Fx names
        reference_curr = self.job_requests_new.get_general_sim_params().get_reference_yield_curve()
        required_fx = [currency + "_" + reference_curr for currency in self.currency_list]
        required_fx = list(set(required_fx))  # convert to set to get unique values
        self.mkd_container.set_currency_list(required_fx)  # TODO Is this right?
        self.mkd_container.set_underlying_list(self.underlying_list)
        if reference_curr == "USD":
            reference_curr = "^IRX"  # TODO: Better mapping
        else:
            raise NotImplementedError("Only USD implemented for now")
        self.mkd_container.set_reference_curve_name(reference_curr)
        try:
            self.mkd_container.load()
        except Exception as e:
            raise error(f"Market data could not be loaded due to {e}")

        # DATABASE FETCH
        # Try to get:
        pass

    def fill_up_params(self):
        for trade_id in self.job_requests_new.get_all().keys():
            # We start with the "default params case" for now
            data = self.db_result.get(trade_id)
            """
            Idea: Data has now the right parameters for each Model specified. If not, those params are the default ones.
            """
            trade_object = self.job_requests_new.get(trade_id)
            params = trade_object.get_all_sim()
            trade_params = trade_object.get_trade_params()
            for params_entry in params:
                # All model unspecific parts here:
                params_entry.set_t_start(0)
                params_entry.set_t_end(self.convert_date(trade_params.get_maturity()))

                # Model specific parts here: For now, we only use default params.
                model = params_entry.get_model_name()

        pass

    def process_params(self):
        """
        This should be the connection between business layer and workforce

        This function should analyze the trades and create a config such that each trades know which model to use and it's parameters
        TODO: Implement the above (blocked by database params mapping / calibration implementation)

        For now we take a fixed model for each asset class / trade type, e.g. BlackScholes for stock options and get some default parameters

        """
        # SIMULATION PARAMETER INITIALIZATION
        # get fallback models for the case of no database connection
        default_models_as_class = self.process_models(self.job_requests_new.get_general_sim_params().get_default_models())
        # Create new simulation object that has the Model params classes
        for id in self.job_requests_new.get_all().keys():
            models = self.job_requests_new.get(id).get_trade_params().get_models()
            trade_type = self.job_requests_new.get(id).get_trade_params().get_category()
            if trade_type == "stock_option":
                if models is None:
                    models_as_class = default_models_as_class.copy()  # Uses default / general sim models
                else:
                    assert isinstance(models, dict), "Models must be a dict"
                    models_as_class = self.process_models(models)  # Uses trade-id specific models
                # For a stock option, the following should be set for meaningful simulation
                self.job_requests_new.get(id).set_underlying_params(models_as_class["stock_option"])
                self.job_requests_new.get(id).set_discount_curve_params(models_as_class["interest_rate"])
                self.job_requests_new.get(id).set_fx_params(models_as_class["foreign_exchange"])
            else:
                raise NotImplementedError(f"Trade type {trade_type} not implemented yet")
        stop = 0

    def run_simulation(self):
        for request in self.job_requests:
            simulation_kernel = SimulationKernel(self.sim_config_params)
            simulation_kernel.set_job_request(self.job_requests[request])
            simulation_kernel.run()
            self.job_results[request] = simulation_kernel.get_job_result()

    def aggregate_results(self):
        sum_value = 0
        for key in self.job_results.keys():
            sum_value += self.job_results[key]
        self.__portfolio_value = sum_value

    @staticmethod
    def process_models(default_models_as_str: dict):
        model_mapping = {
            "BlackScholes": BlackScholesParams,
            "TrolleSchwartz": TrolleSchwartzParams,
            "HestonCIR": HestonCIRParams,
            "HestonCKLS": HestonCKLSParams,
            "CIR": CIRParams
        }
        default_models_as_class = {}
        for key, model_str in default_models_as_str.items():
            model_class = model_mapping.get(model_str)
            if model_class:
                default_models_as_class[key] = model_class()
            else:
                # TODO: Error as this is called for model_class None and Heson -> Somewhere HEstonCir HestonCKLS is missing
                error(f"{model_str} model was not able to be casted to a model param class")
        assert len(default_models_as_class) == len(default_models_as_str), "All models must be casted to a class"
        return default_models_as_class

    @staticmethod
    def convert_date( input_date: str) -> date:
        given_date = datetime.strptime(input_date, '%Y-%m-%d')
        return date(given_date.year, given_date.month, given_date.day)

    def get_portfolio_value(self):
        return self.__portfolio_value

    @staticmethod
    def connect_to_database(db_params: dict):
        try:
            # Establish the connection
            connection = mysql.connector.connect(
                host=db_params.get("host"),
                database=db_params.get("database"),
                user=db_params.get("user"),
                password=db_params.get("password")
            )

            if connection.is_connected():
                print("Connected to the database")
                return connection, True

        except mysqlError as e:
            print(f"Databank conncection failes due to Error: {e}, switching to default parameters from repository-json")
            # Handle specific error codes if needed
            if e.errno == 2003:  # Error: Can't connect to MySQL server on 'host'
                print("Could not connect to MySQL server.")
            elif e.errno == 1045:  # Error: Access denied for user
                print("Access denied. Check your username and password.")
            elif e.errno == 1049:  # Error: Unknown database
                print("Database does not exist. Check your database name.")
            else:
                print("An unknown error occurred.")
            return None, False

    def fetch_params(self, underlying_name: str, model: str):
        if self.db_status:  # TODO: this method part has to be tested via mocked database
            query = f"SELECT * FROM model_params WHERE date = '{self.today}' AND underlying = '{underlying_name}'"
            db_result = self.get_data_from_db(self.db_connection, query)
            if len(db_result) == 0 or self.has_null_values(db_result[0]):
                print(
                    f"No specific / enough parameters for trade {id} on date {self.today} found, switching to default from database")
                query = "SELECT * FROM model_params WHERE underlying = 'Default'"
                db_result = self.get_data_from_db(self.db_connection, query)

            if isinstance(db_result, list):
                assert len(db_result) == 1, "Exactly one entry expected"
                db_result = db_result[0]  # convert to dict
        else:
            print("No database connection available, switching to default parameters from repository-json")
            db_result = self.default_params[model]
        return db_result

    @staticmethod
    def get_data_from_db(db, query: str):
        try:
            cursor = db.cursor(dictionary=True)
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            print(f"Fetching data failed due to Error: {e}")
            return None

    @staticmethod
    def has_null_values(data):
        for key, value in data.items():
            if value is None:
                return True
        return False

    @staticmethod
    def __get_project_root():
        # Get the absolute path of the current file
        current_file_path = os.path.abspath(__file__)
        # Traverse up the directory tree to find the root directory
        project_root = os.path.dirname(current_file_path)
        while not os.path.exists(os.path.join(project_root, '.git')) and project_root != os.path.dirname(project_root):
            project_root = os.path.dirname(project_root)
        return project_root

    def __load_and_set_default(self, key: str):
        with open(self.config.get("default_model_params").get(key), 'r') as file:
            self.default_params[key] = json.load(file)

    @staticmethod
    def __validate_portfolio(portfolio_dict: dict):
        keys_required_fields_toplayer = ["simulation_config", "trades"]
        for key in keys_required_fields_toplayer:
            # TODO: Finish this validation
            try:
                portfolio_dict.get(key)
            except Exception as e:
                raise KeyError(f"Required key {key} not found in portfolio json: {e}")
        # keys_simulation_config = ["n_paths", "discretization", "default_models", "reference_yield_curve", "use_constant_interest_rate"]
        pass
