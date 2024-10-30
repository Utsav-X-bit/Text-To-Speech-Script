import requests
import json
import time 
import pygame
import os
import sys
Mail = "sifike6650@ofionk.com"
Pass = "asHKasdhk@jhd1"
def get_auth_token():
    global auth_token
    url0 = 'https://api.voice-gen.ai/v1/signin'
    data = {"email":Mail,"password":Pass}
    headers = {
    "accept": "application/json",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "content-length": "61",
    "content-type": "application/json",
    "origin": "https://app.voice-gen.ai",
    "priority": "u=1, i",
    "referer": "https://app.voice-gen.ai/",
    "sec-ch-ua": '"Not)A;Brand";v="99", "Opera GX";v="113", "Chromium";v="127"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 OPR/113.0.0.0"
    }

    response = requests.post(url0,headers=headers, json=data)

    if response.status_code == 200: 
        response_data = response.json()
        auth_token = response_data.get('AccessToken')
        print(auth_token)
    else:
        print(f"Failed with status code: {response.status_code}")
        print(response.text)




def text_to_speech(text):
    global code_ref
    get_auth_token()
    url1 = 'https://api.voice-gen.ai/v1/conversion/text'
    data = {
        "title": "Ai-Speech",
        "text": text,
        "voice": 3756,
        "speed": 1,
        "output": "mp3",
        "is_clone": False
    }

    headers = {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "authorization": 'Bearer '+auth_token,  
        "content-length": "59677",
        "content-type": "application/json",
        "origin": "https://app.voice-gen.ai",
        "priority": "u=1, i",
        "referer": "https://app.voice-gen.ai/",
        "sec-ch-ua": '"Not)A;Brand";v="99", "Opera GX";v="113", "Chromium";v="127"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 OPR/113.0.0.0"
    }


    response = requests.post(url1,headers=headers, json=data)

    if response.status_code == 200:
        print(response.text) 
        response_data = response.json()
        code_ref = response_data.get('code_ref')
        print(code_ref)
    else:
        print(f"Failed with status code: {response.status_code}")
        print(response.text)
    os.system('cls')
    print("Generating Speech.....")
    def status_call():
        global status 
        url2 = "https://api.voice-gen.ai/v1/conversion/"+code_ref
        response = requests.get(url2,headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            status = response_data.get('status')
            status_chk()
        else:
            print(f"Failed with status code: {response.status_code}")
            print(response.text)    



    def status_chk():
        if status == 'completed' :
                url3 = "https://api.voice-gen.ai/v1/library"
                response = requests.get(url3,headers=headers)
                if response.status_code == 200:
                    response_data = response.json()
                    url_file = None
                    for item in response_data:
                        if item.get("code_ref") == code_ref:
                            url_file = item.get("url_file")
                            break
                    if url_file:
                        print("URL File:", url_file)
                        response = requests.get(url_file)
                        if response.status_code == 200:
                            with open('./speech/'+code_ref+".mp3", "wb") as file:
                                file.write(response.content)
                            print("Audio file downloaded successfully.")
                            os.system('cls')

                        else:
                            print(f"Failed to download the Respose file. Status code: {response.status_code}")


                    else:
                        print("Code ref not found.")
        else:
            time.sleep(1)
            status_call()
    
    status_call()
    def print_typing_effect(text, delay=0.03):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()
    
    pygame.mixer.init()

    pygame.mixer.music.load('./speech/'+code_ref+".mp3")
    pygame.mixer.music.play()
    time.sleep(1)
    print_typing_effect(text, delay=0.03)
    
    

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    

text_to_speech('Hello! How are you Doing. I hope all you are doing good . Is there anything in which I can help ? ')