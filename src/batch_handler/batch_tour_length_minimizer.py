import uuid

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
    batch_id = 0

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