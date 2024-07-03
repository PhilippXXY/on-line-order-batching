import copy
import random
import time
import uuid
from src.core.logic.batch_tour_length_calculator import calculate_tour_length_s_shape_routing
from src.core.logic.join_item_information import join_item_id_and_position_csv


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


def iterated_local_search(s_start, max_batch_size, warehouse_layout, warehouse_layout_path, rearrangement_parameter, threshold_parameter, time_limit):
    """
    This function is the main function of the adapted Iterated Local Search Algorithm by Henn. The naming of the variables is based on another paper by Henn.

    :param s_initial: A list of batches to optimize.
    :param max_batch_size: The maximum size of orders a batch can contain.
    :param warehouse_layout: A dictionary containing the warehouse layout information.
    :param rearrangement_parameter: A constant between [0;1] which determines the amount of perturbation.
    :param threshold_parameter: A constant between [0;1] which determines the threshold to choose a solution.
    :param time_limit: The maximum time in seconds the algorithm is allowed to run.
    """
    # Initialize the variables
    s = []
    ils_running = True
    improvement_found = False
    # Get the initial batches and copy them to avoid changing the original batches
    s_initial = copy.deepcopy(s_start)
    # Get the first solution by applying the local search phase
    s_asterisk = local_search_phase(s_initial, max_batch_size, warehouse_layout)
    s_incumbent = copy.deepcopy(s_asterisk)

    # Start the loop
    start_time = time.time()
    while ils_running:
        # Apply the perturbation phase
        s = copy.deepcopy(perturbation_phase(copy.deepcopy(s_incumbent), max_batch_size, rearrangement_parameter))
        # Apply the local search phase
        s = local_search_phase(copy.deepcopy(s), max_batch_size, warehouse_layout)
        # Calculate the tour length of the new solution
        d_s = 0
        for batch in copy.deepcopy(s):
            d_s += calculate_tour_length_s_shape_routing(batch, warehouse_layout)[0]
        # Calculate the tour length of the asterisk solution
        d_s_asterisk = 0
        for batch in copy.deepcopy(s_asterisk):
            d_s_asterisk += calculate_tour_length_s_shape_routing(batch, warehouse_layout)[0]
        
        # Check if the new solution is better than the asterisk solution
        if d_s < d_s_asterisk:
            # Update the asterisk solution
            s_asterisk = copy.deepcopy(s)
            # Update the incumbent solution
            s_incumbent = copy.deepcopy(s)
            # Set the flag that an improvement was found
            improvement_found = True

        # Check if any improvement during the time limit was found
        if time.time() - start_time > time_limit:
            if improvement_found:
                # If an improvement was found, continue the loop
                improvement_found = False
                # Set the start time to the current time
                start_time = time.time()
            else:
                # If improvement isn't good enough, exit the loop
                if d_s - d_s_asterisk < threshold_parameter * d_s_asterisk:
                    s_incumbent = copy.deepcopy(s)
                    ils_running = False
                # If no improvement was found, exit the loop
                ils_running = False

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

                            # Ensure the batch sizes are within the maximum limit
                            if sum(len(order['items']) for order in temp_incumbent_batch['orders']) > max_batch_size or \
                               sum(len(order['items']) for order in temp_neighbor_batch['orders']) > max_batch_size:
                                                                
                                # Skip the swap
                                continue
                            
                            # Calculate the tour length of the incumbent and neighbor batch after the swap
                            temp_incumbent_batch_tour_length, _ = calculate_tour_length_s_shape_routing(temp_incumbent_batch, warehouse_layout)
                            temp_neighbor_batch_tour_length, _ = calculate_tour_length_s_shape_routing(temp_neighbor_batch, warehouse_layout)

                            # Check if the swap is an improvement
                            if temp_incumbent_batch_tour_length + temp_neighbor_batch_tour_length < incumbent_batch_tour_length + neighbor_batch_tour_length:

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

                        # Ensure the batch sizes are within the maximum limit
                        if sum(len(order['items']) for order in temp_incumbent_batch['orders']) > max_batch_size or \
                               sum(len(order['items']) for order in temp_neighbor_batch['orders']) > max_batch_size:

                            # Skip the shift
                            continue

                        # Calculate the tour length of the incumbent and neighbor batch after the shift
                        temp_incumbent_batch_tour_length, _ = calculate_tour_length_s_shape_routing(temp_incumbent_batch, warehouse_layout)
                        temp_neighbor_batch_tour_length, _ = calculate_tour_length_s_shape_routing(temp_neighbor_batch, warehouse_layout)

                        # Check if the shift is an improvement
                        if temp_incumbent_batch_tour_length + temp_neighbor_batch_tour_length < incumbent_batch_tour_length + neighbor_batch_tour_length:
                        
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
    iterations = int(len(batches) * rearrangement_parameter + 1)

    # Copy the batches to avoid changing the original batches
    batches_copy = copy.deepcopy(batches)

    # Perform the perturbation phase
    for _ in range(iterations):
        # Select two random batches
        batch_k = random.choice(batches_copy)
        batch_l = random.choice(batches_copy)
        
        # Ensure that the two batches are different
        while batch_k == batch_l:
            batch_l = random.choice(batches_copy)

        # Get random number of orders q
        q = random.randint(1, min(len(batch_k['orders']), len(batch_l['orders'])))

        # Select the first q orders from both batches
        selected_orders_k = batch_k['orders'][:q]
        selected_orders_l = batch_l['orders'][:q]

        # Remove the selected orders from the batches
        batch_k['orders'] = batch_k['orders'][q:]
        batch_l['orders'] = batch_l['orders'][q:]

        new_batch = {
            'batch_id': generate_unique_id(),
            'orders': []
        }

        # Add the selected orders from batch k to batch l if the batch size is not exceeded
        if sum(len(order['items']) for order in batch_l['orders']) + sum(len(order['items']) for order in selected_orders_k) <= max_batch_size:
            batch_l['orders'].extend(selected_orders_k)
        else:
            new_batch['orders'].extend(selected_orders_k)

        # Add the selected orders from batch l to batch k if the batch size is not exceeded
        if sum(len(order['items']) for order in batch_k['orders']) + sum(len(order['items']) for order in selected_orders_l) <= max_batch_size:
            batch_k['orders'].extend(selected_orders_l)
        else:
            new_batch['orders'].extend(selected_orders_l)

        # Add the new batch to the list of batches if it has any orders
        if new_batch['orders']:
            batches_copy.append(new_batch)

    return copy.deepcopy(batches_copy)



def generate_unique_id():
    """
    This function generates a unique id using the uuid library.
    The advantage of using uuid is that it is guaranteed to be unique, why there is no need to check for duplicates and keep track of iterations.

    :return: A unique id as a hexstring.
    """
    return uuid.uuid4().hex