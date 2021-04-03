"""
`ausers` utilties for tena project.

Generated Manually from Linux terminal
 * NAME: Wendirad Demelash
 * DATE: April 3, 2021
"""
import re

from decouple import config
from twilio.rest import Client


class TwilioVerifyer:
    ACCOUNT_SID = config('ACCOUNT_SID', cast=str)
    AUTH_TOKEN = config('AUTH_TOKEN', cast=str)
    SERVICE_ID = config('SERVICE_ID', cast=str)
    INTERNATIONAL = r'\+2519\d{8}$' # E.16 format phone number
    LOCAL = r'09\d{8}$' # Local phone number 

    def __init__(self):
        """ Initialize verifer using client """
        self.client = Client(self.ACCOUNT_SID, self.AUTH_TOKEN)

    def _number(self, number):
        """ convert number to E.16 format
            It need to be changed b/c twilio require
            E.16 format number. """
        if re.match(self.INTERNATIONAL, number):
            return number
        return f'+251{number.strip('0')}'

    def send_verification(self, number):
        """ Send 5 digit verification code to user when required."""
        verification = self.client.verify \
            .services(self.SERVICE_ID) \
            .verifications \
            .create(to=self._number(number), channel='sms')
        return verification.status

    def verify_code(self, number, code):
        """ verify users verification code based on their number """
        verification_check = self.client.verify \
                           .services(self.SERVICE_ID) \
                           .verification_checks \
                           .create(to=self._number(number), code=code)
        return verification_check.status

twilio_verify = TwilioVerifyer()