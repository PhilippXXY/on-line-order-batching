import time
from src.core.logic.batch_tour_length_calculator import calculate_tour_length_s_shape_routing
from src.core.logic.batch_tour_length_minimizer import create_start_batches, generate_unique_id, iterated_local_search


def order_picking_decision_point_ab(orders, max_batch_size, warehouse_layout, rearrangement_parameter, threshold_parameter, time_limit, release_parameter, selection_rule):
    '''
    This function is called when the order picking decision point A or B is reached.

    :param orders: list of customer orders
    :param max_batch_size: maximum batch size
    :param warehouse_layout: dictionary containing the warehouse layout information
    :param rearrangement_parameter: parameter for the rearrangement of the batches [0;1]
    :param threshold_parameter: parameter for the threshold of the batches [0;1]
    :param time_limit: time limit for the iterated local search algorithm
    :param release_parameter: parameter for the release time of the batch [0;1]
    :return: list of batches, release time
    '''
    # Initialize variables
    batches = []
    release_time = 0

    # Generate a set of batches by means of batching heuristic
    batches = create_start_batches(orders, max_batch_size)
    batches = iterated_local_search(batches, max_batch_size, warehouse_layout, rearrangement_parameter, threshold_parameter, time_limit)

    # When only one batch is available, the batch won't be released immediately, in order to prevent the case that a new order arrives, which could be added to the batch.
    if len(batches) == 1:
        st_batch = calculate_tour_length_s_shape_routing(batches[0]['orders'], warehouse_layout)
        # Initialize a new batch
        new_batches = []

        # Add every order of the batch to new distinct batches
        for order in batches[0]['orders']:
            # Add the order to a new batch
            new_batches.append({
                'batch_id': generate_unique_id(),
                'orders': order
            })

        # For every order in the new batches
        for batch in new_batches:
            # Initialize the tour length of the current order.
            longest_sst = 0
            # Check if the tour length of the current order is bigger than the smallest tour length found so far
            if calculate_tour_length_s_shape_routing(batch['orders'], warehouse_layout) > longest_sst:
                # Update the biggest tour length found so far
                longest_sst = calculate_tour_length_s_shape_routing(batch['orders'], warehouse_layout)
                # Update the batch with the longest single service time
                longest_sst_batch = batch

        # Get the arrival time of the order with the longest single service time
        arrival_time_longest_sst_order = longest_sst_batch['arrival_time']

        # Calculate the scheduled release formula as described in the paper by Henn et al. (2012)
        scheduled_release_formula = ((1 + release_parameter)* arrival_time_longest_sst_order) + (release_parameter*longest_sst) - st_batch
        release_time = max(time.time(), scheduled_release_formula)

        # Add the release time to the batch
        for batch in batches:
            batch['release_time'] = release_time

        return batches

    else:
        # Apply the selection rules
        ordered_for_picking_batches = sort_batches_by_selection_rules(batches, selection_rule)
        # Set the release time to the current time
        release_time = time.time()

        # Add the release time to the batches
        for batch in ordered_for_picking_batches:
            batch['release_time'] = release_time

        return ordered_for_picking_batches
        

def order_picking_decision_point_c(orders, max_batch_size, warehouse_layout, rearrangement_parameter, threshold_parameter, time_limit):
    '''
    This function is called when the order picking decision point C is reached.
    It returns the batches after applying the iterated local search algorithm.

    :param batches: list of batches
    :param max_batch_size: maximum batch size
    :param warehouse_layout: dictionary containing the warehouse layout information
    :param rearrangement_parameter: parameter for the rearrangement of the batches
    :param threshold_parameter: parameter for the threshold of the batches
    :param time_limit: time limit for the iterated local search algorithm
    :return: list of batches
    '''

    batches = create_start_batches(orders, max_batch_size)
    # Apply the iterated local search algorithm to the batches
    batches = iterated_local_search(batches, max_batch_size, warehouse_layout, rearrangement_parameter, threshold_parameter, time_limit)
    # Add the release time to the batches
    for batch in batches:
        # Set the release time to the current time
        batch['release_time'] = time.time()

    return batches


def sort_batches_by_selection_rules(batches, warehouse_layout, selection_rule):
    '''
    This function sorts the batches according to the selection rule.

    :param batches: list of batches
    :param warehouse_layout: dictionary containing the warehouse layout information
    :param selection_rule: selection rule to be applied
    :return: list of sorted batches
    '''

    if selection_rule == 'SHORT' or selection_rule == 'short':
        batches = selection_rule_short(batches, warehouse_layout)
    elif selection_rule == 'LONG' or selection_rule == 'long':
        batches = selection_rule_long(batches, warehouse_layout)
    elif selection_rule == 'SAV' or selection_rule == 'sav':
        batches = selection_rule_sav(batches, warehouse_layout)
    else:
        batches = selection_rule_first(batches)

    return batches


def selection_rule_first(batches):
    '''
    This function sorts the batches according to the first come first serve rule.

    :param batches: list of batches
    :return: list of sorted batches
    '''

    return batches


def selection_rule_short(batches, warehouse_layout):
    '''
    This function sorts the batches according to the shortest tour length.

    :param batches: list of batches
    :param warehouse_layout: dictionary containing the warehouse layout information
    :return: list of sorted batches
    '''
    # Initialize the sorted batches
    sorted_batches = []

    # For every batch in the list of batches
    for batch in batches:
        # Create the key 'tour_length' in the batch dictionary and assign the tour length of the batch to it
        batch['tour_length'] = calculate_tour_length_s_shape_routing(batch['orders'], warehouse_layout)

    # Sort the batches by the tour length ascending
    sorted_batches = sorted(batches, key=lambda x: x['tour_length'])

    return sorted_batches


def selection_rule_long(batches, warehouse_layout):
    '''
    This function sorts the batches according to the longest tour length.

    :param batches: list of batches
    :param warehouse_layout: dictionary containing the warehouse layout information
    :return: list of sorted batches
    '''
    # Initialize the sorted batches
    sorted_batches = []

    # For every batch in the list of batches
    for batch in batches:
        # Create the key 'tour_length' in the batch dictionary and assign the tour length of the batch to it
        batch['tour_length'] = calculate_tour_length_s_shape_routing(batch['orders'], warehouse_layout)

    # Sort the batches by the tour length descending
    sorted_batches = sorted(batches, key=lambda x: x['tour_length'], reverse=True)

    return sorted_batches


def selection_rule_sav(batches, warehouse_layout):
    '''
    This function sort the batches by comparing the savings of the batches in comparison to the single service time.

    :param batches: list of batches
    :param warehouse_layout: dictionary containing the warehouse layout information
    :return: list of sorted batches
    '''
    # Initialize the sorted batches
    sorted_batches = []

    # For every batch in the list of batches
    for batch in batches:
        # Initialize the sum of the single service times
        single_service_time = 0

        # For every order in the batch
        for order in batch['orders']:
            # Create for every order a batch with only the order
            order_batch = [{'orders': [order]}]
            # Calculate the single service time of the order
            single_service_time += calculate_tour_length_s_shape_routing(order_batch, warehouse_layout)

        # Calculate the savings of the batch
        batch['savings'] = single_service_time - calculate_tour_length_s_shape_routing(batch['orders'], warehouse_layout)

    # Sort the batches by the savings descending
    sorted_batches = sorted(batches, key=lambda x: x['savings'], reverse=True)

    return sorted_batches

