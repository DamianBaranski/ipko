# iPKO python library


This simple python library can be use to connect to ipko.pl site.

In this version you can only get account number and history.

Example:
```python
from ipko import PKO
data = PKO()
data.login('login','password')
print(data.account)      #print account number
print(data.getHistory()) #print history
```

Author: Damian Barański

# iPKO biblioteka python

Ta biblioteka pozwala na połaczenie się ze stroną ipko.pl

W aktualnej wersji pozwala pobrać numer konta oraz historię.

Przykład użycia:
```python
from ipko import PKO
data = PKO()
data.login('login','password')
print(data.account)      #print account number
print(data.getHistory()) #print history
```

Autor: Damian Barański

