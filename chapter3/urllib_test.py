import urllib.request
import urllib.parse

url = 'https://bbs.ngacn.cc'
resp_nga = urllib.request.urlopen(url)

print(resp_nga.status)
print(resp_nga.getheaders())
print(resp_nga.getheader('Content-Type'))

