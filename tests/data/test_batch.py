# Warehouse layout example
warehouse_layout = {
    'max_x_position': 20,
    'max_y_position': 10,
    'max_z_position': 5,
}

# Sets of test data
test_batches=[
    #0
    [
        {'item_id': 281, 'abs_x_position': 5, 'abs_y_position': 6, 'abs_z_position': 0},
        {'item_id': 579, 'abs_x_position': 11, 'abs_y_position': 5, 'abs_z_position': 3},
        {'item_id': 570, 'abs_x_position': 11, 'abs_y_position': 3, 'abs_z_position': 4},
        {'item_id': 17, 'abs_x_position': 0, 'abs_y_position': 3, 'abs_z_position': 1},
        {'item_id': 505, 'abs_x_position': 10, 'abs_y_position': 0, 'abs_z_position': 4},
        {'item_id': 842, 'abs_x_position': 16, 'abs_y_position': 8, 'abs_z_position': 1},
        {'item_id': 907, 'abs_x_position': 18, 'abs_y_position': 1, 'abs_z_position': 1},
        {'item_id': 696, 'abs_x_position': 13, 'abs_y_position': 9, 'abs_z_position': 0},
        {'item_id': 28, 'abs_x_position': 0, 'abs_y_position': 5, 'abs_z_position': 2},
        {'item_id': 201, 'abs_x_position': 4, 'abs_y_position': 0, 'abs_z_position': 0}
    ],

    #1
    [
        {'item_id': 376, 'abs_x_position': 7, 'abs_y_position': 5, 'abs_z_position': 0},
        {'item_id': 165, 'abs_x_position': 3, 'abs_y_position': 2, 'abs_z_position': 4},
        {'item_id': 182, 'abs_x_position': 3, 'abs_y_position': 6, 'abs_z_position': 1},
        {'item_id': 518, 'abs_x_position': 10, 'abs_y_position': 3, 'abs_z_position': 2},
        {'item_id': 228, 'abs_x_position': 4, 'abs_y_position': 5, 'abs_z_position': 2},
        {'item_id': 702, 'abs_x_position': 14, 'abs_y_position': 0, 'abs_z_position': 1},
        {'item_id': 862, 'abs_x_position': 17, 'abs_y_position': 2, 'abs_z_position': 1}
    ],

    #2 (equal as 1 but in different order)
    [
        {'item_id': 228, 'abs_x_position': 4, 'abs_y_position': 5, 'abs_z_position': 2},
        {'item_id': 182, 'abs_x_position': 3, 'abs_y_position': 6, 'abs_z_position': 1},
        {'item_id': 518, 'abs_x_position': 10, 'abs_y_position': 3, 'abs_z_position': 2},
        {'item_id': 702, 'abs_x_position': 14, 'abs_y_position': 0, 'abs_z_position': 1},
        {'item_id': 862, 'abs_x_position': 17, 'abs_y_position': 2, 'abs_z_position': 1},
        {'item_id': 376, 'abs_x_position': 7, 'abs_y_position': 5, 'abs_z_position': 0},
        {'item_id': 165, 'abs_x_position': 3, 'abs_y_position': 2, 'abs_z_position': 4}
    ],

    #3
    [
        {'item_id': 891, 'abs_x_position': 17, 'abs_y_position': 8, 'abs_z_position': 0},
        {'item_id': 746, 'abs_x_position': 14, 'abs_y_position': 9, 'abs_z_position': 0}
    ],

    #4
    [
        {'item_id': 307, 'abs_x_position': 6, 'abs_y_position': 1, 'abs_z_position': 1},
        {'item_id': 994, 'abs_x_position': 19, 'abs_y_position': 8, 'abs_z_position': 3},
        {'item_id': 192, 'abs_x_position': 3, 'abs_y_position': 8, 'abs_z_position': 1},
        {'item_id': 506, 'abs_x_position': 10, 'abs_y_position': 1, 'abs_z_position': 0},
        {'item_id': 260, 'abs_x_position': 5, 'abs_y_position': 1, 'abs_z_position': 4},
        {'item_id': 362, 'abs_x_position': 7, 'abs_y_position': 2, 'abs_z_position': 1},
        {'item_id': 1000, 'abs_x_position': 19, 'abs_y_position': 9, 'abs_z_position': 4}
    ],

    #5
    [
        {'item_id': 68, 'abs_x_position': 1, 'abs_y_position': 3, 'abs_z_position': 2},
        {'item_id': 696, 'abs_x_position': 13, 'abs_y_position': 9, 'abs_z_position': 0},
        {'item_id': 932, 'abs_x_position': 18, 'abs_y_position': 6, 'abs_z_position': 1},
        {'item_id': 366, 'abs_x_position': 7, 'abs_y_position': 3, 'abs_z_position': 0},
        {'item_id': 66, 'abs_x_position': 1, 'abs_y_position': 3, 'abs_z_position': 1},
        {'item_id': 721, 'abs_x_position': 14, 'abs_y_position': 4, 'abs_z_position': 1},
        {'item_id': 670, 'abs_x_position': 13, 'abs_y_position': 3, 'abs_z_position': 1},
        {'item_id': 307, 'abs_x_position': 6, 'abs_y_position': 1, 'abs_z_position': 1}
    ],

    #6
    [
        {'item_id': 78, 'abs_x_position': 1, 'abs_y_position': 5, 'abs_z_position': 2},
        {'item_id': 87, 'abs_x_position': 1, 'abs_y_position': 7, 'abs_z_position': 1},
        {'item_id': 101, 'abs_x_position': 2, 'abs_y_position': 0, 'abs_z_position': 0},
        {'item_id': 47, 'abs_x_position': 0, 'abs_y_position': 9, 'abs_z_position': 1},
        {'item_id': 110, 'abs_x_position': 2, 'abs_y_position': 1, 'abs_z_position': 4},
        {'item_id': 85, 'abs_x_position': 1, 'abs_y_position': 6, 'abs_z_position': 4},
        {'item_id': 102, 'abs_x_position': 2, 'abs_y_position': 0, 'abs_z_position': 1},
        {'item_id': 111, 'abs_x_position': 2, 'abs_y_position': 2, 'abs_z_position': 0}
    ],

    #7
    [
        {'item_id': 963, 'abs_x_position': 19, 'abs_y_position': 2, 'abs_z_position': 2},
        {'item_id': 351, 'abs_x_position': 7, 'abs_y_position': 0, 'abs_z_position': 0},
        {'item_id': 397, 'abs_x_position': 7, 'abs_y_position': 9, 'abs_z_position': 1},
        {'item_id': 341, 'abs_x_position': 6, 'abs_y_position': 8, 'abs_z_position': 0}
    ],

    #8
    [
        {'item_id': 735, 'abs_x_position': 14, 'abs_y_position': 6, 'abs_z_position': 4}
    ],

    #9
    [
        {'item_id': 975, 'abs_x_position': 19, 'abs_y_position': 4, 'abs_z_position': 4},
        {'item_id': 223, 'abs_x_position': 4, 'abs_y_position': 4, 'abs_z_position': 2},
        {'item_id': 28, 'abs_x_position': 0, 'abs_y_position': 5, 'abs_z_position': 2},
        {'item_id': 881, 'abs_x_position': 17, 'abs_y_position': 6, 'abs_z_position': 0},
        {'item_id': 433, 'abs_x_position': 8, 'abs_y_position': 6, 'abs_z_position': 2},
        {'item_id': 943, 'abs_x_position': 18, 'abs_y_position': 8, 'abs_z_position': 2},
        {'item_id': 351, 'abs_x_position': 7, 'abs_y_position': 0, 'abs_z_position': 0},
        {'item_id': 143, 'abs_x_position': 2, 'abs_y_position': 8, 'abs_z_position': 2},
        {'item_id': 704, 'abs_x_position': 14, 'abs_y_position': 0, 'abs_z_position': 3},
        {'item_id': 155, 'abs_x_position': 3, 'abs_y_position': 0, 'abs_z_position': 4}
    ],

    #10
    [
        {'item_id': 282, 'abs_x_position': 5, 'abs_y_position': 6, 'abs_z_position': 1},
        {'item_id': 776, 'abs_x_position': 15, 'abs_y_position': 5, 'abs_z_position': 0},
        {'item_id': 384, 'abs_x_position': 7, 'abs_y_position': 6, 'abs_z_position': 3},
        {'item_id': 301, 'abs_x_position': 6, 'abs_y_position': 0, 'abs_z_position': 0}
    ],

    #11 (equal as 10 but with one duplicate)
    [
        {'item_id': 282, 'abs_x_position': 5, 'abs_y_position': 6, 'abs_z_position': 1},
        {'item_id': 776, 'abs_x_position': 15, 'abs_y_position': 5, 'abs_z_position': 0},
        {'item_id': 384, 'abs_x_position': 7, 'abs_y_position': 6, 'abs_z_position': 3},
        {'item_id': 384, 'abs_x_position': 7, 'abs_y_position': 6, 'abs_z_position': 3},
        {'item_id': 301, 'abs_x_position': 6, 'abs_y_position': 0, 'abs_z_position': 0}
    ]
]