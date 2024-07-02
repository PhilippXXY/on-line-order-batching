import time
from src.core.logic.batch_selector import order_picking_decision_point_ab, order_picking_decision_point_c
from src.core.logic.batch_tour_length_calculator import calculate_tour_length_s_shape_routing

def initial_orders_arrived(orders, max_batch_size, warehouse_layout, warehouse_layout_path, rearrangement_parameter, threshold_parameter, time_limit, release_parameter, selection_rule):
    '''
    This function is called when the initial order release is reached.

    :param orders: list of orders
    :param max_batch_size: maximum batch size
    :param warehouse_layout: dictionary containing the warehouse layout information
    :param warehouse_layout_path: path to the warehouse layout
    :param rearrangement_parameter: parameter for the rearrangement of the batches
    :param threshold_parameter: parameter for the threshold of the batches
    :param release_parameter: parameter for the release of the batches
    :param selection_rule: selection rule for the batches
    :return: list of batches with their release time
    '''
    # Get sorted batches with their release time
    batches = order_picking_decision_point_ab(orders, max_batch_size, warehouse_layout, warehouse_layout_path, rearrangement_parameter, threshold_parameter, time_limit, release_parameter, selection_rule)
    return batches

def new_order_arrives(order, max_batch_size, warehouse_layout, warehouse_layout_path, rearrangement_parameter, threshold_parameter, release_parameter, selection_rule, orders):
    '''
    This function is called when a new order arrives.

    :param order: new order
    :param max_batch_size: maximum batch size
    :param warehouse_layout: dictionary containing the warehouse layout information
    :param warehouse_layout_path: path to the warehouse layout
    :param rearrangement_parameter: parameter for the rearrangement of the batches
    :param threshold_parameter: parameter for the threshold of the batches
    :param release_parameter: parameter for the release of the batches
    :param selection_rule: selection rule for the batches
    :param orders: list of orders
    :return: list of batches with their release time
    '''
    # Add the order to the list of orders
    orders.append(order)
    # Get sorted batches with their release time
    batches = order_picking_decision_point_ab(orders, max_batch_size, warehouse_layout, warehouse_layout_path, rearrangement_parameter, threshold_parameter, release_parameter, selection_rule)
    return batches

def last_order_arrives(order, max_batch_size, warehouse_layout, rearrangement_parameter, threshold_parameter, time_limit, orders):
    '''
    This function is called when the last order arrives.

    :param order: last order
    :param max_batch_size: maximum batch size
    :param warehouse_layout: dictionary containing the warehouse layout information
    :param rearrangement_parameter: parameter for the rearrangement of the batches
    :param threshold_parameter: parameter for the threshold of the batches
    :param time_limit: time limit for the iterated local search algorithm
    :param orders: list of orders
    :return: list of batches with their release time
    '''
    # Add the order to the list of orders
    orders.append(order)
    # Get sorted batches with their release time
    batches = order_picking_decision_point_c(orders, max_batch_size, warehouse_layout, rearrangement_parameter, threshold_parameter, time_limit)
    return batches

def picker_starts_tour(batch, warehouse_layout):
    '''
    This function is called when the picker starts the tour.

    :param batch: batch to be picked
    :param warehouse_layout: dictionary containing the warehouse layout information
    :return: batch, start time, arrival time
    '''
    # Start the tour
    start_time = time.time()
    # Get the tour length
    tour_length , batches = calculate_tour_length_s_shape_routing(batch, warehouse_layout)
    # Calculate the tour time assuming 1 second per 5 warehouse units
    tour_time = tour_length / 5
    # Arrival time assuming 1 second per 5 warehouse units
    arrival_time = start_time + tour_time

    # Return start time and arrival time
    return batch, start_time, arrival_time
