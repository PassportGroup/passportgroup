from enum import Enum


class TimeInterval(Enum):
    one_minute = '1 min'
    five_minutes = '5 mins'
    ten_minutes = '10 mins'
    fifteen_minutes = '15 mins'
    twenty_minutes = '20 mins'
    twenty_five_minutes = '25 mins'
    thirty_minutes = '30 mins'
    forty_five_minutes = '45 mins'
    one_hour = '1 hour'
    two_hours = '2 hours'
    three_hours = '3 hours'
    five_hours = '5 hours'
    six_hours = '6 hours'
    twelve_hours = '12 hours'
    twenty_four_hours = '24 hours'


class PassportTaskStatus(Enum):
    active = 'Active'
    disabled = 'Disabled'
