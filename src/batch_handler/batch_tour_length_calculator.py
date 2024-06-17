# Initialize the direction of the tour. It can be either True (upwards) or False (downwards).
direction = True

def calculate_tour_length_s_shape_routing(batch, warehouse_layout):
    '''
    This function calculates the total tour length of the batch using the S-Shape routing algorithm.

    :param batch: A list of dictionaries, each containing 'id', 'abs_x_position', 'abs_y_position', and 'abs_z_position'.
    :param warehouse_layout: A dictionary containing the warehouse layout information.
    :return: The total tour length of the batch.
    '''

    # Sort the batch by the x-coordinate, y-coordinate, and z-coordinate
    sorted_batch = sort_and_transform_batch_s_shape_routing(batch)
    #Store the warehouse layout information as a maximum y and z position and the maximum x position transformed
    max_x_position_transformed = round(warehouse_layout['max_x_position']/2,0)
    max_y_position = warehouse_layout['max_y_position']
    max_z_position = warehouse_layout['max_z_position']

    # Initialize the total tour length
    total_tour_length = 0
    # Initialize the current position	
    starting_position = (0, -1, 0) # The starting position is one unit below the first aisle
    current_position = starting_position

    for item in sorted_batch:
        # Get the item position
        item_position = (item['abs_x_position'], item['abs_y_position'], item['abs_z_position'])

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

    return total_tour_length, sorted_batch



def sort_and_transform_batch_s_shape_routing(unsorted_batch):
    """
    This function sorts the batch primarily by the x-coordinate, secondarily by the y-coordinate, and lastly by the z-coordinate. Additionally, it transforms the x-coordinate so that aisles which are on the opposite side of each other and only need to traversed once will be regarded as one.

    :param unsorted_batch: A list of dictionaries, each containing 'id', 'abs_x_position', 'abs_y_position', and 'abs_z_position'.
    :return: The sorted batch.
    """
    transformed_batch = []
    for item in unsorted_batch:
        # Transform the x-coordinate
        transformed_item=item.copy()
        if transformed_item['abs_x_position']%2==0:
            # If the x-coordinate is even, divide it by 2
            transformed_item['abs_x_position']=(transformed_item['abs_x_position'])/2
        else:
            # If the x-coordinate is odd, subtract 1 and divide it by 2, so that it has the same value as the opposite aisle
            transformed_item['abs_x_position']=(transformed_item['abs_x_position']-1)/2
        transformed_batch.append(transformed_item)
    # Sort the batch by the x-coordinate, y-coordinate, and z-coordinate
    return sorted(transformed_batch, key=lambda x: (x['abs_x_position'], x['abs_y_position'], x['abs_z_position']))




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
    
    if(current_position[0]==item_position[0]):
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