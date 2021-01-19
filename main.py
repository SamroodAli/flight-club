from data_manager import DataManager


# Instances needed
data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
print(sheet_data)