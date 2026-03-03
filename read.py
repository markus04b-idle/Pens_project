from sqlmodel import Session, select
from models import engine, Bio
import pandas as pd

with Session(engine) as session:
    statement = select(Bio.player, Bio.pos)
    records = session.exec(statement).all()

records_df = pd.DataFrame(records, columns=["player", "pos"])
print(records_df)


# another example:

# with Session(engine) as session:
#     statement = (
#         select(Bio.first_name, Bio.last_name, Bio.position)
#         .order_by(Bio.position, Bio.last_name)
#     )
#     records = session.exec(statement).all()
    
# records_df = pd.DataFrame(records, columns=["first_name", "last_name", "position"])
# print(records_df)