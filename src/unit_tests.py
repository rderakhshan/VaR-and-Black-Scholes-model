import os
import sys
import pandas as pd
# Add the project's root directory to sys.path to enable importing from 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.logger import logging
from src.exception import CustomException
from src.components.Pricing import Pricing
from src.utils import (data_transformation, Option_results_generator,
                                             VaR_outout_generator, unit_test_parity)
#==================================================================================#
# Required parameters.                                                             #
#==================================================================================#
# Input parameters 
Trade_date    = "11/23/2022"
Expire_date   = "05/10/2023"
Interest_rate = 0.005
Divident_ampl = 0.0
No_of_divide  = 5
Volatility    = 0.3
Covar_yield   = 0
#==================================================================================#
# Unit test part.                                                                  #
#==================================================================================#

class unit_test:
    
    def __init__(self, Trade_date, Expire_date, Interest_rate, Divident_ampl,
                 Volatility, Covar_yield, No_of_divide, test_type):
        
        if test_type   == "In money":
            self.Sp_price            = 19                           
            self.St_price            = 17 
        elif test_type == "At money":
            self.Sp_price            = 17                           
            self.St_price            = 17
        elif test_type == "Out of money":         
            self.Sp_price            = 17                           
            self.St_price            = 19
            
        self.Tr_date                 = Trade_date                                                  
        self.Ex_date                 = Expire_date                                     	
        self.Ir_rate                 = Interest_rate                          
        self.Dv_ampl                 = Divident_ampl
        self.Volatality              = Volatility
        self.Covar_yield             = Covar_yield
        self.No_DV_payments          = No_of_divide

        pricing                      = Pricing(self.Tr_date, self.Ex_date,
                                            self.Sp_price, self.St_price, 
                                            self.Ir_rate, self.Dv_ampl,
                                            self.Volatality, self.Covar_yield, self.No_DV_payments)

        Dividents                    = pricing.Forward_price()
        D1_forward, D2_forward       = pricing.d1_and_d2_forward_price()
        D1_spot, D2_spot             = pricing.d1_and_d2_spot_price()
        call_forward, put_forward    = pricing.Call_and_put_from_forward()
        call_spot, put_spot          = pricing.Call_and_put_from_spot()

        call_minus_put_from_spot     = float("{:.2f}".format(call_spot - put_spot))
        call_minus_put_from_forward  = float("{:.2f}".format(call_forward - put_forward))

        call_minus_put_from_parity   = unit_test_parity(self.Tr_date, self.Ex_date,
                                                    self.Sp_price, self.St_price, self.Ir_rate)
                
        Test_spot    = call_minus_put_from_spot    - call_minus_put_from_parity
        Test_forward = call_minus_put_from_forward - call_minus_put_from_parity
        
        Result = pd.DataFrame([[Test_spot, Test_forward, 
                                self.Sp_price, self.St_price]], index = ["C-P"], 
                              columns = ["With Forward minus parity",
                                         "With Spot minus parity", "Spot price", "Strike price"])
        
        Result.to_excel(f"./Results/{test_type}.xlsx")

        
# if __name__=="__main__":

#     unit_test(Trade_date, Expire_date, Interest_rate, Divident_ampl,
#                  Volatility, Covar_yield, No_of_divide, "In money")
