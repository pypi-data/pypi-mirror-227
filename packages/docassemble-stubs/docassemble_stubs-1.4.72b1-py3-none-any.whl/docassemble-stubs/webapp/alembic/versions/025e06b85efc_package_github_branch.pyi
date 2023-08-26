from _typeshed import Incomplete
from docassemble.webapp.database import dbtableprefix as dbtableprefix

revision: str
down_revision: str
branch_labels: Incomplete
depends_on: Incomplete

def upgrade() -> None: ...
def downgrade() -> None: ...
