import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class ProductPreference:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)
    
    def get_preference(self, product_name, customer_type):
        return self.data.loc[self.data['Models'] == product_name][customer_type].values[0]

class TransmissionCost:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)
    
    def get_cost(self, platform_name, customer_type):
        index = customer_type[-1]
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

def display_roi_matrix(roi_calculator, products, platforms):

    # ... other parts of the code ...
    # Using a colorful colormap
    colors = plt.cm.jet(np.linspace(0, 1, len(platforms)))


    fig, axs = plt.subplots(2, 5, figsize=(20, 12))
    fig.tight_layout(pad=4.0)
    fig.subplots_adjust(bottom=0.2)  # Adjusting the bottom space for the legend

    for i, product in enumerate(products):
        rois = [roi_calculator.calculate(product, platform) for platform in platforms]
        ax = axs[i//5, i%5]
        bars = ax.bar(platforms, rois, color=colors)
        ax.set_title(product)
        ax.set_ylabel('ROI')
        ax.set_xticks([])  
        ax.set_ylim(0, max(rois) + 0.1)

    # Making the suptitle bold
    fig.suptitle("Investment Differences in Different Platforms Due to Product Preferences", fontsize=16, y=1.08, fontweight='bold')

    ax_legend = fig.add_axes([0.15, 0.08, 0.7, 0.05])
    ax_legend.axis('off')
    ax_legend.legend(handles=axs[0,0].containers[0], labels=platforms, 
                     loc='center', ncol=4, mode="expand")

    # Adding notes and copyrights
    fig.text(0.1, 0.01, "NOTE: For demonstration purposes only. Actual results may vary based on model training and parameters.", ha='left', fontsize=10, color='red')
    fig.text(0.9, 0.01, "2023 © kang xiaowen", ha='right', fontsize=10)

    plt.savefig("ROI_Comparison.png", dpi=300, bbox_inches='tight')
    plt.show()






if __name__ == "__main__":
    preference_file = 'd4_data_map_product_costomerType.csv'
    cost_file = 'd3_data_map_delivery_cost_media.csv'
    
    roi_calculator = ROICalculator(preference_file, cost_file)

    products = ['Toyota Corolla', 'Toyota RAV4', 'Toyota Camry', 'Toyota Land Cruiser', 'Toyota Hilux', 
                'Toyota Prius', 'Toyota Tacoma', 'Toyota Highlander', 'Toyota Sienna', 'Toyota 4Runner']
    
    platforms = ['Youtube', 'Facebook', 'WhatsApp', 'Instagram', 'WeChat', 'TikTok', 'QQ', 'Weibo', 'Twitter', 
                 'LinkedIn', 'Snapchat', 'Pinterest', 'Reddit', 'Telegram', 'LINE', 'Viber', 'IMO', 'Zalo', 'VK', 'Odnoklassniki']

    display_roi_matrix(roi_calculator, products, platforms)
