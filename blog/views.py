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
    '''Dict subclass for counting hashable objects.  Sometimes called a bag
    or multiset.  Elements are stored as dictionary keys and their counts
    are stored as dictionary values.

    >>> Counter('zyzygy')
    Counter({'y': 3, 'z': 2, 'g': 1})

    '''

    def __init__(self, iterable=None, **kwds):
        '''Create a new, empty Counter object.  And if given, count elements
        from an input iterable.  Or, initialize the count from another mapping
        of elements to their counts.

        >>> c = Counter()                           # a new, empty counter
        >>> c = Counter('gallahad')                 # a new counter from an iterable
        >>> c = Counter({'a': 4, 'b': 2})           # a new counter from a mapping
        >>> c = Counter(a=4, b=2)                   # a new counter from keyword args

        '''        
        self.update(iterable, **kwds)

    def __missing__(self, key):
        return 0

    def most_common(self, n=None):
        '''List the n most common elements and their counts from the most
        common to the least.  If n is None, then list all element counts.

        >>> Counter('abracadabra').most_common(3)
        [('a', 5), ('r', 2), ('b', 2)]

        '''        
        if n is None:
            return sorted(self.iteritems(), key=itemgetter(1), reverse=True)
        return nlargest(n, self.iteritems(), key=itemgetter(1))

    def elements(self):
        '''Iterator over elements repeating each as many times as its count.

        >>> c = Counter('ABCABC')
        >>> sorted(c.elements())
        ['A', 'A', 'B', 'B', 'C', 'C']

        If an element's count has been set to zero or is a negative number,
        elements() will ignore it.

        '''
        for elem, count in self.iteritems():
            for _ in repeat(None, count):
                yield elem

    # Override dict methods where the meaning changes for Counter objects.

    @classmethod
    def fromkeys(cls, iterable, v=None):
        raise NotImplementedError(
            'Counter.fromkeys() is undefined.  Use Counter(iterable) instead.')

    def update(self, iterable=None, **kwds):
        '''Like dict.update() but add counts instead of replacing them.

        Source can be an iterable, a dictionary, or another Counter instance.

        >>> c = Counter('which')
        >>> c.update('witch')           # add elements from another iterable
        >>> d = Counter('watch')
        >>> c.update(d)                 # add elements from another counter
        >>> c['h']                      # four 'h' in which, witch, and watch
        4

        '''        
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
        'Like dict.copy() but returns a Counter instance instead of a dict.'
        return Counter(self)

    def __delitem__(self, elem):
        'Like dict.__delitem__() but does not raise KeyError for missing values.'
        if elem in self:
            dict.__delitem__(self, elem)

    def __repr__(self):
        if not self:
            return '%s()' % self.__class__.__name__
        items = ', '.join(map('%r: %r'.__mod__, self.most_common()))
        return '%s({%s})' % (self.__class__.__name__, items)

    # Multiset-style mathematical operations discussed in:
    #       Knuth TAOCP Volume II section 4.6.3 exercise 19
    #       and at http://en.wikipedia.org/wiki/Multiset
    #
    # Outputs guaranteed to only include positive counts.
    #
    # To strip negative and zero counts, add-in an empty counter:
    #       c += Counter()

    def __add__(self, other):
        '''Add counts from two counters.

        >>> Counter('abbb') + Counter('bcc')
        Counter({'b': 4, 'c': 2, 'a': 1})


        '''
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter()
        for elem in set(self) | set(other):
            newcount = self[elem] + other[elem]
            if newcount > 0:
                result[elem] = newcount
        return result

    def __sub__(self, other):
        ''' Subtract count, but keep only results with positive counts.

        >>> Counter('abbbc') - Counter('bccd')
        Counter({'b': 2, 'a': 1})

        '''
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter()
        for elem in set(self) | set(other):
            newcount = self[elem] - other[elem]
            if newcount > 0:
                result[elem] = newcount
        return result

    def __or__(self, other):
        '''Union is the maximum of value in either of the input counters.

        >>> Counter('abbb') | Counter('bcc')
        Counter({'b': 3, 'c': 2, 'a': 1})

        '''
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
        ''' Intersection is the minimum of corresponding counts.

        >>> Counter('abbb') & Counter('bcc')
        Counter({'b': 1})

        '''
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
    finally:    
        return ["none", "none", "none"]

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