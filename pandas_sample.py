import pandas as pd

import pandas as pd
test = pd.read_csv('input.csv', names=['COLUMN1','COLUMN2'])
for i, row in test.iterrows():
    c1 = row['COLUMN1']
    c2 = row['COLUMN2']
    f = open(c1+'.xml', "a")
    f.write(c2)
    f.close()
