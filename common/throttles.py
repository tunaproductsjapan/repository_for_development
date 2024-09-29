from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class TunaAnnonThrottle(AnonRateThrottle):
    rate = '10/hour'

class TunaUserThrottle(UserRateThrottle):
    rate = '50/day'