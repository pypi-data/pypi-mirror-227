"""
  ____       _ ____  _ _         _____           _ _    _ _
 / ___|  ___(_) __ )(_) |_ ___  |_   _|__   ___ | | | _(_) |_
 \___ \ / __| |  _ \| | __/ _ \   | |/ _ \ / _ \| | |/ / | __|
  ___) | (__| | |_) | | ||  __/   | | (_) | (_) | |   <| | |_
 |____/ \___|_|____/|_|\__\___|   |_|\___/ \___/|_|_|\_\_|\__|

AI functions- using your TERMite output to make AI-ready data, and using the SciBite AI api to
generate insights.

"""


__author__ = 'SciBite'
__version__ = '0.6.0'
__copyright__ = '(c) 2023, SciBite Ltd'
__license__ = 'Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License'


import os
import json
import requests
import itertools
import nltk.data
import urllib.parse
import termite_toolkit.termite as termite

class SciBiteAIClient():
    def __init__(self):
        self.models = None
        self.sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        self.scibiteai_url = ''
        self.scibiteai_auth = ()
        self.termite_url =''
        self.termite_auth = ()

    def encode_data_for_url(self, data):
        url_str = '?'

        for idx, datum in enumerate(data):
            if idx != 0:
                url_str += '&'
            url_str += ('%s=' % datum + urllib.parse.quote(str(data[datum])))

        return url_str


    ###
    #Core functionality
    ###

    def set_scibite_ai_credentials(self, scibite_ai_addr, scibite_ai_user='',
        scibite_ai_pass=''):
        """
        Set credentials for the SciBite AI server.

        :param string scibite_ai_addr: Address for the SciBite AI server (e.g. 127.0.0.1:8000)
        :param string scibite_ai_user: Username for the SciBite AI server http (if required)
        :param string scibite_ai_pass: Password for the SciBite AI server http (if required)
        """

        self.scibiteai_url = scibite_ai_addr
        self.scibiteai_auth=(scibite_ai_user,scibite_ai_pass)


    def set_termite_credentials(self, termite_addr, termite_user='', termite_pass=''):
        """
        Set credentials for the TERMite server.

        :param string termite_addr: Address for the TERMite server (e.g. 127.0.0.1:9090)
        :param string termite_user: Username for the TERMite server http (if required)
        :param string termite_pass: Password for the TERMite server http (if required)
        """

        self.termite_url = termite_addr
        if termite_user and termite_pass:
            self.termite_auth = (termite_user,termite_pass)

    ###
    #Models functionality
    ###


    def list_model_types(self):
        """
        List the broad categories of models supported by the SciBite AI platform.
        """
        req = '/models'

        response = requests.get(
            f'http://{self.scibiteai_url}{req}',
            auth=self.scibiteai_auth
        )

        return response.json()

    def list_models(self, model_type):
        """
        List models of a specific type.

        :param string type_: The category of models you would like to list (e.g. 'ner')
        """

        req = '/models/%s' % model_type

        response = requests.get(
            f'http://{self.scibiteai_url}{req}',
            auth=self.scibiteai_auth
        )

        return response.json()

    def load_model(self, model_type, model):
        """
        Load a specific model of a specific type.

        :param string type_: The category of the model you would like to load
        :param string model: The specific name of the model you would like to load
        """
        req = '/models/%s/load' % model_type
        data = {'model': model}

        response = requests.post(
            f'http://{self.scibiteai_url}{req}{self.encode_data_for_url(data)}',
            auth=self.scibiteai_auth
        )

        return response.json()


    def unload_model(self, model_type, model):
        """
        Unload a specific model of a specific type.

        :param string type_: The category of the model you would like to unload
        :param string model: The specific name of the model you would like to unload
        """
        req = '/models/%s/unload' % model_type
        data = {'model': model}

        response = requests.post(
            f'http://{self.scibiteai_url}{req}{self.encode_data_for_url(data)}',
            auth=self.scibiteai_auth
        )

        return response.json()

    ###
    #NER functionality
    ###
    def ner_from_sent(self, models, sent, res_format='scibite',hits_only=False):
        """Pass a sentence within which you would like to identify examples of
        entities of a specific type
        :param string models: The type of entities you want to identify
        :param string sent: The sentence where you wish to identify the entities of interest
        :param string res_format: The format of the response (by default it's scibite json)
        :param boolean hits_only: If set to true will return the hits only and not the original
        sentence(s) By default it is set to false"""
        req = '/ner/predict_sentences'

        data = {
            'models' : models,
            'res_format': res_format,
            'hits_only': hits_only
        }

        response = requests.post(
            f'http://{self.scibiteai_url}{req}{self.encode_data_for_url(data)}',
            json={'sentences': sent}
            auth=self.scibiteai_auth
        )

        return response.json()

    def ner_from_file(self, models, file, res_format='scibite', hits_only=False):
        """Pass a document containing sentences within which you would like to identify examples of
        entities of a specific type
        :param string models: The type of entities you want to identify
        :param string file: The filepath of the document (.txt file) where you
        wish to identify the entities of interest
        :param string res_format: The format of the response (by default it's scibite json)
        :param boolean hits_only: If set to true will return the hits only and not the original
        sentences within the document. By default it is set to false"""
        req = '/ner/predict_file'
        file_obj = open(file, 'rb')
        file_name = os.path.basename(file)

        data = {
            'models' : models,
            'res_format' : res_format,
            'hits_only' : hits_only
        }

        response = requests.post(
            f'http://{self.scibiteai_url}{req}{self.encode_data_for_url(data)}',
            files={"file": (file_name, file_obj)},
            auth=self.scibiteai_auth
        )

        return response.json()['task_id']

    ###
    #QA functionality
    ###


    def qa_from_json(self, model, file):
        """
        Pass a file containing SQuAD formatted json questions/contexts to answer said questions.

        :param string model: The model trained to answer the question
        :param string file: The filepath of the document containing SQuAD formatted questions
        you wish to have answered
        """
        req='/qa/predict_json'
        file_obj = open(file, 'rb')
        file_name = os.path.basename(file)
        data = {'model':model}

        response = requests.post(
            f'http://{self.scibiteai_url}{req}{self.encode_data_for_url(data)}',
            files={"file": (file_name, file_obj)},
            auth=self.scibiteai_auth
        )

        return response.json()['task_id']

    def qa_from_text(self, model, question, context):
        """
        Pass a question and the given context to get an answer to said question
        :param string model: The model trained to answer the question
        :param string question: The question we want answered
        :param string context: The context where the answered may be found. Usually
        a paragraph.
        """
        req='/qa/predict_text'
        data = {'model': model, 'context':context, 'question':question}

        response = requests.post(
            f'http://{self.scibiteai_url}{req}{self.encode_data_for_url(data)}',
            auth=self.scibiteai_auth
        )

        return response.json()

    ###
    #RE functionality
    ###


    def re_from_sent(self, models, sent,split_paragraphs=True):
        """
        Pass a sentence within which you would like to identify a relationship using a specific
        model.

        :param string models: The models trained to identify your relationships of interest
        :param string sent: The sentence you wish to assess for your relationship of interest
        :param boolean split_paragraphs: Split text into paragraphs or keep it as whole
        """
        req = '/re/predict_sentences'

        data = {'models': models, 'sentences': sent, 'split' :split_paragraphs}
        data['termite_url'] = self.termite_url
        if self.termite_auth:
            data['termite_http_user'] = self.termite_auth[0]
            data['termite_http_pass'] = self.termite_auth[1]

        response = requests.post(
            f'http://{self.scibiteai_url}{req}{self.encode_data_for_url(data)}',
            auth=self.scibiteai_auth
        )

        return response.json()


    def re_from_file(self, models, file, return_negatives=False):
        """
        Pass a document within which you would like to identify sentences containing relationships
        using a specific model. Returns the task id

        :param string models: The models trained to identify your relationships of interest
        :param string document: The filepath of the document you wish to search for your
        relationship of interest
        """
        req = '/re/predict_file'
        file_obj = open(file, 'rb')
        file_name = os.path.basename(file)
        data = {'models': models}
        if self.termite_auth:
            data['termite_http_user'] = self.termite_auth[0]
            data['termite_http_pass'] = self.termite_auth[1]

        response = requests.post(
            f'http://{self.scibiteai_url}{req}{self.encode_data_for_url(data)}',
            files={"file": (file_name, file_obj)},
            auth=self.scibiteai_auth
        )

        return response.json()['task_id']

    def task_status(self,task_id):
        """
        Gets thte task status for the task_id provided
        :param string task_id: The task_id for the task we're interested in
        """
        req = '/tasks/'+task_id+'/status'
        response = requests.get(f'http://{self.scibiteai_url}{req}')
        return response.json()['task_status']

    def task_results(self,task_id):
        """
        Downloads the json output for the task_id provided
        :param string task_id: The task_id for the task we're interested in
        """
        req = '/tasks/'+task_id+'/download'
        response = requests.get(f'http://{self.scibiteai_url}{req}')
        return response.json()


