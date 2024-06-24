import copy
import random
import time
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


def iterated_local_search(s_initial, max_batch_size, warehouse_layout, rearrangement_parameter, threshold_parameter, time_limit):
    """
    This function is the main function of the adapted Iterated Local Search Algorithm by Henn. The naming of the variables is based on another paper by Henn.

    :param s_initial: A list of batches to optimize.
    :param max_batch_size: The maximum size of orders a batch can contain.
    :param warehouse_layout: A dictionary containing the warehouse layout information.
    :param rearrangement_parameter: A constant between [0;1] which determines the amount of perturbation.
    :param threshold_parameter: A constant between [0;1] which determines the threshold to choose a solution.
    :param time_limit: The maximum time in seconds the algorithm is allowed to run.
    """
    # Initial solution provided by the FCFS rule
    s = s_initial
    # Get the first solution by applying the local search algorithm
    s_asterisk = local_search_phase(s_initial, max_batch_size, warehouse_layout)
    # Set the incumbent solution to the first solution
    s_incumbent = s_asterisk

    # Set the flag
    is_optimal = False

    # Perform the iterations while the flag is not set
    while not is_optimal:
        # Set the start time to the current time
        start_time = time.time()
        # Calculate the tour length of the incumbent solution
        d_s_incumbent = sum(calculate_tour_length_s_shape_routing(batch, warehouse_layout)[0] for batch in s_incumbent)
        
        # Perform the iterations inside the time limit
        while time.time()-start_time < time_limit:
            # Change the batches by applying the perturbation phase
            s = perturbation_phase(s_incumbent, max_batch_size, rearrangement_parameter)
            # Improve the batches using the local search algorithm
            s = local_search_phase(s, max_batch_size, warehouse_layout)

            # Calculate the total tour length of the batches s
            d_s = sum(calculate_tour_length_s_shape_routing(batch, warehouse_layout)[0] for batch in s)
            # Calculate the total tour length of the batches s_asterisk
            d_s_asterisk = sum(calculate_tour_length_s_shape_routing(batch, warehouse_layout)[0] for batch in s_asterisk)

            # Check if the total tour length of the batches s is less than the total tour length of the batches s_asterisk
            if  d_s < d_s_asterisk:
                # Set the improved batches as the new batches s_asterisk
                s_asterisk = s
                # Set the improved batches as the new incumbent batches
                s_incumbent = s

        # Check if the total tour length of the incumbent batches is less than the total tour length of the batches s_asterisk
        if d_s_incumbent < d_s_asterisk and (d_s - d_s_asterisk) < (threshold_parameter*d_s_asterisk):
            # Set the incumbent batches as the new batches s_asterisk
            s_incumbent = s_asterisk
            # Set the flag
            is_optimal = True

    return s_asterisk
  

def local_search_phase(initial_batches, max_batch_size, warehouse_layout):
    """
    This function is the local search phase of the adapted Iterated Local Search Algorithm by Henn.

    :param batches: A list of batches to optimize.
    :param max_batch_size: The maximum size of orders a batch can contain.
    :param warehouse_layout: A dictionary containing the warehouse layout information.
    :return: A list of optimized batches.
    """
    # Calculate the tour length of the initial batches
    initial_batches_tour_length = sum(calculate_tour_length_s_shape_routing(batch, warehouse_layout)[0] for batch in initial_batches)
    # Initialize the variables
    improved_batches_tour_length = 0

    # Improve the batches using the local search algorithm
    while improved_batches_tour_length < initial_batches_tour_length:
        # Improve the batches using the local search swap algorithm
        improved_batches = local_search_swap(initial_batches,max_batch_size, warehouse_layout)
        # Calculate the total tour length of the improved batches after a swap
        improved_batches_tour_length = sum(calculate_tour_length_s_shape_routing(batch, warehouse_layout)[0] for batch in improved_batches)
        # Set the improved batches as the new start batches 
        initial_batches = improved_batches
        initial_batches_tour_length = improved_batches_tour_length
        # Improve the batches using the local search shift algorithm
        improved_batches = local_search_shift(initial_batches, max_batch_size, warehouse_layout)
        # Calculate the total tour length of the improved batches after a shift
        improved_batches_tour_length = sum(calculate_tour_length_s_shape_routing(batch, warehouse_layout)[0] for batch in improved_batches)
        # Set the improved batches as the new start batches
        initial_batches = improved_batches
        initial_batches_tour_length = improved_batches_tour_length

    return improved_batches


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

            # Delete empty batches
            batches = [batch for batch in batches if batch['orders']]

    return batches



