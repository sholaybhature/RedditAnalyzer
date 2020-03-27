import praw
import requests
import requests
import datetime
from collections import Counter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googletrans import Translator
from translate import Translator as trans
translator = Translator()
analyzer = SentimentIntensityAnalyzer()
import spacy

nlp = spacy.load("en_core_web_sm")

user = 'username'
print(f'Username: {user} \n')

url_comment = f'https://api.pushshift.io/reddit/search/comment/?author={user}&size=1000'
url_submission = f'https://api.pushshift.io/reddit/search/submission/?author={user}&size=1000'

def most_frequent(List):
    occurence_count = Counter(List)
    return occurence_count.most_common(1)[0][0]

def sentiment_analyzer_scores(text):

    score = analyzer.polarity_scores(text)
    lb = score['pos']
    lb_neg = score['neg']
    if lb >= 0.80:
        return 'positive'
    else:
        return 'neutral'

def comments():
    json = requests.get(url_comment)
    json_data = json.json()
    objects = json_data['data']
    ls_body = []
    ls_sub = []
    ls_date = []
    ls_score = []
    ls_time = []
    ls_wholesome = []

    for info in objects:
        text_body = info['body']
        text_sub = info['subreddit']
        text_date = info['created_utc']
        text_score = info['score']
        ls_date.append(text_date)
        ls_body.append(text_body)
        ls_sub.append(text_sub)
        ls_score.append(text_score)

    for i in ls_body:
        try:
            if 15 < len(i):
                sentiment = sentiment_analyzer_scores(i)
                if sentiment == 'positive':
                    ls_wholesome.append(i)
                else:
                    None
        except Exception:
            pass

    total_karma_comments = sum(ls_score)
    total_comments = len(ls_body)
    most_common_sub_comments = most_frequent(ls_sub)

    index_most_upvoted = ls_score.index(max(ls_score))

    print(f'Total comments: {total_comments}')
    print(f'Subreddit on which you most commented on: {most_common_sub_comments}')
    if ls_wholesome != []:
        print(f'Your most wholesome comment: {ls_wholesome[0]} \n')

    for i in ls_date:
        time = datetime.datetime.fromtimestamp(i).strftime('%Y-%m-%d')
        ls_time.append(time)

    most_common_time = most_frequent(ls_time)
    print(f'Date you made most comments: {most_common_time} \n')

    ls_location = []
    ls_org = []
    ls_product = []
    ls_person = []
    ls_art = []
    ls_money = []

    for i in ls_body:
        doc = nlp(i)
        for ent in doc.ents:
            if ent.label_ == 'GPE':
                ls_location.append(ent.text.capitalize())
            elif ent.label_ == 'ORG':
                ls_org.append(ent.text.upper())
            elif ent.label_ == 'PRODUCT':
                ls_product.append(ent.text.capitalize())
            elif ent.label_ == 'PERSON':
                ls_person.append(ent.text.capitalize())
            elif ent.label_ == 'WORK_OF_ART':
                ls_art.append(ent.text.capitalize())
            elif ent.label_ == 'MONEY':
                ls_money.append(ent.text.capitalize())
            else:
                None

    if ls_location == []:
        None
    else:
        ls_location_ = most_frequent(ls_location)
        print(f'{user} lives in {ls_location_}?')

    if ls_org == []:
        None
    else:
        ls_org_ = most_frequent(ls_org)
        print(f'{user} studies/works at {ls_org_}?')
    if ls_product == []:
        None
    else:
        ls_product_ = most_frequent(ls_product)
        print(f'{user} knows about {ls_product_}?')
    if ls_person == []:
        None
    else:
        ls_person_ = most_frequent(ls_person)
        print(f'{user} knows about {ls_person_}?')
    if ls_art == []:
        None
    else:
        ls_art_ = most_frequent(ls_art)
        print(f'{user} has read/listened  {ls_art_}?\n')

    if len(ls_money) > 5:
        print(f'{user} knows about Finance.')

def posts():
    json = requests.get(url_submission)
    json_data = json.json()
    objects = json_data['data']
    ls_title = []
    ls_score_posts = []
    ls_num_comments = []
    ls_sub_posts = []

    for info in objects:
        text_title = info['title']
        text_sub_posts = info['subreddit']
        text_score = info['score']
        text_num_comments = info['num_comments']
        ls_title.append(text_title)
        ls_sub_posts.append(text_sub_posts)
        ls_score_posts.append(text_score)
        ls_num_comments.append(text_num_comments)


    most_common_sub_posts = most_frequent(ls_sub_posts)
    total_posts = len(ls_title)
    print(f'Total posts: {total_posts}')
    print(f'Subreddit on which you most posted on: {most_common_sub_posts}')
    index_most_upvoted = ls_num_comments.index(max(ls_num_comments))
    post_num_most_comments = ls_num_comments[index_most_upvoted]
    post_most_comments = ls_title[index_most_upvoted]
    print(f'Your post with most comments ({post_num_most_comments}) : {post_most_comments}.')
    total_karma_posts = sum(ls_score_posts)//2


comments()
posts()
