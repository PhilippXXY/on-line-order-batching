import time
from src.core.logic.batch_selector import order_picking_decision_point_ab, order_picking_decision_point_c
from src.core.logic.batch_tour_length_calculator import calculate_tour_length_s_shape_routing

orders = []



def new_order_arrives(order, max_batch_size, warehouse_layout, rearrangement_parameter, threshhold_parameter, release_parameter, selection_rule, orders):
    # Add the order to the list of orders
    orders.append(order)

    # Get sorted batches with their release time
    batches = order_picking_decision_point_ab(orders, max_batch_size, warehouse_layout, rearrangement_parameter, threshhold_parameter, release_parameter, selection_rule)

    return batches


def last_order_arrives (order, max_batch_size, warehouse_layout, rearrangement_parameter, threshhold_parameter, time_limit, orders):
    # Add the order to the list of orders
    orders.append(order)

    # Get sorted batches with their release time
    batches = order_picking_decision_point_c(orders, max_batch_size, warehouse_layout, rearrangement_parameter, threshhold_parameter, time_limit)

    return batches


def picker_starts_tour(batch, warehouse_layout):
    # Start the tour
    start_time = time.time()
    # Arrival time assuming 1 second per 5 warehouse units
    arrival_time = start_time + calculate_tour_length_s_shape_routing(batch['orders'], warehouse_layout) / 5

    # Return start time and arrival time
    return batch, start_time, arrival_time
