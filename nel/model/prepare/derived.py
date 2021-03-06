#!/usr/bin/env python
import math
import re
import logging
import marshal
import os
import operator
import unicodedata

from time import time
from collections import defaultdict, Counter
from schwa import dr
from .. import model

from ..model import Redirects
from ..model import WordVectors
from ..model import EntityMentionContexts
from ..model import mmdict
from ..model import Links
from ..model import EntityOccurrence, EntityCooccurrence
from ..model import Candidates

from .util import trim_subsection_link, normalise_wikipedia_link
from ...util import parmapper

log = logging.getLogger()

class BuildEntitySet(object):
    "Build redirect model from wikipedia-redirect tsv."
    def __init__(self, page_model_path, entity_set_model_path):
        self.page_model_path = page_model_path
        self.entity_set_model_path = entity_set_model_path

    def __call__(self):
        log.info('Building entity set for corpus: %s', self.page_model_path)

        class Doc(dr.Doc):
            name = dr.Field()

        entities = set()

        with open(self.page_model_path,'r')  as f:
            reader = dr.Reader(f, Doc.schema())
            for i, doc in enumerate(reader):
                if i % 500000 == 0:
                    log.debug('Processed %i documents...', i)
                entities.add(doc.name)

        log.info('Writing entity set model to file: %s', self.entity_set_model_path)
        with open(self.entity_set_model_path, 'wb') as f:
            marshal.dump(entities, f)

    @classmethod
    def add_arguments(cls, p):
        p.add_argument('page_model_path', metavar='PAGE_MODEL')
        p.add_argument('entity_set_model_path', metavar='ENTITY_SET_MODEL')
        p.set_defaults(cls=cls)
        return p

class BuildLinkModels(object):
    "Build link derived models from a docrep corpus."
    def __init__(self, page_model_path, redirect_model_tag, entities_model_tag, model_tag):
        self.page_model_path = page_model_path
        self.redirect_model_tag = redirect_model_tag
        self.entities_model_tag = entities_model_tag
        self.model_tag = model_tag

    def __call__(self):
        log.info('Building page link derived models from: %s', self.page_model_path)

        class Link(dr.Ann):
            anchor = dr.Field()
            target = dr.Field()

        class Doc(dr.Doc):
            name = dr.Field()
            links = dr.Store(Link)

        redirects = model.Redirects(self.redirect_model_tag, prefetch=True)

        log.info('Loading entity set...')
        entity_model = model.Entities(self.entities_model_tag)
        entity_set = set(entity_model.iter_ids())

        if entity_set:
            log.info("Building link models over %i entities...", len(entity_set))
        else:
            log.warn("Entity set (%s) is empty, build will not yield results.", self.entities_model_tag)
            return

        entity_counts = defaultdict(int)
        name_entity_counts = defaultdict(lambda:defaultdict(int))
        with open(self.page_model_path,'r')  as f:
            reader = dr.Reader(f, Doc.schema())
            for i, doc in enumerate(reader):
                if i == 10000 or i % 250000 == 0:
                    log.info('Processed %i documents...', i)

                for link in doc.links:
                    # we may want to ignore subsection links when generating name models
                    # sometimes a page has sections which refer to subsidiary entities
                    # links to these may dilute the name posterior for the main entity
                    # for now we just add everything to keep it simple
                    target = trim_subsection_link(link.target)
                    target = normalise_wikipedia_link(target)
                    target = redirects.map(target)
                    target = trim_subsection_link(target)

                    #occurrence.add(target, doc.name)

                    # ignore out-of-kb links in entity and name probability models
                    if target in entity_set:
                        entity_counts[target] += 1
                        name_entity_counts[self.normalise_name(link.anchor)][target] += 1

        ep_model = model.EntityPrior(self.model_tag)
        ep_model.create(entity_counts.iteritems())
        entity_counts = None
        nep_model = model.NameProbability(self.model_tag)
        nep_model.create(name_entity_counts.iteritems())
        nep_model = None
        # occurrence = EntityOccurrence() # todo: occurrence model datastore backend
        log.info('Done')

    def normalise_name(self, name):
        return name.lower()

    @classmethod
    def add_arguments(cls, p):
        p.add_argument('page_model_path', metavar='PAGE_MODEL_PATH')
        p.add_argument('redirect_model_tag', metavar='REDIRECT_MODEL_TAG')
        p.add_argument('entities_model_tag', metavar='ENTITIES_MODEL_TAG')
        p.add_argument('model_tag', metavar='MODEL_TAG')
        p.set_defaults(cls=cls)
        return p

