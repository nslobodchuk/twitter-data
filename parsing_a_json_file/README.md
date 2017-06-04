This text describes how parse a JSON file with tweets in order to visualize relations between users with a graph.

1. Open a terminal.
2. Use `cd` to navigate to the directory with your Twitter data project.
3. `mkdir parsing_a_json_file`
4. `cd parsing_a_json_file`
5. `curl -o twitter_parser.py https://raw.githubusercontent.com/nslobodchuk/twitter-data/master/parsing_a_json_file/twitter_parser.py`
6. `curl -o index.html https://raw.githubusercontent.com/nslobodchuk/twitter-data/master/parsing_a_json_file/index.html`
7. Open "twitter_parser.py" with your favorite code editor and read the comments in order to understand what it does.
7. Put the JSON file with tweets into the current directory and name it "tweets.json"
8. `python3 twitter_parser.py`
9. `python3 -m http.server 8888`
10. Open the browser and navigate to http://localhost:8888