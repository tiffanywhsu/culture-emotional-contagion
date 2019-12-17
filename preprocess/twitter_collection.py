import tweepy
import datetime
import time
import unicodecsv
import jsonpickle
import botometer
import logging

#####################################################################################
## Customize the variables in this box
## Input auth keys

## output:
## txt file of user ids from stream results
## json file of all stream results

country = 'USA' # 'USA' or 'japan'
date = '12.16.19.9pm'
timeelapse = 1      # number of days to collect

# auth keys
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

mashape_key = ""
twitter_app_auth = {
    'consumer_key': '',
    'consumer_secret': '',
    'access_token': '',
    'access_token_secret': ''
    }
######################################################################################

if country == 'USA':
    lang = 'en'
    country_code = 'US'
elif country == 'japan':
    lang = 'ja'
    country_code = 'JP'

logging.basicConfig()


####### STREAMING FOR TWEETS AND USERS ###################################################
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


# error handling
if (not api):
    print ("Problem Connecting to API")


# inherit from the StreamListener object
class MyStreamListener(tweepy.StreamListener):

    # overload the on_status method
    def on_status(self, status):
        try:
            result = bom.check_account(status.user.id)

            # if user fits filter criteria   
            if status.place.country_code == country_code and status.user.lang == lang and status.lang == lang and result['display_scores']['user'] < 1 and status.user.id_str not in existingUsers and status.user.id_str not in usersThisRound:
                print status.user.id
                print "bot result: ", result['display_scores']['user']

                with open(file_statuses_json, 'a') as fs:

                    fs.write(jsonpickle.encode(status._json, unpicklable=False) + '\n')

                with open(file_userids, 'a') as fu:
                    users.add(status.user.id_str)
                    fu.write(status.user.id_str + '\n')
                fu.close()

                return False

            else:
                return True

        # error handling
        except BaseException as e:
            print("Error on_status: %s" % str(e))

        return True

    # error handling
    def on_error(self, status):
        #print(status)
        return True

    # timeout handling
    def on_timeout(self):
        return True


# existing user ID list
existingUsers = []
with open('data/' + country+'_existing_users.txt', 'r') as fexist:
    for line in fexist:
        existingUsers.append(line[:-1])
existingUsers = set(existingUsers)
fexist.close()

# files to save things too
file_users_statuses = 'data/' + country + '_stream_' + date + '_statuses_users.csv'
file_statuses_json = 'data/' + country + '_stream_' + date + '.json'
file_userids = 'data/' + country + '_stream_' + date + '_users.txt'
file_users_friends = 'data/' + country + '_stream_' + date + '_users_friends.txt'
file_friends_statuses = 'data/' + country + '_stream_' + date + '_statuses_friends.csv'
file_header = 'data/' + country + '_stream_' + date + '_statuses_header.csv'

with open(file_users_statuses, 'a') as f:
    f.write('userid,message,updated_time\n')
f.close()
with open(file_friends_statuses, 'a') as f:
    f.write('friendid,userid,message,updated_time\n')
f.close()
with open(file_header, 'w') as f:
    f.write('sub,total_friends,used_friends\n')
f.close()

# getting Geo ID
places = api.geo_search(query=country, granularity='country')
coordinates = places[0].bounding_box.coordinates
geocoord = [coordinates[0][0][0], coordinates[0][0][1], coordinates[0][2][0], coordinates[0][2][1]]
print geocoord

usersThisRound = set([])

starttime = datetime.datetime.now()

