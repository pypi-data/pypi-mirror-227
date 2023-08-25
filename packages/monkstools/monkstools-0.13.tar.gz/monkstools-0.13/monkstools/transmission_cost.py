import pandas as pd


class TransmissionCost:
    def __init__(self, file_path):
        print("TransmissionCost: Loading the transmission cost data...")
        self.data = pd.read_csv(file_path)
        print("TransmissionCost: Data loaded successfully!")
    
    def get_cost(self, platform_name, customer_type, verbose=False):
        if verbose:
            print(f"TransmissionCost: Calculating cost for {platform_name} and {customer_type}...")
        index = customer_type[-1]
        cost_values = self.data.loc[self.data['Media'] == platform_name]["Cost"+index].values
        if len(cost_values) == 0:
            raise ValueError(f"No cost found for platform {platform_name} and customer type {customer_type}")
        if verbose:
            print(f"TransmissionCost: Cost calculation complete! Passing to the next function...")
        return cost_values[0]
