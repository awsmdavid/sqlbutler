from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import Q
from collections import Counter, defaultdict, OrderedDict
from blog.models import essayData, word
import string
import operator

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf


articles = ["a", "the", "an"]
common_words = ["i", "you", "he", "she", "it", "they", "is", "and", "to", "we", "of", "that"]

def index(request):
    return render(request, 'blog/index.html')

# def submit(request):
#     return render(request, 'blog/results.html')

def results(request):
    if request.method == 'POST':
        # cast request essay as string and store
        text = str(request.POST.get('text'))
        # strip punctuation
        words_without_punc = text.translate(string.maketrans("",""), string.punctuation)
        # generate iterable of words
        words = words_without_punc.split()

        # list comp to lower case for each word
        all_words = [word.lower() for word in words]

        # count words and generate key value pair
        all_words_count = Counter(all_words)

        # remove articles and common words
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
        synonyms = "thing, that, it, yeah"

        new_list = [[(n[0], n[1],synonyms)] for n in top_words]

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