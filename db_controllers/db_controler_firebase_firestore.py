import constants
from unit import Unit

import firebase_admin
from firebase_admin import firestore

import logging

class FirebaseDB():
    def __init__(self) -> None:
        self._project_id = constants.FIREBASE_PROJECT_ID

        self._app = firebase_admin.initialize_app()
        self._db = firestore.client()

#CREATE
    def _create(self, collection_id:str, document_id:str = None, create_dict:dict = {}, merge:bool = False):
    #Three options to write data:
        #1) Set the data of a document within a collection, explicitly specifying a document identifier.
        #2) Add a new document to a collection. In this case, Cloud Firestore automatically generates the document identifier.
        #3) Create an empty document with an automatically generated identifier, and assign data to it later.

    #Cloud Firestore lets you write a variety of data types inside a document, 
    # including strings, booleans, numbers, dates, null, and nested arrays and objects. 
    # Cloud Firestore always stores numbers as doubles, regardless of what type of number you use in your code.

    #If the document does not exist, it will be created. If the document does exist, its contents will be overwritten
    #   unless you specify that the data should be merged into the existing document, as follows:
    #   doc_ref.set(update_dict, merge=True)


        collection_ref = self._db.collection(collection_id)
        if document_id is not None:
            #When you use set() to create a document, you must specify an ID
            doc_ref = collection_ref.document(document_id)
            doc_ref.set(create_dict, merge)
        else:
            #Let firebase auto-generate the id by calling 'add()'
            collection_ref.add(create_dict)

            #To use the reference (to the most recent document) later, call 'document()'
            #new_doc_ref = collection_ref.document()

#READ
    #Three options to load data:
        #Call a method to get the data once.
        #   Want to use this one, since we load it in as mods or packs are selected
        #       but Python does not support having an offline source
        #Set a listener to receive data-change events.
        #Bulk-load Firestore snapshot data from an external source via data bundles.
    def _read_all_in_collection(self, collection_id:str):
        collection_ref = self._db.collection(collection_id)
        docs = collection_ref.stream()

        return docs

    def _read_where(self, field:str, comparator:str, value, recursion_query):
            
        docs = recursion_query.where(field, comparator, value)

        return docs

    def _read_and(self, query_list:list, collection_id:str = None):

        if self._check_query_list_valid(query_list) == False:
            logging.warn(f"Firestore: tried to perform range (<, <=, >, >=) or not equals (!=) comparisons on two different fields")

            return None


        collection_ref = self._db.collection(collection_id)

        recursion_query = collection_ref

        for query_dict in query_list:
            recursion_query = self._read_where(query_dict['field'], query_dict['comparator'], query_dict['value'], recursion_query=recursion_query)

        return recursion_query.stream()

    def _check_query_list_valid(self, query_list:list):

        query_list_valid = True
        
        valid_comparators = {">", "<", ">=", "==", "<=", "!=", "array-contains", "array-contains-any", "in", "not-in"}

        #You can perform range (<, <=, >, >=) or not equals (!=) comparisons only on a single field

        comparators_that_need_unique_fields = {"<", ">", "<=", ">=", "!="}

        #for example, I can't find units with more than X health and less than Y min_initiative
        #   Maybe you can get around this with 'in'

        unique_fields = []
        for query_dict in query_list:
            if query_dict['comparator'] not in valid_comparators:
                query_list_valid = False

                logging.warn(f"Firestore: Tried to run a WHERE opperation with invalid comparator {query_dict['comparator']}!")

                break


            if query_dict['comparator'] in comparators_that_need_unique_fields:
                if query_dict['field'] not in unique_fields:
                    if len(unique_fields) == 1:

                        #That is, if the comparator can only be run on a unique field, 
                        # check if we're already a comparator that also needs a unique field
                        query_list_valid = False

                        logging.warning(f"Firestore: Tried to run two where clauses with comparators on two different fields!")

                        break
                    else:
                        unique_fields = [query_dict['field']]
                        #the first one is fine, but it fails after the second one

        return query_list_valid

    def _read_collection_group(self, collection_group_id:str):
        #I don't need this now, but maybe if I want to get units of the same name from different "expansion packs"
            #Actually, since units would be at the top of the pack, this wouldn't work wthout restructuring

        #These would have been set beforehand by collection_ref.doc_ref.collection(sub_collection_id)
        #EX: expansion_pack_collection.doc_ref.collection(u'insects')

        #If you attempt a compound query with a range clause that doesn't map to an existing index, you receive an error. 
        #The error message includes a direct link to create the missing index in the Firebase console.

        collection_group_ref = self._db.collection_group(collection_group_id)
        #You can call where on this
        pass

    def _read_single(self, collection_id:str, document_id:str):
        collection_ref = self._db.collection(collection_id)
        doc_ref = collection_ref.document(document_id)

        if doc_ref.exists:
            # If there is no document at the location referenced by docRef,
            # the resulting document will be empty and calling exists on it will return false.
            return doc_ref.to_dict()
        else:
            logging.warn(f"Tried to get a firebase doc named {document_id} which does not exist!")
            return None

    def _docs_to_dicts(self, docs):
        #call after read_all and read_where
        dicts = [doc.to_dict() for doc in docs]

        return dicts

#UPDATE
    def _update(self, collection_id:str, document_id:str = None, update_dict:dict = {}):
        #To update some fields of a document without overwriting the entire document, use the update() method:
        #you can use "dot notation" to reference nested fields within the document when you call update()
        #{field.subfield : new_value}
        collection_ref = self._db.collection(collection_id)
        doc_ref = collection_ref.document(document_id)
        doc_ref.update(update_dict)

#DELETE
    def _delete(self, collection_id:str, document_id:str):
        #Deleting a document does not delete its subcollections!
        #You can still access the subcollection documents by reference
        collection_ref = self._db.collection(collection_id)
        doc_ref = collection_ref.document(document_id)

        doc_ref.delete()

    def _delete_field(self, collection_id:str, document_id:str, field:str):
        collection_ref = self._db.collection(collection_id)
        doc_ref = collection_ref.document(document_id)
        
        #To delete specific fields from a document
        doc_ref.update({field: firestore.DELETE_FIELD})

#Project-specific
    def save_unit(self, unit):
        self._create(collection_id = 'units', document_id = unit.name, create_dict = unit.to_dict(), merge=True)

    def update_unit(self, unit):
        #This is unused, for now
        self._update(collection_id = 'units', document_id = unit.name, update_dict = unit.to_dict())

    def get_unit_list_by_name(self, unit_name, game_version):
        #Firestore does not support what one might consider a %like% clause in WHERE

        name_query_dict = {'field': 'name', 'comparator': '==','value': unit_name}
        game_version_query_dict = {'field': 'game_version', 'comparator': '>=', 'value': game_version}

        query_dicts = [name_query_dict, game_version_query_dict]

        fetched_data = self._docs_to_dicts(self._read_and(query_dicts, 'units'))

        self.unit_list = [Unit.from_dict(data) for data in fetched_data]

        return self.unit_list

    #These two aren't called because I don't see a need for them, but I wanted to include them to prove I could
    def add_ai_type(self, unit_name:str, ai_type:str):
        #union = append
        self._update('units', unit_name, {u'ai_types' : firestore.ArrayUnion([ai_type])})

    def remove_ai_type(self, unit_name:str, ai_type:str):
        #remove = remove()
        self._update('units', unit_name, {u'ai_types' : firestore.ArrayRemove([ai_type])})

#OTHER NOTES

    #Increment a numeric value
    #doc_ref.update({"population": firestore.Increment(50)})