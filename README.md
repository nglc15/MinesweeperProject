# MinesweeperProject


This repository holds the Minesweeper project for UCI's CS 171 Introduction to Artifical Intelligence class.

This project automatically solves randomly generated Minesweeper boards.

To create randomly generated worlds, locate to the WorldGenerator directory and issue the command "./generateSuperEasy.sh" or "./generateTournament.sh".
SuperEasy generates 1000 easy worlds (5x5 board with 1 bombs),
Tournament gerenates 1000 beginner (8x8 board with 10 bombs), 1000 intermediate (16x16 board with 40 bombs) , and 1000 hard worlds (16x30 board with 99 bombs).
***all generated boards will be placed in the /Problems directory***

To run the project, locate the "Minesweeper_Python/src" directory and run the code: "python3 Main.py -f <pathway to the /Problems Directory>.
The resulting print statement will show how many boards were successfully solved.