###
# Helper Functions
###

def get_hits(termiteTags, hierarchy=None, vocabs=None):
    '''
    Uses termiteTags and hierarchy to collect info on the highest priority hits.

    :param array termiteTags: Locations of TERMite hits found, extracted from the TERMite json
    :param dict hierarchy: Dictionary with a hierarchy of vocabs to prioritise in case of overlap
    :param array(str) vocabs: List of vocabs to be substituted, ordered by priority. These vocabs MUST be in the TERMite results. If left
    empty, all vocabs found will be used with random priority where overlaps are found.
    :return array(dict):
    '''
    hits = []
    for hit in termiteTags:
        if not vocabs:
            if hit['entityType'] not in hierarchy:
                hierarchy[hit['entityType']] = len(hierarchy)
        else:
            if hit['entityType'] not in vocabs:
                continue

        if 'fls' in hit['exact_array'][0]: #TERMite 6.3...
            hitLocs, subsumeStates = hit['exact_array'], hit['subsume']
        else: #TERMite 6.4...
            hitLocs = []
            subsumeStates = []
            for hit_array in hit['exact_array']:
                hitLocs.append({'fls': [hit_array['sentence'], hit_array['start'], hit_array['end']]})
                subsumeStates.append(hit_array['subsumed'])

        assert len(hitLocs) == len(subsumeStates)

        for idx, hitLoc in enumerate(hitLocs):
            if hitLoc['fls'][0] < 1:
                continue
            hitInfo = {}
            hitInfo['entityType'], hitInfo['entityID'], hitInfo['entityName'] = hit['entityType'], hit['hitID'], hit[
                'name']
            breakBool = False
            hitInfo['startLoc'], hitInfo['endLoc'] = hitLoc['fls'][1], hitLoc['fls'][2]
            if subsumeStates[idx] == False:  # If hit is not subsumed...
                for hitIdx, hit_ in enumerate(hits):
                    # Compare to already found hits to check there's no conflict
                    if ((hit_['endLoc'] >= hitInfo['startLoc'] and hit_['endLoc'] <= hitInfo['endLoc']) or
                            (hit_['startLoc'] >= hitInfo['startLoc'] and hit_['startLoc'] <= hitInfo['endLoc'])):
                        # If they overlap, check their position in the hierarchy
                        if hierarchy[hit_['entityType']] >= hierarchy[hitInfo['entityType']]:
                            del hits[hitIdx]
                            break
                        else:
                            breakBool = True
                            break
            if not breakBool:
                hits.append(hitInfo)
    return hits


