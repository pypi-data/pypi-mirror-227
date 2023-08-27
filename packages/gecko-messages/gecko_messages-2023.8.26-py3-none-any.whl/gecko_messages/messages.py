
from collections import namedtuple

date_t = namedtuple("date_t","year month day")
clock_time_t = namedtuple("clock_time_t","hour minute seconds")
vec_t = namedtuple("vec_t", "x y z")
quat_t = namedtuple("quat_t", "w x y z")
gps_t = namedtuple("gps_t", "lat lon altitude hdop satellites fix date time") # 4f2B3B3B
msg_t = namedtuple("msg_t", "a g m q gps temperature pressure timestamp")