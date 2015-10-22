import os
import threading
import time
import smtplib
from email.mime.text import MIMEText
'''
Carrier Email to SMS Gateway
*****************************************************************


Alltel [10-digit phone number]@message.alltel.com
Example: 1234567890@message.alltel.com

AT&T (formerly Cingular) [10-digit phone number]@txt.att.net
[10-digit phone number]@mms.att.net (MMS)
[10-digit phone number]@cingularme.com
Example: 1234567890@txt.att.net

Boost Mobile [10-digit phone number]@myboostmobile.com
Example: 1234567890@myboostmobile.com

Nextel (now Sprint Nextel) [10-digit telephone number]@messaging.nextel.com
Example: 1234567890@messaging.nextel.com

Sprint PCS (now Sprint Nextel) [10-digit phone number]@messaging.sprintpcs.com
[10-digit phone number]@pm.sprint.com (MMS)
Example: 1234567890@messaging.sprintpcs.com

T-Mobile [10-digit phone number]@tmomail.net
Example: 1234567890@tmomail.net

US Cellular [10-digit phone number]email.uscc.net (SMS)
[10-digit phone number]@mms.uscc.net (MMS)
Example: 1234567890@email.uscc.net

Verizon [10-digit phone number]@vtext.com
[10-digit phone number]@vzwpix.com (MMS)
Example: 1234567890@vtext.com

Virgin Mobile USA [10-digit phone number]@vmobl.com
Example: 1234567890@vmobl.com

'''

def email(address='leoliu@u.northwestern.edu',content=None,subject=None):

    msg = MIMEText(content)
    if subject is not None:
        msg['Subject']=subject

    msg['From']='leo'
    msg['To'] = address

    # Credentials (if needed)
    username = os.getenv('email_address',None)
    password = os.getenv('email_password',None)

    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(msg['From'], [address], msg.as_string())
    server.quit()

if __name__ == '__main__':
    email(address='2243100552@messaging.sprintpcs.com')
    #check_cass()
