import pandas as pd

# Create your Pandas DataFrame
d = {'username': ['Alice', 'Bob', 'Carl'],
     'age': [18, 22, 43],
     'income': [100000, 98000, 111000]}
df = pd.DataFrame(d)

for label, content in df.var().iteritems():
    print(label, content)
    
XD = df.var().to_numpy()

print(XD)