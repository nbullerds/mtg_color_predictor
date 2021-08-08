from classes.card_puller import card_puller as cp
from pymongo import MongoClient
from typing import List, Dict, Set, Any


class db_init:

    def __init__(self, connection_str: str = '', db_name: str = '',
                coll_name = '', api_connection_str = '') -> None:
        
        self._connection_str = connection_str
        self._db_name = db_name
        self._coll_name = coll_name

        # initilize _coll = None for lazy evaluation
        self._coll = None
        
        # the card_puller connection string can be changed if needed
        if api_connection_str:
            self.card_puller = cp(api_connection_str)
        else:
             self.card_puller = cp()
        
    def connect_collection(self) -> None:
        '''
        Uses self.connecting_str to connect to the collection and sets 
        sefl.collection.
        '''
        connection = MongoClient(self.connection_str)
        db = connection[self.db_name]
        coll = db[self.coll_name]
        self._coll = coll
        
        return None

    def build_id_set(self) -> None:
        '''
        builds self.current_ids which is a set of the current ids in the mongo
        database. These ids can be checked agains
        '''
        # Define projection
        projection_key = 'id'
        id_projection_doc = {'$project': {projection_key: True}}
        
        # Aggregate all documents and project out id
        raw_id_projections = self.coll.aggregate([id_projection_doc])
        
        # Convert the raw projections into a set of ids.
        self._id_set = db_init.raw_to_set(raw_projections = raw_id_projections, 
                                        key = projection_key)
        
        return None

    def build_card_list(self) -> None:
        '''
        build_card_list uses the card_puller package to grab all the cards from
        api.magicthegatering.ip/cards and stors them in a list.
        '''
        self._card_list = self.card_puller.build_card_list()
        return None

    def filter_new_cards(self, card_list: List[Dict[str, Any]],
                        id_set: Set[str]) -> List[Dict[str, Any]]:
        '''
        filter_new_cards takes in card_list and id_set and returns a list of 
        cards whose id are not in id_set, i.e. it returns a list of cards that
        are not curretnly in the card database.
        
        :param card_list: List of cards to be filtered
        :param id_set: A set of ids used to filter the card list.
        :type card_list: list[dict[str, any]]
        :type id_set: set[str]
        :returns: List of cards whose ids are not in id_set
        '''

        new_card_list = []
        for card in card_list:
            try:
                if card['id'] not in id_set: new_card_list.append(card)
            except:
                continue
        
        self._new_card_list = new_card_list
        return new_card_list

    def update_db(self) -> None:
        '''
        Updates the db with cards that are new, i.e. not already in the db.
        '''
        # Build self.card_list of all cards from mtg api
        self.build_card_list()
        # Build set of card ids that are already in the db
        self.build_id_set()
        # Filter and buld self.new_card_list
        self.filter_new_cards(card_list=self.card_list, id_set=self.id_set)

        self.coll.insert_many(self.new_card_list)

        return None


    def raw_to_set(raw_projections: List[Dict[str, str]],
                 key: str) -> Set[str]:
        '''
        Takes a list from a mongo aggregation and projection and grabes all of 
        the values for key and puts them into a set.

        :param raw_prjections: Returned documents form mongo aggregation.
        :param key: values from raw_projections with corresponding key are 
        placed into the set.
        :type raw_projectsions: list[dict[str,str]]
        :type key: str
        :returns: set of the values from raw_projections with corresponding key
        '''

        values_list = []
        for projection in raw_projections:
            # In the off chance that we're missing a key, just keep going.
            try:
                values_list.append(projection[key])
            except:
                continue

        return set(values_list)


    ##############
    # Properties #
    ##############
    @property
    def new_card_list(self):
        return self._new_card_list

    @property
    def db_name(self):
        return self._db_name

    @property
    def coll_name(self):
        return self._coll_name

    @property
    def connection_str(self):
        return self._connection_str

    @property
    def coll(self):
        if self._coll is None:
            self.connect_collection()
        return self._coll

    @property
    def id_set(self):
        return self._id_set

    @property
    def card_list(self):
        return self._card_list

    @property
    def new_card_list(self):
        return self._new_card_list