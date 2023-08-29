# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qwen']

package_data = \
{'': ['*']}

install_requires = \
['SentencePiece',
 'accelerate',
 'datasets',
 'deepspeed',
 'einops',
 'lion-pytorch',
 'matplotlib',
 'numpy',
 'torch',
 'transformers']

setup_kwargs = {
    'name': 'qwen',
    'version': '0.1.0',
    'description': 'Qwen VL - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n\n# Qwen-VL\nMy personal implementation of the model from "Qwen-VL: A Frontier Large Vision-Language Model with Versatile Abilities", they haven\'t released model code yet sooo...\n\n\n# Install\n`pip3 install qwen`\n\n---\n\n# Usage\n```python\n\nimport torch\nfrom qwen.model import QwenVL\n\n#usage\nimg = torch.randn(1, 3, 256, 256)\ncaption = torch.randint(0, 20000, (1, 1024))\n\nmodel = QwenVL()\noutput = model(img, caption)\nprint(output.shape)\n\n```\n\n----\n\n# Inference\n```python\n\nfrom qwen.inference import QwenVLChat\n\n\nqwen_chat = QwenVLChat(model_name="Qwen/Qwen-VL-Chat", device_map="cuda")\nresponse = qwen_chat.chat([\n    {"image": "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg"},\n    {"text": "这是什么?"}\n])\nprint(response)\n\n\n\n```\n\n\n# Training\n* [There is a file with a table of all the datasets used in the paper here](docs/datasets.md)\n\n```python\nfrom qwen.train import Train\n\n\ndef train():\n    os.environ[\'MASTER_ADDR\'] #\'localhost\'\n    os.environ[\'MASTER_PORT\'] #= \'9994\'\n    \n    # # [CRITICAL] Pay attention to this when scaling to multiple GPUs and clusters\n    os.environ[\'RANK\']       #= str(0) # Number of nodes (servers)\n    os.environ[\'WORLD_SIZE\'] # = str(torch.cuda.device_count())\n\n    dist.init_process_group(backend=\'nccl\') #init_method="env://")\n    \n    Train()\n\nif __name__ == \'__main__\':\n    train()\n\n\n```\n\n1. Set the environment variables:\n   - `ENTITY_NAME`: Your wandb project name\n   - `OUTPUT_DIR`: Directory to save the weights (e.g., `./weights`)\n   - `MASTER_ADDR`: For distributed training\n   - `MASTER_PORT` For master port distributed training\n   - `RANK`- Number of nodes services\n   - `WORLD_SIZE` Number of gpus\n\n2. Configure the training:\n   - Accelerate Config\n   - Enable Deepspeed 3\n   - Accelerate launch train_distributed_accelerate.py\n\nFor more information, refer to the [Training SOP](DOCs/TRAINING.md).\n\n\n----\n\n\n\n# Todo\n\n- [ ] Position aware vision language adapter, compresses image features. Singer layer cross attention module inited randomly => group of trainable embeddings as query vectors + image features from the visual encoder as keys for cross attention ops => OUTPUT: compresses visual feature sequence to a fixed lnegth of 256, 2d absolute positional encodings are integrated into the cross attentions mechanisms query key pairs => compressed feature sequence of length of 256 => fed into decoder llm\n\n- [ ] Bounding Boxes, for any given accurate bounding box, a norm process is applied in the range [0, 1000] and transformed into a string format (Xtope, Ytople)(Xottomright, Ybottomright) -> the string is tokenized as text and does not require positional vocabulary. Detection strings and regular text strings, two special tokens <box> and </box> are added to the beginning and end of the bounding box string. + another sed of special tokens (<ref> and </ref>) is introduced.\n\n# Citations\n\nPlease use the following to cite this work:\n\n```latex\n@article{bai2023qwen,\n  title={Qwen-VL: A Frontier Large Vision-Language Model with Versatile Abilities},\n  author={Bai, Jinze and Bai, Shuai and Yang, Shusheng and Wang, Shijie and Tan, Sinan and Wang, Peng and Lin, Junyang and Zhou, Chang and Zhou, Jingren},\n  journal={arXiv preprint arXiv:2308.12966},\n  year={2023},\n  url={https://doi.org/10.48550/arXiv.2308.12966}\n}\n\n```\n\nFor more details, please refer to the\xa0[full paper](https://doi.org/10.48550/arXiv.2308.12966).\n\n\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/Qwen-VL',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
