# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['softmax_one']

package_data = \
{'': ['*']}

install_requires = \
['torch']

setup_kwargs = {
    'name': 'softmax-one',
    'version': '0.0.1',
    'description': 'softmax-one - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n\n# Quiet Attention - A Novel Modification to Softmax Function for Attention Mechanism\n\n```math\n(\\text{softmax}_1(x))_i = \\frac{\\exp(x_i)}{1 + \\sum_j \\exp(x_j)}\n```\n\nAttention mechanism has been a groundbreaking innovation in deep learning, and forms the backbone of the Transformer models, which powers the state-of-the-art language models like GPT4 and LLAMA. However, there is a persistent off-by-one bug in the traditional attention mechanism that can make the models harder to compress and deploy.\n\nIntroducing Quiet Attention, an innovative tweak to the traditional softmax function, allowing the attention heads to express \'no preference\' and remain quiet. The slight adjustment to the denominator allows the vector to tend to zero if it prefers, rather than forcing the attention head to make an annotation.\n\n[This is a paper by Evan Miller, here\'s the link](https://www.evanmiller.org/attention-is-off-by-one.html)\n\n\n## Formula\n\nHere\'s the modified formula for the softmax function, also referred to as "Softmax1" or "Quiet Attention" formula:\n\n```math\n(\\text{softmax}_1(x))_i = \\frac{\\exp(x_i)}{1 + \\sum_j \\exp(x_j)}\n```\n\n## Architecture\n\nThe critical difference between Softmax1 and traditional softmax lies in their negative limit behavior. In a scenario where all the entries in a vector are significantly less than zero and the model wants to avoid an annotation altogether, softmax_one allows it, unlike softmax.\n\nSoftmax1 essentially provides an \'escape hatch\' when the attention head wants to remain quiet. The total output weight from Softmax1 varies based on the vector input, as opposed to softmax, which always emits the same total weight. This can significantly improve the model\'s performance, especially when dealing with noisy inputs.\n\n\n## Installation\n\nClone the repository:\n\n```\ngit clone https://github.com/kyegomez/AttentionIsOFFByOne.git\npip3 install -r requirements.txt\ncd AttentionIsOFFByOne\npython3 example.py\n```\n\n## Unit Tests\n\nThis repository contains extensive unit tests that aim to cover all possible scenarios and ensure the reliability of the solution. You can run the tests using the following command:\n\n```bash\npython -m unittest test.py\n```\n\n## Benchmarks\n\nA benchmarking suite is included to compare the performance of the `softmax_one` function with the PyTorch native `softmax` function. We provide metrics across different tensor sizes to understand how they perform under varying loads.\n\nTo run the benchmarks, use the following command:\n\n```bash\npython benchmark.py\n```\n\nYou can find the results in the `benchmarks/results/` directory. The results include execution time and memory usage for each function across a variety of tensor sizes.\n\n## Usage\n\nYou can use the Softmax1 function just like you would use the traditional softmax function. Here\'s a simple example:\n\n```python\nimport torch\nfrom softmax_one.softmax_one import softmax_one\n\nx = torch.randn(5)\ny = softmax_one(x, dim=0)\n```\n\n\n## Implementation\n\n```python\n# Define the softmax_one function with added one in the denominator , which helps to reduce\n#the negative impact impact of tiny values in the softmax function and improves numerical stability\ndef softmax_one(x, dim=None, _stacklevel=3, dtype=None):\n    #subtract the max for stability\n    x = x - x.max(dim=dim, keepdim=True).values\n    #compute exponentials\n    exp_x = torch.exp(x)\n    #compute softmax values and add on in the denominator\n    return exp_x / (1 + exp_x.sum(dim=dim, keepdim=True))\n\n```\n\n\n## Contributions\n\nContributions are welcome! Please submit a pull request or create an issue if you have any improvements or find any bugs.\n\n## License\n\nThis project is licensed under the MIT License - see the `LICENSE` file for details.\n\n\n# Experiments \n\nIt\'s really slow in basic python I will implement it in cuda\n\n```\nINFO:root:Running benchmark for tensor size (10, 10)...\nINFO:root:F.softmax time: 0.0022182464599609375 s\nINFO:root:softmax_one time: 0.04441571235656738 s\nINFO:root:Running benchmark for tensor size (100, 100)...\nINFO:root:F.softmax time: 0.01704573631286621 s\nINFO:root:softmax_one time: 0.07482171058654785 s\nINFO:root:Running benchmark for tensor size (1000, 1000)...\nINFO:root:F.softmax time: 0.060335397720336914 s\nINFO:root:softmax_one time: 3.0616047382354736 s\nINFO:root:Running benchmark for tensor size (10000, 10000)...\nINFO:root:F.softmax time: 52.80402970314026 s\nINFO:root:softmax_one time: 128.78072810173035 s\nINFO:root:Chart display is off.\n\n```',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/AttentionIsOFFByOne',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
