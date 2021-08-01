import re
import requests

from typing import Dict, List, Any

class card_puller:
    '''
    This class contains methods for pagniating through the magic card api 
    provided by https://api.magicthegathering.io/v1/<item>.
    '''

    def __init__(self, base_url: str = 'https://api.magicthegathering.io/v1/cards') -> None:
        '''
        :param url: URL for the domain serving the apis 
        :type url: str
        :returns: none
        '''

        self._base_url = base_url
        self._pointer_dict = {}
        self._card_list = []

    def get(self, url) -> None:
        response = requests.get(url)
        
        # Pick out the d
        self.headers = response.headers

        # The get request returns a dict with only one entry 'cards'. This key
        # contains a list of the cards returned for the given page.
        self.card_page = response.json()['cards']
        
        # use get_pgaination_pointers to get update the pointers based on the 
        # response
        self.get_pagination_pointers()

        return None

    def get_base_page(self) -> None:
        self.get(self.base_url)

    def get_next_page(self) -> None:
       
        # If there is a next url then get the cards and return true.
        if 'next' in self.pointer_dict.keys():
            self.get(self.pointer_dict['next'])
            return True

        return False
        
    def build_card_list(self) -> None:
        '''
        Builds card list starting at base_url. The function will paginate through
        until the end of the pages. Each page will be appended onto the list of
        cards.
        '''
        # Get the base page
        self.get_base_page()
        
        # Begin card list with the base page
        card_list = self.card_page

        # get_next_page is true when a page was gotten. False at end of pages.
        while self.get_next_page():
            print('in while')
            card_list.extend(self.card_page)

        self._card_list = card_list
        return None


    def get_pagination_pointers(self) -> Dict[str, str]:
        '''
        Take in the headers and parse the response for the pagination pointers
        :returns: Return a dictionary of pointers for the pagination. Pointer 
        labels are first, last, prev, next.
        '''

        # The list of pointers is contained the the 'link' key and is a long 
        # string where different pointer are separated by ','. It also contains
        # some unnecessary whitespace. Strip whitespace and split on ','.
        pointer_list = self.headers['link'].replace(' ', '').split(',')

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

        self._pointer_dict = pointer_dict

        return pointer_dict

    ##############
    # Properties #
    ##############

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def pointer_dict(self) -> Dict:
        return self._pointer_dict

    @property
    def card_list(self) -> List[Dict]:
        return self._card_list

