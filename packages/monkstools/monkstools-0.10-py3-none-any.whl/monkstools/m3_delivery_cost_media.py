# 在monkstools/platform_customers.py
import pandas as pd
import matplotlib.pyplot as plt

class PlatformCustomers:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)

    def get_platform_customer_preference(self, platform_name, customer_type):
        return self.data.loc[self.data['Media'] == platform_name][customer_type].values[0]

    def get_transmission_cost(self, platform_name, customer_type):
        return self.data.loc[self.data['Media'] == platform_name]["Cost"+customer_type[-1]].values[0]

if __name__ == "__main__":
    platforms = PlatformCustomers('d3_data_map_delivery_cost_media.csv')

    # 1. 打印数据
    print(platforms.data)
    
    # 2. 展示图：每类客户对20类媒体的偏好
    medias = platforms.data['Media'].unique()  # 提取所有媒体的名字
    customer_columns = ["CustomerType1", "CustomerType2", "CustomerType3", "CustomerType4", "CustomerType5"]
    number_of_customers = len(customer_columns)

    fig, axarr = plt.subplots(number_of_customers, 1, figsize=(15, 20))
    
    for idx, customer in enumerate(customer_columns): 
        customer_values = [platforms.get_platform_customer_preference(media, customer) for media in medias]
        axarr[idx].bar(medias, customer_values)
        axarr[idx].set_title(f'{customer} Media Preferences')
        axarr[idx].set_ylabel('Preference Value')
        axarr[idx].tick_params(axis='x', rotation=45)
        
    plt.tight_layout()
    plt.show()
