import time
import json
import smtplib, ssl
from os.path import exists
from selenium import webdriver
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium.webdriver.common.by import By

def get_data(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)
    elements1 = driver.find_elements(By.CLASS_NAME, 't1jojoys.dir.dir-ltr')
    elements2 = driver.find_elements(By.CLASS_NAME, 'cy5jw6o.dir.dir-ltr a')

    titles = []
    links = []
    listing_ids = []
    for e1, e2 in zip(elements1, elements2):
        titles.append(e1.text)
        links.append(e2.get_attribute('href'))
        listing_ids.append(e2.get_attribute('target'))
    return titles, links, listing_ids

def difference(new_titles, old_titles):
    diff = [i for i in new_titles if i not in old_titles]
    return diff

def send_email(title, body_data):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = ""
    receiver_email = ""
    password = ""
    subject = title
    body = body_data[0]
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    # Add body to email
    message.attach(MIMEText(body, "plain", "utf-8"))
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    print('email has been sent')

    # Save titles to a json file
def store_titles(titles):
    with open('titles.json', 'w') as f:
        json.dump(titles, f)
    print("titles saved to json")

def store_links(links):
    with open('links.json', 'w') as f:
        json.dump(links, f)
    print("links saved to json")

def store_listing_ids(listing_ids):
    with open('listing_ids.json', 'w') as f:
        json.dump(listing_ids, f)
    print("listing_ids saved to json")

def runit(url):
    data = get_data(url)
    new_titles = list(data.keys())
    new_urls = list(data.values())
    with open('titles.json', 'r') as f:
        old_titles = json.load(f)
    diff_titles = difference(new_titles, old_titles)
    #if diff_titles:
        #for title in diff_titles:
            #send_email(title, data[title])
    store_titles(new_titles)

city = 'Columbia'
state = 'Missouri'
country = 'United-States'
nights = 1
guest_count = 2
url = f"https://www.airbnb.com/s/{city}--{state}--{country}/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&price_filter_input_type=2&price_filter_num_nights={nights}&channel=EXPLORE&date_picker_type=calendar&query=Columbia%2C%20MO&place_id=ChIJyYKBu_Or3IcRIG-9ui1pEaA&checkin=2023-03-31&checkout=2023-04-01&adults=2&source=structured_search_input_header&search_type=filter_change&pagination_search=true&price_min=10&price_max=86"

#if exists('titles.json'):
    #runit(url)
#else:
data = get_data(url)
titles = data[0]
links = data[1]
listing_ids = data[2]
store_titles(titles)
store_links(links)
store_listing_ids(listing_ids)


#send_email("test", titles)