import pkg_resources
from monkstools import ROICalculator

def display_roi_matrix(roi_calculator, products, platforms):
    for product in products:
        for platform in platforms:
            roi = roi_calculator.calculate(product, platform)
            print(f"ROI for {product} on {platform}: {roi}")

def main():
    # 使用pkg_resources获取CSV文件的路径
    preference_file_path = pkg_resources.resource_filename('monkstools', 'd4_data_map_product_costomerType.csv')
    cost_file_path = pkg_resources.resource_filename('monkstools', 'd3_data_map_delivery_cost_media.csv')
    
    roi_calculator = ROICalculator(preference_file_path, cost_file_path)

    products = ['Toyota Corolla', 'Toyota RAV4', 'Toyota Camry', 'Toyota Land Cruiser', 'Toyota Hilux', 
                'Toyota Prius', 'Toyota Tacoma', 'Toyota Highlander', 'Toyota Sienna', 'Toyota 4Runner']
    
    platforms = ['Youtube', 'Facebook', 'WhatsApp', 'Instagram', 'WeChat', 'TikTok', 'QQ', 'Weibo', 'Twitter', 
                 'LinkedIn', 'Snapchat', 'Pinterest', 'Reddit', 'Telegram', 'LINE', 'Viber', 'IMO', 'Zalo', 'VK', 'Odnoklassniki']

    display_roi_matrix(roi_calculator, products, platforms)

if __name__ == "__main__":
    main()
