# 在monkstools/customer_preferences.py
import pandas as pd

class CustomerPreferences:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)

    def get_customer_preference(self, customer_name, preference_name):
        return self.data.loc[self.data['客户'] == customer_name][preference_name].values[0]
