import copy
import uuid

from src.batch_handler.batch_tour_length_calculator import calculate_tour_length_s_shape_routing

def create_start_batches(orders, max_batch_size):
    """
    This function creates the initial batches out of the orders by assigning them after the First-Come-First-Serve principle.

    :param orders: A list of non devisable orders.
    :param max_batch_size: The maximum size of a batch.
    :return: A list of batches to start with.
    """
    # Initialize the variables
    batches = []
    current_batch = []
    current_batch_size = 0

    # Assign the orders to the batches
    for order in orders:
        # Check if the order fits into the current batch
        if len(order['items']) + current_batch_size <= max_batch_size:
            # Add the order to the current batch
            current_batch.append(order)
            # Update the current batch size
            current_batch_size += len(order['items'])
        # If the order does not fit into the current batch
        else:
            # Add the current batch to the list of batches
            batches.append({
                'batch_id': generate_unique_id(),
                'orders': current_batch
            })
            # Start a new batch
            current_batch = [order]
            current_batch_size = len(order['items'])

    # Add the last batch to the list of batches    
    if current_batch:
        batches.append({
            'batch_id': generate_unique_id(),
            'orders': current_batch
        })

    return batches


def generate_unique_id():
    """
    This function generates a unique id using the uuid library.
    The advantage of using uuid is that it is guaranteed to be unique, why there is no need to check for duplicates and keep track of iterations.

    :return: A unique id as a hexstring.
    """
    return uuid.uuid4().hex


#TODO: Implement the local search phase
def local_search_phase(start_batches, max_batch_size, warehouse_layout):
    """
    This function is the local search phase of the adapted Iterated Local Search Algorithm by Henn.
    """
    pass
    

def local_search_swap(batches, max_batch_size, warehouse_layout):
    """
    This function is the swap operator of the local search phase of the adapted Iterated Local Search Algorithm by Henn.

    :param batches: A list of batches to optimize.
    :param max_batch_size: The maximum size of orders a batch can contain.
    :param warehouse_layout: A dictionary containing the warehouse layout information.
    :return: A list of optimized batches.
    """
    # Initialize the variables
    is_optimal = False

    # Continue until no improvement is found
    while not is_optimal:
        # Initialize the flag
        improvement_found = False
        # Iterate over all pairs of batches
        for i, incumbent_batch in enumerate(batches):
            for j, neighbor_batch in enumerate(batches):
                # Skip the same batch
                if i != j:
                    # Calculate the tour length of the incumbent and neighbor batch before the swap
                    incumbent_batch_tour_length, _ = calculate_tour_length_s_shape_routing(incumbent_batch, warehouse_layout)
                    neighbor_batch_tour_length, _ = calculate_tour_length_s_shape_routing(neighbor_batch, warehouse_layout)

                    # Iterate over all pairs of orders
                    for incumbent_order in list(incumbent_batch['orders']):
                        for neighbor_order in list(neighbor_batch['orders']):
                            # Create a copy of the batches to test the swap
                            temp_incumbent_batch = copy.deepcopy(incumbent_batch)
                            temp_neighbor_batch = copy.deepcopy(neighbor_batch)

                            # Swap complete orders
                            temp_incumbent_batch['orders'].remove(incumbent_order)
                            temp_neighbor_batch['orders'].remove(neighbor_order)
                            temp_incumbent_batch['orders'].append(neighbor_order)
                            temp_neighbor_batch['orders'].append(incumbent_order)

                            # Debugging information
                            # print(f"Trying swap: Incumbent Order {incumbent_order['order_id']} with Neighbor Order {neighbor_order['order_id']}")
                            # print(f"Temp Incumbent Batch Size: {sum(len(order['items']) for order in temp_incumbent_batch['orders'])}, Temp Neighbor Batch Size: {sum(len(order['items']) for order in temp_neighbor_batch['orders'])}")

                            # Ensure the batch sizes are within the maximum limit
                            if sum(len(order['items']) for order in temp_incumbent_batch['orders']) > max_batch_size or \
                               sum(len(order['items']) for order in temp_neighbor_batch['orders']) > max_batch_size:
                                
                                # Debugging information
                                # print("Swap rejected due to batch size limit.")
                                
                                # Skip the swap
                                continue
                            
                            # Calculate the tour length of the incumbent and neighbor batch after the swap
                            temp_incumbent_batch_tour_length, _ = calculate_tour_length_s_shape_routing(temp_incumbent_batch, warehouse_layout)
                            temp_neighbor_batch_tour_length, _ = calculate_tour_length_s_shape_routing(temp_neighbor_batch, warehouse_layout)

                            # Check if the swap is an improvement
                            if temp_incumbent_batch_tour_length + temp_neighbor_batch_tour_length < incumbent_batch_tour_length + neighbor_batch_tour_length:
                                
                                # Debugging information
                                #print(f"Improvement found by swapping orders between batches {i} and {j}")
                                #print(f"Original Incumbent Batch Tour Length: {incumbent_batch_tour_length}, Neighbor Batch Tour Length: {neighbor_batch_tour_length}")
                                #print(f"New Incumbent Batch Tour Length: {temp_incumbent_batch_tour_length}, New Neighbor Batch Tour Length: {temp_neighbor_batch_tour_length}")

                                # Update the batches
                                batches[i] = temp_incumbent_batch
                                batches[j] = temp_neighbor_batch
                                # Update the flag
                                improvement_found = True
                                # Break the loop
                                break
                        if improvement_found:
                            break
                if improvement_found:
                    break
            if improvement_found:
                break
                
        if not improvement_found:
            # Exit the loop as no improvement was found
            is_optimal = True

    return batches

    

