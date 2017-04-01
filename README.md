# MiniTWOW-Tools
Some python scripts for minitwow voting and response management

## Usage

You will need to install Python 3 and Pillow

Make a folder with the name of the TWOW episode, for this example, we will name it "exampleTwow"

You will need a file with the prompt in it named "prompt.txt"

You will need a file with all the responses named "responses.txt", one response per line

You will need a file with all the twowers' names, on the lines corresponding to their response in a file named "twowers.txt"

Optionally, put each of the Twowers' booksonas into the booksonas folder

To generate voting slides, go into the command line and type

`python votingScreenGenerator.py exampleTwow`

By default, it will generate 10 slides, if you want more, use `-i`. eg

`python votingScreenGenerator.py exampleTwow -i 100`

creates 100 random voting slides.

To count votes, use

`python countVotes.py [response folder]`

Use flag `-t` to specify how many twowers get the golden background/prize

Use flag `-e` to specify which percentage of twowers get eliminated

Alternatively, if you want to specify how many twowers get eliminated use use a negative number
