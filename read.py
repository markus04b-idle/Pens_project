from sqlmodel import Session, select
from models import engine, Bio
import pandas as pd

with Session(engine) as session:
    # `Bio` is an alias for `Roster`; select fields that exist in the model
    statement = select(Bio.player, Bio.pos)
    records = session.exec(statement).all()

records_df = pd.DataFrame(records, columns=["player", "pos"])
print(records_df)