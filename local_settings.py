#"""
#Configuration Settings
#Includes keys for Twilio, etc.  Second stanza intended for Heroku deployment.
#"""

# Uncomment to configure in file.
ACCOUNT_SID = "AC769071c77d687518f99a02229c033113"
AUTH_TOKEN = "4f3a050634d10862a4d814cce9ae99a6"
SONYA_APP_SID = "APcd3bb5ab62875814291adf7ddbc5620b"
#SONYA_CALLER_ID = "+16197291964"
SONYA_CALLER_ID = "+18589223338"

#for reference, my twilio # = "+16692423359"

# Begin Heroku configuration - configured through environment variables.
import os
os.environ['ACCOUNT_SID'] = ACCOUNT_SID
os.environ['AUTH_TOKEN'] = AUTH_TOKEN
os.environ['SONYA_APP_SID'] = SONYA_APP_SID
os.environ['SONYA_CALLER_ID'] = SONYA_CALLER_ID

