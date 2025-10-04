from dateutil.parser import parse
datatype : str = ''
valu = '40'
tval = valu.count('.')
dswitch : bool = False
if tval == 0:
    try:
        f = int(valu)
    except:
        f = valu
    if isinstance(valu, int):
        datatype = 'Number'
    else:
        try:
            parse(valu, fuzzy=False)
            dswitch = True
        except ValueError:
            dswitch = False

        if dswitch == True:
            datatype = 'Date'
        else:
            datatype = 'Text'
elif tval == 1:
    bust = valu.split('.')
    if bust[0].isnumeric() and bust[1].isnumeric():
        f = float(valu)
        if len(bust[1]) == 2:
            datatype = 'Currency'
        else:
            datatype = 'Decimal'
    elif isinstance(bust[1], str) == True: 
        f = str(valu)
        datatype = 'Text'


print(datatype)