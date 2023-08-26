# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gpt4', 'gpt4.utils']

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
    'name': 'gpt4-torch',
    'version': '0.0.3',
    'description': 'GPT4 - Pytorch',
    'long_description': "[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n\n\n# GPT4\nThe open source implementation of the base model behind GPT-4 from OPENAI [Language + Multi-Modal], click here for the [Research Paper](https://arxiv.org/pdf/2303.08774.pdf)\n\n\n# Installation\n`pip install gpt4-torch`\n\n\n# Usage\n\nHere's an illustrative code snippet that showcases GPT-3 in action:\n\n\n```python\nimport torch\nfrom gpt4 import GPT4\n\n# Generate a random input sequence\nx = torch.randint(0, 256, (1, 1024)).cuda()\n\n# Initialize GPT-3 model\nmodel = GPT4()\n\n# Pass the input sequence through the model\noutput = model(x)\n```\n\n## MultiModal Iteration\n* Pass in text and and image tensors into GPT4\n```python\nimport torch\nfrom gpt4.gpt4 import GPT4MultiModal\n\n#usage\nimg = torch.randn(1, 3, 256, 256)\ntext = torch.randint(0, 20000, (1, 1024))\n\n\nmodel = GPT4MultiModal()\noutput = model(text, img)\n\n```\n\n\n# 📚 Training\n\n```python\nfrom gpt4 import train\n\ntrain()\n\n```\n\nFor further instructions, refer to the [Training SOP](DOCs/TRAINING.md).\n\n\n1. Set the environment variables:\n   - `ENTITY_NAME`: Your wandb project name\n   - `OUTPUT_DIR`: Directory to save the weights (e.g., `./weights`)\n   - `MASTER_ADDR`: For distributed training\n   - `MASTER_PORT` For master port distributed training\n   - `RANK`- Number of nodes services\n   - `WORLD_SIZE` Number of gpus\n\n2. Configure the training:\n   - Accelerate Config\n   - Enable Deepspeed 3\n   - Accelerate launch train_distributed_accelerate.py\n\nFor more information, refer to the [Training SOP](DOCs/TRAINING.md).\n",
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/gpt3',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
