# monkstools/top_module.py

from person_group import PersonGroup
from secondary_preference import SecondaryPreference

class TopModule:
    def __init__(self, data):
        print("a) Initiating TopModule program...")
        self.person_group = PersonGroup(data['person_group'])
        self.secondary_preference = SecondaryPreference(data['secondary_preference'])

    def calculate_roi(self):
        print("b) Starting ROI calculation...")
        # Call analyze methods from submodules
        self.person_group.analyze()
        self.secondary_preference.analyze()

        result = "Some ROI Calculation Result"  # This is just an example
        print(f"c) The result is: {result}")

    def display_results(self):
        print("d) Done.")

# Test statement
if __name__ == "__main__":
    sample_data = {
        "person_group": "...",  # mock data
        "secondary_preference": "..."  # mock data
    }
    top_module = TopModule(sample_data)
    top_module.calculate_roi()
    top_module.display_results()
