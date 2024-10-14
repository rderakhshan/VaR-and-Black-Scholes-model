import numpy as np
import pandas as pd
from datetime import datetime, timedelta
 

def data_transformation(df):
    
    # Selecting only required columns and renaming columns for just a convinience
    df = df[["date", "Portfolio", "market rate", "market rate.1"]]

    df = df.rename(columns = {"date":"Date", "market rate":"Currency 1",
                                            "market rate.1":"Currency 2"})

    df.to_csv("./Artifacts/VaR.csv")
    
def Option_results_generator(D1_forward, D2_forward, D1_spot, D2_spot, call_forward, put_forward, call_spot, put_spot):
    
    # print("Calculated d1 and d2 from forward price method are: ({:.4f}, {:.4f})".format(D1_forward, D2_forward))
    
    # print("Calculated d1 and d2 from spot price method are: ({:.4f}, {:.4f})".format(D1_spot, D2_spot))
    
    # print("Calculated d1 and d2 from spot price method are: ({:.4f}, {:.4f})".format(call_forward, put_forward))
    
    # print("Calculated d1 and d2 from spot price method are: ({:.4f}, {:.4f})".format(call_spot, put_spot))
    
    Result = pd.DataFrame([[D1_forward, D2_forward, call_forward,put_forward ],
        [D1_spot, D2_spot, call_spot, put_spot]], columns = ["d1 ", "d2", "call", "put"], index = ["with forward price", "with spot price"])

    Result.to_excel("./Results/Options.xlsx")    

def VaR_outout_generator(VaRs):

    column  = ["VaR (1-d) for shift type, Absloute", 
                                        "VaR (1-d) for shift type, Relative",
                                        "VaR (1-d) for shift type, Logarithmic"]
    VaRs = pd.DataFrame(VaRs, columns = column)
    VaRs.to_excel("./Results/VaR.xlsx", index = False)
    

def unit_test_parity(Trade_date, Expire_date, Spot_price, Strike_price, Interest_rate):

    # end def# Convert the input date strings to datetime objects
    start_date = datetime.strptime(Trade_date, '%m/%d/%Y')
    end_date = datetime.strptime(Expire_date  , '%m/%d/%Y')

    # Calculate the total number of days between the start and end dates
    total_days = (end_date - start_date).days

    time_horozon = ((end_date - start_date).days)/365

    # Parity condition C - P = S - DK

    c_p = float(Spot_price - Strike_price*np.exp(- Interest_rate*time_horozon))
    
    print(float("{:.2f}".format(c_p)))

    return  float("{:.2f}".format(c_p))
