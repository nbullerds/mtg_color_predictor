import re
import requests

from typing import Dict, List, Any

class card_puller:
    '''
    This class contains methods for pagniating through the magic card api 
    provided by https://api.magicthegathering.io/v1/<item>.
    '''

    def __inti__(self, base_url: str = 'https://api.magicthegathering.io/v1/cards') -> None:
        '''
        :param url: URL for the domain serving the apis 
        :type url: str
        :returns: none
        '''

        self._base_url = url
        self.url = url

    def get(self, url) -> Dict[str, Dict[str, Any]]:
        response = requests.get(url)
        
        # Pick out the d
        self.headers = response.headers

        # The get request returns a dict with only one entry 'cards'. This key
        # contains a list of the cards returned for the given page.
        self.card_list = response.json()['cards']

        return self.headers, self.card_list

    def pagination_pointers(headers: Dict[str, str]) -> Dict[str, str]:
        '''
        Take in the headers and parse the response for the pagination pointers
        :param headers: Dictionary containing the headers key/values
        :type headers: Dict[str, str]
        :returns: Return a dictionary of pointers for the pagination. Pointer 
        labels are first, last, prev, next.
        '''

        # The list of pointers is contained the the 'link' key and is a long 
        # string where different pointer are separated by ','. It also contains
        # some unnecessary whitespace. Strip whitespace and split on ','.
        pointer_list = headers['link'].replace(' ', '').split(',')

        # Initialize dictionary to store pointers after parsing
        pointer_dict = {}
        
        for pointer in pointer_list:
            # Split on ; to separate the url from the pointer name
            pointer_url, pointer_name = pointer.split(';')
            
            # remove the < and > characters from the url
            pointer_url = re.sub('[<>]', '', pointer_url)

            # extract the Name from the 'rel="Name"'string. Splitting on '"' 
            # will give a list of ['rel=', 'Name', '']. Extract the Name.
            pointer_name = pointer_name.split('"')[1]

            pointer_dict[pointer_name] = pointer_url

        return pointer_dict

            

        ##############
        # Properties #
        ##############

        @property
        def base_url(self) -> str:
            return self._base_url

        @property
        def url(self) -> str:
            return self._url

        @url.setter
        def url(self, url) -> None:
            assert type(url) == str, 'url must be type string'

            self._url = url
