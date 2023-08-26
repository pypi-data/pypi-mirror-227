from _typeshed import Incomplete
from docassemble.base.config import daconfig as daconfig
from docassemble.base.error import DAError as DAError

dbuser: Incomplete
dbpassword: Incomplete
dbhost: Incomplete
dbport: Incomplete
dbprefix: Incomplete
dbname: Incomplete
dbtableprefix: Incomplete
connect_string: str
pool_pre_ping: Incomplete
alchemy_connect_string: str
alchemy_connect_args: Incomplete
ssl_mode: Incomplete
filename: Incomplete
# These are within an if, so they might or might not be present
local_parameter: Incomplete
postgres_parameter: Incomplete

def connection_string(): ...
def alchemy_connection_string(): ...
def connect_args(): ...
