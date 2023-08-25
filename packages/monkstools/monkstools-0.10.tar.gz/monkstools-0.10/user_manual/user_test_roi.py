# user_test_roi.py
import pkg_resources
import matplotlib.pyplot as plt
from monkstools.roi_calculator import ROICalculator, display_roi_matrix  # Assuming the filename is 'roi_calculator.py'

def test_display_roi_matrix():

    # 
    preference_file = pkg_resources.resource_filename('monkstools', 'd4_data_map_product_costomerType.csv')
    cost_file = pkg_resources.resource_filename('monkstools', 'd3_data_map_delivery_cost_media.csv')
    
    roi_calculator = ROICalculator(preference_file, cost_file)

    products = ['Toyota Corolla', 'Toyota RAV4', 'Toyota Camry', 'Toyota Land Cruiser', 'Toyota Hilux', 
                'Toyota Prius', 'Toyota Tacoma', 'Toyota Highlander', 'Toyota Sienna', 'Toyota 4Runner']
    
    platforms = ['Youtube', 'Facebook', 'WhatsApp', 'Instagram', 'WeChat', 'TikTok', 'QQ', 'Weibo', 'Twitter', 
                 'LinkedIn', 'Snapchat', 'Pinterest', 'Reddit', 'Telegram', 'LINE', 'Viber', 'IMO', 'Zalo', 'VK', 'Odnoklassniki']

    display_roi_matrix(roi_calculator, products, platforms)

    # Verify manually by checking the displayed chart or saved "ROI_Comparison.png"
    # Optionally, you could also add some automated assertions here based on expected values or behaviors

if __name__ == "__main__":
    test_display_roi_matrix()
    print("Test executed. Please verify the output chart.")
