import smtplib, imapclient,imaplib, pyzmail, requests, os
from pytube import YouTube
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders
import details # This contains my email and password, I created this module create yours with mYemail and mYpassword has variables 

# Read the email for message from your personal email then extract the youtube url

imapObj = imapclient.IMAPClient("imap.gmail.com", ssl=True)
imapObj.login(details.mYemail, details.mYpassword)
folder = imapObj.select_folder("INBOX", readonly=False)
UIDs = imapObj.search("UNSEEN FROM yourpersonalemail@gmail.com")

imaplib._MAXLINE = 10000000

rawMessages = imapObj.fetch(UIDs, ["BODY[]"])
for a in UIDs:
    message = pyzmail.PyzMessage.factory(rawMessages[a][b"BODY[]"])
    if message.get_subject().lower() == "do task now":
        theUrl = message.text_part.get_payload().decode(message.text_part.charset)

print("Youtube url is",theUrl)

# Download the youtube video

yt = YouTube(theUrl)

availableStreams = yt.streams.filter(progressive=True,type="video")
theStreams = []

theTitle = availableStreams.first().title
print("TITLE:",theTitle)
count = -1
for a in availableStreams:
    count = count + 1
    theStreams.append(a)
    print(theStreams[count].resolution, "and file size is " + str(round(theStreams[count].filesize / 1000000,2)) + "mb")


downloads_dir = "c:\\Users\\user\\desktop\\YT_downloads"

theName = theTitle.split(" ")
theFilename = "_".join(theName) + ".mp4"

os.makedirs(downloads_dir, exist_ok=True)

theVid = availableStreams.first().download(output_path=downloads_dir, filename=theFilename)

print("Your bot: Video has been downloaded",theVid)

# Send the video back to my email

mail_content = """Hello sir,
The downloaded video %s has been attached.
Thank You."""%(theTitle)

theMessage = MIMEMultipart()
theMessage["From"] = details.mYemail
theMessage["To"] = "yourpersonalemail.com"
theMessage["Subject"] = "Downloaded youtube video"

theMessage.attach(MIMEText(mail_content, "plain"))
attach_file_name = theVid
attach_file = open(attach_file_name, "rb")
payload = MIMEApplication(attach_file.read())

payload.add_header('Content-Disposition',
                'attachment; filename="%s"' %(attach_file_name) )
theMessage.attach(payload)

session = smtplib.SMTP_SSL("smtp.gmail.com", 465)
session.ehlo()
session.login(details.mYemail,details.mYpassword)

text = theMessage.as_string()
session.sendmail(details.mYemail, "yourpersonalemail@gmail.com", text)
print("Sent")
session.quit()