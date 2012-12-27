from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import random
import smtplib
 
# Here's where everybody who's participating goes
giver_dict = {
                     'Riddle number 1'  : 'notrealemail@gmail.com',
                     'Riddle number 2'  : 'notrealemail2@gmail.com'
                     }
riddle_dict = {
                  'Riddle number 1' : 'Riddle text goes here!',
                  'Riddle number 2' : 'Riddle text goes here!',
                  'Riddle number 3' : 'Riddle text goes here!'
                  }

# initialize the master list variable
master_list = ''
 
# This is prepended onto all of the generated emails. It should include all the details about the rules, dates, etc.
standard_email_intro = 'This is an auto-generated email for the REVEALING of your CallFire Secret Santa. If you want to know the identify of your Secret Santa, correctly answer the riddle below.\n\nThe general guidelines are:\n-You will have 3 chances to correctly answer the riddle.\n-Please do not cheat by looking up the answer online. That would be lame.\n\n\n'
 
# Gmail user info for the socalrobosecretsanta account
gmail_user = "notrealemail@gmail.com"
gmail_pwd = "notrealpassword"
 
# Create the directory for output
try:
    os.makedirs('./output')
except OSError:
    pass
 
# Function to send the emails (all sent emails are also stored locally in the ./output folder)
def send_email(to, message):
    # store the local .txt file for each email sent
    print("Writing .txt for " + to)
    email_output = open('./output/' + to + '.txt', 'w')
    email_output.write(message)
    # send the actual email
    print("Sending email to " + to)
    msg = MIMEMultipart()
 
    msg['From'] = gmail_user
    msg['To'] = to
    msg['Subject'] = "Your Secret Santa RIDDLE! Answer correctly to reveal your Santa\'s identity! "
 
    msg.attach(MIMEText(message))
    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pwd)
    mailServer.sendmail(gmail_user, to, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.close()
    return True
 
# Shuffle the giver keys into a random list, then assign pairings based on the order of said list
randomgivers = list(giver_dict.keys())
random.shuffle(randomgivers)
previousgiver = randomgivers[len(randomgivers)-1]
for giver in randomgivers:
    riddle = riddle_dict[previousgiver]
    recipient = previousgiver
    master_list += giver + ' is getting riddle ' + recipient + '\n'
    # This is the line that, once uncommented, will generate and send the secret santa assignments
    send_email(giver_dict[giver], standard_email_intro + '\nYou have been randomly assigned: ' + recipient + '\n\n' + recipient + ': ' + riddle + '\n\nGood luck!')
    previousgiver = giver
 
# Once everything has run it's course, output the master list to ./output
# and send it to nottherealusername@gmail.com
print('Writing master .txt')
master_list_output = open('./output/master_list' + '.txt', 'w')
master_list_output.write(master_list)
send_email(gmail_user, master_list)
print('finished')
