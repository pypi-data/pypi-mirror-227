from product_preference import ProductPreference
from transmission_cost import TransmissionCost
from roi_calculator import ROICalculator

if __name__ == "__main__":
    print("roi_main: Initiating the main module...")
    
    preference_file = 'd4_data_map_product_costomerType.csv'
    cost_file = 'd3_data_map_delivery_cost_media.csv'
    
    print("roi_main: Creating the ROI Calculator object...")
    roi_calculator = ROICalculator(preference_file, cost_file)

    products = ['Toyota Corolla', 'Toyota RAV4', 'Toyota Camry', 'Toyota Land Cruiser', 'Toyota Hilux', 
                'Toyota Prius', 'Toyota Tacoma', 'Toyota Highlander', 'Toyota Sienna', 'Toyota 4Runner']
    
    platforms = ['Youtube', 'Facebook', 'WhatsApp', 'Instagram', 'WeChat', 'TikTok', 'QQ', 'Weibo', 'Twitter', 
                 'LinkedIn', 'Snapchat', 'Pinterest', 'Reddit', 'Telegram', 'LINE', 'Viber', 'IMO', 'Zalo', 'VK', 'Odnoklassniki']


    print("roi_main: Displaying the ROI matrix...")
    ROICalculator.display_roi_matrix(roi_calculator, products, platforms)
    print("roi_main: Completed!")


