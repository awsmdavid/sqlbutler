from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import Q
from collections import defaultdict, OrderedDict
from blog.models import essayData, word
import string
import operator
import codecs
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
# for lookup
import urllib
import re

#for counter
from operator import itemgetter
from heapq import nlargest
from itertools import repeat, ifilter

class Counter(dict):
    def __init__(self, iterable=None, **kwds): 
        self.update(iterable, **kwds)

    def __missing__(self, key):
        return 0

    def most_common(self, n=None):     
        if n is None:
            return sorted(self.iteritems(), key=itemgetter(1), reverse=True)
        return nlargest(n, self.iteritems(), key=itemgetter(1))

    def elements(self):
        for elem, count in self.iteritems():
            for _ in repeat(None, count):
                yield elem

    # Override dict methods where the meaning changes for Counter objects.

    @classmethod
    def fromkeys(cls, iterable, v=None):
        raise NotImplementedError(
            'Counter.fromkeys() is undefined.  Use Counter(iterable) instead.')

    def update(self, iterable=None, **kwds):    
        if iterable is not None:
            if hasattr(iterable, 'iteritems'):
                if self:
                    self_get = self.get
                    for elem, count in iterable.iteritems():
                        self[elem] = self_get(elem, 0) + count
                else:
                    dict.update(self, iterable) # fast path when counter is empty
            else:
                self_get = self.get
                for elem in iterable:
                    self[elem] = self_get(elem, 0) + 1
        if kwds:
            self.update(kwds)

    def copy(self):
        return Counter(self)

    def __delitem__(self, elem):
        if elem in self:
            dict.__delitem__(self, elem)

    def __repr__(self):
        if not self:
            return '%s()' % self.__class__.__name__
        items = ', '.join(map('%r: %r'.__mod__, self.most_common()))
        return '%s({%s})' % (self.__class__.__name__, items)

    def __add__(self, other):
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter()
        for elem in set(self) | set(other):
            newcount = self[elem] + other[elem]
            if newcount > 0:
                result[elem] = newcount
        return result

    def __sub__(self, other):
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter()
        for elem in set(self) | set(other):
            newcount = self[elem] - other[elem]
            if newcount > 0:
                result[elem] = newcount
        return result

    def __or__(self, other):
        if not isinstance(other, Counter):
            return NotImplemented
        _max = max
        result = Counter()
        for elem in set(self) | set(other):
            newcount = _max(self[elem], other[elem])
            if newcount > 0:
                result[elem] = newcount
        return result

    def __and__(self, other):
        if not isinstance(other, Counter):
            return NotImplemented
        _min = min
        result = Counter()
        if len(self) < len(other):
            self, other = other, self
        for elem in ifilter(self.__contains__, other):
            newcount = _min(self[elem], other[elem])
            if newcount > 0:
                result[elem] = newcount
        return result


if __name__ == '__main__':
    import doctest
    print doctest.testmod()



articles = ["a", "the", "an"]
common_words = ["i", "you", "he", "she", "it", "they", "is", "and", "to", "we", "of", "that", "with", "in"]


#TODO: figure out if word is noun or verb
def lookup(word):
    http_request = urllib.urlopen("http://www.dictionaryapi.com/api/v1/references/thesaurus/xml/"+word+"?key=849aa01b-8361-4b26-a618-8c42bfeb0f74")
    xml = http_request.read()
    #blindly take first entry, regardless of meaning
    try:
        definition = re.split('<mc>|</mc>',xml)[1]
        synonyms = re.split('<syn>|</syn>',xml)[1]
        part_of_speech = re.split('<fl>|</fl>',xml)[1]
        # loop to find all definitions
        return [part_of_speech, definition, synonyms]
    except:    
        return ["N/A", "N/A", "N/A"]

def index(request):
    return render(request, 'blog/index.html')

# def submit(request):
#     return render(request, 'blog/results.html')

def results(request):
    if request.method == 'POST':
        # cast request essay as string and store
        text = request.POST.get('text')     

        # convert from unicode to text /bytes - prevents crap out from bullets
        text = text.encode('utf-8').strip()

        # strip punctuation
        words_without_punc = text.translate(string.maketrans("",""), string.punctuation)

        # generate iterable of words
        words = words_without_punc.split()

        # list comp to lower case for each word
        all_words = [word.lower() for word in words]

        # count words and generate key value pair
        all_words_count = Counter(all_words)

        # remove articles and common words
        # TODO: remove other words?
        for a in articles:
            del all_words_count[a]

        for a in common_words:
            del all_words_count[a]

        words_and_count_array = all_words_count

        # returns n most common elements in counter, converts counter to dict
        # TODO: be smarter about number of results, ignore ones with count of 1, perhaps if they are not used consecutively
        number_of_results=5
        top_words = words_and_count_array.most_common()[:number_of_results]

        # generate synonyms for word
        new_list = [[(n[0], n[1],lookup(n[0]))] for n in top_words]

        essay_data = essayData(text=text, word_list = words, words_count = all_words_count)
        # top_word = word(word=top_word, count=count_of_top_word)
        return render(request, 'blog/results.html', { 'search_results': essay_data, 'top_words': top_words, 'new_list':new_list})
    return render(request, 'blog/index.html')




def splitText(text):
    return text.split()

def removePunc(text):
    #syntax translate(find text (mapper), text to replace)
    return text.translate(string.maketrans("",""), string.punctuation)

def countWords(list):
    return Counter(list)

def taketextandcount(text):
    return splitText(removePunc(text))



#     #Collect All the words into a list
# for line in response:
#     #print "Line = " , line
#     line_words = line.split()
#     for word in line_words:  # looping each line and extracting words
#         each_word.append(word)

# #for every word collected, in dict same_words
# #if a key exists, such that key == word then increment Mapping Value by 1
# # Else add word as new key with mapped value as 1
# for words in each_word:
#     if words.lower() not in same_words.keys() :
#         same_words[words.lower()]=1
#     else:
#         same_words[words.lower()]=same_words[words.lower()]+1

# for each in same_words.keys():
#     print "word = ",each, ", count = ",same_words[each]