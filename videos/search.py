from .models import Video
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

def search_videos(search_query, class_filters, filters):
    if class_filters == [] or class_filters == '':
        return []
    
    videolist = _filterClasses(class_filters)

    videolist = _filterLearnStyle(videolist, filters[0])
    videolist = _filterTimeLength(videolist, filters[1])

    finalList = []
    videolist = _sortbyRelevance(search_query, videolist, filters[3])
    
    if (filters[2] == 'TimeS'):
        finalList = _sortbyTime(videolist, True)
    elif (filters[2] == 'TimeL'):
        finalList = _sortbyTime(videolist, False)
    elif (filters[2] == 'Approval'):
        finalList = _sortbyApproval(videolist, filters[3])
    elif (filters[2] == 'Views'):
        finalList = _sortbyViews(videolist, filters[3])
    elif (filters[2] == 'Comments'):
        finalList = _sortbyComments(videolist, filters[3])
    else:
        return videolist

    returnList = []
    for vidObj in finalList:
        returnList.append(vidObj.getVideo())
    return returnList

def _filterClasses(class_filters):
    if 'All' in class_filters:
        return Video.objects.all()   
    videolist = []

    for class_ in class_filters:
        videolist += list(filter(lambda video: class_ in video.class_choice and video not in videolist, Video.objects.all()))
    
    return videolist

def _filterLearnStyle(videolist, learn_style):
    if learn_style == [] or learn_style == '': 
        return videolist

    new_video_list = []
    for style in learn_style:
        new_video_list += list(filter(lambda video: video.user.profile.learning_style == style, videolist))

    return new_video_list

def _filterTimeLength(videolist, time_lengths):
    if time_lengths == '' or time_lengths == []:
        return videolist

    if len(time_lengths) == 4:
        return videolist

    new_video_list = []
    if 'short' in time_lengths:
        new_video_list += list(filter(lambda video: video.youtubedata.time_length <= 300, videolist))
    if 'medium' in time_lengths:
        new_video_list += list(filter(lambda video: video.youtubedata.time_length > 300 and video.youtubedata.time_length <= 900, videolist))
    if 'semi-long' in time_lengths:
        new_video_list += list(filter(lambda video: video.youtubedata.time_length > 900 and video.youtubedata.time_length <= 1500, videolist))
    if 'long' in time_lengths:
        new_video_list += list(filter(lambda video: video.youtubedata.time_length > 1500, videolist))

    return new_video_list

def _sortbyViews(videolist, sort_using):
    if sort_using == 'Unitube':
        videolist = list(map(lambda video: MatchedVideo(video.num_views, video), videolist))
    else:
        videolist = list(map(lambda video: MatchedVideo(video.youtubedata.num_views, video), videolist))

    return sorted(videolist, reverse=True)

def _sortbyComments(videolist, sort_using):
    if sort_using == 'Unitube':
        videolist = list(map(lambda video: MatchedVideo(video.commentthread.num_comments, video), videolist))
    else:
        videolist = list(map(lambda video: MatchedVideo(video.youtubedata.num_comments, video), videolist))

    return sorted(videolist, reverse=True)

def _sortbyTime(videolist, shortest):
    videolist = list(map(lambda video: MatchedVideo(video.youtubedata.time_length, video), videolist))
    if shortest:
        return sorted(videolist)
    else:
        return sorted(videolist, reverse=True)

def _sortbyApproval(videolist, sort_using):
    if sort_using == 'Unitube':
        videolist = list(map(lambda video: MatchedVideo(video.avg_rating, video), videolist))
    else:
        videolist = list(map(lambda video: MatchedVideo(video.youtubedata.num_likes - video.youtubedata.num_dislikes, video), videolist))

    return sorted(videolist, reverse=True)

def _sortbyRelevance(search_query, videolist, sort_using):
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

        title_words = video.youtubedata.title.lower().split()
        desc_words = video.youtubedata.description.lower().split()

        score += _wordScore(word_query, titleTrie) * 2.0
        score += _wordScore(word_query, descTrie)
        
        if (score != 0.0):
            finalList.append(MatchedVideo(score, video))
    
    finalList.sort(reverse=True)
    returnList = []
    for vidObj in finalList:
        returnList.append(vidObj.getVideo())
    return returnList







