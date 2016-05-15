** Author: ** Joe Polin

** Class:** CIS xxx (omitted to prevent future students from finding this on Google)

** Date:** Spring 2014

** Description:** Sudoku solver written for Artificial Intelligence class.

## Usage 

From command line, run

```
$ python solveSudoku.py file_name
```

where file_name contains 9 rows of 9 characters laying out the board. Refer to example files for more information.

You can change the format of the printed board by changing the **pretty** flag in the main method.

## High level approach

Every cell has 9 a domain of 9 possible values. Our goal is to reduce that domain to exactly 1 value for every cell. The function processOfElimination recursively examines the board, removing values in a domain that cannot be true because of a certain value in the same row/column/sub-grid. It also calls the AC3 function which uses the AC3 algorithm (https://en.wikipedia.org/wiki/AC-3_algorithm) to make more difficult deductions. 

solveSudoku accepts a non-reduced board and calls processOfElimination on it. If processOfElimination cannot reduce the board completely, then solveSudoku guesses the value for one of the cells (I choose from the un-reduced cell with the fewest options in its domain). If the board ever becomes invalid, then the most recent guess is removed from the domain, and the search resumes one level above that branch. In this way, solveSudoku's recursive calls create a depth-first search on all cell values that cannot be determined at first glance.


