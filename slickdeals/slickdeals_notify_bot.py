import requests
from bs4 import BeautifulSoup
import smtplib
import time
from datetime import datetime

base_url = "https://www.slickdeals.net/"
prefix = "https://slickdeals.net/newsearch.php?q="
suffix = "&pp=20&sort=newest&forumid%5B%5D=71&forumid%5B%5D=30&forumid%5B%5D=9&forumid%5B%5D=54&forumid%5B%5D=25&forumid%5B%5D=53&forumid%5B%5D=4&forumid%5B%5D=44&forumid%5B%5D=39&forumid%5B%5D=10&forumid%5B%5D=38&vote=6&forumchoice%5B%5D=9&forumchoice%5B%5D=41&forumchoice%5B%5D=44&forumchoice%5B%5D=4&forumchoice%5B%5D=39&forumchoice%5B%5D=54&forumchoice%5B%5D=10&forumchoice%5B%5D=25&forumchoice%5B%5D=38&forumchoice%5B%5D=53&forumchoice%5B%5D=30&forumchoice%5B%5D=71&r=1&rating="
checked = []
gmail_user = '@gmail.com' # your bot sent_from email
gmail_password = 'abcabcxyz' # your bot sen_from email password
sent_from = gmail_user
sent_to = ['target_email@gmail.com'] # sent_to email

minimum_rating = 3 # at least rating of 3
# keywords_list = ["amazon", "staples"]


def check_keywords(keywords):
    search_part = '+'.join(keywords.strip().split())
    url = ''.join([prefix, search_part, suffix, str(minimum_rating)])
    print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    z = soup.find_all("div", class_="dealWrapper")
    first_element = z[0]
    if first_element.find("div", class_="dealBadge expired") is not None: # expired
        print("Latest deal expired, skipping.")
        return
    deal_title_tag = first_element.find("a", class_="dealTitle bp-c-link")
    link = deal_title_tag["href"]
    deal_id_start_index = link.find("/f/") + 3
    deal_id = link[deal_id_start_index: deal_id_start_index + 8]
    title = deal_title_tag.getText()
    print(deal_id)
    if deal_id not in checked:
        send_mail(keywords, title, link)
        checked.append(deal_id)


def send_mail(keywords, title, link):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_password)
        msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % (sent_from, ",".join(sent_to), "Slideals new deal found matching keyowrd(s): " + keywords, str(datetime.now()), title + "\n\n" + base_url + link)
        server.sendmail(sent_from, sent_to, msg)
        server.close()
        print("New deal found, email sent.")
    except:
        print('Something went wrong sending email')

def main():
    while True:  # recover on exception
        while True:
            try:
                with open("keywords.txt", "r") as f:
                    lines = f.read().splitlines()
                f.close()
                for keywords in lines:
                    print("Start checking keyword(s): " + keywords)
                    check_keywords(keywords)
                    time.sleep(10)
                time.sleep(30)
            except:
                continue
            break

if __name__ == "__main__":
    main()
