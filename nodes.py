from transformers import MarianMTModel, MarianTokenizer
import requests
import random
import json
from hashlib import md5

marian_list = [
    "opus-mt-zh-en",
    "opus-mt-rn-en",
    "opus-mt-taw-en",
    "opus-mt-az-en",
    "opus-mt-ru-en",
]

lang_list = [
    'auto','zh', 'yue', 'kor', 'th', 'pt','el','bul','fin','slo','cht','wyw'
,'fra','ara','de','nl','est','cs','swe','jp','spa','ru','it','pl']

def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()

class LoadMarianMTCheckPoint:
    @classmethod
    def INPUT_TYPES(cls):
        
        # default_model_path = Path(folder_paths.models_dir) / "marian_models"
        # marian_list = [str(p.name) for p in default_model_path.iterdir()]
        return {
            "required": {
                "checkpoint": (marian_list, {"multiline": False,"default": "opus-mt-zh-en"}),
            }
        }
        
    RETURN_TYPES = ("MODEL","TOKENIZER")
    RETURN_NAMES = ("model","tokenizer")
    FUNCTION = "load_marian_mt"
    CATEGORY = "kkTranslator"

    def load_marian_mt(self, checkpoint):
        # default_model_path = Path(folder_paths.models_dir) / "marian_models"
        model_name = 'Helsinki-NLP/' + checkpoint
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)

        return (model,tokenizer)


class PromptTranslateToText:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL", ),
                "tokenizer": ("TOKENIZER", ),
                "prompt_text": ("STRING", {"multiline": True,"default": "你好"}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "run"
    CATEGORY = "kkTranslator"

    def run(self, model,tokenizer,prompt_text):
        translated = model.generate(**tokenizer(prompt_text, return_tensors="pt", padding=True))
        text = ""
        for t in translated:
            text += tokenizer.decode(t, skip_special_tokens=True) 
            print(text)

        return (text,)
    
 
class PromptBaiduFanyiToText:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "appid": ("STRING", {"multiline": False,"default": ""}),
                "secretkey": ("STRING", {"multiline": False,"default": ""}),
                "from_lang": (lang_list, {"multiline": True,"default": "auto"}),
                "prompt_text": ("STRING", {"multiline": True,"default": "你好"}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "run"
    CATEGORY = "kkTranslator"

    def run(self, appid,secretkey,from_lang,prompt_text):
        if appid == "" or secretkey == "":
            raise "Please input your appid and secretkey"
        endpoint = 'http://api.fanyi.baidu.com'
        path = '/api/trans/vip/translate'
        
        url = endpoint + path
        salt = random.randint(32768, 65536)
        sign = make_md5(appid + prompt_text + str(salt) + secretkey)
        # Build request
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'appid': appid, 'q': prompt_text, 'from': from_lang, 'to': 'en', 'salt': salt, 'sign': sign}

        # Send request
        r = requests.post(url, params=payload, headers=headers)
        result = r.json()

        text = result['trans_result'][0]['dst']
        
        return (text,)
    

# A dictionary that contains all nodes you want to export with their names
NODE_CLASS_MAPPINGS = {
    "PromptTranslateToText": PromptTranslateToText,
    "LoadMarianMTCheckPoint":LoadMarianMTCheckPoint,
    "PromptBaiduFanyiToText": PromptBaiduFanyiToText,
}
 
# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptTranslateToText": "Prompt Translate to Text",
    "LoadMarianMTCheckPoint":"Load MarianMT CheckPoint",
    "PromptBaiduFanyiToText": "Prompt Baidu Fanyi to Text",
}


if __name__ == "__main__":
    # load = LoadMarianMTCheckPoint()
    # load.load_marian_mt("opus-mt-zh-en")
    fanyi = PromptBaiduFanyiToText()
    fanyi.run("xxxxxxxxxx", "xxxxxxxxxxxxxx", "zh", "你好")