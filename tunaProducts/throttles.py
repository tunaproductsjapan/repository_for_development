from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class LoginThrottle(AnonRateThrottle):
    rate = '10/hour'

class RefreshThrottle(UserRateThrottle):
    rate = '50/day'