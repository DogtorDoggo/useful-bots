import praw
from pprint import pprint

bot_id = ''


def main():
    # info of the account that you want to delete messages from, not of bot account
    reddit = praw.Reddit(client_id='',
                         client_secret='',
                         user_agent='whatever user agent',
                         username='',
                         password='')

    messages = reddit.inbox.messages(limit=None)
    # print(sum(1 for x in messages))
    count = 0
    for message in messages:
        print("Checking: " + message.id)
        if message.author.name == bot_id:
            print("sender id: " + message.author.name)
            message.delete()
            print("https://www.reddit.com/message/messages/" + message.id + " deleted.\n")
            count += 1
        # print(message.title)
    print(str(count) + " messages from " + bot_id + " deleted.")


if __name__ == "__main__":
    main()
