import csv
import random
import matplotlib.pyplot as plt

# 20 major media platforms
media_platforms = ["Youtube", "Facebook", "WhatsApp", "Instagram", "WeChat", "TikTok", "QQ", "Weibo", "Twitter", "LinkedIn", "Snapchat", "Pinterest", "Reddit", "Telegram", "LINE", "Viber", "IMO", "Zalo", "VK", "Odnoklassniki"]

# Customer categories
customer_categories = ["CustomerType1", "CustomerType2", "CustomerType3", "CustomerType4", "CustomerType5"]

# Generate CSV file
filename = 'd3_data_map_delivery_cost_media.csv'
with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write header
    headers = ["Media"] + customer_categories + ["Cost"+str(i+1) for i in range(len(customer_categories))]
    writer.writerow(headers)

    # Generate data for each media platform
    for media in media_platforms:
        media_data = [media]
        for _ in customer_categories:
            media_data.append(round(random.uniform(0, 1), 2))
        for _ in customer_categories:
            media_data.append(round(random.uniform(0, 1), 2))
        writer.writerow(media_data)

# Print a few lines of the CSV
with open(filename, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for i, row in enumerate(reader):
        if i <= 2:  # Print header and first two media
            print(row)

# Plotting cost of transmission for different media platforms for each customer category
data = []
with open(filename, 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header
    for row in reader:
        data.append(row)

fig, axs = plt.subplots(5, 1, figsize=(15, 15))
for idx, ax in enumerate(axs):
    costs = [float(row[idx + len(customer_categories) + 1]) for row in data]
    ax.bar(media_platforms, costs)
    ax.set_title(customer_categories[idx] + "'s Transmission Cost on Different Media Platforms'")
    ax.set_ylabel('Cost')
    ax.set_ylim(0, 1)
    ax.set_xticklabels(media_platforms, rotation=45, ha='right')
    
plt.tight_layout()
plt.show()
