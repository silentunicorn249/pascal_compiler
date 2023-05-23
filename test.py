import re
sub = 'nested_ifelse_Checking'
if re.match("^[a-zA-Z][a-zA-Z0-9]|_*$", sub):
    print('success')
else:
    print('fail')