def local_search_shift(batches, max_batch_size, warehouse_layout):
    """
    This function is the shift operator of the local search phase of the adapted Iterated Local Search Algorithm by Henn.
    """
    # Initialize the variables
    is_optimal = False
    # Continue until no improvement is found
    while not is_optimal:
        # Initialize the flag
        improvement_found = False
        # Iterate over all pairs of batches
        for i, incumbent_batch in enumerate(batches):
            for j, neighbor_batch in enumerate(batches):
                # Skip the same batch
                if i != j:
                    # Calculate the tour length of the incumbent and neighbor batch before the swap
                    incumbent_batch_tour_length, _ = calculate_tour_length_s_shape_routing(incumbent_batch, warehouse_layout)
                    neighbor_batch_tour_length, _ = calculate_tour_length_s_shape_routing(neighbor_batch, warehouse_layout)

                    # Iterate over all pairs of orders
                    for incumbent_order in list(incumbent_batch['orders']):
                        # Create a copy of the batches to test the swap
                        temp_incumbent_batch = copy.deepcopy(incumbent_batch)
                        temp_neighbor_batch = copy.deepcopy(neighbor_batch)

                        # Shift the order to the neighbor batch
                        temp_incumbent_batch['orders'].remove(incumbent_order)
                        temp_neighbor_batch['orders'].append(incumbent_order)

                        # Debugging information
                        # print(f"Trying shift: Incumbent Order {incumbent_order['order_id']} to Neighbor Batch")
                        # print(f"Temp Incumbent Batch Size: {sum(len(order['items']) for order in temp_incumbent_batch['orders'])}, Temp Neighbor Batch Size: {sum(len(order['items']) for order in temp_neighbor_batch['orders'])}")

                        # Ensure the batch sizes are within the maximum limit
                        if sum(len(order['items']) for order in temp_incumbent_batch['orders']) > max_batch_size or \
                               sum(len(order['items']) for order in temp_neighbor_batch['orders']) > max_batch_size:
                            
                            # Debugging information
                            # print("Shift rejected due to batch size limit.")

                            # Skip the shift
                            continue

                        # Calculate the tour length of the incumbent and neighbor batch after the shift
                        temp_incumbent_batch_tour_length, _ = calculate_tour_length_s_shape_routing(temp_incumbent_batch, warehouse_layout)
                        temp_neighbor_batch_tour_length, _ = calculate_tour_length_s_shape_routing(temp_neighbor_batch, warehouse_layout)

                        # Check if the shift is an improvement
                        if temp_incumbent_batch_tour_length + temp_neighbor_batch_tour_length < incumbent_batch_tour_length + neighbor_batch_tour_length:
                            
                            # Debugging information
                            #print(f"Improvement found by shifting order {incumbent_order['order_id']} to batch {j}")
                            #print(f"Original Incumbent Batch Tour Length: {incumbent_batch_tour_length}, Neighbor Batch Tour Length: {neighbor_batch_tour_length}")
                            #print(f"New Incumbent Batch Tour Length: {temp_incumbent_batch_tour_length}, New Neighbor Batch Tour Length: {temp_neighbor_batch_tour_length}")

                            # Update the batches
                            batches[i] = temp_incumbent_batch
                            batches[j] = temp_neighbor_batch
                            # Update the flag
                            improvement_found = True
                            # Break the loop
                            break
                    if improvement_found:
                        break
            if improvement_found:
                break
        
        if not improvement_found:
            # Exit the loop as no improvement was found
            is_optimal = True

    return batches


#TODO: Implement the perturbation phase
def perturbation_phase():
    """
    This function is the perturbation phase of the adapted Iterated Local Search Algorithm by Henn.
    """
    pass