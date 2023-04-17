import sqlalchemy as db



engine = db.create_engine("sqlite://test.db")
connection = engine.connect()
metadata = db.MetaData()
node = db.Table(Nodes, metadata,
    db.Column(id, db.Integer, primary_key=True),
    db.Column(id, db.String,primary_key=True),
    db.Column(id, db.Integer, primary_key=True),
    db.Column(id, db.Integer, primary_key=True),
    db.Column(id, db.Integer, primary_key=True),
    db.Column(id, db.Integer, primary_key=True)


)
