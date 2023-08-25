# 在monkstools/m1_get_customer_media.py


import pandas as pd
import matplotlib.pyplot as plt

class CustomerPreferences:
    def __init__(self):
        self.data = pd.read_csv('d1_data_map_customer_media.csv')

    def get_customer_preference(self, customer_name, *preference_names):
        return self.data.loc[self.data['Customer'] == customer_name][list(preference_names)].values[0]

if __name__ == "__main__":
    preferences = CustomerPreferences()
    
    # 1. 打印Car
    car_value = preferences.get_customer_preference('Customer1', 'Car')
    print(f"Customer1's preference for Car: {car_value[0]}")
    
    # 2. 打印Car, Youtube
    car_youtube_values = preferences.get_customer_preference('Customer1', 'Car', 'Youtube')
    print(f"Customer1's preference for Car: {car_youtube_values[0]}, Youtube: {car_youtube_values[1]}")

    media_list = ["Car", "EcoFriendly", "OrganicFood", "QualityEducation", "RealEstate", "FitnessAndSport", 
                  "Youtube", "Facebook", "WhatsApp", "Instagram", "WeChat", "TikTok", "QQ", 
                  "Weibo", "Twitter", "LinkedIn", "Snapchat", "Pinterest", "Reddit", "Telegram"]
    
    # 3. 打印第一个客户，对20个媒体的偏好度
    values_customer1 = preferences.get_customer_preference('Customer1', *media_list)
    for media, value in zip(media_list, values_customer1):
        print(f"Customer1's preference for {media}: {value}")

    values_customer2 = preferences.get_customer_preference('Customer2', *media_list)

    fig, ax = plt.subplots(2, 1, figsize=(15, 10))
    
    ax[0].bar(media_list, values_customer1)
    ax[0].set_title('Customer1 Media Preferences')
    ax[0].set_ylabel('Preference Value')
    ax[0].tick_params(axis='x', rotation=45)
    
    ax[1].bar(media_list, values_customer2)
    ax[1].set_title('Customer2 Media Preferences')
    ax[1].set_ylabel('Preference Value')
    ax[1].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.show()
