from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import random
import smtplib
 
# Here's where everybody who's participating goes
giver_dict = {
                     'RYANN'  : 'notrealemail@gmail.com',
                     'DUDE X' : 'notrealemail2@gmail.com'
                     }
# This is where everyone tells their Secret Santa what they're interested in
interest_dict = {
                  'RYANN' : 'Learning to code, geeky toys from ThinkGeek.com, Sriracha!(Or Sriracha products)',
                  'DUDE X': 'Doing cool stuff, more random stuff, other awesome stuff"
                  }

# initialize the master list variable
master_list = ''
 
# This is prepended onto all of the generated emails. It should include all the details about the rules, dates, etc.
standard_email_intro = 'This is an auto-generated email for the Secret Santa gift exchange!\n\nThe general guidelines are:\n- Approximately $15 gift\n- Make sure to bring your gift to the office by Friday, December 14th. They will be delivered at the Holiday Party. (For those who will not be attending the party, gifts will be given in the office on a date TBD, but near the 15th)\n-Include a gift receipt if possible to allow for exchanges!\n-Lastly, make sure to label your gift with the recipient\'s name!\n\n\n'
 
# Gmail user info for the socalrobosecretsanta account
gmail_user = "email@callfire.com"
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
    msg['Subject'] = "HO HO HO!! It's Your Secret Santa Assignment! Shhhh... "
 
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
    # This links the giver's interests to the pairings
    interest = interest_dict[previousgiver]
    recipient = previousgiver
    master_list += giver + ' is giving to ' + recipient + '\n'
    # This is the line that, once uncommented, will generate and send the secret santa assignments
    send_email(giver_dict[giver], standard_email_intro + 'You should be: ' + giver + '\nYou are giving to: ' + recipient + '\n\n' + recipient + '\'S HINTS: ' + interest + '\n\nSee you at the gift exchange!')
    previousgiver = giver
 
# Once everything has run it's course, output the master list to ./output
# and send it to nottherealusername@gmail.com
print('Writing master .txt')
master_list_output = open('./output/master_list' + '.txt', 'w')
master_list_output.write(master_list)
send_email(gmail_user, master_list)
print('finished')
