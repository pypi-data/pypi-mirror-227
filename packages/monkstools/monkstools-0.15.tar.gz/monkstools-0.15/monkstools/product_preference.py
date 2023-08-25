import pandas as pd



import pandas as pd

class ProductPreference:
    def __init__(self, file_path):
        print("ProductPreference: Loading the preference data...")
        self.data = pd.read_csv(file_path)
        print("ProductPreference: Data loaded successfully!")
    
    def get_preference(self, product_name, customer_type,verbose=False):
        if verbose:
            print(f"ProductPreference: Calculating preference for {product_name} and {customer_type}...")
        preference = self.data.loc[self.data['Models'] == product_name][customer_type].values[0]
        if verbose:
            print(f"ProductPreference: Preference calculation complete! Passing to the next function...")
        return preference


# class ProductPreference:
#     def __init__(self, file_path):
#         self.data = pd.read_csv(file_path)
    
#     def get_preference(self, product_name, customer_type):
#         return self.data.loc[self.data['Models'] == product_name][customer_type].values[0]
