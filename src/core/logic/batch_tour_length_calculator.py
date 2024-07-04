import math

import click


# Initialize the direction of the tour. It can be either True (upwards) or False (downwards).
direction = True

def calculate_tour_length_s_shape_routing(batch, warehouse_layout):
    '''
    This function calculates the total tour length of the batch using the S-Shape routing algorithm.

    :param batch: A list of dictionaries, each containing 'id', 'abs_x_position', 'abs_y_position', and 'abs_z_position'.
    :param warehouse_layout: A dictionary containing the warehouse layout information.
    :return: The total tour length of the batch, and the sorted batch.

    '''
    global direction
    direction = True
    try:
        # Sort the batch by the x-coordinate, y-coordinate, and z-coordinate
        sorted_batch = sort_and_transform_batch_s_shape_routing(batch)
        #Store the warehouse layout information as a maximum y position and the maximum x position transformed. z position is not needed for the S-Shape routing
        max_x_position_transformed = round(warehouse_layout['max_x_position']/2,0)
        max_y_position = warehouse_layout['max_y_position']
        max_z_position = warehouse_layout['max_z_position']

        # Initialize the total tour length
        total_tour_length = 0
        # Initialize the current position	
        starting_position = (0, -1) # The starting position is one unit below the first aisle
        current_position = starting_position

        for i, item in enumerate(sorted_batch):
            # Get the item position
            item_position = (item['abs_x_position'], item['abs_y_position'])

            #calculate the distance to the next item
            if i > 0 and (sorted_batch[i]['abs_x_position'], sorted_batch[i]['abs_y_position']) == (sorted_batch[i-1]['abs_x_position'], sorted_batch[i-1]['abs_y_position']):
                # If the current item is the same as the previous item, skip it
                distance=0
            else:
                # Calculate the distance between the current position and the item position
                distance = calculate_distance_to_next_item(current_position, starting_position, item_position, max_y_position)
            # Update the current position
            current_position = item_position
            # Update the total tour length
            total_tour_length += distance

        #Calculate way back to the starting position
        distance = calculate_distance_to_starting_position(current_position, starting_position)
        # Update the total tour length
        total_tour_length += distance

    except Exception as e:
        click.secho(f'calculate_tour_length_s_shape_routing encountered an error: {e}', fg='red')
        return None, None
    
    return total_tour_length, sorted_batch



def sort_and_transform_batch_s_shape_routing(unsorted_batch):
    """
    This function sorts the batch primarily by the x-coordinate, secondarily by the y-coordinate, and lastly by the z-coordinate. Additionally, it transforms the x-coordinate so that aisles which are on the opposite side of each other and only need to traversed once will be regarded as one.

    :param unsorted_batch: A list of dictionaries, each containing 'id', 'abs_x_position', 'abs_y_position', and 'abs_z_position'.
    :return: The sorted batch.
    """
    # Initialize the transformed batch
    transformed_batch = []
    # Iterate over all orders and items
    for order in unsorted_batch['orders']:
        for item in order['items']:
            # Check if the item is a dictionary
            if not isinstance(item, dict):
                raise TypeError(f"Expected item to be a dict, got {type(item)}")
            # Transform the x-coordinate
            transformed_item = item.copy()
            # Check if the item has an 'abs_x_position' key
            if 'abs_x_position' not in transformed_item:
                raise KeyError(f"Item {item} does not have 'abs_x_position'")
            # Divide the x-coordinate by 2 and round up to the nearest integer to transform the x-coordinate into corresponding aisles
            transformed_item['abs_x_position'] = math.ceil(transformed_item['abs_x_position'] / 2)
            # Append the transformed item to the transformed batch
            transformed_batch.append(transformed_item)

    # Sort the batch by the x-coordinate
    sorted_batch = sorted(transformed_batch, key=lambda x: (x['abs_x_position'], x['abs_y_position'], x['abs_z_position']))

    # Group items by x_position (aisle)
    grouped_batch = {}
    for item in sorted_batch:
        aisle = item['abs_x_position']
        if aisle not in grouped_batch:
            grouped_batch[aisle] = []
        grouped_batch[aisle].append(item)

    # Get sorted aisles in order of appearance
    sorted_aisles = sorted(grouped_batch.keys())

    # Sort items within each aisle
    final_sorted_batch = []
    for index, aisle in enumerate(sorted_aisles):
        items = grouped_batch[aisle]
        if index % 2 == 0:
            # Ascending order for first, third, fifth, etc.
            final_sorted_batch.extend(sorted(items, key=lambda x: x['abs_y_position']))
        else:
            # Descending order for second, fourth, sixth, etc.
            final_sorted_batch.extend(sorted(items, key=lambda x: x['abs_y_position'], reverse=True))

    return final_sorted_batch



def calculate_distance_to_next_item(current_position, starting_position, item_position, max_y_position):
    """
    This function calculates the distance between the current position and the item position in the warehouse.

    :param current_position: A tuple containing the current x-coordinate, y-coordinate, and z-coordinate.
    :param item_position: A tuple containing the item's x-coordinate (transformed), y-coordinate, and z-coordinate.
    :param max_y_position: The maximum y-coordinate in the warehouse.
    :return: The distance between the current position and the item position.
    """
    
    # Declare the global variables
    global direction
    
    if(current_position==starting_position):
        #If the current position is the starting position
        distance=abs(current_position[0]-item_position[0])+abs(current_position[1]-item_position[1])
    else:
        if((current_position[0], current_position[1]) == (item_position[0], item_position[1])):
            #If the item is on the same position as the current position
            distance=0
        elif(current_position[0]==item_position[0]):
                #If the item is on the same aisle as the current position
                distance=abs(current_position[1]-item_position[1]) #Calculate the y-distance to the item
        else:
                #If the item is on a different aisle than the current position
                if(direction):
                    #If the direction is upwards
                    #Calculate the y-distance to the end of the aisle. As the y-coordinate starts at 0, we have to do one more step to get to the end of the aisle
                    distance=abs(current_position[1]-(max_y_position))
                    #Calculate the x-distance to the item
                    distance+=abs(current_position[0]-item_position[0])
                    #Calculate the y-distance to the item from the end of the aisle.
                    distance+=abs((max_y_position)-item_position[1])
                    #Change the direction
                    direction=False
                else:
                    #If the direction is downwards
                    #Calculate the y-distance to the end of the aisle. As the y-coordinate starts at 0, we have to do one more step to get to the end of the aisle
                    distance=abs(current_position[1]-starting_position[1])
                    #Calculate the x-distance to the item
                    distance+=abs(current_position[0]-item_position[0])
                    #Calculate the y-distance to the item from the end of the aisle.
                    distance+=abs(starting_position[1]-item_position[1])
                    #Change the direction
                    direction=True

    return distance



def calculate_distance_to_starting_position(current_position, starting_position):
    """
    This function calculates the distance between the current position and the starting position in the warehouse.

    :param current_position: A tuple containing the current x-coordinate, y-coordinate, and z-coordinate.
    :param starting_position: A tuple containing the starting x-coordinate, y-coordinate, and z-coordinate.
    :param max_x_position: The maximum x-coordinate in the warehouse.
    :param max_y_position: The maximum y-coordinate in the warehouse.
    :param max_z_position: The maximum z-coordinate in the warehouse.
    :return: The distance between the current position and the starting position.
    """
    #Calculate the distance to the starting position
    distance = abs(current_position[0]-starting_position[0])+abs(current_position[1]-starting_position[1])

    return distance