class BuildContextModels(object):
    "Build link derived models from a docrep corpus."
    def __init__(self, docs_path, model_tag):
        self.docs_path = docs_path
        self.model_tag = model_tag

        class Token(dr.Ann):
            norm = dr.Field()
        class Doc(dr.Doc):
            name = dr.Field()
            tokens = dr.Store(Token)
        self.doc_schema = Doc.schema()

    def process_chunk(self, path):
        bows = []
        with open(path,'r')  as f:
            for doc in dr.Reader(f, self.doc_schema):
                bows.append((doc.name, Counter(t.norm.lower() for t in doc.tokens)))
        return bows

    def iter_file_names(self):
        for path, _, files in os.walk(self.docs_path):
            for filename in files:
                if filename.endswith('.dr'):
                    yield os.path.join(path, filename)

    def iter_doc_bows(self):
        with parmapper(self.process_chunk, recycle_interval=None) as pm:
            for _, instances in pm.consume(self.iter_file_names()):
                for x in instances:
                    yield x

    def __call__(self):
        log.info('Building ctx models from: %s', self.docs_path)
        total_docs = 4850000
        start_time = time()

        dfs = defaultdict(int)
        def process_bows():
            for i, (name, bow) in enumerate(self.iter_doc_bows()):
                for term in bow.iterkeys():
                    dfs[term] += 1
                if i % 100000 == 0:
                    if i > 0:
                        dps = i / (time() - start_time)
                        eta = ((total_docs - i) / dps) / 60.0
                    else:
                        dps, eta = 0, 0
                    log.info('Processed %i documents... (%.1f dps, %.1f mins)', i, dps, eta)
                yield (name, bow)

        tf_model = model.EntityTermFrequency(self.model_tag)
        tf_model.create(process_bows())
        df_model = model.TermDocumentFrequency(self.model_tag)
        df_model.create(total_docs, dfs.iteritems())
        log.info('Done')

    @classmethod
    def add_arguments(cls, p):
        p.add_argument('docs_path', metavar='DOCS_PATH')
        p.add_argument('model_tag', metavar='MODEL_TAG')
        p.set_defaults(cls=cls)
        return p

class BuildTitleRedirectNames(object):
    "Builds alias model using the title of an entity page (e.g. Some_Entity) and the title of redirects."
    def __init__(self, title_model_path, redirect_model_path, alias_model_path):
        self.title_model_path = title_model_path
        self.redirect_model_path = redirect_model_path
        self.alias_model_path = alias_model_path
        self.underscores_re = re.compile('_+')

    def convert_title_to_name(self, entity):
        # strip parts after a comma
        comma_idx = entity.find(',_')
        if comma_idx > 0:
            entity = entity[:comma_idx]

        # strip components in brackets
        lb_idx = entity.rfind('_(')
        if lb_idx > 0:
            rb_idx = entity.find(')', lb_idx)
            if rb_idx > 0:
                entity = entity[:lb_idx] + entity[rb_idx+1:]
        
        # replace underscores with spaces
        return self.underscores_re.sub(' ', entity)

    def __call__(self):
        log.info('Loading entity titles: %s' % self.title_model_path)
        titles = marshal.load(open(self.title_model_path, 'rb'))

        log.info('Loading entity redirects: %s' % self.redirect_model_path)
        redirects = Redirects.read(self.redirect_model_path).get_redirects_by_entity()

        log.info('Processing entity titles...')
        aliases = {}
        alias_count = 0
        for entity in titles:
            entity_titles = set(redirects.get(entity, []))
            entity_titles.add(entity)
            
            entity_aliases = set(self.convert_title_to_name(t) for t in entity_titles)
            alias_count += len(entity_aliases)
            aliases[entity] = list(entity_aliases)

        log.info('Writing entity alias model (%i entities, %i names): %s' % (len(aliases), alias_count, self.alias_model_path))
        marshal.dump(aliases, open(self.alias_model_path,'wb'))

    @classmethod
    def add_arguments(cls, p):
        p.add_argument('title_model_path', metavar='IN_TITLE_MODEL_FILE')
        p.add_argument('redirect_model_path', metavar='IN_REDIRECT_MODEL_FILE')
        p.add_argument('alias_model_path', metavar='OUT_ALIAS_MODEL_FILE')
        p.set_defaults(cls=cls)
        return p

def get_mention_term_counts(emw):
    entity, mentions, window = emw
    rhs_len = None if window == None else window / 2
    lhs_len = None if window == None else window - rhs_len

    global ngram_vocab

    counts = Counter()
    for _, l, n, r in mentions:
        lhs, name, rhs = tokenize(l), tokenize(n), tokenize(r)

        if window == None: tokens = lhs + name + rhs
        else:              tokens = lhs[-lhs_len:] + name + rhs[:rhs_len]

        counts.update(ngrams(tokens, 3, ngram_vocab))

    return (entity, counts)

def iter_common_lemma_names():
    for synset in wordnet.all_synsets():
        for name in synset.lemma_names:
            if name.islower():
                yield name

