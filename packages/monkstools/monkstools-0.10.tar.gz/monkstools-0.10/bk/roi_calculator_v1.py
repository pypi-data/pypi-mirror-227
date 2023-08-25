import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
# ROI Calculator is as defined in previous examples
# products and platforms are lists as defined before

class ROICalculator:
    # This is just a placeholder, you can replace it with the actual calculation method
    def calculate(self, product, platform):
        # For the sake of this example, return a random ROI between 0 and 1.
        import random
        return random.random()

roi_calculator = ROICalculator()

products = ["Toyota Corolla", "Toyota RAV4", "Toyota Camry", "Toyota Land Cruiser", "Toyota Hilux",
            "Toyota Prius", "Toyota Tacoma", "Toyota Highlander", "Toyota Sienna", "Toyota 4Runner"]

platforms = ["Youtube", "Facebook", "WhatsApp", "Instagram", "WeChat", "TikTok", "QQ", "Weibo",
             "Twitter", "LinkedIn", "Snapchat", "Pinterest", "Reddit", "Telegram", "LINE",
             "Viber", "IMO", "Zalo", "VK", "Odnoklassniki"]

# Specifying colors for each platform
colors = plt.cm.viridis(np.linspace(0, 1, len(platforms)))

def display_roi_matrix(roi_calculator, products, platforms):
    fig, axs = plt.subplots(2, 5, figsize=(20, 10))
    fig.tight_layout(pad=4.0)

    for i, product in enumerate(products):
        rois = [roi_calculator.calculate(product, platform) for platform in platforms]
        ax = axs[i//5, i%5]
        bars = ax.bar(platforms, rois, color=colors)
        ax.set_title(product)
        ax.set_ylabel('ROI')
        ax.set_xticks([])
        ax.set_ylim(0, max(rois) + 0.1)  # Adding some padding on top
        if i == 9:  # only the last subplot should have x labels for clarity
            ax.set_xticks(platforms)
            ax.set_xticklabels(platforms, rotation=90)

    # Adding a legend for the platforms
    fig.subplots_adjust(bottom=0.25)
    ax_legend = fig.add_axes([0.15, 0.08, 0.7, 0.05])
    ax_legend.axis('off')
    ax_legend.legend(handles=axs[0,0].containers[0], labels=platforms, 
                     loc='center', ncol=4, mode="expand")

    # Saving the figure to an image
    plt.savefig("ROI_Comparison.png", dpi=300, bbox_inches='tight')
    plt.show()

display_roi_matrix(roi_calculator, products, platforms)
