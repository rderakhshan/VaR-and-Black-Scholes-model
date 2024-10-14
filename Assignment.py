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
import numpy as np   # For numericall array 
import pandas as pd  # For dataframe calculations
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
# Input parameters 
Trade_date    = "11/23/2022"
Expire_date   = "05/10/2023"
Spot_price    = 19 # In unit of currency
Strike_price  = 17 # 
Interest_rate = 0.005
Divident_ampl = 0.0
No_of_divide  = 5
Volatility    = 0.3
Covar_yield   = 0
#==================================================================================#
# Required parameters for VaR calculations.                                        #
#==================================================================================#
list_curre  = ["Currency 1", "Currency 2"]
list_values = [153084.81   ,  95891.51   ] 
#==================================================================================#
# Data ingestion and transformation for VaR calculations                           #
#==================================================================================#
excel_df = EXLLoader("./Experiments/Data/", "VaR.xlsx")
df       = excel_df.load_exl()
data_transformation(df)
#==================================================================================#
# Option part.                                                                     #
#==================================================================================#
pricing = Pricing(Trade_date, Expire_date, Spot_price, Strike_price, 
                Interest_rate, Divident_ampl, Volatility, Covar_yield,  No_of_divide)

Dividents                 = pricing.Forward_price()
D1_forward, D2_forward    = pricing.d1_and_d2_forward_price()
D1_spot, D2_spot          = pricing.d1_and_d2_spot_price()
call_forward, put_forward = pricing.Call_and_put_from_forward()
call_spot, put_spot       = pricing.Call_and_put_from_spot()

Option_results_generator(D1_forward, D2_forward, D1_spot, D2_spot, 
                         call_forward, put_forward, call_spot, put_spot)
#==================================================================================#
# VaR part.                                                                     #
#==================================================================================#
csv_df = CSVLoader("./Artifacts/", "VaR.csv")
df     = csv_df.load_csv()

Value_at_Risk_abs = VaR(df, list_curre, list_values, "Absloute")
Value_at_Risk_rel = VaR(df, list_curre, list_values, "Relative")
Value_at_Risk_log = VaR(df, list_curre, list_values, "Logarithmic")

VaRs = [[float("{:.4f}".format(Value_at_Risk_abs.Value_at_risk())),
        float("{:.4f}".format(Value_at_Risk_rel.Value_at_risk())),
        float("{:.4f}".format(Value_at_Risk_log.Value_at_risk()))]]

VaR_outout_generator(VaRs)

for test_type in ["In money", "At money", "Out of money"]:
    unit_test(Trade_date, Expire_date, Interest_rate, Divident_ampl,
                    Volatility, Covar_yield, No_of_divide, test_type)