class BuildCandidateModel(object):
    "Builds a model mapping aliases to entites for candidate generation"
    def __init__(self, entities_model_tag, redirect_model_tag, name_model_tag, model_tag):
        self.name_model_tag = name_model_tag
        self.model_tag = model_tag

        self.underscores_re = re.compile('_+')

        self.redirects = Redirects(redirect_model_tag, prefetch=True)

        log.info('Pre-fetching kb entity set...')
        self.entities_model = model.Entities(entities_model_tag)
        self.entity_set = set(self.redirects.map(e) for e in self.entities_model.iter_ids())
 
    def convert_title_to_name(self, entity):
        # strip parts after a comma
        comma_idx = entity.find(',_')
        if comma_idx > 0:
            entity = entity[:comma_idx]

        # strip components in brackets
        lb_idx = entity.rfind('_(')
        if lb_idx > 0:
            rb_idx = entity.find(')', lb_idx)
            if rb_idx > 0:
                entity = entity[:lb_idx] + entity[rb_idx+1:]
        
        # replace underscores with spaces
        return self.underscores_re.sub(' ', entity)
    
    def iter_entity_aliases(self):
        # Include some predefined alias set, e.g. yago-means
        #log.info('Loading aliases: %s ...', self.alias_model_path)
        #alias_model = marshal.load(open(self.alias_model_path,'rb'))
        #log.info('Enumerating aliases for %i entities...' % len(alias_model))
        #for entity, names in alias_model.iteritems():
        #    entity = redirects.get(entity, entity)
        #    for name in names:
        #        yield entity, name
        #alias_model = None

        log.info('Enumerating mappings from canonical titles in entities model...')
        for eid, label, _ in self.entities_model.iter_entities():
            eid = self.redirects.map(eid)
            if self.include_entity(eid):
                title = self.convert_title_to_name(eid)
                yield eid, title
                if title != label:
                    yield eid, label

                ascii_title = unicodedata.normalize('NFKD', label).encode('ascii','ignore')
                if ascii_title != title:
                    yield eid, ascii_title

        log.info('Enumerating redirect titles...')
        for source, target in self.redirects.cache.iteritems():
            if self.include_entity(target):
                yield target, self.convert_title_to_name(source)

        log.info('Enumerating mappings in name probability model...')
        name_model = model.NameProbability(self.name_model_tag)
        for name, entities_iter in name_model.iter_name_entities():
            for eid in entities_iter:
                eid = self.redirects.map(eid)
                if self.include_entity(eid):
                    yield eid, name

    def include_entity(self, entity):
        return entity in self.entity_set

    def __call__(self):
        log.info('Building candidate model...')
        Candidates(self.model_tag).create(self.iter_entity_aliases())
        log.info("Done.")

    @classmethod
    def add_arguments(cls, p):
        p.add_argument('entities_model_tag', metavar='ENTITIES_MODEL_TAG')
        p.add_argument('redirect_model_tag', metavar='REDIRECT_MODEL_TAG')
        p.add_argument('name_model_tag', metavar='NAME_MODEL_TAG')
        p.add_argument('model_tag', metavar='CANDIDATE_MODEL_TAG')
        p.set_defaults(cls=cls)
        return p

class BuildEntityCooccurrenceFromOccurrence(object):
    "Builds model of entity conditional probability from occurrence model."
    def __init__(self, occurrence_model_path, probability_model_path):
        self.occurrence_model_path = occurrence_model_path
        self.out_path = probability_model_path

    def __call__(self):
        log.info('Building entity coocurrence statistics "from entity occurrence model...')
        occurrence_model = EntityOccurrence.read(self.occurrence_model_path)

        log.info('Computing occurrence counts...')
        occurrence_counts = {k:len(e) for k, e in occurrence_model.d.iteritems()}

        log.info('Inverting occurrence model..')
        entities_by_occurrence = defaultdict(set)
        for e, occurrences in occurrence_model.d.iteritems():
            for o in occurrences:
                entities_by_occurrence[o].add(e)

        occurrence_model = None

        log.info('Computing cooccurrence counts over %i pages...' % len(entities_by_occurrence))
        cooccurrence_counts = {}
        for i, loc in enumerate(entities_by_occurrence.keys()):
            entities = entities_by_occurrence[loc]

            if i % 500000 == 0:
                log.info('Processed %i pages... %i pairs', i, len(cooccurrence_counts))
            for a in entities:
                for b in entities:
                    if a != b:
                        if a > b:
                            a, b = b, a
                        if a not in cooccurrence_counts:
                            cooccurrence_counts[a] = {b:1}
                        else:
                            if b not in cooccurrence_counts[a]:
                                cooccurrence_counts[a][b] = 1
                            else:
                                cooccurrence_counts[a][b] += 1

        log.info('Building EntityCooccurrence model...')
        ec = EntityCooccurrence(cooccurrence_counts, occurrence_counts)
        ec.write(self.out_path)

    @classmethod
    def add_arguments(cls, p):
        p.add_argument('occurrence_model_path', metavar='OCCURRENCE_MODEL')
        p.add_argument('probability_model_path', metavar='PROBABILITY_MODEL')
        p.set_defaults(cls=cls)
        return p