def markup(
        docjsonx,
        normalisation='id',
        substitute=True,
        wrap=False,
        wrapChars=('{!', '!}'),
        vocabs=None,
        labels=None,
        replacementDict=None
):
    '''
    Receives TERMite docjsonx output. Processes the original text, normalising identified hits.

    :param str docjsonx: JSON string generated by TERMite. Must be docjsonx.
    :param str normalisation: Type of normalisation to substitute/add (must be 'id', 'type', 'name', 'typeplusname' or 'typeplusid')
    :param bool substitute: Whether to replace the found term (or add normalisation alongside)
    :param bool wrap: Whether to wrap found hits with 'bookends'
    :param tuple(str) wrapChars: Tuple of length 2, containing strings to insert at start/end of found hits
    :param array(str) vocabs: List of vocabs to be substituted, ordered by priority. These vocabs MUST be in the TERMite results. If left
    empty, all vocabs found will be used with random priority where overlaps are found.
    :param dict replacementDict: Dictionary with <VOCAB>:<string_to_replace_hits_in_vocab>. '~ID~' will be replaced with the entity id,
    and '~TYPE~' will be replaced with the vocab name. Example: {'GENE':'ENTITY_~TYPE~_~ID~'} would result in BRCA1 -> ENTITY_GENE_BRCA1.
    replacementDict supercedes normalisation. ~NAME~ can also be used to get the preferred name.
    :return dict:
    '''

    results = {}

    validTypes = ['id', 'type', 'name', 'typeplusname', 'typeplusid']
    if normalisation not in validTypes:
        raise ValueError(
            'Invalid normalisation requested. Valid options are \'id\', \'name\', \'type\', \'typeplusname\' and \'tyeplusid\'.'
        )

    if len(wrapChars) != 2 or not all(isinstance(wrapping, str) for wrapping in wrapChars):
        raise ValueError('wrapChars must be a tuple of length 2, containing strings.')

    if labels:
        if labels not in ['word', 'char']:
            raise ValueError('labels, if specified, must be either \'word\' or \'char\'')

    hierarchy = {}
    if vocabs:
        for idx, vocab in enumerate(vocabs):
            hierarchy[vocab] = idx

    if isinstance(docjsonx, str):
        json_docs = json.loads(docjsonx)
    else:
        json_docs = docjsonx

    for doc_idx, doc in enumerate(json_docs):
        text = doc['body']

        try:
            substitutions = get_hits(doc['termiteTags'], hierarchy=hierarchy, vocabs=vocabs)
        except KeyError:
            results[doc_idx] = {'termited_text': text}
            continue

        if len(substitutions) > 0:
            substitutions.sort(key=lambda x: x['startLoc'])
            substitutions = reversed(substitutions)

        if wrap:
            prefix = wrapChars[0]
            postfix = wrapChars[1]
        else:
            prefix, postfix = '', ''

        for sub in substitutions:
            subtext = ''
            if replacementDict:
                subtext = replacementDict[sub['entityType']].replace(
                    '~TYPE~', sub['entityType']
                ).replace(
                    '~ID~', sub['entityID']
                ).replace(
                    '~NAME~', sub['entityName']
                )
            elif normalisation == 'id':
                subtext = '_'.join([sub['entityType'], sub['entityID']])
                if not substitute:
                    subtext += ' %s' % text[sub['startLoc']:sub['endLoc']]
            elif normalisation == 'type':
                subtext = sub['entityType']
                if not substitute:
                    subtext += ' %s' % text[sub['startLoc']:sub['endLoc']]
            elif normalisation == 'name':
                subtext = sub['entityName']
                if not substitute:
                    subtext += ' %s' % text[sub['startLoc']:sub['endLoc']]
            elif normalisation == 'typeplusname':
                subtext = '%s %s' % (sub['entityType'], sub['entityName'])
                if not substitute:
                    subtext += ' %s' % text[sub['startLoc']:sub['endLoc']]
            elif normalisation == 'typeplusid':
                subtext = '%s %s' % (
                    sub['entityType'],
                    '_'.join([sub['entityType'], sub['entityID']])
                )

                if not substitute:
                    subtext += ' %s' % text[sub['startLoc']:sub['endLoc']]

            text = text[:sub['startLoc']] + prefix + subtext + postfix + text[sub['endLoc']:]

        results[doc_idx] = {'termited_text': text}

    return results


