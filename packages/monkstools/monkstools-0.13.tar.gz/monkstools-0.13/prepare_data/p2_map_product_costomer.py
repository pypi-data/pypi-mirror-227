import csv
import random
import matplotlib.pyplot as plt

# Top 10 Toyota models globally
models = ["Toyota Corolla", "Toyota RAV4", "Toyota Camry", "Toyota Land Cruiser", "Toyota Hilux", "Toyota Prius", "Toyota Tacoma", "Toyota Highlander", "Toyota Sienna", "Toyota 4Runner"]

# Product features
features = ["EcoFriendly", "SeatCount", "Mileage", "PowerConsumption", "Price", "EnergySaving", "Speed", "MultiPurpose"]

# Customer categories
customer_categories = ["CustomerType1", "CustomerType2", "CustomerType3", "CustomerType4", "CustomerType5"]

# Generate CSV file
with open('d2_data_map_perfer_product_customer.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write header
    writer.writerow(["Product"] + features + customer_categories)
    # Generate data for 10 products
    for i in range(10):
        product_data = [models[i]]
        # Generate data for features
        for _ in features:
            product_data.append(round(random.uniform(0.5, 0.9), 2))
        # Generate preference data for each customer type
        for _ in customer_categories:
            product_data.append(round(random.uniform(0, 1), 2))
        writer.writerow(product_data)

# Print the first few lines of the CSV
with open('d2_data_map_perfer_product_customer.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for i, row in enumerate(reader):
        if i <= 3:  # Print header and first three products
            print(row)

# Plotting preference of first three products for different customer types
with open('d2_data_map_perfer_product_customer.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header

    fig, axs = plt.subplots(3, 1, figsize=(10, 12))
    
    for ax in axs:
        product_data = next(reader)
        product_name = product_data[0]
        customer_preferences = product_data[len(features)+1:]
        
        ax.bar(customer_categories, [float(val) for val in customer_preferences])
        ax.set_title(product_name + "'s Customer Preferences")
        ax.set_ylabel('Preference Score')
        ax.set_ylim(0, 1)
    
    plt.tight_layout()
    plt.show()
