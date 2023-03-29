# Theo-sdk 

Theo-sdk is a CLI which runs API calls to the [Lord of the Rings API](https://the-one-api.dev/), specifically the movie and quotes endpoint. 

# Quickstart

## List all possible flags
```python3 app.py --help```

## Retrieve only movies and their rotten tomatoes score

```python3 app.py --access-token=<your_token> --movie --field-filter=name,rottenTomatoesScore```

## Get quotes from The Fellowship of the Ring with mention of Frodo in dialog

```python3 app.py --creds-json=creds.json --quote --field-filter=dialog,character --movie-id=5cd95395de30eff6ebccde5d --search-filter=dialog,Frodo```

## List all movies and their attributes

```python3 app.py --creds-json=creds.json --movie```

Note that the python3 script also can run off a shebang.
```./app.py --creds-json=creds.json --movie```

## Run unittests

```python3 -m unittest app_test.py```

# Prereqs
The following prereqs are needed in order to test and use the theo-sdk CLI.
	
	1. The theo-sdk CLI uses Python3.
	2. The theo-sdk CLI only uses 1 non-std python library which is the requests library. One can download the library using `pip3 install requests --upgrade`
	3. Usage of the theo-sdk CLI requires a auth token from the Lord of the Rings API. One can sign up [here](https://the-one-api.dev/sign-up).

Once a token is acquired it is passed into the CLI either as a flag parameter `--access-token=<token>` or read in as a json file `--creds-json=<path_to_json_file>`. The json file should be formatted as 
```
{"access-token": "<your-generated-token>"}
```
# Design
See the following image for the logic flow of the CLI
![alt text](theo-sdk.png)

