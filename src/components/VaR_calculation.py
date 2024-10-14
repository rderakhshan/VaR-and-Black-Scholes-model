import os
import sys
import numpy as np
import pandas as pd
from dataclasses import dataclass

# Add the project's root directory to sys.path to enable importing from 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.logger import logging
from src.exception import CustomException


class CSVLoader:
    def __init__(self, directory, filename):
        self.directory = directory
        self.filename = filename

    def load_csv(self):
        file_path = os.path.join(self.directory, self.filename)
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"{self.filename} not found in {self.directory}")
        return pd.read_csv(file_path)


# df = pd.read_csv("/Users/vahid/Downloads/Project/Artifacts/VaR.csv")


class VaR:
    """" 
    The code is designed to claclate historical VaR (1 day with .99 confidence level) for the FX portfolio assuming no corrolation between currencies.
    """
    
    def __init__(self, df, list_curre, list_values, shift_type):

        self.df               = df                                    # Date, portfolio and market rate are loaded as dataframe               
        self.list             = []                                    # Empty list to collect the values of shifts
        self.shift_type       = shift_type                            # Shift types e.g., Absloute, Relative, Logarithmic
        self.list_curre       = list_curre                            # List of currencies e.g., Currency 1	, Currency 2	
        self.list_values      = list_values                           # SPOT Portfolio values for each currency
        self.Parial_p_and_l   = pd.DataFrame([0]*self.df.shape[0], 
                                                columns = ["p & l"])  # Zero vector to store the values of partial PnL

    # The below method is calculating the VaR while looping over each currency 
    def Value_at_risk(self):

        for Asset, Value in zip(self.list_curre, self.list_values):

            # For each given currency, the below part of code calculates the 1-day shift
            # for each given type of shift e.g.,  Absloute, Relative, Logarithmic

            for i in range(self.df.shape[0] - 1):
                    
                    # calculating 1-day shift while the shift type is Absloute
                    if  self.shift_type == "Absloute":

                        self.list.append(self.df[Asset].iloc[i] - self.df[Asset].iloc[i+1])

                    # calculating 1-day shift while the shift type is Logarithmic
                    elif self.shift_type== "Logarithmic":

                        self.list.append(np.exp(np.log(self.df[Asset].iloc[i]/self.df[Asset].iloc[i+1])) - 1)

                    # calculating 1-day shift while the shift type is Relative
                    elif self.shift_type== "Relative":

                        self.list.append((self.df[Asset].iloc[i]- self.df[Asset].iloc[i+1])/(self.df[Asset].iloc[i+1]))

            # Just for the convinience, the last element will be zero
            self.list.append(0)
            
            # Partial PnL is collecting share of each currency
            self.Parial_p_and_l["p & l"]   = self.Parial_p_and_l["p & l"] + pd.Series(self.list, name = "P & L")*Value

            # Clearing the list to be used again
            self.list = []
            
        # Sorting the obtained total PnL to select the second and third worst PnL    
        self.Parial_p_and_l = self.Parial_p_and_l.sort_values(by = "p & l", ascending = False)
        
        # According to the methodology. 
        self.VaR            = 0.4*self.Parial_p_and_l["p & l"].iloc[-2] + 0.6*self.Parial_p_and_l["p & l"].iloc[-3] 

        return self.VaR
    

    # The below method is calculating the VaR while looping over each currency 
    def p_and_l(self):

        self.loss_distribution = pd.DataFrame([], columns = ["P & L"])

        for Asset, Value in zip(self.list_curre, self.list_values):

            # For each given currency, the below part of code calculates the 1-day shift
            # for each given type of shift e.g.,  Absloute, Relative, Logarithmic

            for i in range(self.df.shape[0] - 1):
                    
                    # calculating 1-day shift while the shift type is Absloute
                    if  self.shift_type == "Absloute":

                        self.list.append(self.df[Asset].iloc[i] - self.df[Asset].iloc[i+1])

                    # calculating 1-day shift while the shift type is Logarithmic
                    elif self.shift_type== "Logarithmic":

                        self.list.append(np.exp(np.log(self.df[Asset].iloc[i]/self.df[Asset].iloc[i+1])) - 1)

                    # calculating 1-day shift while the shift type is Relative
                    elif self.shift_type== "Relative":

                        self.list.append((self.df[Asset].iloc[i]- self.df[Asset].iloc[i+1])/(self.df[Asset].iloc[i+1]))

            # Just for the convinience, the last element will be zero
            self.list.append(0)
            
            # Partial PnL is collecting share of each currency
            self.loss_distribution   = pd.concat([self.loss_distribution, pd.Series(self.list, name = str(Asset) + "P & L")], axis = 1)

            # Clearing the list to be used again
            self.list = []

        return self.loss_distribution
    
# if __name__=="__main__":
    
    # # Example usage
    # list_curre  = ["Currency 1", "Currency 2"]
    # list_values = [153084.81   ,  95891.51   ] 
    
    # df = pd.read_csv("/Users/vahid/Downloads/Project/Artifacts/VaR.csv")
    
    # Value_at_Risk_abs = VaR(df, list_curre, list_values, "Absloute")
    # Value_at_Risk_rel = VaR(df, list_curre, list_values, "Relative")
    # Value_at_Risk_log = VaR(df, list_curre, list_values, "Logarithmic")

    # Loss_distributions = Value_at_Risk_abs.p_and_l()
    
    # # print("The calculated Value at Risk (Var 1-d) while the shift type is Absloute is    :{:.2f}".format(Value_at_Risk_abs.Value_at_risk()))
    # # print("The calculated Value at Risk (Var 1-d) while the shift type is Relative is    :{:.2f}".format(Value_at_Risk_rel.Value_at_risk()))
    # # print("The calculated Value at Risk (Var 1-d) while the shift type is Logarithmic is :{:.2f}".format(Value_at_Risk_log.Value_at_risk()))
    
        
    # Results = [[float("{:.4f}".format(Value_at_Risk_abs.Value_at_risk())),
    #                            float("{:.4f}".format(Value_at_Risk_rel.Value_at_risk())),
    #                        float("{:.4f}".format(Value_at_Risk_log.Value_at_risk()))]]
    # column  = ["VaR (1-d) for shift type, Absloute", 
    #                                    "VaR (1-d) for shift type, Relative",
    #                                    "VaR (1-d) for shift type, Logarithmic"]
    
    # Result = pd.DataFrame(Results, columns = column)
    # Result.to_excel("/Users/vahid/Downloads/Project/Results/VaR.xlsx", index = False)