def perturbation_phase(batches, max_batch_size, rearrangement_parameter):
    """
    This function is the perturbation phase of the adapted Iterated Local Search Algorithm by Henn.

    :param batches: A list of batches to optimize.
    :param max_batch_size: The maximum size of orders a batch can contain.
    :param rearrangement_parameter: A constant between [0;1] which determines the amount of perturbation.
    """
    # Calculate the amount of iterations for the perturbation phase
    iterations = int(len(batches)*rearrangement_parameter+1)

    # Perform the perturbation phase for the amount of iterations
    for _ in range(iterations):
        # Get the amount of batches
        batches_amount = len(batches)
        # Select two batches randomly
        batch_k_index = random.randint(0, batches_amount - 1)
        batch_l_index = random.randint(0, batches_amount - 1)
        batch_k = batches[batch_k_index]
        batch_l = batches[batch_l_index]
        # Get the amount of orders in the batches
        orders_amount_k = len(batch_k['orders'])
        orders_amount_l = len(batch_l['orders'])
        # Get the minimum amount of orders in the selected batches
        min_orders_amount = min(orders_amount_k, orders_amount_l)

        # Only proceed if there are orders to swap
        if min_orders_amount > 0:
            # Calculate the amount of orders to swap
            orders_amount_to_swap_q = random.randint(1, int(min_orders_amount))

            # Store the first q orders
            temp_batch_k_first_q = batch_k['orders'][:orders_amount_to_swap_q]
            temp_batch_l_first_q = batch_l['orders'][:orders_amount_to_swap_q]

            # Remove the first q orders
            batch_k['orders'] = batch_k['orders'][orders_amount_to_swap_q:]
            batch_l['orders'] = batch_l['orders'][orders_amount_to_swap_q:]

            # Initliaze a batch for the orders that could not be swapped
            new_batch = {
                'batch_id': generate_unique_id(),
                'orders': []
            }

            for order in temp_batch_k_first_q:
                # Check if the sum of the shortened batch and the currently iterated order exceeds the maximum batch size
                if sum(len(order['items']) for order in batch_l['orders']) + len(order['items']) > max_batch_size:
                    # Add the orders to a new batch
                    new_batch['orders'].append(order)
                else:
                    # Add the orders to batch l
                    batch_l['orders'].append(order)
                
            for order in temp_batch_l_first_q:
                # Check if the sum of the shortened batch and the currently iterated order exceeds the maximum batch size
                if sum(len(order['items']) for order in batch_k['orders']) + len(order['items']) > max_batch_size:
                    # Add the orders to a new batch
                    new_batch['orders'].append(order)
                else:
                    # Add the orders to batch k
                    batch_k['orders'].append(order)

            # Check if the batch with the orders that could not be swapped is empty
            if new_batch['orders']:
                # Get the length of the new batch
                new_batch_size = sum(len(order['items']) for order in new_batch['orders'])
                if new_batch_size > max_batch_size:
                    # Split the orders into two groups
                    orders_group_1 = new_batch['orders'][:int(new_batch_size / 2)]
                    orders_group_2 = new_batch['orders'][int(new_batch_size / 2):]
                    # Assign the orders to two new batches
                    new_batch_1 = {
                        'batch_id': generate_unique_id(),
                        'orders': orders_group_1
                    }
                    new_batch_2 = {
                        'batch_id': generate_unique_id(),
                        'orders': orders_group_2
                    }
                    # Append the new batches to the list of batches
                    batches.append(new_batch_1)
                    batches.append(new_batch_2)
                else:
                    # Append the new batch to the list of batches
                    batches.append(new_batch)

    return batches