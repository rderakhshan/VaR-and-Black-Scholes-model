import os
import sys
import numpy as np
import pandas as pd
import plotly.express as px
from scipy.stats import norm
import matplotlib.pyplot as plt
from dataclasses import dataclass
import plotly.figure_factory as ff
from datetime import datetime, timedelta

# Add the project's root directory to sys.path to enable importing from 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.unit_tests import unit_test
from src.logger import logging
from src.exception import CustomException
from src.components.Pricing import Pricing
from src.components.VaR_calculation import VaR, CSVLoader
from src.components.data_ingestion import EXLLoader
from src.utils import data_transformation, Option_results_generator, VaR_outout_generator

#==================================================================================#
# Required parameters.                                                             #
#==================================================================================#
# Input parameters for option pricing calculations
Trade_date    = "11/23/2022"   # Trade initiation date
Expire_date   = "05/10/2023"   # Option expiration date
Spot_price    = 19             # Current underlying asset price
Strike_price  = 17             # Option strike price
Interest_rate = 0.005          # Risk-free interest rate
Divident_ampl = 0.0            # Dividend yield
No_of_divide  = 5              # Number of dividends
Volatility    = 0.3            # Volatility of the underlying asset
Covar_yield   = 0              # Covariance yield

#==================================================================================#
# Required parameters for VaR calculations.                                        #
#==================================================================================#
list_curre  = ["Currency 1", "Currency 2"]   # List of currencies considered for VaR
list_values = [153084.81, 95891.51]          # Corresponding values for each currency

#==================================================================================#
# Data ingestion and transformation for VaR calculations                           #
#==================================================================================#
logging.info("Data ingestion part for VaR calcualtion is started.")
# Load data from an Excel file for VaR calculations
excel_df = EXLLoader("./Experiments/Data/", "VaR.xlsx")
df = excel_df.load_exl()  # Load the Excel data into a DataFrame
data_transformation(df)   # Perform any required data transformation
logging.info("Data ingestion part for VaR calcualtion is done.")

#==================================================================================#
# Option pricing calculations.                                                     #
#==================================================================================#
logging.info("Option pricing calculation is strarted.")
# Create an instance of the Pricing class with the given parameters
pricing = Pricing(Trade_date, Expire_date, Spot_price, Strike_price, 
                  Interest_rate, Divident_ampl, Volatility, Covar_yield, No_of_divide)

# Perform calculations for pricing
Dividents = pricing.Forward_price()                        # Calculate forward price
D1_forward, D2_forward = pricing.d1_and_d2_forward_price() # Calculate d1 and d2 for forward price
D1_spot, D2_spot = pricing.d1_and_d2_spot_price()          # Calculate d1 and d2 for spot price
call_forward, put_forward = pricing.Call_and_put_from_forward() # Call and put prices from forward price
call_spot, put_spot = pricing.Call_and_put_from_spot()      # Call and put prices from spot price

# Generate option pricing results
Option_results_generator(D1_forward, D2_forward, D1_spot, D2_spot, 
                         call_forward, put_forward, call_spot, put_spot)
logging.info("Option pricing calculation is done.")

#==================================================================================#
# Value at Risk (VaR) calculations.                                                #
#==================================================================================#
logging.info("Loading the transformed data for VaR calculation is started.")
# Load VaR-related data from a CSV file
csv_df = CSVLoader("./Artifacts/", "VaR.csv")
df = csv_df.load_csv()  # Load the CSV data into a DataFrame
logging.info("Loading the transformed data for VaR calculation is done.")

logging.info("VaR calculations for three different shift-types is started.")
# Calculate different types of VaR: Absolute, Relative, and Logarithmic
Value_at_Risk_abs = VaR(df, list_curre, list_values, "Absloute")
Value_at_Risk_rel = VaR(df, list_curre, list_values, "Relative")
Value_at_Risk_log = VaR(df, list_curre, list_values, "Logarithmic")

# Format the VaR results to four decimal places
VaRs = [[float("{:.4f}".format(Value_at_Risk_abs.Value_at_risk())),
         float("{:.4f}".format(Value_at_Risk_rel.Value_at_risk())),
         float("{:.4f}".format(Value_at_Risk_log.Value_at_risk()))]]

# Generate the output for VaR calculations
VaR_outout_generator(VaRs)
logging.info("VaR calculations for three different shift-types is done.")
#==================================================================================#
# Unit testing for different scenarios: "In money", "At money", "Out of money"     #
#==================================================================================#
logging.info("Unit test part is started.")
for test_type in ["In money", "At money", "Out of money"]:
    # Run unit tests with different option moneyness scenarios
    unit_test(Trade_date, Expire_date, Interest_rate, Divident_ampl,
              Volatility, Covar_yield, No_of_divide, test_type)
logging.info("Unit test part is done.")