def pairwise_markup(
        docjsonx,
        pairwise_types_a,
        pairwise_types_b,
        normalisation='id',
        wrap=False,
        wrapChars=('{!', '!}'),
        substitute=True,
        replacementDict=None
):
    '''
    Receives TERMite docjsonx, returns a dictionary with pairwise TERMited substitutions.

    :param docjsonx: JSON string generated by TERMite. Must be docjsonx.
    :param array(str) pairwise_types_a: list of VOCABs to be found on one side of the pairwise relationships
    :param array(str) pairwise_types_b: list of VOCABS to be found on the other side of the pairwise relationships
    :param str normalisation: Type of normalisation to substitute/add (must be 'id', 'type', 'name', 'typeplusname' or 'typeplusid')
    :param bool substitute: Whether to replace the found term (or add normalisation alongside)
    :param bool wrap: Whether to wrap found hits with 'bookends'
    :param tuple(str) wrapChars: Tuple of length 2, containing strings to insert at start/end of found hits
    :param dict replacementDict: Dictionary with <VOCAB>:<string_to_replace_hits_in_vocab>. '~ID~' will be replaced with the entity id,
    and '~TYPE~' will be replaced with the vocab name. Example: {'GENE':'ENTITY_~TYPE~_~ID~'} would result in BRCA1 -> ENTITY_GENE_BRCA1
    replacementDict supercedes normalisation. ~NAME~ can also be used to get the preferred name.
    :return dict: a dictionary containing entity combinations to their respective masked sentences
    '''

    output = {}
    ent_id_to_hit_json = {}
    pairwise_ids_a = []
    pairwise_ids_b = []
    try:
        for hit in docjsonx[0]['termiteTags']:
            if hit['entityType'] in pairwise_types_a:
                pairwise_ids_a.append(hit['hitID'])
            elif hit['entityType'] in pairwise_types_b:
                pairwise_ids_b.append(hit['hitID'])
            else:
                continue

            ent_id_to_hit_json[hit['hitID']] = hit

    except TypeError:
        raise('Error retrieving results from TERMite')

    except KeyError:
        pass

    combos = itertools.product(pairwise_ids_a, pairwise_ids_b)

    for combo in combos:
        termiteTags = [ent_id_to_hit_json[combo[0]], ent_id_to_hit_json[combo[1]]]
        docjsonx[0]['termiteTags'] = termiteTags
        output[combo] = markup(
            docjsonx,
            vocabs=pairwise_types_a+pairwise_types_b,
            normalisation=normalisation,
            wrap=wrap,
            wrapChars=wrapChars,
            substitute=substitute,
            replacementDict=replacementDict
        )[0]['termited_text']
    return output


