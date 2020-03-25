from posting.models import Video
from django.contrib.auth.models import User
from .trie import Trie


common_trie = Trie()
COMMON_WORDS = ['a', 'the', 'an', 'as', 'at', 'if', 'are', 'and', 'am', 'be', 'by', 'was', 'I']

for word in COMMON_WORDS:
    common_trie.insert(word)

class MatchedVideo(object):
    
    def __init__(self, score, video):
        self._video = video
        self._score = score
    
    def __lt__(self, other):
        return self._score < other._score

    def __gt__(self, other):
        return self._score > other._score

    def __eq__(self, other):
        return self._score == other._score

    def getVideo(self):
        return self._video

def _wordScore(query, trie):
    score = 0.0
    for word in query:
        found, searchScore = trie.search(word)
        if found:
            isCommon, _ = common_trie.search(word)
            if isCommon:
                score += searchScore
            else:
                score += 2.0 * searchScore
        else:
            score = searchScore


    return score

 

def search_videos(search_query, class_choice):
    if class_choice == 'All':
        videolist = Video.objects.all()
    else:
        videolist = Video.objects.filter(class_choice=class_choice)

    word_query = search_query.lower().split()

    finalList = []
    for video in videolist:
        score = 0.0
        titleTrie = Trie()
        descTrie = Trie()
        title_words = video.title.lower().split()
        desc_words = video.description.lower().split()

        for word in title_words:
            titleTrie.insert(word)
        for word in desc_words:
            descTrie.insert(word)

        score += _wordScore(word_query, titleTrie) * 2.0
        score += _wordScore(word_query, descTrie)

        finalList.append(MatchedVideo(score, video))

    finalList.sort(reverse=True)
    returnList = []
    for vidObj in finalList:
        returnList.append(vidObj.getVideo())
    return returnList







