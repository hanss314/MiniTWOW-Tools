# MiniTWOW-Tools
Some python scripts for minitwow voting and response management

Vote predictor by some_nerd(the pi guy)

## Usage

### Voting Slide Generator

To generate voting slides, go into the command line and type

`python3 votingScreenGenerator.py twow_folder [-i amount]`

Replace 'response_folder' with the name of the folder the responses are in

Use the '-i' flag to change the number of slides that are generated

### Generating Booksonas

Run the python script and type the person's name to generate a book

Optionally, run it with a text file containing names as an argument and it will generate booksonas for all the names in that text file

The vote counter will automatically generate booksonas

### Tallying votes 

Usage: `python3 voteConverter.py twow_folder [-t number_of_gold] [-e percent_elim'd]`

Use a negative 'percent_elim'd' to specify number to elim rather than percent

Store the votes in votes.csv Column A should be the voter and Column B should be the vote

You will need to put the twompt in a file called prompt.txt

### Making predictions

You will have to keep track of your previous twows in history.txt

Put the newest twows at the top of the file and the oldest at the bottom

Make sure all the twows contain a results.csv which will be created by the vote counter

## Issues and suggestions

Put issues and suggestions in the issues tab
