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
# Input parameters for unit testing
Trade_date    = "11/23/2022"  # Date of the trade
Expire_date   = "05/10/2023"  # Option expiration date
Interest_rate = 0.005         # Annualized interest rate
Divident_ampl = 0.0           # Dividend amount (if any)
No_of_divide  = 5             # Number of dividend payments
Volatility    = 0.3           # Volatility of the underlying asset
Covar_yield   = 0             # Covariance yield

#==================================================================================#
# Unit test class for option pricing parity testing                                #
#==================================================================================#

class unit_test:
    """
    This class performs unit tests for option pricing using different market scenarios:
    "In money," "At money," and "Out of money." It computes the difference between
    call and put option prices based on the spot and forward prices and compares 
    these values to a parity calculation such that it calculates the difference of
    C-P from both simulation and parity identity. If the obtained value for C-P is the
    same from both methods, the obtained C-P should be zero (or very close to zero).

    Attributes:
        Sp_price (float): Spot price of the asset
        St_price (float): Strike price of the option
        Tr_date (str): Trade date
        Ex_date (str): Expiration date
        Ir_rate (float): Interest rate
        Dv_ampl (float): Dividend amount
        Volatality (float): Volatility of the asset
        Covar_yield (float): Covariance yield
        No_DV_payments (int): Number of dividend payments
    """

    def __init__(self, Trade_date, Expire_date, Interest_rate, Divident_ampl,
                 Volatility, Covar_yield, No_of_divide, test_type):
        """
        Initializes the unit_test object with input parameters and performs
        option pricing calculations based on the test type.

        Parameters:
            Trade_date (str): The trade date.
            Expire_date (str): The option expiration date.
            Interest_rate (float): The annualized interest rate.
            Divident_ampl (float): The dividend amount.
            Volatility (float): The volatility of the underlying asset.
            Covar_yield (float): The covariance yield.
            No_of_divide (int): The number of dividend payments.
            test_type (str): The test scenario, one of "In money," "At money," or "Out of money."
        """
        # Set spot and strike prices based on the test type
        if test_type == "In money":
            self.Sp_price = 19  # Spot price higher than strike price                          
            self.St_price = 17  
        elif test_type == "At money":
            self.Sp_price = 17  # Spot price equal to strike price                          
            self.St_price = 17
        elif test_type == "Out of money":         
            self.Sp_price = 17  # Spot price lower than strike price                         
            self.St_price = 19
            
        # Initialize other parameters
        self.Tr_date = Trade_date                                                  
        self.Ex_date = Expire_date                                     	
        self.Ir_rate = Interest_rate                          
        self.Dv_ampl = Divident_ampl
        self.Volatality = Volatility
        self.Covar_yield = Covar_yield
        self.No_DV_payments = No_of_divide

        # Perform pricing calculations
        pricing = Pricing(self.Tr_date, self.Ex_date, self.Sp_price, self.St_price, 
                          self.Ir_rate, self.Dv_ampl, self.Volatality, 
                          self.Covar_yield, self.No_DV_payments)

        Dividents = pricing.Forward_price()
        D1_forward, D2_forward = pricing.d1_and_d2_forward_price()
        D1_spot, D2_spot = pricing.d1_and_d2_spot_price()
        call_forward, put_forward = pricing.Call_and_put_from_forward()
        call_spot, put_spot = pricing.Call_and_put_from_spot()

        # Calculate differences between call and put prices for spot and forward
        call_minus_put_from_spot = float("{:.2f}".format(call_spot - put_spot))
        call_minus_put_from_forward = float("{:.2f}".format(call_forward - put_forward))

        # Calculate parity value
        call_minus_put_from_parity = unit_test_parity(self.Tr_date, self.Ex_date,
                                                      self.Sp_price, self.St_price, 
                                                      self.Ir_rate)
                
        # Calculate differences from parity for spot and forward prices
        Test_spot = call_minus_put_from_spot - call_minus_put_from_parity
        Test_forward = call_minus_put_from_forward - call_minus_put_from_parity
        
        # Store the results in a DataFrame
        Result = pd.DataFrame([[Test_spot, Test_forward, 
                                self.Sp_price, self.St_price]], index=["C-P"], 
                              columns=["With Forward minus parity",
                                       "With Spot minus parity", 
                                       "Spot price", "Strike price"])
        
        # Save the results to an Excel file
        Result.to_excel(f"./Results/{test_type}.xlsx")

# if __name__ == "__main__":
#     # Example usage
#     unit_test(Trade_date, Expire_date, Interest_rate, Divident_ampl,
#               Volatility, Covar_yield, No_of_divide, "In money")
