# ComfyUI_kkTranslator_nodes

[简体中文](./README_CN.md)| English

These nodes are mainly used to translate prompt words from other languages into English.
`PromptTranslateToText` implements prompt word translation based on Helsinki NLP translation model.It doesn't require internet connection。
## Install
1. Clone this repository to the custom of ComfyUI In the nodes folder。
```
cd custom_nodes
git clone https://github.com/kingzcheung/ComfyUI_kkTranslator_nodes
```
2. Run the following command to install dependencies
```
python -m pip install -r requirements.txt
```

3. cd `models` and mkdir `kkTranslator`:
```bash
cd models
mkdir kkTranslator
cd kkTranslator
huggingface-cli download --resume-download Helsinki-NLP/opus-mt-zh-en --local-dir opus-mt-zh-en  --local-dir-use-symlinks False
```
You can also download the model from 
- [Helsinki-NLP/opus-mt-zh-en](https://huggingface.co/Helsinki-NLP/opus-mt-zh-en)
- [Helsinki-NLP/opus-mt-rn-en](https://huggingface.co/Helsinki-NLP/opus-mt-rn-en)
- [Helsinki-NLP/opus-mt-taw-en](https://huggingface.co/Helsinki-NLP/opus-mt-taw-en)
- [Helsinki-NLP/opus-mt-az-en](https://huggingface.co/Helsinki-NLP/opus-mt-az-en)
- [Helsinki-NLP/opus-mt-ru-en](https://huggingface.co/Helsinki-NLP/opus-mt-ru-en)
- [Helsinki-NLP/opus-mt-ja-en](https://huggingface.co/Helsinki-NLP/opus-mt-ja-en)
- [Helsinki-NLP/opus-mt-en-ru](https://huggingface.co/Helsinki-NLP/opus-mt-en-ru)
- [Helsinki-NLP/opus-mt-en-jap](https://huggingface.co/Helsinki-NLP/opus-mt-en-jap)
- [Helsinki-NLP/opus-mt-en-rn](https://huggingface.co/Helsinki-NLP/opus-mt-en-rn)

4. Restart your ComfyUI

## Usage
Download this workflow to view the demonstration: [marian_mt_workflow](./marian_mt_workflow.json)

![Alt text](image.png)
