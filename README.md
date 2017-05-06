# MiniTWOW-Tools
Some python scripts for minitwow voting and response management

## Usage
To generate voting slides, go into the command line and type

`python votingScreenGenerator.py [response file]`

Replace `[response file]` with the name of the file containing all the responses seperated by line breaks

By default, it will generate 10 slides, if you want more, use `-i`. eg

`python votingScreenGenerator.py [response file] -i 100`

creates 100 random voting slides.
