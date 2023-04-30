from datetime import datetime
last = datetime.strptime("2018-01-31", "%Y-%m-%d").timestamp()
start = datetime.now().timestamp()
print(start - last)