#!/usr/local/bin/python3

"""Python SDK for Lord of the Rings API movie endpoint.

This CLI executes calls to the Lord of the Rings API 
movie endpoint which covers the following:
 -/movie
 -/movie/{id}
 -/movie/{id}/quote


"""

from typing import Optional,List,Dict,Any

import argparse
import logging
import json
import requests


logging.basicConfig(level=logging.INFO)
API_PREFIX = "https://the-one-api.dev/v2"

def list_movies(header: dict,
                search_filter: Optional[str] = None,
                field_filter: Optional[List[str]] = None) -> List[Any]:
    """Lists movies with search filter and field filter.
    
       Args:
        header: request header 
        search_filter: comma separated key,value for search filtering 
        field_filter: comma separated fields to retreive from results

      Raises:
        ValueError if search field is incorrectly formatted
    
      Returns list of records of movies
    """
    endpoint = "/movie/"
    request = _make_api_request(header, endpoint)
    result = []
    if search_filter:
        field_split = search_filter.split(",")
        if len(field_split)!=2:
            raise ValueError(f"Incorrect search_field {search_field} "
                              "please provide 1 key,value for search")
        key, val = field_split
        for movie in request:
            if val in str(movie[key]):
                result.append(movie)
    else:
        result = request
    if field_filter:
        result =[{key: old_dict[key] for key in field_filter.split(",")} for old_dict in result]
    return result

    

def retrieve_movie(header:dict, 
                   id: str, 
                   field_filter: Optional[List[str]] = None) -> Dict:
    """Retrieves specific movie information and with field filter.
    
      Args:
        header: request header 
        id: movie_id from LOTR api
        field_filter: comma separated fields to retreive from results
    
      Returns:
        Dictionary of movie attributes
    """
    endpoint = f"/movie/{id}/"
    request = _make_api_request(header, endpoint)[0]
    if field_filter:
        return {key: request[key] for key in field_filter.split(",")}
    return request
    

def list_quotes(header:dict, id: str,
                search_filter:Optional[str] =None, 
                field_filter:Optional[List[str]] = None) -> List[Any]:
    """Lists quotes for a movie with search filter and field filter.
    
      Args:
        header: request header 
        search_filter: comma separated key,value for search filtering 
        field_filter: comma separated fields to retreive from results

      Raises:
        ValueError if search field is incorrectly formatted

      Returns:
        List of quotes with attributes
    """

    endpoint = f"/movie/{id}/quote/"
    request = _make_api_request(header, endpoint)
    result = []
    if search_filter:
        field_split = search_filter.split(",")
        if len(field_split)!=2:
            raise ValueError(f"Incorrect search_field {search_field} "
                              "please provide 1 key,value for search")
        key, val = field_split
        for movie in request:
            if val in str(movie[key]):
                result.append(movie)
    else:
        result= request
    if field_filter:
        result =[{key: old_dict[key] for key in field_filter.split(",")} for old_dict in result]
    return result
     
def _make_api_request(header: dict, endpoint: str) -> Dict:
    """Executes api call at given endpoint and returns json result.
    
      Args:
        endpoint: api endpoint
        access_token: access token retrieve for api

      Raises:
        ValueError if request status is not 200

      Returns:
        List of API records from call
    """
    endpoint = f"{API_PREFIX}{endpoint}"
    logging.info(f"Running call to {endpoint}")
    result = requests.get(endpoint, headers=header)
    if result.status_code != 200:
        err_code, err_text = result.status_code, result.text
        raise ValueError(f"API request failed with error code {err_code}"
                            f" and text {err_text}")
    return result.json()["docs"]


def get_header(args:argparse.Namespace) ->Dict:
    """Processes CLI args for API call with authentication.
    
     Args:
      args: argument flags passed into CLI as argparse.Namespace 

     Raises:
      RuntimeError if access_token or cred_file not specified

     Returns:
      Request header in the form of a dict  
    """
    if args.access_token:
        return {"Authorization": f"Bearer {args.access_token}" }
    elif args.creds_json:
        with open(args.creds_json, 'r') as creds_json:
            access_token = json.load(creds_json)['access-token']
        return {"Authorization": f"Bearer {access_token}" }
    raise RuntimeError("No token or credentials json provided. Please see --help")

def process_call(args: argparse.Namespace):
    """Processes CLI args for API call with authentication.
    
     Args:
      args: argument flags passed into CLI as argparse.Namespace 

     Raises:
      RuntimeError if incorrect combination of flags used
    """
    header = get_header(args) 
    logging.info(f"Using {header}")
    if args.movie and args.quote:
        raise RuntimeError("Both movie lookup or quote lookup flag found. "
                           "Please specify one or the other")
    if args.quote and not args.movie_id:
        raise RuntimeError("Quote lookup requested but no movie id provided."
                           "Please specify a movie id for quote lookup")

    result =""
    if args.movie:
        if args.movie_id:
            result = retrieve_movie(header, args.movie_id, args.field_filter)
        else:
            result = list_movies(header, 
                                 search_filter=args.search_filter, 
                                 field_filter=args.field_filter)
    elif args.quote:
        result = list_quotes(header, args.movie_id, args.search_filter, args.field_filter)
    
    logging.info(f"API request results: {result}")

def main():
    parser = argparse.ArgumentParser(
        description=__doc__,  # Prepend help doc with this file's docstring.
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '-c',
        '--creds-json',
        type=str,
        required=False,
        help='path to credentials json file which will contain access_token field')
    parser.add_argument(
        '-a',
        '--access-token',
        type=str,
        required=False,
        help='access token value for Lord of the Rings API')
    parser.add_argument(
        '-m',
        '--movie',
        action='store_true',
        required=False,
        help='Look up movie')
    parser.add_argument(
        '-i',
        '--movie-id',
        type=str,
        required=False,
        help='Use movie id')
    parser.add_argument(
        '-q',
        '--quote',
        action='store_true',
        required=False,
        help='Look up quotes')
    parser.add_argument(
        '-s',
        '--search-filter',
        type=str,
        required=False,
        help='Comma separated key/value for simple contains filtering')
    parser.add_argument(
        '-f',
        '--field-filter',
        type=str,
        required=False,
        help='Comma separated fields for filtering from the result')
    args = parser.parse_args()
    process_call(args)
    
if __name__=="__main__":
    main()
