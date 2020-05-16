from urllib.parse import quote_plus
import praw

checked = []

sendToRedditor = "sent_to_redditor_id" # who you wawnt to send the alert 
reddit = praw.Reddit(client_id='client_id',
                     client_secret='client_secret',
                     user_agent='whatever user agent you put here',
                     username='reddit_id',
                     password='reddit_password')


# e.g. new_post_alert_with_keywords("politics", "Hillary", "trump", "biden"), keyworsd are of logical OR relationship
# to only match an exclusive_keyword, we can use like new_post_alert_with_keywords("politics", "exclusive_keyword", "")

def new_post_alert_with_keywords_or(subreddit_name, exclusive_keyword, *keywords):
    for submission in reddit.subreddit(subreddit_name).new(limit=1):
        if submission.id not in checked and exclusive_keyword.lower() not in submission.title.lower():
            keyword_match_flag = False
            for keyword in keywords:
                if keyword.lower() in submission.title.lower():
                    keyword_match_flag = True
                    break
            if keyword_match_flag == True:
                # title length limit is 100
                title = "New post matching \"" + "|".join(keywords) + "\" and excluding \"" + exclusive_keyword + "\" found at " + subreddit_name
                text = submission.title \
                       + "\n\nLink:\n\n" + submission.permalink \
                       + "\n\nExternal URL:\n\n" + submission.url \
                       + "\n\nSubreddit URL:\n\n" + reddit.subreddit(subreddit_name).url + "new"
                reddit.redditor(sendToRedditor).message(title, text)
                checked.append(submission.id)
                print("Found new r/" + subreddit_name + " post matching: " + "/".join(keywords))


def new_post_alert_with_keywords_and(subreddit_name, exclusive_keyword, *keywords):
    for submission in reddit.subreddit(subreddit_name).new(limit=1):
        if submission.id not in checked and exclusive_keyword.lower() not in submission.title.lower():
            keyword_match_flag = True
            for keyword in keywords:
                if keyword.lower() not in submission.title.lower():
                    keyword_match_flag = False
                    break
            if keyword_match_flag == True:
                # title length limit is 100
                title = "New post matching \"" + " & ".join(keywords) + "\" and excluding \"" + exclusive_keyword + "\" found at " + subreddit_name
                # text = submission.title + "\n\nLink:\n\n" + submission.permalink + "\n\nExternal URL:\n\n" + submission.url
                text = submission.title \
                       + "\n\nLink:\n\n" + submission.permalink \
                       + "\n\nExternal URL:\n\n" + submission.url \
                       + "\n\nSubreddit URL:\n\n" + reddit.subreddit(subreddit_name).url + "new"
                reddit.redditor(sendToRedditor).message(title, text)
                checked.append(submission.id)
                print("Found new r/" + subreddit_name + " post matching: " + "/".join(keywords))


def main():
    global reddit

    while True: # repeat on exception
        while True:
            try:
                new_post_alert_with_keywords_or("politics", "exclusive_keyword", "") # any new posts from r/politics
                new_post_alert_with_keywords_or("pics", "cat", "dog", "horse") # new posts from r/pics including dog or horse but NOT cat
                new_post_alert_with_keywords_and("GameDeals", "exclusive_keyword", "steam", "free") # new posts from r/gamedeals including steam and free
                new_post_alert_with_keywords_and("GameDeals", "exclusive_keyword", "epic", "free")# new posts from r/gamedeals including epic and free
            except:
                continue
            break


if __name__ == "__main__":
    main()
