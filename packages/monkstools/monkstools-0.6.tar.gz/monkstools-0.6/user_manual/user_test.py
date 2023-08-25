from monkstools.top_module import TopModule

def main():
    # Sample user data
    data = {
        "person_group": "TensorData Representation",  # Replace with actual data
        "secondary_preference": "Preferences Dataset"  # Replace with actual data
    }

    # Utilizing monkstools for ROI computation
    instance = TopModule(data)
    instance.calculate_roi()
    instance.display_results()

if __name__ == "__main__":
    main()