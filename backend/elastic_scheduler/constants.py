from datetime import timedelta

ISOFORMAT_STRLEN = 40
SCHEDULING_WINDOW = timedelta(weeks=3)

FIFTEEN_MINUTES = timedelta(minutes=15)

BIT_SPLITTABLE = 1 << 0
BIT_OVERLAPPABLE = 1 << 1
BIT_INVISIBLE = 1 << 2
