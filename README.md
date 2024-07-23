# On-line Order Batching Algorithm

## Table of Contents
1. [Introduction](#blue_book-introduction)
2. [Order Picking in Warehouse](#factory-order-picking-in-warehouse)
3. [Project Details](#scroll-project-details)
4. [How to Run](#computer-how-to-run)
5. [Inputs](#keyboard-inputs)
6. [Outputs](#incoming_envelope-outputs)
7. [Testing and Debugging](#test_tube-testing-and-debugging)
8. [Useful Links](#link-useful-links)

## :blue_book: Introduction

This project is part of the [4D4L project](https://www.ifl.kit.edu/forschungsprojekte_5762.php) at the [Institute of Material Handling and Logistics (IFL)](https://www.ifl.kit.edu/index.php) from the [Karlsruhe Institute of Technology (KIT)](https://www.kit.edu/).

The algorithm addresses the on-line order batching problem in an order-picking warehouse, with the goal of minimizing the total completion time of customer orders arriving within a certain period. It modifies heuristic approaches used for static order batching to handle dynamic situations, based on the scientific paper by Sebastian Henn, which can be read [here](https://www.sciencedirect.com/science/article/pii/S0305054812000020/).

The detailed paper for this project is available directly on [GitHub](Implementation%20of%20Algorithms%20for%20On-Line%20Order%20Batching%20in%20an%20Order%20Picking%20Warehouse%20Using%20Python.pdf) or in the [KITopen Repository](https://doi.org/10.5445/ir/1000172331).

## :factory: Order Picking in Warehouse

In manual order picking systems, order pickers walk or ride through a distribution warehouse to collect items required by customers. Order batching involves combining indivisible customer orders into picking orders. The choice of an appropriate batching method can significantly reduce the completion time of a set of customer orders.

## :scroll: Project Details

- **Objective**: Minimize the total completion time of customer orders.
- **Methodology**: Modify heuristic approaches for static order batching to suit dynamic situations.
- **Application**: Suitable for manual, single-person order picking systems in warehouses.

## :computer: How to Run without git
1. **Download the repository**
   - Click on the "Code" button and select "Download ZIP" or download the latest release.
   - Extract the ZIP file to the desired location.
2. **Navigate to the Project Directory**
   ```bash
   cd path/to/extracted/on-line-order-batching
   ```
3. **Create and Activate a Virtual Environment**:
   ```bash
   python -m venv env
   ```
   ```bash
   env\Scripts\activate # On MacOS use `env/bin/activate`
   ```
4. **Install the package**
   ```bash
   pip install .
   ```
5. **Start the Program**
   ```bash
   python -m src.main
   ```

### :keyboard: Inputs
- **Warehouse Layout**: A CSV file where the positions of the items inside the warehouse are stored. Example file: [warehouse_positions.csv](tests/data/warehouse_positions.csv).
- **Orders**: A JSON file from which the CLI thread can take orders to be released to the core logic. Example file: [test_orders.json](tests/data/test_orders.json).
- **Maximum Batch Size**: The maximum number of items that can be picked in one batch (positive integers only).
- **Initial Order Release**: The number of orders released when the program starts (positive integers only).
- **Tour Length Units per Second**: Emulates the speed of how many tour length units per second get passed (positive integers only).
- **Rearrangement Parameter**: Determines the perturbation level in the Iterated Local Search algorithm (values between 0 and 1).
- **Threshold Parameter**: Difference a new best solution must have to be selected in the ILS algorithm (values between 0 and 1).
- **Release Parameter**: Determines waiting time for new orders when only one batch is left (values between 0 and 1).
- **Time Limit**: Sets the time to find a new optimum in the ILS algorithm (positive integers only).
- **Selection Rule**:
  - `FIRST`: Sort by found batches ascending.
  - `SHORT`: Sort by batches with the lowest tour length.
  - `LONG`: Sort by batches with the longest tour length.
  - `SAV`: Sort by batches with the highest tour length savings compared to individual orders.
 
### :incoming_envelope: Outputs
The program provides a detailed table showcasing batches and their respective orders, along with all necessary information. The arrival time is calculated based on the predefined parameter for tour length units per second.
For tour length calculations, the S-Shape Routing method is used, ensuring orders are sorted in a way that allows the picker to follow the routing scheme directly.
```
┌────────────────────────────────────────────┬────────────────────────────────────────────┐
│ Batch ID: 31b7c880111a4336a3221ea7c012ee4d │ Order ID: 4f157778550442f6984026080494fefd │
│                                            │ Item ID: 321, X: 6, Y: 4, Z: 0             │
│                                            │ Item ID: 432, X: 8, Y: 6, Z: 1             │
│                                            │ Item ID: 543, X: 10, Y: 8, Z: 2            │
│                                            │ Item ID: 654, X: 13, Y: 0, Z: 3            │
│                                            │ Item ID: 765, X: 15, Y: 2, Z: 4            │
│                                            │                                            │
│                                            │ Order ID: 07b1cc984117410d9878c0913ab867bb │
│                                            │ Item ID: 135, X: 2, Y: 6, Z: 4             │
│                                            │ Item ID: 246, X: 4, Y: 9, Z: 0             │
│                                            │ Item ID: 357, X: 7, Y: 1, Z: 1             │
│                                            │ Item ID: 468, X: 9, Y: 3, Z: 2             │
│                                            │ Item ID: 579, X: 11, Y: 5, Z: 3            │
│                                            │                                            │
│                                            │ Order ID: 39e8e66100d548b59ed8c8376b7e0aac │
│                                            │ Item ID: 680, X: 13, Y: 5, Z: 4            │
│                                            │ Item ID: 790, X: 15, Y: 7, Z: 4            │
│                                            │ Item ID: 801, X: 16, Y: 0, Z: 0            │
│                                            │ Item ID: 912, X: 18, Y: 2, Z: 1            │
│                                            │ Item ID: 102, X: 2, Y: 0, Z: 1             │
├────────────────────────────────────────────┼────────────────────────────────────────────┤
│ Items sorted by S-Shape-Routing:           │ Item ID: 102, X: 1, Y: 0, Z: 1             │
│                                            │ Item ID: 135, X: 1, Y: 6, Z: 4             │
│                                            │ Item ID: 246, X: 2, Y: 9, Z: 0             │
│                                            │ Item ID: 321, X: 3, Y: 4, Z: 0             │
│                                            │ Item ID: 432, X: 4, Y: 6, Z: 1             │
│                                            │ Item ID: 357, X: 4, Y: 1, Z: 1             │
│                                            │ Item ID: 468, X: 5, Y: 3, Z: 2             │
│                                            │ Item ID: 543, X: 5, Y: 8, Z: 2             │
│                                            │ Item ID: 579, X: 6, Y: 5, Z: 3             │
│                                            │ Item ID: 654, X: 7, Y: 0, Z: 3             │
│                                            │ Item ID: 680, X: 7, Y: 5, Z: 4             │
│                                            │ Item ID: 790, X: 8, Y: 7, Z: 4             │
│                                            │ Item ID: 765, X: 8, Y: 2, Z: 4             │
│                                            │ Item ID: 801, X: 8, Y: 0, Z: 0             │
│                                            │ Item ID: 912, X: 9, Y: 2, Z: 1             │
├────────────────────────────────────────────┼────────────────────────────────────────────┤
│ Amount of Orders:                          │ 3                                          │
├────────────────────────────────────────────┼────────────────────────────────────────────┤
│ Amount of Items:                           │ 15                                         │
├────────────────────────────────────────────┼────────────────────────────────────────────┤
│ Tour Length in warehouse units:            │ 104                                        │
├────────────────────────────────────────────┼────────────────────────────────────────────┤
│ Start Time:                                │ 11:56:42.3                                 │
├────────────────────────────────────────────┼────────────────────────────────────────────┤
│ Arrival Time:                              │ 11:56:47.5                                 │
├────────────────────────────────────────────┼────────────────────────────────────────────┤
│ Tour Time in seconds:                      │ 00:05.2                                    │
└────────────────────────────────────────────┴────────────────────────────────────────────┘
```

### :test_tube: Testing and Debugging
To get more information for debugging purposes, switch to the [develop branch](../../tree/develop) and run the program with:
```bash
python -m src.main -d
```
In this branch, test files are available to check the functions separately.

### :link: Useful Links
- [Paper of this project](https://doi.org/10.5445/ir/1000172331)
- [Scientific Paper by Sebastian Henn](https://www.sciencedirect.com/science/article/pii/S0305054812000020/)
- [4D4L Project](https://www.ifl.kit.edu/forschungsprojekte_5762.php)
- [Institute of Material Handling and Logistics (IFL)](https://www.ifl.kit.edu/index.php)
- [Karlsruhe Institute of Technology (KIT)](https://www.kit.edu/)
