import csv
import random
import matplotlib.pyplot as plt

# 20个主要的媒体平台
media_platforms = ["Youtube", "Facebook", "WhatsApp", "Instagram", "WeChat", "TikTok", "QQ", "Weibo", "Twitter", "LinkedIn", "Snapchat", "Pinterest", "Reddit", "Telegram", "LINE", "Viber", "IMO", "Zalo", "VK", "Odnoklassniki"]

# 偏好列表
preferences = ["Car", "EcoFriendly", "OrganicFood", "QualityEducation", "RealEstate", "FitnessAndSport"]

# 生成CSV文件
with open('d1_data_map_customer_media.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # 写入标题
    writer.writerow(["Customer"] + preferences + media_platforms)
    # 为100个客户生成数据
    for i in range(1, 101):
        customer_name = "Customer" + str(i)
        customer_data = [customer_name]
        # 生成偏好数据
        for _ in preferences:
            customer_data.append(round(random.uniform(0, 1), 2))
        # 生成媒体偏好数据
        for _ in media_platforms:
            customer_data.append(round(random.uniform(0, 1), 2))
        writer.writerow(customer_data)

# 绘制前三个客户的媒体偏好图
with open('d1_data_map_customer_media.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # 跳过标题行
    fig, axs = plt.subplots(3, 1, figsize=(15, 12))
    
    for ax in axs:
        customer_data = next(reader)
        customer_name = customer_data[0]
        media_preferences = customer_data[len(preferences)+1:]
        
        ax.bar(media_platforms, [float(val) for val in media_preferences])
        ax.set_title(customer_name + "'s Media Preferences")
        ax.set_ylabel('Preference Score')
        ax.set_ylim(0, 1)
        ax.set_xticklabels(media_platforms, rotation=45, ha="right")
    
    plt.tight_layout()
    plt.show()