def text_markup(
        text,
        termiteAddr='http://localhost:9090/termite',
        vocabs=['GENE', 'INDICATION', 'DRUG'],
        normalisation='id',
        wrap=False,
        wrapChars=('{!', '!}'),
        substitute=True,
        replacementDict=None,
        termite_http_user=None,
        termite_http_pass=None,
        include_json=False
):
    '''
    Receives plain text, returns text with TERMited substitutions.

    :param str text: Text in which to markup entities
    :param str normalisation: Type of normalisation to substitute/add (must be 'id', 'type', 'name', 'typeplusname' or 'typeplusid')
    :param bool substitute: Whether to replace the found term (or add normalisation alongside)
    :param bool wrap: Whether to wrap found hits with 'bookends'
    :param tuple(str) wrapChars: Tuple of length 2, containing strings to insert at start/end of found hits
    :param array(str) vocabs: List of vocabs to be substituted, ordered by priority. These vocabs MUST be in the TERMite results. If left
    empty, all vocabs found will be used with random priority where overlaps are found.
    :param dict replacementDict: Dictionary with <VOCAB>:<string_to_replace_hits_in_vocab>. '~ID~' will be replaced with the entity id,
    and '~TYPE~' will be replaced with the vocab name. Example: {'GENE':'ENTITY_~TYPE~_~ID~'} would result in BRCA1 -> ENTITY_GENE_BRCA1
    replacementDict supercedes normalisation. ~NAME~ can also be used to get the preferred name.
    :return str:
    '''

    termite_handle = termite.TermiteRequestBuilder()
    termite_handle.set_url(termiteAddr)
    termite_handle.set_text(text)
    termite_handle.set_entities(','.join(vocabs))
    termite_handle.set_subsume(True)
    termite_handle.set_input_format("txt")
    termite_handle.set_output_format("doc.jsonx")

    if termite_http_pass:
        termite_handle.set_basic_auth(
            termite_http_user,
            termite_http_pass,
            verification=False
        )

    docjsonx = termite_handle.execute()
    # print(docjsonx)

    if include_json:
        return markup(
            docjsonx,
            vocabs=vocabs,
            normalisation=normalisation,
            wrap=wrap,
            wrapChars=wrapChars,
            substitute=substitute,
            replacementDict=replacementDict
        )[0]['termited_text'], docjsonx

    return markup(
        docjsonx,
        vocabs=vocabs,
        normalisation=normalisation,
        wrap=wrap,
        wrapChars=wrapChars,
        substitute=substitute,
        replacementDict=replacementDict
    )[0]['termited_text']


