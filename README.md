# On-line Order Batching Algorithm

## Table of Contents
1. [Introduction](#blue_book-introduction)
2. [Order Picking in Warehouse](#factory-order-picking-in-warehouse)
3. [Project Details](#scroll-project-details)
4. [How to Run](#computer-how-to-run)
5. [Inputs](#keyboard-inputs)
6. [Testing and Debugging](#test_tube-testing-and-debugging)
7. [Useful Links](#link-useful-links)

## :blue_book: Introduction

This project is part of the [4D4L project](https://www.ifl.kit.edu/forschungsprojekte_5762.php) at the [Institute of Material Handling and Logistics (IFL)](https://www.ifl.kit.edu/index.php) from the [Karlsruhe Institute of Technology (KIT)](https://www.kit.edu/).

The algorithm addresses the on-line order batching problem in an order-picking warehouse, with the goal of minimizing the total completion time of customer orders arriving within a certain period. It modifies heuristic approaches used for static order batching to handle dynamic situations, based on the scientific paper by Sebastian Henn, which can be read [here](https://www.sciencedirect.com/science/article/pii/S0305054812000020/).

The detailed paper for this project is available directly [on GitHub](Implementation%20of%20'Algorithms%20for%20on-line%20order%20batching%20in%20an%20order%20picking%20warehouse'%20using%20Python.PDF) or in the [KITopen Repository](https://publikationen.bibliothek.kit.edu/1000172331).

## :factory: Order Picking in Warehouse

In manual order picking systems, order pickers walk or ride through a distribution warehouse to collect items required by customers. Order batching involves combining indivisible customer orders into picking orders. The choice of an appropriate batching method can significantly reduce the completion time of a set of customer orders.

## :scroll: Project Details

- **Objective**: Minimize the total completion time of customer orders.
- **Methodology**: Modify heuristic approaches for static order batching to suit dynamic situations.
- **Application**: Suitable for manual, single-person order picking systems in warehouses.

## :computer: How to Run without git
1. **Download the repository**
   - Click on the "Code" button and select "Download ZIP".
   - Extract the ZIP file to the desired location.
2. **Navigate to the Project Directory**
   ```bash
   cd path/to/extracted/on-line-order-batching
   ```
3. **Create and Activate a Virtual Environment**:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```
4. **Install the Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
5. **Install the package**
   ```bash
   pip install .
   ```
6. **Start the Program**
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

### :test_tube: Testing and Debugging
To get more information for debugging purposes, switch to the [develop branch](../../tree/develop) and run the program with:
```bash
python -m path.to.your.folder.src.main -d
```
In this branch, test files are available to check the functions separately.

### :link: Useful Links
- [Paper of this project](https://publikationen.bibliothek.kit.edu/1000172331)
- [Scientific Paper by Sebastian Henn](https://www.sciencedirect.com/science/article/pii/S0305054812000020/)
- [4D4L Project](https://www.ifl.kit.edu/forschungsprojekte_5762.php)
- [Institute of Material Handling and Logistics (IFL)](https://www.ifl.kit.edu/index.php)
- [Karlsruhe Institute of Technology (KIT)](https://www.kit.edu/)
