from rest_framework.throttling import AnonRateThrottle

class ContactRateThrottle(AnonRateThrottle):
    scope = 'contacts'