def pairwise_text_markup(
        text,
        pairwise_types_a,
        pairwise_types_b,
        termiteAddr='http://localhost:9090/termite',
        normalisation='id',
        wrap=False,
        wrapChars=('{!', '!}'),
        substitute=True,
        replacementDict=None,
        termite_http_user=None,
        termite_http_pass=None,
        include_json=False
):
    '''
    Receives plain text, returns a dictionary with pairwise TERMited substitutions.

    :param str text: Text in which to markup entities
    :param array(str) pairwise_types_a: list of VOCABs to be found on one side of the pairwise relationships
    :param array(str) pairwise_types_b: list of VOCABS to be found on the other side of the pairwise relationships
    :param str normalisation: Type of normalisation to substitute/add (must be 'id', 'type', 'name', 'typeplusname' or 'typeplusid')
    :param bool substitute: Whether to replace the found term (or add normalisation alongside)
    :param bool wrap: Whether to wrap found hits with 'bookends'
    :param tuple(str) wrapChars: Tuple of length 2, containing strings to insert at start/end of found hits
    :param dict replacementDict: Dictionary with <VOCAB>:<string_to_replace_hits_in_vocab>. '~ID~' will be replaced with the entity id,
    and '~TYPE~' will be replaced with the vocab name. Example: {'GENE':'ENTITY_~TYPE~_~ID~'} would result in BRCA1 -> ENTITY_GENE_BRCA1
    replacementDict supercedes normalisation. ~NAME~ can also be used to get the preferred name.
    :return dict: a dictionary containing entity combinations to their respective masked sentences
    '''
    t = termite.TermiteRequestBuilder()
    t.set_url(termiteAddr)
    t.set_text(text)
    t.set_entities(','.join(pairwise_types_a+pairwise_types_b))
    t.set_subsume(True)
    t.set_input_format("txt")
    t.set_output_format("doc.jsonx")
    if termite_http_pass:
        t.set_basic_auth(termite_http_user, termite_http_pass, verification=False)
    docjsonx = t.execute()

    if include_json:
        return pairwise_markup(
            docjsonx,
            pairwise_types_a=pairwise_types_a,
            pairwise_types_b=pairwise_types_b,
            normalisation=normalisation,
            wrap=wrap,
            wrapChars=wrapChars,
            substitute=substitute,
            replacementDict=replacementDict
        ), docjsonx

    return pairwise_markup(
        docjsonx,
        pairwise_types_a=pairwise_types_a,
        pairwise_types_b=pairwise_types_b,
        normalisation=normalisation,
        wrap=wrap,
        wrapChars=wrapChars,
        substitute=substitute,
        replacementDict=replacementDict
    )


def label(docjsonx, vocabs, labelLevel='word'):
    '''
    Receives TERMite output docjsonx and returns split text with labels as to what entities are found in that part of the text.

    :param str docjsonx: JSON string generated by TERMite. Must be docjsonx.
    :param str labelLevel: Labels for where hits are found in the text. Must be 'char' or 'word', word by default
    :param array(str) vocabs: List of vocabs to be substituted, ordered by priority. These vocabs MUST be in the TERMite results. If left
    empty, all vocabs found will be used with random priority where overlaps are found.
    :return dict:
    '''

    results = {}
    hierarchy = {}
    for idx, vocab in enumerate(vocabs):
        hierarchy[vocab] = idx

    if isinstance(docjsonx, str):
        j = json.loads(docjsonx)
    else:
        j = docjsonx

    for docIdx, doc in enumerate(j):
        text = doc['body']

        splitText, labels = None, None
        if labelLevel == 'word':
            splitText = text.split()
        elif labelLevel == 'char':
            splitText = list(text)

        labels = [0 for i in splitText]

        try:
            hits = get_hits(doc['termiteTags'], hierarchy=hierarchy, vocabs=vocabs)
        except KeyError:
            results[docIdx] = {'split_text': splitText, 'labels': labels}
            continue

        for hit in hits:
            if labelLevel == 'char':
                for i in range(hit['startLoc'], hit['endLoc']):
                    labels[i] = hierarchy[hit['entityType']] + 1
            elif labelLevel == 'word':
                cursor = 0
                for wIdx, w in enumerate(splitText):
                    if cursor >= hit['startLoc'] and cursor <= hit['endLoc']:
                        labels[wIdx] = hierarchy[hit['entityType']] + 1
                    cursor += len(w) + 1

        results[docIdx] = {'split_text': splitText, 'labels': labels}

    return results
