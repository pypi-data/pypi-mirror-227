import csv
import random
import matplotlib.pyplot as plt

# Top 10 Toyota models globally
models = ["Toyota Corolla", "Toyota RAV4", "Toyota Camry", "Toyota Land Cruiser", "Toyota Hilux", "Toyota Prius", "Toyota Tacoma", "Toyota Highlander", "Toyota Sienna", "Toyota 4Runner"]

# Customer categories
customer_categories = ["CustomerType1", "CustomerType2", "CustomerType3", "CustomerType4", "CustomerType5"]

# Generate CSV file
filename = 'd4_data_map_product_costomerType.csv'
with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write header
    headers = ["Models"] + customer_categories
    writer.writerow(headers)

    # Generate data for each model
    for model in models:
        model_data = [model]
        for _ in customer_categories:
            model_data.append(round(random.uniform(0, 1), 2))
        writer.writerow(model_data)

# Print a few lines of the CSV
with open(filename, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for i, row in enumerate(reader):
        if i <= 2:  # Print header and first two models
            print(row)

# Plotting attraction level of different Toyota models for each customer category
data = []
with open(filename, 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header
    for row in reader:
        data.append(row)

fig, axs = plt.subplots(5, 1, figsize=(15, 15))
for idx, ax in enumerate(axs):
    attraction_levels = [float(row[idx + 1]) for row in data]
    ax.bar(models, attraction_levels)
    ax.set_title(customer_categories[idx] + "'s Attraction Level for Different Toyota Models")
    ax.set_ylabel('Attraction Level')
    ax.set_ylim(0, 1)
    ax.set_xticklabels(models, rotation=45, ha='right')
    
plt.tight_layout()
plt.show()
