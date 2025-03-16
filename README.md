
# Polygon Inclusion Algorithms

This project focuses on the inclusion of polygons algorithm. The goal was to determine which polygons are directly contained within other polygons from a set of simple polygons. The project was developed as part of my Object-Oriented Programming course during my second year at [Ensimag](https://ensimag.grenoble-inp.fr/en) in the Information Systems Engineering course.

![Illustration](art.png)

### Problem Description

Given a set of simple polygons, the task was to identify which polygons are directly included within others. The input was a file containing polygons, and the output should be a list showing the parent-child relationships between polygons.

### Input Format

The input is a `.poly` file, where:
- Each line consists of three elements: an integer, a float (x-coordinate), and a float (y-coordinate).
- The integer represents the polygon index (starting from 0).
- The two floats are the x and y coordinates of a point.

The polygons are described by their vertices, and the file lists them in the order of polygon 0, polygon 1, and so on. The polygons do not have any intersecting segments with other polygons, and within a single polygon, only consecutive segments can intersect at their endpoints.

### Output

The output is a list that indicates the parent polygon for each polygon. For example:
For the file `10x10.poly`, the solution might be:
```
[-1, 0]
```
This means polygon 0 has no parent, and polygon 1 is contained within polygon 0.

## How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/polygon-inclusion-2023.git
   cd polygon-inclusion-2023
   ```

2. Ensure you have all the required dependencies installed. You may need Python 3.x and additional libraries such as NumPy.

3. Run the main program with an input `.poly` file:
   ```bash
   python main.py <input_file.poly>
   ```

4. The results will be printed to the standard output in the required format.


## Algorithm Implemented

1. Point-in-Polygon Algorithms
   - **Ray-Casting**: Counts ray intersections to determine point inclusion.
   - **Grid Point-in-Polygon**: Uses a grid system to optimize point-in-polygon tests, applying Ray-Casting locally within grid cells.

2. Line Generation Algorithms

   - **DDA (Digital Differential Analyzer)**: Generates lines for polygon traversal.
   - **Fast Voxel Traversal Algorithm**: A more precise approach for identifying traversed grid cells.

3. **Inclusion Traversal Algorithms**

   - **Naive Algorithm**: Sort polygons by area and test inclusion pairwise.
   - **Potential Inclusion** Detection: Optimizes the naive algorithm using linked lists and cell-based traversal.

## Performance Analysis

- Ray-Casting performs well for small polygons.
- Grid Point-in-Polygon becomes efficient with pre-built grids but is slower when recalculating grids for every polygon.

## Future Improvements

- Optimize the algorithm to handle more complex polygons and larger datasets efficiently.
- Add support for more complex polygon operations such as intersection or union of polygons.
- Implement a graphical visualization of polygon inclusion relationships.

## License
Academic project - Ensimag.

