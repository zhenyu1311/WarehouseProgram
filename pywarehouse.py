class StorageBin:
    def __init__(self, rack, shelf, bin, length, width, depth, load_capacity):
        self.rack = rack
        self.shelf = shelf
        self.bin = bin
        self.length = length
        self.width = width
        self.depth = depth
        self.load_capacity = load_capacity
        self.remaining_volume = length * width * depth
        self.remaining_weight = load_capacity
        self.items_inside = {}

    @property
    def id(self):
        return f"Rack {self.rack} Shelf {self.shelf} Bin {self.bin}"

    def add_item(self, item, quantity=1):
        if item.name in self.items_inside:
            self.items_inside[item.name]["quantity"] += quantity
        else:
            self.items_inside[item.name] = {"quantity": quantity, "weight": item.weight * quantity}

    def remove_item(self, item_name, quantity):
        if item_name in self.items_inside:
            current_quantity = self.items_inside[item_name]["quantity"]
            if quantity <= current_quantity:
                self.items_inside[item_name]["quantity"] -= quantity
                self.items_inside[item_name]["weight"] -= item.weight * quantity
                print(f"Removed {quantity} {item_name}(s) from {self.id}.")
                print(f"Remaining Volume in {self.id}: {self.remaining_volume} cm^3")
                print(f"Remaining Weight in {self.id}: {self.remaining_weight} kg")
            else:
                print(f"Not enough {item_name}(s) in {self.id}.")
        else:
            print(f"No {item_name}(s) in {self.id}.")

class InventoryItem:
    def __init__(self, sku, name, length, width, height, weight):
        self.sku = sku
        self.name = name
        self.length = length
        self.width = width
        self.height = height
        self.weight = weight

    def __str__(self):
        return f"{self.name} (SKU: {self.sku}, Dimensions: {self.length}x{self.width}x{self.height} cm, Weight: {self.weight} kg)"

class StorageShelf:
    def __init__(self, rack, shelf, num_bins, bin_length, bin_width, bin_depth, bin_load_capacity):
        self.rack = rack
        self.shelf = shelf
        self.bins = [StorageBin(rack, shelf, bin, bin_length, bin_width, bin_depth, bin_load_capacity)
                     for bin in range(1, num_bins + 1)]

class StorageRack:
    def __init__(self, rack, num_shelves, num_bins, bin_length, bin_width, bin_depth, bin_load_capacity):
        self.rack = rack
        self.shelves = [StorageShelf(rack, shelf, num_bins, bin_length, bin_width, bin_depth, bin_load_capacity)
                       for shelf in range(1, num_shelves + 1)]