# collection
usernum = 0
while (datetime.datetime.now()-starttime).days < timeelapse:
    print usernum

    ## STREAM USER
    users = set([])
    # connecting to the twitter streaming API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # error handling
    if (not api):
        print ("Problem Connecting to API")

    # create a stream object
    twitter_stream = tweepy.Stream(auth, MyStreamListener())
    # create bot check object
    bom = botometer.Botometer(wait_on_ratelimit=True, mashape_key=mashape_key,**twitter_app_auth)
    # collect user
    twitter_stream.filter(locations=geocoord)

    user = list(users)[0]
    print 'userid: ', user

    userAccessible = 1

    ## GET FRIENDS
    # use AppAuth
    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    print 'getting friends...'
    friends = []

    while True:
        try:
            for item in tweepy.Cursor(api.friends_ids, user_id=user).items():
                friends.append(item)
            print 'number of friends: ', len(friends)
            break
        except tweepy.RateLimitError:
            print('sleep 15 minutes')
            time.sleep(900)
            continue
        except tweepy.TweepError as e:
            print('At sub %s, TweepError %s' % (str(user), e.reason))
            if e.reason == 'Twitter error response: status code = 429':
                print('sleep 15 minutes')
                time.sleep(900)
            elif 'Failed to send request: HTTPSConnectionPool' in e.reason:
                print ('sleep 10 seconds')
                time.sleep(10)
            continue

    ## GET STATUSES
    print 'getting user statuses...'
    while True:
        try:
            with open(file_users_statuses, 'a') as f:
                writer = unicodecsv.writer(f, encoding='utf-8')
                print 'user status user: ', user
                for status in api.user_timeline(user_id=user, include_rts=False, trim_user=True, count=200):
                    row = []
                    if status.lang == lang:
                        row.append(user)
                        row.append(status.text)
                        row.append(status.created_at)
                        writer.writerow(row)
            f.close()
            break
        except tweepy.RateLimitError:
            print('sleep 8 minutes')
            time.sleep(480)
            continue
        except tweepy.TweepError as e:
            print('At sub %s, TweepError %s ' % (str(sub), e.reason))
            if e.message == 'Over capacity':
                print('sleep 8 minutes')
                time.sleep(480)
            elif e.reason == 'Twitter error response: status code = 429':
                print('sleep 8 minutes')
                time.sleep(480)
            elif 'Failed to send request: HTTPSConnectionPool' in e.reason:
                print ('sleep 10 seconds')
                time.sleep(10)
            else:
                print ('user inaccessible')
                userAccessible = 0
            continue

    if not userAccessible:
        continue


    ## GET FRIENDS STATUSES
    print 'getting friends statuses...'
    i = 0
    numInaccessible = 0
    while i < len(friends):
        print i
        sub = friends[i]
        try:
            with open(file_friends_statuses, 'a') as f:
                writer = unicodecsv.writer(f, encoding='utf-8')
                for status in api.user_timeline(user_id=sub, trim_user=True, exclude_replies=True, count=200):
                    # for status in tweepy.Cursor(api.user_timeline, user_id=sub, exclude_replies=True, trim_user=True).items(100):
                    row = []
                    if status.lang == lang:
                        # if status.is_quote_status:
                        #     if hasattr(status, 'quoted_states'):
                        #         print status.text + status.quoted_status.text
                        #         statuslist.append(status.text + status.quoted_status.text)
                        # else:
                        row.append(sub)
                        row.append(user)
                        row.append(status.text)
                        row.append(status.created_at)
                        writer.writerow(row)
            i += 1

        except tweepy.RateLimitError:
            print('sleep 8 minutes')
            time.sleep(480)
            continue
        except tweepy.TweepError as e:
            print('At sub %s, TweepError %s' % (str(sub), e.reason))
            if e.reason == 'Twitter error response: status code = 429':
                print('sleep 8 minutes')
                time.sleep(480)
            elif 'Failed to send request: HTTPSConnectionPool' in e.reason:
                print ('sleep 10 seconds')
                time.sleep(10)
            else:
                numInaccessible += 1
                i += 1
            continue

    print "write to header..."
    with open(file_header, 'a') as hf:
        hf.write(str(sub) + ',' + str(len(friends)) + ',' + str(len(friends)-numInaccessible) + '\n')

    # write to friends
    with open(file_users_friends, 'a') as outf:
        for friend in friends:
            outf.write(str(user) + ' ' + str(friend) + '\n')
    outf.close()

    usersThisRound.add(user)
    print 'user finished', usernum
    usernum += 1

# save user to existing users
with open('data/' + country+'_existing_users.txt', 'a') as fexist:
    with open(file_userids, 'r') as fu:    
        for line in fu:
            fexist.write(line)
    fu.close()
fexist.close()

