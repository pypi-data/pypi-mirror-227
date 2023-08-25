# 在monkstools/roi_calculator.py
# from m1_get_customer_media import CustomerPreferences
# # from m2_get_product import ProductModule
# from m3_delivery_cost_media import PlatformCustomers
# from m4_product_costomerType import ProductCustomers
import pandas as pd
import matplotlib.pyplot as plt

class ProductPreference:
    def __init__(self, file_path):
        self.data = pd.read_csv('d4_data_map_product_costomerType.csv')
    
    def get_preference(self, product_name, customer_type):
        return self.data.loc[self.data['Models'] == product_name][customer_type].values[0]


class TransmissionCost:
    def __init__(self, file_path):
        self.data = pd.read_csv('d3_data_map_delivery_cost_media.csv')
    
    # def get_cost(self, platform_name, customer_type):
    #     return self.data.loc[self.data['Media'] == platform_name]["Cost"+customer_type[-1]].values[0]
    def get_cost(self, platform_name, customer_type):
        # Check if platform_name is in the data
        if platform_name not in self.data['Media'].values:
            raise ValueError(f"{platform_name} not found in the data.")

        # Check if customer_type index is valid
        index = customer_type[-1]
        if index not in ['1', '2', '3', '4', '5']:
            raise ValueError(f"Invalid customer type index: {index}")

        # Retrieve the cost
        cost_values = self.data.loc[self.data['Media'] == platform_name]["Cost"+index].values
        if len(cost_values) == 0:
            raise ValueError(f"No cost found for platform {platform_name} and customer type {customer_type}")
        
        return cost_values[0]



class ROICalculator:
    def __init__(self, preference_file, cost_file):
        self.product_pref = ProductPreference(preference_file)
        self.trans_cost = TransmissionCost(cost_file)

    def calculate(self, product_name, platform_name):
        total_cost = 1
        total_roi = 0
        
        for i in range(1, 6):  # 5 types of customers
            customer_type = f"CustomerType{i}"
            preference = self.product_pref.get_preference(product_name, customer_type)
            transmission_cost = self.trans_cost.get_cost(platform_name, customer_type)
            total_roi += preference * (total_cost / transmission_cost)
        
        return total_roi




def display_roi(roi_calculator, products, platforms):
    data = {}
    for platform in platforms:
        roi_values = []
        for product in products:
            roi_values.append(roi_calculator.calculate(product, platform))
        data[platform] = roi_values
    
    for platform, values in data.items():
        plt.figure(figsize=(15, 7))
        plt.bar(products, values)
        plt.xlabel('Products')
        plt.ylabel('ROI Value')
        plt.title(f'ROI Values for Different Products on {platform}')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


# if __name__ == "__main__":
#     preference_file = 'd4_data_map_product_costomerType.csv'
#     cost_file = 'd3_data_map_delivery_cost_media.csv'
    
#     roi_calculator = ROICalculator(preference_file, cost_file
#     display_roi(roi_calculator, products, platforms)
def display_roi_matrix(roi_calculator, products, platforms):
    fig, axs = plt.subplots(2, 5, figsize=(20, 10))
    fig.tight_layout(pad=4.0)

    for i, product in enumerate(products):
        rois = [roi_calculator.calculate(product, platform) for platform in platforms]
        ax = axs[i//5, i%5]
        ax.bar(platforms, rois, color='skyblue')
        ax.set_title(product)
        ax.set_ylabel('ROI')
        ax.set_xticks([])
        ax.set_ylim(0, max(rois) + 0.1)  # Adding some padding on top
        if i >= 5:  # only the bottom subplots should have x labels
            ax.set_xticks(platforms)
            ax.set_xticklabels(platforms, rotation=90)

    plt.show()


if __name__ == "__main__":
    preference_file = 'd4_data_map_product_costomerType.csv'
    cost_file = 'd3_data_map_delivery_cost_media.csv'
    
    roi_calculator = ROICalculator(preference_file, cost_file)

    products = ['Toyota Corolla', 'Toyota RAV4', 'Toyota Camry', 'Toyota Land Cruiser', 'Toyota Hilux', 
                'Toyota Prius', 'Toyota Tacoma', 'Toyota Highlander', 'Toyota Sienna', 'Toyota 4Runner']
    
    platforms = ['Youtube', 'Facebook', 'WhatsApp', 'Instagram', 'WeChat', 'TikTok', 'QQ', 'Weibo', 'Twitter', 
                 'LinkedIn', 'Snapchat', 'Pinterest', 'Reddit', 'Telegram', 'LINE', 'Viber', 'IMO', 'Zalo', 'VK', 'Odnoklassniki']

    import matplotlib.pyplot as plt



    # ... Assuming your ROI calculator and lists of products/platforms are set up as before ...
    display_roi_matrix(roi_calculator, products, platforms)

    #display_roi(roi_calculator, products, platforms)


