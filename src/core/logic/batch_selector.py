import copy
import datetime
import time
import traceback

import click
from src.core.logic.batch_tour_length_calculator import calculate_tour_length_s_shape_routing
from src.core.logic.batch_tour_length_minimizer import create_start_batches, generate_unique_id, iterated_local_search
from src.vars import shared_variables
from tabulate import tabulate


def order_picking_decision_point_ab(orders, max_batch_size, warehouse_layout, warehouse_layout_path, rearrangement_parameter, threshold_parameter, time_limit, release_parameter, selection_rule):
    '''
    This function is called when the order picking decision point A or B is reached.

    :param orders: list of customer orders
    :param max_batch_size: maximum batch size
    :param warehouse_layout: dictionary containing the warehouse layout information
    :param rearrangement_parameter: parameter for the rearrangement of the batches [0;1]
    :param threshold_parameter: parameter for the threshold of the batches [0;1]
    :param time_limit: time limit for the iterated local search algorithm
    :param release_parameter: parameter for the release time of the batch [0;1]
    :param selection_rule: selection rule to be applied
    :return: list of batches, release time
    '''
    # Initialize variables
    batches = []
    release_time = 0
    try:
        # Generate a set of batches by means of batching heuristic
        batches = copy.deepcopy(create_start_batches(orders, max_batch_size))
        # Apply the iterated local search algorithm to the batches when more than one batch is available
        if len(batches) > 1:
            batches = iterated_local_search(copy.deepcopy(batches), max_batch_size, warehouse_layout, warehouse_layout_path, rearrangement_parameter, threshold_parameter, time_limit)
        # When only one batch is available, the batch won't be released immediately, in order to prevent the case that a new order arrives, which could be added to the batch.
        if len(batches) == 1:
            # Calculate the delayed release time of the batch
            batches[0] = calculate_delay_single_batch(copy.deepcopy(batches[0]), warehouse_layout, release_parameter)
            # Return the batch with the release time
            return batches


        else:
            # Apply the selection rules
            ordered_for_picking_batches = copy.deepcopy(sort_batches_by_selection_rules(copy.deepcopy(batches), warehouse_layout, selection_rule))
            # Set the release time to the current time
            release_time = time.time()

            # Add the release time to the batches
            for batch in ordered_for_picking_batches:
                batch['release_time'] = release_time
            return ordered_for_picking_batches
    
    # Catch any exception that might occur
    except Exception as e:
        click.secho(f'Error in order_picking_decision_point_ab: {e}', fg='red')
        if shared_variables.variables.get('debug_mode'):
            click.secho(traceback.print_exc(), fg='red')
        return batches

def order_picking_decision_point_c(orders, max_batch_size, warehouse_layout, warehouse_layout_path, rearrangement_parameter, threshold_parameter, selection_rule, time_limit):
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
    # Generate a set of batches by means of batching heuristic
    batches = create_start_batches(orders, max_batch_size)
    # Copy the batches to prevent the original batches from being changed
    copied_batches = copy.deepcopy(batches)
    # Apply the iterated local search algorithm to the batches when more than one batch is available 
    # As the iterated local search algorithm is only applicable to more than one batch
    if len(batches) > 1:
        # Apply the iterated local search algorithm to the batches
        batches = iterated_local_search(copied_batches, max_batch_size, warehouse_layout, warehouse_layout_path, rearrangement_parameter, threshold_parameter, time_limit)
    # Apply the selection rules
    ordered_for_picking_batches = sort_batches_by_selection_rules(batches, warehouse_layout, selection_rule)
    # Add the release time to the batches
    for batch in ordered_for_picking_batches:
        # Set the release time to the current time
        batch['release_time'] = time.time()

    return ordered_for_picking_batches


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

    try:
        # For every batch in the list of batches
        for batch in batches:
            # Create the key 'tour_length' in the batch dictionary and assign the tour length of the batch to it
            batch['tour_length'] = calculate_tour_length_s_shape_routing(batch, warehouse_layout)[0]

        # Sort the batches by the tour length ascending
        sorted_batches = sorted(batches, key=lambda x: x['tour_length'])
    except Exception as e:
        click.secho(f'Error in selection_rule_short: {e}', fg='red')
        if shared_variables.variables.get('debug_mode'):
            click.secho(traceback.print_exc(), fg='red')

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

    try:
        # For every batch in the list of batches
        for batch in batches:
            # Create the key 'tour_length' in the batch dictionary and assign the tour length of the batch to it
            batch['tour_length'] = calculate_tour_length_s_shape_routing(batch, warehouse_layout)[0]

        # Sort the batches by the tour length descending
        sorted_batches = sorted(batches, key=lambda x: x['tour_length'], reverse=True)
    except Exception as e:
        click.secho(f'Error in selection_rule_long: {e}', fg='red')
        if shared_variables.variables.get('debug_mode'):
            click.secho(traceback.print_exc(), fg='red')

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

    try:
        # For every batch in the list of batches
        for batch in batches:
            # Initialize the sum of the single service times
            single_service_time = 0

            # For every order in the batch
            for order in batch['orders']:
                # Create for every order a batch with only the order
                order_batch = {'batch_id': generate_unique_id(), 'orders': [order]}
                # Calculate the single service time of the order
                single_service_time += calculate_tour_length_s_shape_routing(order_batch, warehouse_layout)[0]

            # Calculate the savings of the batch
            batch['savings'] = single_service_time - calculate_tour_length_s_shape_routing(batch, warehouse_layout)[0]

        # Sort the batches by the savings descending
        sorted_batches = sorted(batches, key=lambda x: x['savings'], reverse=True)
    except Exception as e:
        click.secho(f'Error in selection_rule_sav: {e}', fg='red')
        if shared_variables.variables.get('debug_mode'):
            click.secho(traceback.print_exc(), fg='red')

    return sorted_batches


