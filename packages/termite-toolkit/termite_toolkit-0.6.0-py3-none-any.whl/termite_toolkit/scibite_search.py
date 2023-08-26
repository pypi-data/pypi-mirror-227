
"""
  ____       _ ____  _ _         _____           _ _    _ _
 / ___|  ___(_) __ )(_) |_ ___  |_   _|__   ___ | | | _(_) |_
 \___ \ / __| |  _ \| | __/ _ \   | |/ _ \ / _ \| | |/ / | __|
  ___) | (__| | |_) | | ||  __/   | | (_) | (_) | |   <| | |_
 |____/ \___|_|____/|_|\__\___|   |_|\___/ \___/|_|_|\_\_|\__|

SearchRequestBuilder- make requests to the Scibite Search API and process results.

"""

__author__ = 'SciBite'
__version__ = '0.6.0'
__copyright__ = '(c) 2023, SciBite Ltd'
__license__ = 'Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License'

import requests

class SBSRequestBuilder():
	"""
	Class for creating TEXpress requests
	"""

	def __init__(self):
		self.url = ""
		self.auth_url = ""
		self.token_url =""
		self.payload = {"output": "json", "method": "texpress"}
		self.options = {}
		self.basic_auth = ()
		self.verify_request = True
	
	def set_oauth2_legacy(self,client_id,username,password, verification = True):
		"""
		For SciBite Search version < 2.2

		Pass username and password for the Scibite Search token api
		It then uses these credentials to generate an access token and adds 
		this to the request header.
		:client_id: client_id to access the token api
		:username: scibite search username
		:password: scibite search password for username above
		"""
		if self.token_url !="":
			token_address = self.token_url+"/auth/realms/Scibite/protocol/openid-connect/token"
		#SaaS set up uses a different url for authentication
		elif self.auth_url != "":
			token_address = self.auth_url+"/auth/realms/Scibite/protocol/openid-connect/token"
		else:
			token_address = self.url+"/auth/realms/Scibite/protocol/openid-connect/token"
		
		req = requests.post(token_address, data= {"grant_type": "password","client_id":client_id,"username":username, "password":password}, 
			headers = {"Content-Type": "application/x-www-form-urlencoded"})
		access_token = req.json()["access_token"]
		self.headers = {"Authorization": "Bearer "+ access_token}
		self.verify_request = verification

	def set_oauth2(self, client_id, client_secret, verification = True):
		"""
		For SciBite Search version >= 2.2

		Pass client id and client secret for the Scibite Search token api
		It then uses these credentials to generate an access token and adds 
		this to the request header.
		:client_id: client_id to access the token api e.g. scibitesearch-app
		:client_secret: scibite search client_secret for API use
		"""
		if self.token_url !="":
			token_address = self.token_url+"/auth/realms/Scibite/protocol/openid-connect/token"
		#SaaS set up uses a different url for authentication
		elif self.auth_url != "":
			token_address = self.auth_url+"/auth/realms/Scibite/protocol/openid-connect/token"
		else:
			token_address = self.url+"/auth/realms/Scibite/protocol/openid-connect/token"
		
		req = requests.post(token_address, data= { "grant_type":"client_credentials", "client_id":client_id, "client_secret":client_secret }, 
			headers = {"Content-Type": "application/x-www-form-urlencoded"})
		access_token = req.json()["access_token"]
		self.headers = {"Authorization": "Bearer "+ access_token}
		self.verify_request = verification
		
	def set_token_url(self, token_url):
		"""Set the URL for the token API
		:token_url: the URL for the token API
		"""
		self.token_url = token_url.rstrip('/')
		
	def set_url(self, url):
		"""
		Set the URL of the Scibite Search instance
		:url: the URL of the Scibite Search instance to be hit
		"""
		self.url = url.rstrip('/')
	
	def set_auth_url(self, auth_url):
		"""
		Set the URL of the Scibite Search instance
		:url: the URL of the Scibite Search instance to be hit
		for SaaS instances only, this is different to the search url
		"""
		self.auth_url = auth_url.rstrip('/')
		  
	def get_docs(self,query ='', markup=True, limit = 20,offset = 0, additional_fields=[]):
		"""This endpoint allows searching and retrieval of documents. 
		:query: SSQL query
                :type query: string
		:markup: Whether annotated text should markup the entities
		:type markup: bool
                :limit: Limits the number of results
                :type limit: int
		:offset: The number of resources to skip before returning results. Used for implementing paging.
		:type offset: int
                :additional_fields: Additional document fields to output in the response
                :type additional_fields: list of strings
                """
		options ={"markup":markup,"limit":limit, "offset":offset}
		if query:
			options["queries"]=query
		if additional_fields:
			options["fields"]=additional_fields

		req = requests.get(self.url+"/api/search/v1/documents",params = options, headers = self.headers,verify=self.verify_request)
		return req.json()
	
	def get_entities(self,synonym_name="",limit=20, additional_fields=[]):
		"""Wrapper to call the entity endpoint. Currently only working with the synonymName option. """
		options ={"limit":limit}
		if synonym_name:
			options["synonymName"]=synonym_name
		if additional_fields:
			options["fields"]=additional_fields

		req = requests.get(self.url + "/api/search/v1/entities", params = options, headers = self.headers,verify=self.verify_request)
		return req.json()
	
	def get_document(self,document_id, query='',markup = True):
		"""This endpoint retrieves a customizable view of a document
		:document_id: required, the id of the document to be retrieved
                :type document_id: str
		:query: optional, SSQL query
                :type query: str
		:markup: optional, whether annotated text should markup the entities. Default is true
                :type markup: bool
                """
		options ={"markup":markup}
		if query:
			options["queries"]=query
		

		req = requests.get(self.url + "/api/search/v1/documents/"+document_id, params = options, headers = self.headers,verify=self.verify_request)
		return req.json()

	
	def get_sentences(self,query='',markup =True, limit =20, offset =0):
		"""This endpoint allows searching and retrieval of the sentences in the documents. 
		:query: SSQL query
		:markup: Whether annotated text should markup the entities
		:limit: Limits the number of results
		:offset: The number of resources to skip before returning results. Used for implementing paging.
		"""
		options ={"markup":markup,"limit":limit, "offset":offset}
		if query:
			options["queries"]=query

		req = requests.get(self.url+"/api/search/v1/sentences/",params = options, headers = self.headers,verify=self.verify_request)
		return req.json()
	
	def get_aggregates(self,query='',vocabs = [], sentences = True, significant = False, limit = 20, offset = 0):
		"""This function hits either the document aggregates or sentence aggregates API 
		endpoints and returns aggregate counts for the provided query
		:query: SSQL query
		:vocabs: list of vocabularies to select the entity counts from
		:sentences: True for sentence aggregates, False for Document counts
		:significant: If true it sorts by significance score, if false it sorts by count
		:limit: Limits the number of results
		:offset: The number of resources to skip before returing results. Used for implementing paging.
		"""
		options ={"limit":limit, "offset":offset, "includeVocabularies":vocabs}
		if query:
			options["queries"]=query
		if sentences:
			if significant:
				req = requests.get(self.url+"/api/search/v1/sentence-aggregates/significant-entity",params = options, headers = self.headers,verify=self.verify_request)
			else:
				req = requests.get(self.url+"/api/search/v1/sentence-aggregates/entity",params = options, headers = self.headers,verify=self.verify_request)
		else:
			if significant:
				req = requests.get(self.url+"/api/search/v1/document-aggregates/significant-entity",params = options, headers = self.headers,verify=self.verify_request)
			else:
				req = requests.get(self.url+"/api/search/v1/document-aggregates/entity",params = options, headers = self.headers,verify=self.verify_request)			
		return req.json()

	def entity_mentions (self,text,entities=None):
		"""This endpoint annotates a text string with termite annotations.
		Efectively it works as an API endpoint
                :text: the text to annotate
                :type text: str
                :entities: 
                :type entities: """
		if entities:
			options = {"text":text, "entities":entities}
		else:
			options = {"text":text}
		req = requests.get(self.url+"/jobserver/v1/entitymentions", params = options,headers = self.headers,verify=self.verify_request)
		return req.json()

	def document_schemas (self,json_body):
		"""This endpoint posts a new document schema to a ScibiteSearch instance
                :json_body: a valid JSON containing the new document schema with the correct fields
                :type json_body: JSON string"""
		headers = self.headers
		headers['Content-type']='application/json' 
		requests.post(self.url+ '/api/search/v1/document-schemas', json = json_body,headers = headers,verify=self.verify_request)

		
