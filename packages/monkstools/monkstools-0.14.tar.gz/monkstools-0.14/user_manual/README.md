### README.md

---

# monkstools: Advertising Delivery ROI Analysis Framework

`monkstools` is a Python module designed to analyze and visualize the Return on Investment (ROI) of product advertising across different platforms. It provides insights into which platform might yield the highest returns for advertising a particular product. While this framework is provided for demonstration purposes, the actual results in a production setting would be based on in-depth model training and real-world data.

## Overview

The primary goal of `monkstools` is to serve as a platform for programmers and data analysts to discuss, share, and collaborate on analyzing the ROI of advertising delivery. It's a template to kick-start discussions and exchange ideas on the intricacies of advertising dynamics across different platforms for various products.

## Key Components

**1. ProductPreference Class**
- **Purpose**: Retrieve product preference values for specified products and customer types.
- **Primary Method**: `get_preference(product_name, customer_type, verbose=False)`

**2. TransmissionCost Class**
- **Purpose**: Fetch transmission cost values for designated platforms and customer types.
- **Primary Method**: `get_cost(platform_name, customer_type, verbose=False)`

**3. ROICalculator Class**
- **Purpose**: Compute and visualize ROIs.
- **Primary Methods**:
  - `calculate(product_name, platform_name, verbose=False)`: Computes the ROI for a given product and platform.
  - `display_roi_matrix(roi_calculator, products, platforms)`: Visualizes the ROI matrix.

## Usage Guide

**1. Initialization**

   First, you need to initialize the `ROICalculator` object, which, in turn, initializes the `ProductPreference` and `TransmissionCost` objects.
   
   ```python
   preference_file = 'path_to_preference_file.csv'
   cost_file = 'path_to_cost_file.csv'
   roi_calculator = ROICalculator(preference_file, cost_file)
   ```

**2. Setting Up Products and Platforms**

   Define the list of products and platforms you're interested in analyzing.

   ```python
   products = ['Example Product 1', ...]  
   platforms = ['Example Platform 1', ...] 
   ```

**3. Displaying the ROI Matrix**

   Use the `display_roi_matrix` method of the `ROICalculator` class to compute and showcase the ROI matrix.

   ```python
   ROICalculator.display_roi_matrix(roi_calculator, products, platforms)
   ```

**4. Debugging and Logging**

   Set `verbose=True` when calling methods to print additional debugging and logging information.

## Note

This framework is intended for team discussions and sharing. The specific functions and data here are examples, and in a real-world scenario, deeper model training would be necessary. The final outcome is contingent on actual data and post-deep-training results. This is merely a conceptual framework and thought process to facilitate programmers' exchange of ideas.

---

To leverage this library, ensure `monkstools` is installed and data provided matches expected formats.

---

xiaowen kang. 2023.8.23