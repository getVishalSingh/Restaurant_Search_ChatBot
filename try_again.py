import smtplib
def run():
        #loc = tracker.get_slot('emailid')
        gmail_user = 'restchatbot007@gmail.com'
        gmail_password = 'Chat@P@ssw0rd1'
        sent_from = gmail_user
        to = ['getvishalsingh.007@gmail.com']
        SUBJECT = "Top 10 restaurant list"
        message = "Test"
        TEXT = 'Hey what'
        message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.sendmail(sent_from, to,message)
            server.close()
            print('Email sent!')
        except:
            print('Something went wrong...')
run()