import pandas as pd
import matplotlib.pyplot as plt

class CustomerPreferences:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)

    def get_customer_preference(self, product_name, preference_name):
        return self.data.loc[self.data['Product'] == product_name][preference_name].values[0]

if __name__ == "__main__":
    preferences = CustomerPreferences('d2_data_map_perfer_product_customer.csv')
    
    # 1. 打印数据
    print(preferences.data)
    
    # 2. 绘制不同产品对不同用户的偏好
    products = preferences.data['Product'].unique()  # Assuming the products are under the "Product" column
    
    customer_columns = ["CustomerType1", "CustomerType2", "CustomerType3", "CustomerType4", "CustomerType5"]
    number_of_customers = len(customer_columns)

    fig, axarr = plt.subplots(number_of_customers, 1, figsize=(15, 20))
    
    for idx, customer in enumerate(customer_columns): 
        customer_values = [preferences.get_customer_preference(product, customer) for product in products]
        axarr[idx].bar(products, customer_values)
        axarr[idx].set_title(f'{customer} Product Preferences')
        axarr[idx].set_ylabel('Preference Value')
        axarr[idx].tick_params(axis='x', rotation=45)
        
    plt.tight_layout()
    plt.show()
