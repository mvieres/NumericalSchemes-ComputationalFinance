import json
import mysql.connector
from mysql.connector import Error as mysqlError
from datetime import date, datetime
from webbrowser import Error  # TODO: is this the right error category for fetching data from mysql?
from logging import error, ERROR

from MarketDataContainer.MkdContainer import MkdContainer
from PortfolioEvaluation.Params.AbstractModelParams import AbstractModelParams
from PortfolioEvaluation.Params.BlackScholesParams import BlackScholesParams
from PortfolioEvaluation.Params.HestonCIRParams import HestonCIRParams
from PortfolioEvaluation.Params.HestonCKLSParams import HestonCKLSParams
from PortfolioEvaluation.Params.SimConfigParams import SimConfigParams
from PortfolioEvaluation.Params.StockOptionParams import StockOptionParams
from PortfolioEvaluation.Params.TrolleSchwartzParams import TrolleSchwartzParams
from PortfolioEvaluation.PortfolioParams import PortfolioParams
from PortfolioEvaluation.SimulationKernel import SimulationKernel

#import spepper


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
        self.job_requests = {}
        self.job_results = {}
        self.trades = None
        self.__portfolio_value = None

        self.portfolio_params = PortfolioParams()
        self.sim_config_params = SimConfigParams()
        self.trade_params = {}  # Structure that contains simulation parameters for each trade
        self.default_params = {}

        self.trade_params_str = "trade_params"
        self.simulation_params_str = "simulation_params"

        self.today = date.today()
        self.mkd_container = MkdContainer()
        self.db_params = None
        self.db = None
        self.db_status = None

    def run(self):
        self.read_portfolio()
        self.convert_params()
        self.process_params()
        self.run_simulation()
        self.aggregate_results()

    def read_portfolio(self):
        with open(self.portfolio_str, 'r') as file:
            data = json.load(file)
        self.portfolio_params.from_dict(data)
        # TODO: Implement check for required fields.
        # get database params
        try:
            with open("C:/Users/pkv4e/Documents/db_params.json", 'r') as file:
                self.db_params = json.load(file)
        except Exception as e:
            self.db_status = False
            print(f"Database params could not be loaded due to Error: {e}, continuing without database")
        # get default params for database fallback
        try:
            with open("C:/Users/pkv4e/Documents/GitHub/NumericalSchemes-ComputationalFinance/PortfolioEvaluation/Params/BlackScholesDefault.json", 'r') as file:
                self.default_params["BlackScholes"] = json.load(file)
            with open("C:/Users/pkv4e/Documents/GitHub/NumericalSchemes-ComputationalFinance/PortfolioEvaluation/Params/HestonDefault.json", 'r') as file:
                self.default_params["Heston"] = json.load(file)
        except Exception as e:
            print(f"Default parameters could not be loaded due to Error: {e}")

        # establish database connection for model parameters
        if self.db_status is None:
            self.db, self.db_status = self.connect_to_database(self.db_params)

    def convert_params(self):
        """
        This method should be the end of the business layer,
        i.e. all dicts from the json should be converted to class instances
        This method also extracts the underlying and currency names for the market data container / database query
        """
        self.sim_config_params.from_dict(self.portfolio_params.get_simulation_config())
        self.trades = self.portfolio_params.get_trades()
        # convert trades from list(dicts) to list(ParamInstances) here
        assert isinstance(self.trades, list), "Trades should be a list"
        for trade in self.trades:
            assert len(trade.keys()) == 1, "structure of trades does not match, only one entry in dict allowed"
            trade_entry = list(trade.keys())[0]
            temporary_dict = trade[trade_entry].copy()
            self.underlying_list.append(temporary_dict.get("underlying"))
            self.currency_list.append(temporary_dict.get("notional_currency"))
            if trade_entry == "stock_option":
                trade[trade_entry] = StockOptionParams()
                trade[trade_entry].from_dict(temporary_dict)
            else:
                error("entry with id"+f"{id}"+"in trades did not process the right param class")

    def process_params(self):
        """
        This should be the connection between business layer and workforce

        This function should analyze the trades and create a config such that each trades know which model to use and it's parameters
        TODO: Implement the above (blocked by database params mapping / calibration implementation)

        For now we take a fixed model for each asset class / trade type, e.g. BlackScholes for stock options and get some default parameters

        """

        # Get Fx names
        reference_curr = self.sim_config_params.get_reference_yield_curve()
        required_fx = [currency + "_" + reference_curr for currency in self.currency_list]
        self.mkd_container.set_currency_list(required_fx)
        self.mkd_container.set_underlying_list(self.underlying_list)
        if reference_curr == "USD":
            reference_curr = "^IRX"  # TODO: Mapping of reference yield curve to the ticker names -> the same could be chosen, but e.g. ^IRX for 13week USD yield curve is not intuitive
        else:
            raise ERROR("Other reference yield curves not implemented yet")
        self.mkd_container.set_reference_curve_name(reference_curr)
        try:
            self.mkd_container.load()
        except Exception as e:
            error(f"Market data could not be loaded: {e}")


        # get fallback models for the case of no database connection
        default_models_as_str = self.sim_config_params.get_default_models()
        default_models_as_class = self.process_default_models(default_models_as_str)  # This converts the model from sting to a class object
        # Create new simulation object that has the classes
        # Enforced structure self.job_requests = {"id": {"trade_params": self.trades, "simulation_params": {BlackScholesParams or else}}}

        for trade in self.trades:
            trade_category = list(trade.keys())[0]
            trade_params = trade[trade_category]
            id = trade_params.get_id()
            trade_params.set_category(trade_category)
            self.job_requests[id] = {self.trade_params_str: trade_params}
            self.job_requests[id][self.simulation_params_str] = \
                {"underlying": default_models_as_class.get(trade_category),
                 "interest_rate":default_models_as_class.get("interest_rate") } # In this case, trade_category could be
            # interest_rate. In this case we could
            if trade_category == "interest_rate":
                self.job_requests[id][self.simulation_params_str]["underlying"] = (
                    self.job_requests[id][self.simulation_params_str]["interest_rate"])  #

            # Fill up simulation params
            self.job_requests[id] = self.fill_up_params(self.job_requests[id])

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
    def process_default_models(default_models_as_str: dict):
        model_mapping = {
            "BlackScholes": BlackScholesParams,
            "TrolleSchwartz": TrolleSchwartzParams,
            "HestonCIR": HestonCIRParams,
            "HestonCKLS": HestonCKLSParams
        }
        default_models_as_class = {}
        for key, model_str in default_models_as_str.items():
            model_class = model_mapping.get(model_str)
            if model_class:
                default_models_as_class[key] = model_class()
            else:
                # TODO: Error as this is called for model_class None and Heson -> Somewhere HEstonCir HestonCKLS is missing
                error(f"{model_str} model was not able to be casted to a model param class")
        return default_models_as_class

    def fill_up_params(self, trade_dict: dict):
        """
        This function should convert the trade_dict to a class instance
        """

        underlying_name = trade_dict[self.trade_params_str].underlying
        id = trade_dict[self.trade_params_str].get_id()
        model = trade_dict[self.simulation_params_str]['underlying'].__class__.__name__.replace("Params", "")
        trade_dict['model'] = model
        for type in ['underlying', 'interest_rate']:
            sim_params = trade_dict[self.simulation_params_str][type]
            assert isinstance(sim_params, BlackScholesParams) or isinstance(sim_params, HestonCIRParams) or isinstance(sim_params, TrolleSchwartzParams), "Only BlackScholes and Heston implemented"

            # fetch parameters for simulation: try to get today + underlying. If not possible, use default without a date.
            # If no database connection is available, use default parameters from json in the repository
            db_result = self.fetch_params(underlying_name, model) # TODO not dependent on the for loop

            # Demo implementation for the case stock_option -> BlackScholes TODO
            # Get the most genereal parameters: r, s0, t_start, t_end
            sim_params.set_starting_point(self.mkd_container.get_latest_spot_price(trade_dict[self.trade_params_str].underlying))
            end_date = trade_dict[self.trade_params_str].maturity  # TODO: correct for right times, i.e. today.toordinal() == 0
            sim_params.set_t_start(0)
            sim_params.set_t_end(self.convert_date(end_date).toordinal() - self.today.toordinal())
            # Get the model specific parameters
            sim_params.set_r(self.mkd_container.get_today_short_rate())
            if model == "BlackScholes":
                assert isinstance(sim_params, BlackScholesParams)
                sim_params.set_sigma(self.mkd_container.get_implied_volatility(underlying_name))
                # TODO: for now bs uses implied volatility
            elif model == "Heston":
                assert isinstance(sim_params, HestonCIRParams)
                sim_params.set_sigma(db_result.get("hs_volvol"))
                sim_params.set_kappa(db_result.get("hs_kappa"))
                sim_params.set_theta(db_result.get("hs_theta"))
                sim_params.set_rho(db_result.get("hs_rho"))
                sim_params.set_v0(db_result.get("hs_v0"))  # This should be marked data
            elif model == "TrolleSchwartz":
                # TODO:
                ImportError("TrolleSchwartz not implemented yet")
            else:
                error(f"Model {model} not implemented yet")
        return trade_dict

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
            db_result = self.get_data_from_db(self.db, query)
            if len(db_result) == 0 or self.has_null_values(db_result[0]):
                print(
                    f"No specific / enough parameters for trade {id} on date {self.today} found, switching to default from database")
                query = "SELECT * FROM model_params WHERE underlying = 'Default'"
                db_result = self.get_data_from_db(self.db, query)

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