def calculate_delay_single_batch(batch, warehouse_layout, release_parameter_alpha):
    '''
    This function calculates the release time of a single batch.
    It calculates the release time according to the scheduled release formula as described in the paper by Henn et al. (2012) 4.1 Algorithm 1.
    Additionally it adjusts the release time according to the predefined units per second.

    :param batch: batch to determine the release time
    :param warehouse_layout: dictionary containing the warehouse layout information
    :param release_parameter: parameter for the release time of the batch [0;1]
    :return: batch with release time
    '''
    # Initialize the variables
    tour_length_units_per_second = shared_variables.variables['tour_length_units_per_second'] # Tour length units per second

    st_j_service_time_batch = 0.0 # Service time of the batch in seconds
    st_i_longest_sst_order = 0.0 # Service time of the order with the longest single service time in seconds
    ri_arrival_time_longest_order = 0.0 # Arrival time of the order with the longest single service time in milliseconds
    t_current_time = time.time() # Current time in milliseconds


    # Calculate the tour length of the batch
    tour_length_j_batch, _ = calculate_tour_length_s_shape_routing(batch, warehouse_layout)
    # Calculate the service time of the batch
    st_j_service_time_batch = tour_length_j_batch

    # Add every order of the batch to new distinct batches
    new_batches = []
    for order in batch['orders']:
        new_batches.append({
            'batch_id': generate_unique_id(),
            'orders': [order]
        })

    # Get the service time and the arrival time of the longest taking order
    for i in range(len(new_batches)):
        # Calculate the tour length of the current order
        batch_sst, _ = calculate_tour_length_s_shape_routing(new_batches[i], warehouse_layout)
        # Transform the tour length according to the predefined units per second
        batch_sst = batch_sst
        # Check if the tour length of the current order is bigger than the smallest tour length found so far
        if batch_sst > st_i_longest_sst_order:
            # Update the biggest tour length found so far 
            st_i_longest_sst_order = float(batch_sst)
            # Set the arrival time of the order with the longest single service time
            ri_arrival_time_longest_order_temp = new_batches[i]['orders'][0]['arrival_time']
            # Calculate the difference between the arrival time of the order with the longest single service time and the current time
            ri_arrival_time_longest_order = abs(ri_arrival_time_longest_order_temp - t_current_time)

    # Check if the given values fulfill the conditions given by the paper
    if (1 + release_parameter_alpha) * ri_arrival_time_longest_order + release_parameter_alpha * st_i_longest_sst_order > 2 * t_current_time + st_j_service_time_batch:
        click.secho("Error: The given values do not fulfill the conditions given by the paper.", fg='red')

    # Calculate the scheduled release formula as described in the paper by Henn et al. (2012) 4.1 Algorithm 1
    scheduled_release_by_formula = ((1 + release_parameter_alpha) * ri_arrival_time_longest_order) + (release_parameter_alpha * st_i_longest_sst_order) - st_j_service_time_batch

    # Set the temporary delay to the maximum of the current time and the scheduled release time
    temp_delay = scheduled_release_by_formula

    # Adjust the delay according to the predefined units per second
    temp_delay = temp_delay / tour_length_units_per_second

    # Calculate the release time
    release_time = max(t_current_time, temp_delay + t_current_time)

    # Add the release time to the batch
    batch['release_time'] = release_time

    if shared_variables.variables.get('debug_mode'):
        click.secho(f"Current time: {t_current_time}", fg='yellow')
        click.secho(f"Release time: {release_time}", fg='yellow')
        click.secho(f"Release time by formula: {scheduled_release_by_formula}", fg='yellow')
        click.secho(f'Delay: {release_time - t_current_time}', fg='yellow')

    return batch