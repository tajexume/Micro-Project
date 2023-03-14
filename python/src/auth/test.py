import requests, pathlib



url = "http://mp3converter.com/login"

payload={}
headers = {
  'Authorization': 'Basic dGFqZXh1bWVAZ21haWwuY29tOnBhc3N3b3JkMTIz'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.headers)
print(response.text)

encoded_jwt = response.text
print(encoded_jwt)

filePath = r"C:\Users\tajex\Downloads\y2mate.com - 10 Second Timer_1080p.mp4"
url2 = "http://mp3converter.com/upload"

headers2 = {
  'Authorization': f"{'Bearer ', response.text}",
  'Content-Type': 'video/mp4'
}

files={'files': open(filePath,'rb')}
r=requests.request("POST", url2, files=files, headers=headers2)

print(r.status_code)