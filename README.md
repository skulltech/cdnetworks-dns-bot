# cdnetworks-dns-bot
Tool for automagically adding and deleting DNS zone entries in CDNetworks

### Usage
```
usage: cdnetworks.py [-h] {add,delete} filename

positional arguments:
  {add,delete}  If the script should add or delete DNS zone entries
  filename      File name of the input CSV file

optional arguments:
  -h, --help    show this help message and exit
  ```
  
### Columns in the input CSV file  
```
1. Domain name
2. Zone TTL
3. SOA email
4. SOA TTL
5. Serial number
```
