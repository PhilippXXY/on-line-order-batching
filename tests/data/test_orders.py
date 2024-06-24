# Sets of test data with order ids
test_orders = [
    # 1
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

    # 2
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

    # 3 (equal as #2 but in different order)
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

    # 4
    {
        'order_id': 4,
        'items': [
            {'item_id': 891},
            {'item_id': 746}
        ]
    },

    # 5
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

    # 6
    {
        'order_id': 6,
        'items': [
            {'item_id': 282},
            {'item_id': 776},
            {'item_id': 384},
            {'item_id': 301}
        ]
    },

    # 7 (equal as #6 but with one duplicate)
    {
        'order_id': 7,
        'items': [
            {'item_id': 282},
            {'item_id': 776},
            {'item_id': 384},
            {'item_id': 384},
            {'item_id': 301}
        ]
    },

    # 8 (equal as #4)
    {
        'order_id': 8,
        'items': [
            {'item_id': 891},
            {'item_id': 746}
        ]
    },

    # 9 (equal as #4 but with one duplicate)
    {
        'order_id': 9,
        'items': [
            {'item_id': 891},
            {'item_id': 746},
            {'item_id': 891}
        ]
    },

    # 10
    {
        'order_id': 10,
        'items': [
            {'item_id': 410},
            {'item_id': 564},
            {'item_id': 678},
            {'item_id': 789},
            {'item_id': 234}
        ]
    },

    # 11
    {
        'order_id': 11,
        'items': [
            {'item_id': 111},
            {'item_id': 222},
            {'item_id': 333},
            {'item_id': 444},
            {'item_id': 555}
        ]
    },

    # 12
    {
        'order_id': 12,
        'items': [
            {'item_id': 123},
            {'item_id': 456},
            {'item_id': 789},
            {'item_id': 101},
            {'item_id': 202}
        ]
    },

    # 13
    {
        'order_id': 13,
        'items': [
            {'item_id': 555},
            {'item_id': 666},
            {'item_id': 777},
            {'item_id': 888},
            {'item_id': 999}
        ]
    },

    # 14
    {
        'order_id': 14,
        'items': [
            {'item_id': 321},
            {'item_id': 432},
            {'item_id': 543},
            {'item_id': 654},
            {'item_id': 765}
        ]
    },

    # 15
    {
        'order_id': 15,
        'items': [
            {'item_id': 135},
            {'item_id': 246},
            {'item_id': 357},
            {'item_id': 468},
            {'item_id': 579}
        ]
    },

    # 16
    {
        'order_id': 16,
        'items': [
            {'item_id': 680},
            {'item_id': 790},
            {'item_id': 801},
            {'item_id': 912},
            {'item_id': 102}
        ]
    },

    # 17
    {
        'order_id': 17,
        'items': [
            {'item_id': 300},
            {'item_id': 400},
            {'item_id': 500},
            {'item_id': 600},
            {'item_id': 700}
        ]
    },

    # 18
    {
        'order_id': 18,
        'items': [
            {'item_id': 812},
            {'item_id': 923},
            {'item_id': 103},
            {'item_id': 204},
            {'item_id': 305}
        ]
    },

    # 19
    {
        'order_id': 19,
        'items': [
            {'item_id': 450},
            {'item_id': 560},
            {'item_id': 670},
            {'item_id': 780},
            {'item_id': 890}
        ]
    },

    # 20
    {
        'order_id': 20,
        'items': [
            {'item_id': 501},
            {'item_id': 602},
            {'item_id': 703},
            {'item_id': 804},
            {'item_id': 905}
        ]
    },

    # 21
    {
        'order_id': 21,
        'items': [
            {'item_id': 213},
            {'item_id': 324}
        ]
    },

    # 22
    {
        'order_id': 22,
        'items': [
            {'item_id': 567},
            {'item_id': 678},
            {'item_id': 789}
        ]
    },

    # 23
    {
        'order_id': 23,
        'items': [
            {'item_id': 890},
            {'item_id': 901},
            {'item_id': 123},
            {'item_id': 234}
        ]
    },

    # 24
    {
        'order_id': 24,
        'items': [
            {'item_id': 345},
            {'item_id': 456},
            {'item_id': 567}
        ]
    },

    # 25
    {
        'order_id': 25,
        'items': [
            {'item_id': 678},
            {'item_id': 789},
            {'item_id': 890},
            {'item_id': 901}
        ]
    },

    # 26
    {
        'order_id': 26,
        'items': [
            {'item_id': 101},
            {'item_id': 202},
            {'item_id': 303}
        ]
    },

    # 27
    {
        'order_id': 27,
        'items': [
            {'item_id': 404},
            {'item_id': 505}
        ]
    },

    # 28
    {
        'order_id': 28,
        'items': [
            {'item_id': 606},
            {'item_id': 707},
            {'item_id': 808},
            {'item_id': 909}
        ]
    },

    # 29
    {
        'order_id': 29,
        'items': [
            {'item_id': 100},
            {'item_id': 200},
            {'item_id': 300},
            {'item_id': 400},
            {'item_id': 500}
        ]
    },

    # 30
    {
        'order_id': 30,
        'items': [
            {'item_id': 600},
            {'item_id': 700},
            {'item_id': 800}
        ]
    },

    # 31
    {
        'order_id': 31,
        'items': [
            {'item_id': 711},
            {'item_id': 821},
            {'item_id': 931},
            {'item_id': 102},
            {'item_id': 203}
        ]
    },

    # 32
    {
        'order_id': 32,
        'items': [
            {'item_id': 314},
            {'item_id': 425},
            {'item_id': 536}
        ]
    },

    # 33
    {
        'order_id': 33,
        'items': [
            {'item_id': 647},
            {'item_id': 758},
            {'item_id': 869},
            {'item_id': 980},
            {'item_id': 101}
        ]
    },

    # 34
    {
        'order_id': 34,
        'items': [
            {'item_id': 212},
            {'item_id': 323},
            {'item_id': 434},
            {'item_id': 545}
        ]
    },

    # 35
    {
        'order_id': 35,
        'items': [
            {'item_id': 656},
            {'item_id': 767},
            {'item_id': 878}
        ]
    },

    # 36
    {
        'order_id': 36,
        'items': [
            {'item_id': 989},
            {'item_id': 100},
            {'item_id': 211},
            {'item_id': 322},
            {'item_id': 433}
        ]
    },

    # 37
    {
        'order_id': 37,
        'items': [
            {'item_id': 544},
            {'item_id': 655},
            {'item_id': 766},
            {'item_id': 877},
            {'item_id': 988}
        ]
    },

    # 38
    {
        'order_id': 38,
        'items': [
            {'item_id': 199},
            {'item_id': 299},
            {'item_id': 399},
            {'item_id': 499}
        ]
    },

    # 39
    {
        'order_id': 39,
        'items': [
            {'item_id': 599},
            {'item_id': 699},
            {'item_id': 799},
            {'item_id': 899},
            {'item_id': 999}
        ]
    },

    # 40
    {
        'order_id': 40,
        'items': [
            {'item_id': 101},
            {'item_id': 202},
            {'item_id': 303},
            {'item_id': 404},
            {'item_id': 505}
        ]
    },

    # 41
    {
        'order_id': 41,
        'items': [
            {'item_id': 606},
            {'item_id': 707},
            {'item_id': 808},
            {'item_id': 909}
        ]
    },

    # 42
    {
        'order_id': 42,
        'items': [
            {'item_id': 111},
            {'item_id': 222},
            {'item_id': 333},
            {'item_id': 444},
            {'item_id': 555}
        ]
    },

    # 43
    {
        'order_id': 43,
        'items': [
            {'item_id': 666},
            {'item_id': 777},
            {'item_id': 888},
            {'item_id': 999}
        ]
    },

    # 44
    {
        'order_id': 44,
        'items': [
            {'item_id': 123},
            {'item_id': 234},
            {'item_id': 345},
            {'item_id': 456}
        ]
    },

    # 45
    {
        'order_id': 45,
        'items': [
            {'item_id': 567},
            {'item_id': 678},
            {'item_id': 789},
            {'item_id': 890},
            {'item_id': 901}
        ]
    },

    # 46
    {
        'order_id': 46,
        'items': [
            {'item_id': 12},
            {'item_id': 123},
            {'item_id': 234},
            {'item_id': 345},
            {'item_id': 456}
        ]
    },

    # 47
    {
        'order_id': 47,
        'items': [
            {'item_id': 567},
            {'item_id': 678},
            {'item_id': 789},
            {'item_id': 890},
            {'item_id': 901}
        ]
    },

    # 48
    {
        'order_id': 48,
        'items': [
            {'item_id': 102},
            {'item_id': 203},
            {'item_id': 203},
            {'item_id': 405},
            {'item_id': 405}
        ]
    },

    # 49
    {
        'order_id': 49,
        'items': [
            {'item_id': 607},
            {'item_id': 708},
            {'item_id': 809},
            {'item_id': 910}
        ]
    },

    # 50
    {
        'order_id': 50,
        'items': [
            {'item_id': 11}
        ]
    }
]
