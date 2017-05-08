# MiniTWOW-Tools
Some python scripts for minitwow voting and response management

## Usage

### Voting Slide Generator

To generate voting slides, go into the command line and type

`python3 votingScreenGenerator.py twow_folder [-i amount]`

Replace 'response_folder' with the name of the folder the responses are in

Use the '-i' flag to change the number of slides that are generated

### Generating Booksonas

Run the python script and type the person's name to generate a book

Optionally, run it with a text file containing names as an argument and it will generate booksonas for all the names in that text file

### Gathering votes

Gather all the votes in a file called "votes.txt", then run `python3 voteConverter.py twow_folder`

### Tallying votes 

Usage: `python3 voteConverter.py twow_folder [-t number_of_gold] [-e percent_elim'd]`

Use a negative 'percent_elim'd' to specify number to elim rather than percent

You will need to put the twompt in a file called prompt.txt

## Issues and suggestions

Put issues and suggestions in the issues tab