class BuildOccurrenceFromLinks(object):
    "Builds link cooccurrence model from outlink model."
    def __init__(self, link_model_path, redirect_model_path, occurrence_model_path):
        self.link_model_path = link_model_path
        self.out_path = occurrence_model_path

        log.info('Loading redirect model: %s ...', redirect_model_path)
        self.redirect_model = marshal.load(open(redirect_model_path, 'rb'))

    def __call__(self):
        log.info('Building entity occurrence model from outlinks...')
        occurrence_model = EntityOccurrence()
        link_model = Links.read(self.link_model_path)

        for page, links in link_model.iteritems():
            for e in links:
                hidx = e.rfind('#')
                if hidx != -1:
                    e = e[:hidx]
                e = self.redirect_model.get(e, e)
                occurrence_model.add(e, page)

        occurrence_model.write(self.out_path)

    @classmethod
    def add_arguments(cls, p):
        p.add_argument('link_model_path', metavar='LINK_MODEL')
        p.add_argument('redirect_model_path', metavar='REDIRECT_MODEL_PATH')
        p.add_argument('occurrence_model_path', metavar='OCCURRENCE_MODEL')
        p.set_defaults(cls=cls)
        return p

class BuildOccurrenceFromMentions(object):
    "Builds link cooccurrence model from entity mention contexts."
    def __init__(self, mention_model_path, occurrence_model_path):
        self.mention_model_path = mention_model_path
        self.out_path = occurrence_model_path

    def __call__(self):
        log.info('Building entity occurrence model from mention contexts...')
        occurence_model = EntityOccurrence()

        mention_iter = EntityMentionContexts.iter_entity_mentions_from_path(self.mention_model_path)
        for i, (e, mentions) in enumerate(mention_iter):
            if i % 250000 == 0: 
                log.debug('Processed %i mentions...' % i)
            for url, _, _, _ in mentions:
                occurence_model.add(e, url)

        occurence_model.write(self.out_path)
        log.info('Done')

    @classmethod
    def add_arguments(cls, p):
        p.add_argument('mention_model_path', metavar='MENTION_MODEL')
        p.add_argument('occurrence_model_path', metavar='OCCURRENCE_MODEL')
        p.set_defaults(cls=cls)
        return p

class FilterTermModel(object):
    "Filter model."
    def __init__(self, inpath, outpath):
        self.in_path = inpath
        self.out_path = outpath

    def __call__(self):
        wv = WordVectors.read('/n/schwa11/data0/linking/erd/full/models/googlenews300.wordvector.model')
        vocab = set(wv.vocab.iterkeys())
        wv = None

        log.debug('Loading term model...')

        term_model = mmdict(self.in_path)

        def iter_filted_terms(eds):
            for i, (e, d) in enumerate(eds):
                if i % 100000 == 0:
                    log.debug('Processed %i entities...' % i)

                yield e, {t:c for t,c in d.iteritems() if t in vocab}

        mmdict.write(self.out_path, iter_filted_terms(term_model.iteritems()))

    @classmethod
    def add_arguments(cls, p):
        p.add_argument('inpath', metavar='INFILE')
        p.add_argument('outpath', metavar='OUTFILE')
        p.set_defaults(cls=cls)
        return p

class BuildIdfsForEntityContext(object):
    "Builds term inverse document frequency model from an entity term frequency model."
    def __init__(self, inpath, outpath):
        self.in_path = inpath
        self.out_path = outpath

    def __call__(self):       
        # todo: fix wv_vocab at module scope

        wv = WordVectors.read('/n/schwa11/data0/linking/models/googlenews300.wordvector.model')
        vocab = set(wv.vocab.iterkeys())
        wv = None

        log.debug('Computing dfs over entity context model...')

        dfs = defaultdict(int)
        entity_count = 0
        for i, d in enumerate(mmdict.static_itervalues(self.in_path)):
            if i % 250000 == 0:
                log.debug("Processed %i entities..." % i)
            for t in d.iterkeys():
                if t in vocab:
                    dfs[t] += 1
            entity_count += 1
        
        def iter_term_idfs():
            for t, df in dfs.iteritems():
                yield (t, math.log(entity_count/df))

        log.debug('Writing idf model: %s' % self.out_path)
        mmdict.write(self.out_path, iter_term_idfs())

    @classmethod
    def add_arguments(cls, p):
        p.add_argument('inpath', metavar='INFILE')
        p.add_argument('outpath', metavar='OUTFILE')
        p.set_defaults(cls=cls)
        return p
