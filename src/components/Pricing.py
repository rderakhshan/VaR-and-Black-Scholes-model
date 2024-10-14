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
from src.logger import logging
from src.exception import CustomException



# # Input parameters 
# Trade_date    = "11/23/2022"
# Expire_date   = "05/10/2023"
# Spot_price    = 19 # In unit of currency
# Strike_price  = 17 # 
# Interest_rate = 0.005
# Divident_ampl = 0.0
# No_of_divide  = 5
# Volatility    = 0.3
# Covar_yield   = 0


class Pricing:
    """" 
    The code is designed to claclate historical VaR (1 day with .99 confidence level) for the FX portfolio assuming no corrolation between currencies.
    """
    
    def __init__(self, Trade_date, Expire_date, Spot_price, Strike_price, Interest_rate, Divident_ampl, Volatility, Covar_yield, Number_of_payments):

        self.Tr_date             = Trade_date                                                  
        self.Ex_date             = Expire_date                               
        self.Sp_price            = Spot_price                           
        self.St_price            = Strike_price                           	
        self.Ir_rate             = Interest_rate                          
        self.Dv_ampl             = Divident_ampl
        self.Volatality          = Volatility
        self.Covar_yield         = Covar_yield
        self.No_DV_payments      = Number_of_payments

    def Forward_price(self):

        # Convert the input date strings to datetime objects
        start_date = datetime.strptime(self.Tr_date, '%m/%d/%Y')
        end_date = datetime.strptime(self.Ex_date  , '%m/%d/%Y')

        # Calculate the total number of days between the start and end dates
        self.total_days = (end_date - start_date).days

        # Calculate the interval between each generated date
        interval = self.total_days / (self.No_DV_payments + 1)
        
        # Generate the dates
        dates = [start_date + timedelta(days=interval * i) for i in range(1, self.No_DV_payments + 1)]
        
        # Calculate the relative days between the generated dates and the end date
        self.relative_days = [abs((end_date - date).days) / 365 for date in dates]

        self.divident_points = [self.Dv_ampl] * len(self.relative_days)

        # Forward pricing calculation part

        self.F = self.Sp_price*np.exp((self.Ir_rate - self.Covar_yield)*(self.total_days/365))

        for i in range(self.No_DV_payments):

            self.F = self.F - self.divident_points[i]*np.exp(-(self.Ir_rate - self.Covar_yield)*self.relative_days[i])

        return self.F
    

    def d1_and_d2_forward_price(self):

        self.d1 = (np.log(self.F/self.St_price) + (0.5*(self.Volatality**2))*(self.total_days/365))/(self.Volatality*np.sqrt(self.total_days/365)) 

        self.d2 = self.d1 - self.Volatality*np.sqrt(self.total_days/365)

        return self.d1, self.d2


    def d1_and_d2_spot_price(self):

        self.d1 = ((np.log(self.Sp_price/self.St_price)) + (self.Ir_rate +0.5*(self.Volatality**2))*(self.total_days/365))/(self.Volatality*np.sqrt(self.total_days/365))
        
        self.d2 = self.d1 - self.Volatality*np.sqrt(self.total_days/365)

        return self.d1, self.d2
    

    def Call_and_put_from_forward(self):

        self.d1_BL = (np.log(self.F/self.St_price) + (0.5*(self.Volatality**2))*(self.total_days/365))/(self.Volatality*np.sqrt(self.total_days/365)) 

        self.d2_BL = self.d1 - self.Volatality*np.sqrt(self.total_days/365)


        # Call and put price

        self.call = (self.F*norm.cdf(self.d1_BL, loc = 0, scale = 1)   - self.St_price*norm.cdf(self.d2_BL, loc = 0, scale = 1))*np.exp(- self.Ir_rate*(self.total_days/365))

        self.put  = (self.St_price*norm.cdf(-self.d2_BL, loc = 0, scale = 1) - self.F*norm.cdf(-self.d1_BL, loc = 0, scale = 1))*np.exp(- self.Ir_rate*(self.total_days/365))

        return self.call, self.put


    def Call_and_put_from_spot(self):

        self.d1_BL = ((np.log(self.Sp_price/self.St_price)) + (self.Ir_rate + 0.5*self.Volatality**2)*(self.total_days/365))/(self.Volatality*np.sqrt(self.total_days/365))

        self.d2_BL = self.d1 - self.Volatality*np.sqrt(self.total_days/365)

        self.call = norm.cdf(self.d1_BL, loc = 0, scale = 1)*self.Sp_price - norm.cdf(self.d2_BL, loc = 0, scale = 1)*self.St_price*np.exp(- self.Ir_rate*(self.total_days/365))

        self.put  = norm.cdf(-self.d2_BL, loc = 0, scale = 1)*self.St_price*np.exp(- self.Ir_rate*(self.total_days/365)) - norm.cdf(-self.d1_BL, loc = 0, scale = 1)*self.Sp_price

        return self.call, self.put

# if __name__=="__main__":
    
#     pricing = Pricing(Trade_date, Expire_date, Spot_price, Strike_price, 
#                       Interest_rate, Divident_ampl, Volatility, Covar_yield,  No_of_divide)
    
#     Dividents = pricing.Forward_price()

#     # print(Dividents)
    
#     D1_forward, D2_forward = pricing.d1_and_d2_forward_price()
#     print("Calculated d1 and d2 from forward price method are: ({:.4f}, {:.4f})".format(D1_forward, D2_forward))
    
#     D1_spot, D2_spot = pricing.d1_and_d2_spot_price()
#     print("Calculated d1 and d2 from spot price method are: ({:.4f}, {:.4f})".format(D1_spot, D2_spot))
    
#     call_forward, put_forward = pricing.Call_and_put_from_forward()
#     print("Calculated d1 and d2 from spot price method are: ({:.4f}, {:.4f})".format(call_forward, put_forward))
    
#     call_spot, put_spot = pricing.Call_and_put_from_spot()
#     print("Calculated d1 and d2 from spot price method are: ({:.4f}, {:.4f})".format(call_spot, put_spot))
    
#     Result = pd.DataFrame([[D1_forward, D2_forward, call_forward,put_forward ],
#         [D1_spot, D2_spot, call_spot, put_spot]], columns = ["d1 ", "d2", "call", "put"], index = ["with forward price", "with spot price"])
    
#     Result.to_excel("/Users/vahid/Downloads/Project/Results/Options.xlsx")
    