class Warehouse:
    def __init__(self):
        self.storage_racks = []
        self.inventory_items = []  # List to store created InventoryItem instances

    def create_storage_rack(self, rack_number, num_shelves, num_bins_per_shelf, bin_length, bin_width, bin_depth, bin_load_capacity):
        rack = StorageRack(rack_number, num_shelves, num_bins_per_shelf, bin_length, bin_width, bin_depth, bin_load_capacity)
        self.storage_racks.append(rack)

    def add_possible_item(self, item):
        # Add an InventoryItem to the inventory list for possible addition later
        self.inventory_items.append(item)
        print(f"Item {item.name} added to possible items for addition.")

    def add_item_to_warehouse(self):
        if not self.inventory_items:
            print("No items available in the inventory. Add items before attempting to add to the warehouse.")
            return

        print("Available Items:")
        for i, item in enumerate(self.inventory_items, start=1):
            print(f"{i}. {item}")

        item_index = int(input("Enter the index of the item you want to add to the warehouse: ")) - 1

        if not (0 <= item_index < len(self.inventory_items)):
            print("Invalid item index. Please choose a valid item.")
            return

        selected_item = self.inventory_items[item_index]

        print("Available Bins:")
        for rack in self.storage_racks:
            for shelf in rack.shelves:
                for bin in shelf.bins:
                    print(f"{bin.id} - Remaining Volume: {bin.remaining_volume} cm^3, Remaining Weight: {bin.remaining_weight} kg")

        rack_number = int(input("Enter the rack number for the bin: "))
        shelf_number = int(input("Enter the shelf number for the bin: "))
        bin_number = int(input("Enter the bin number: "))

        selected_bin = None
        for rack in self.storage_racks:
            if rack.rack == rack_number:
                for shelf in rack.shelves:
                    if shelf.shelf == shelf_number:
                        for bin in shelf.bins:
                            if bin.bin == bin_number:
                                selected_bin = bin
                                break

        if selected_bin is None:
            print("Invalid bin selection. Please choose a valid bin.")
            return

        if selected_bin.remaining_volume < selected_item.length * selected_item.width * selected_item.height or \
                selected_bin.remaining_weight < selected_item.weight:
            print("Sorry, no more space in this bin. Choose another bin or create a new one.")
            return

        # Update bin's remaining volume and weight
        selected_bin.remaining_volume -= selected_item.length * selected_item.width * selected_item.height
        selected_bin.remaining_weight -= selected_item.weight

        # Add item to the bin
        selected_bin.add_item(selected_item)

        print(f"Item {selected_item.name} added to bin {selected_bin.id}.")
        print(f"Remaining Volume in {selected_bin.id}: {selected_bin.remaining_volume} cm^3")
        print(f"Remaining Weight in {selected_bin.id}: {selected_bin.remaining_weight} kg")

    def check_bin_status(self):
        print("Bin Status:")
        for rack in self.storage_racks:
            for shelf in rack.shelves:
                for bin in shelf.bins:
                    print(f"{bin.id} - Remaining Volume: {bin.remaining_volume} cm^3, Remaining Weight: {bin.remaining_weight} kg")
                    print("Items Inside:")
                    for item_name, item_info in bin.items_inside.items():
                        print(f"  {item_name}: Quantity - {item_info['quantity']}, Weight - {item_info['weight']} kg")

    def remove_item_from_bin(self):
        print("Available Bins:")
        for rack in self.storage_racks:
            for shelf in rack.shelves:
                for bin in shelf.bins:
                    print(bin.id)

        rack_number = int(input("Enter the rack number for the bin: "))
        shelf_number = int(input("Enter the shelf number for the bin: "))
        bin_number = int(input("Enter the bin number: "))

        selected_bin = None
        for rack in self.storage_racks:
            if rack.rack == rack_number:
                for shelf in rack.shelves:
                    if shelf.shelf == shelf_number:
                        for bin in shelf.bins:
                            if bin.bin == bin_number:
                                selected_bin = bin
                                break

        if selected_bin is None:
            print("Invalid bin selection. Please choose a valid bin.")
            return

        print("Items Inside the Bin:")
        for item_name, item_info in selected_bin.items_inside.items():
            print(f"{item_name}: Quantity - {item_info['quantity']}")

        item_name_to_remove = input("Enter the name of the item you want to remove: ")
        quantity_to_remove = int(input("Enter the quantity to remove: "))

        selected_bin.remove_item(item_name_to_remove, quantity_to_remove)

def main():
    warehouse = Warehouse()

    while True:
        print("Select an option:")
        print("A - Create Storage Rack")
        print("B - Create New Item")
        print("C - Add Item to Warehouse")
        print("D - Remove Item from Bin")
        print("L - List Inventory Items")
        print("Z - Check Bin Status")
        print("Q - Quit")
        option = input("Enter your choice: ").upper()

        if option == 'A':
            # Create Storage Rack
            rack_number = int(input("Rack Number: "))
            num_shelves = int(input("Number of shelves: "))
            num_bins_per_shelf = int(input("Number of bins per shelf: "))
            bin_length = int(input("Bin Length (cm): "))
            bin_width = int(input("Bin Width (cm): "))
            bin_depth = int(input("Bin Depth (cm): "))
            bin_load_capacity = int(input("Bin Load Capacity (kg): "))
            warehouse.create_storage_rack(rack_number, num_shelves, num_bins_per_shelf, bin_length, bin_width, bin_depth, bin_load_capacity)
            print("Storage Rack created.")
        elif option == 'B':
            # Create new item, not add into warehouse
            sku = input("Enter SKU: ")
            name = input("Enter Item Name: ")
            length = int(input("Enter Item Length (cm): "))
            width = int(input("Enter Item Width (cm): "))
            height = int(input("Enter Item Height (cm): "))
            weight = int(input("Enter Item Weight (kg): "))
            new_item = InventoryItem(sku, name, length, width, height, weight)

            # Add the item to the warehouse's list of possible items for addition
            warehouse.add_possible_item(new_item)
        elif option == 'C':
            # Add item to warehouse
            warehouse.add_item_to_warehouse()
        elif option == 'D':
            # Remove item from bin
            warehouse.remove_item_from_bin()
        elif option == 'L':
            # List Inventory Items
            print("Inventory Items:")
            for item in warehouse.inventory_items:
                print(item)
        elif option == 'Z':
            # Check Bin Status
            warehouse.check_bin_status()
        elif option == 'Q':
            print("Exiting the program.")
            break

if __name__ == "__main__":
    main()
