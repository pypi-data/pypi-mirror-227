# 在monkstools/product_customers.py
import pandas as pd
import matplotlib.pyplot as plt

class ProductCustomers:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)

    def get_customer_product_preference(self, customer_name, product_name):
        return self.data.loc[self.data['Models'] == product_name][customer_name].values[0]

if __name__ == "__main__":
    products = ProductCustomers('d4_data_map_product_costomerType.csv')
    
    # 1. 打印数据
    print(products.data)

    # 2. 绘制图片：5类客户对10类产品的偏好
    models = products.data['Models'].unique()  # 提取所有产品的名字
    customer_columns = ["CustomerType1", "CustomerType2", "CustomerType3", "CustomerType4", "CustomerType5"]
    number_of_customers = len(customer_columns)

    fig, axarr = plt.subplots(1, number_of_customers, figsize=(20, 5))

    for idx, customer in enumerate(customer_columns): 
        customer_values = [products.get_customer_product_preference(customer, model) for model in models]
        axarr[idx].bar(models, customer_values)
        axarr[idx].set_title(f'{customer} Product Preferences')
        axarr[idx].set_ylabel('Preference Value')
        axarr[idx].tick_params(axis='x', rotation=45)
        
    plt.tight_layout()
    plt.show()
