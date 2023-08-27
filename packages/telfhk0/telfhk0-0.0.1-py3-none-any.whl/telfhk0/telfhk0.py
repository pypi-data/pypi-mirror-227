from os import system as screen
try:
	from requests import post as REQ
	from requests import get as REQ2
except:
    screen("pip install requests")

class Telegram:
    def __init__(self, chat, token):
        self.chat = chat
        self.token = token
     
    def SendMessage(self,text):
        data = {
            "UrlBox": f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat}&text={text}",
            "AgentBox": "Google Chrome",
            "VersionsList": "HTTP/1.1",
            "MethodList": "GET"
        }
        REQ("https://www.httpdebugger.com/tools/ViewHttpHeaders.aspx", data=data)

    def MultiMessage(self, chats_id,text):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        for i in chats_id:
            response = REQ(url, json={"chat_id": i, "text": text})
        
    def DownloadIR(self,link):
        data = {
            "UrlBox": f"https://api.telegram.org/bot{self.token}/sendDocument?chat_id={self.chat}&document={link}",
            "AgentBox": "Google Chrome",
            "VersionsList": "HTTP/1.1",
            "MethodList": "GET"
        }
        REQ("https://www.httpdebugger.com/tools/ViewHttpHeaders.aspx", data=data)         

          
    def SendPhoto(self,address,caption):
        url = f"https://api.telegram.org/bot{self.token}/sendPhoto?chat_id={self.chat}&caption={caption}"
        files = {'photo': open(address, 'rb')}           
        r = REQ(url,files=files)

    def SendFile(self,address,caption):
        url = f"https://api.telegram.org/bot{self.token}/sendDocument?chat_id={self.chat}&caption={caption}"
        files = {'document': open(address, 'rb')}           
        r = REQ(url,files=files)
    def SendVideo(self,address,caption):
        url = f"https://api.telegram.org/bot{self.token}/sendVideo?chat_id={self.chat}&caption={caption}"
        files = {'video': open(address, 'rb')}           
        r = REQ(url,files=files) 

    def SendSticker(self,sticker):
        url = f"https://api.telegram.org/bot{self.token}/sendSticker?chat_id={self.chat}"
        files = {'sticker': open(sticker, 'rb')}           
        r = REQ(url,files=files)

    def EditMessage(self,id,text):
        url = f"https://api.telegram.org/bot{self.token}/editMessageText?chat_id={self.chat}"
        data = {'message_id': id,'text':text}           
        r = REQ(url,data=data)

    def InfoBot(self):
        url = f'https://api.telegram.org/bot{self.token}/getMe'
        r = REQ2(url).text
        data = r.json()
        if r.status_code == 200:
            print(f"ID: {data['result']['id']}\nNAME : {data['result']['first_name']}")
                
    def Forward(self,target,id):
        url = f"https://api.telegram.org/bot{self.token}/forwardMessage?chat_id={self.chat}&from_chat_id={target}&message_id={id}"
        r = REQ(url)
        
    def GetProfile(self,user,limit,name):
        url = f"https://api.telegram.org/bot{self.token}/getUserProfilePhotos"
        params = {
        'user_id': user,
        'limit': limit
    }
        r = REQ(url,params=params)
        if r.status_code == 200:
            data = r.json()
            if data['result']['total_count'] > 0:
                file_id = data['result']['photos'][0][0]['file_id']        
                get_file_url = f"https://api.telegram.org/bot{self.token}/getFile"
                params = {'file_id': file_id}
                response = REQ2(get_file_url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    file_path = data['result']['file_path']
                    file_url = f"https://api.telegram.org/file/bot{self.token}/{file_path}"
                    response = REQ2(file_url)
                    if response.status_code == 200:
                        ur = f"https://api.telegram.org/bot{self.token}/sendPhoto?chat_id={self.chat}"
                        with open(name, 'wb') as file:
                            file.write(response.content)
                            files = {'photo': open(name, 'rb')}
                            r = REQ(ur,files=files)
                
    def DeletWebhok(self):
        url = f"https://api.telegram.org/{self.token}/deleteWebhook"       
        r = REQ(url)
            
    def SetWebhok(self,url):
        url = f"https://api.telegram.org/bot{self.token}/setWebhook?url={url}"       
        r = REQ(url)
        
    def get_last_message(self):
        url = f'https://api.telegram.org/bot{self.token}/getUpdates' 

        response = REQ2(url)
        data = response.json()
  
        if 'result' in data and data['result']:
       
            last_message = data['result'][-1]
            return last_message

        return None

    def Reply(self,text):
        last_message = self.get_last_message()

        if last_message:
            chat_id = last_message['message']['chat']['id']
            message_id = last_message['message']['message_id']
            reply_text = text

            url = f'https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat}' 
            data = {
            'text': reply_text,
            'reply_to_message_id': message_id
            }

            headers = {
            'Content-Type': 'application/json'
            }

            response = REQ(url, json=data, headers=headers)

    def GetMessage(self,number):
        url = f'https://api.telegram.org/bot{self.token}/getUpdates'
        response = REQ2(url)
        data = response.json()
        if 'result' in data and data['result']:
            last_message = data['result'][number]
            return (last_message['message']['text'])
        else:
            return None
         
    def MessageID(self,number):        
        get_updates_url = f'https://api.telegram.org/bot{self.token}/getUpdates'
        params = {'chat_id': self.chat}
        response = REQ2(get_updates_url, params=params)
        data = response.json()

        if response.status_code == 200 and data['ok']:
            if data['result']:
       
                last_5_messages = data['result'][-number:]
                for message in last_5_messages:
                    message_id = message['message']['message_id']
                    text = message['message']['text']
                    print(f"Text : {text}\nMessage Id : {message_id}")                                                                     
    def SendVoice(self,address, caption):
        url = f"https://api.telegram.org/bot{self.token}/sendVoice?chat_id={self.chat}"
        data = {"caption": caption}
        files = {"voice": open(address, "rb")}
        response = REQ(url, data=data, files=files) 
        
    def get_last_message_id(self,number):
        url = f"https://api.telegram.org/bot{self.token}/getUpdates"
        response = REQ2(url)
    
        if response.status_code == 200:
            data = response.json()
            if data["ok"] and data["result"]:
                last_message_id = data["result"][-number]["message"]["message_id"]
                return last_message_id

        return None                 
                                   
    def DeleteMessage(self,number):
        message_id = self.get_last_message_id(number)
        if message_id:
            url = f"https://api.telegram.org/bot{self.token}/deleteMessage"
            params = {"chat_id": self.chat, "message_id": message_id}
            response = REQ(url, params=params)