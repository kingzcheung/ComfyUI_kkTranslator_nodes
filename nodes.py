from transformers import MarianMTModel, MarianTokenizer
import folder_paths
from pathlib import Path

marian_list = [
    "opus-mt-zh-en",
    "opus-mt-rn-en",
    "opus-mt-taw-en",
    "opus-mt-az-en",
    "opus-mt-ru-en",

]

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
    
 
# A dictionary that contains all nodes you want to export with their names
NODE_CLASS_MAPPINGS = {
    "PromptTranslateToText": PromptTranslateToText,
    "LoadMarianMTCheckPoint":LoadMarianMTCheckPoint,
}
 
# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptTranslateToText": "Prompt Translate to Text",
    "LoadMarianMTCheckPoint":"Load MarianMT CheckPoint",
}


if __name__ == "__main__":
    load = LoadMarianMTCheckPoint()
    load.load_marian_mt("opus-mt-zh-en")