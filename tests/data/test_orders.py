# Sets of test data with order ids
test_orders = [
    #0
    {
        'order_id': 1,
        'items': [
            {'item_id': 281},
            {'item_id': 579},
            {'item_id': 570},
            {'item_id': 17},
            {'item_id': 505},
            {'item_id': 842},
            {'item_id': 907},
            {'item_id': 696},
            {'item_id': 28},
            {'item_id': 201}
        ]
    },

    #1
    {
        'order_id': 2,
        'items': [
            {'item_id': 376},
            {'item_id': 165},
            {'item_id': 182},
            {'item_id': 518},
            {'item_id': 228},
            {'item_id': 702},
            {'item_id': 862}
        ]
    },

    #2 (equal as 1 but in different order)
    {
        'order_id': 3,
        'items': [
            {'item_id': 228},
            {'item_id': 182},
            {'item_id': 518},
            {'item_id': 702},
            {'item_id': 862},
            {'item_id': 376},
            {'item_id': 165}
        ]
    },

    #3
    {
        'order_id': 4,
        'items': [
            {'item_id': 891},
            {'item_id': 746}
        ]
    },

    #4
    {
        'order_id': 5,
        'items': [
            {'item_id': 307},
            {'item_id': 994},
            {'item_id': 192},
            {'item_id': 506},
            {'item_id': 260},
            {'item_id': 362},
            {'item_id': 1000}
        ]
    },

    #5
    {
        'order_id': 6,
        'items': [
            {'item_id': 282},
            {'item_id': 776},
            {'item_id': 384},
            {'item_id': 301}
        ]
    },

    #6 (equal as 5 but with one duplicate)
    {
        'order_id': 7,
        'items': [
            {'item_id': 282},
            {'item_id': 776},
            {'item_id': 384},
            {'item_id': 384},
            {'item_id': 301}
        ]
    }
]
