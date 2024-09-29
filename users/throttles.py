from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class TestThrottle(AnonRateThrottle):
    rate = '5/day'