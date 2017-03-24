from PIL import Image
import re
from requests import Session
import base64

# Get QR Code Image from root-me

#
# # KALI PROXY
#
# proxies = {
#   'http': 'http://192.168.188.157:8080',
#   'https': 'https://192.168.188.157:8080',
# }
#

# Challenge URL
url = "http://challenge01.root-me.org/programmation/ch7/"

# Regex declaration
regex=".*image/png;base64,(?P<image>.*)\" /><br/>.*"
p = re.compile(regex)
flagRegex=".*Congratz, le flag est (?P<flag>.*)</p></p>.*"
p3 = re.compile(flagRegex)
regexApiQRCODE=".*\n.*\n.*\n.*The key is (?P<flag>.*)</pre>.*"
p4 = re.compile(regexApiQRCODE)


# HTTP session
s = Session()

# GET Method
r = s.get(url, stream=True)

# Save cookie to injeect in the response
c = r.cookies

# Save the response to the GET request
response = r.content

# Grab b64 img in the response
m = p.match(response)
# print "b64 img:" + m.group("image")
qrcodeChall = m.group("image")

# Convert b64 image to png file
qrcodeImg = open('qrcode.png', 'wb')
qrcodeImg.write(base64.decodestring(qrcodeChall))
qrcodeImg.close()


# Merge qrcode with base QRCode
baseQR = Image.open('baseqr.png')
baseQR = baseQR.convert("RGBA")

challQR = Image.open('qrcode.png')
challQR = challQR.convert("RGBA")
final = Image.blend(challQR,baseQR,0.5).convert("L")
final = final.point(lambda x: 0 if x<200 else 255, '1')
final.save('final.png')
width, height = final.size


# API QRCODE decoder
urlApiQRCODE = "https://zxing.org/w/decode"
files = {'file': open('final.png', 'rb')}

# Open HTTP session
sAPI = Session()

# With or without proxie POST request
# rAPI = sAPI.post(urlApiQRCODE,files=files,proxies=proxies,verify=False)
rAPI = sAPI.post(urlApiQRCODE,files=files)

# Parse flag in the HTTP response
flag = p4.match(rAPI.content).group("flag")
print "response: " + flag

r = s.post(url, cookies=c, verify=False, data={'metu': flag})

if p3.match(r.content):
    print "Flag: " + p3.match(r.content).group("flag")
else :
    print "try again"
    print r.content
