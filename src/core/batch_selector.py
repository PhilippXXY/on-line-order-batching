import math
import time
from src.core.batch_tour_length_calculator import calculate_tour_length_s_shape_routing
from src.core.batch_tour_length_minimizer import create_start_batches, generate_unique_id, iterated_local_search


def order_picking_decision_point_ab(orders, max_batch_size, warehouse_layout, rearrangement_parameter, threshold_parameter, time_limit, release_parameter):
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

        return batches, release_time


    else:
        # Apply the selection rules
        ordered_for_picking_batches = selection_rules(batches)
        # Set the release time to the current time
        release_time = time.time()

        return ordered_for_picking_batches, release_time
        


def order_picking_decision_point_c(batches, max_batch_size, warehouse_layout, rearrangement_parameter, threshold_parameter, time_limit):
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

    # Apply the iterated local search algorithm to the batches
    batches = iterated_local_search(batches, max_batch_size, warehouse_layout, rearrangement_parameter, threshold_parameter, time_limit)

    return batches


#TODO: Implement the following function
def selection_rules(batches):
    pass