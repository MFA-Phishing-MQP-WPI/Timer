FILE = 'temp.csv'
datas = open(FILE, 'r').read().split('\n')
open(FILE, 'w').write(
    ','.join(
        [member for member in datas]
    )
)