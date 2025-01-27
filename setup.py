from setuptools import setup, find_packages
setup(
    name='omniparser demo',
    version='0.1.0',
    packages=find_packages(include=['ominparser demo']),
    install_requires=[
        'fastapi',
        'transformers',
        'langchain',
        'torch',
        'easyocr',
        'torchvision',
        'supervision==0.18.0',
        'openai==1.3.5',
        'transformers',
        'ultralytics', #==8.1.24',
        'azure-identity',
        'numpy',
        'opencv-python',
        'opencv-python-headless',
        'gradio',
        'dill',
        'accelerate',
        'timm',
        'einops==0.8.0',
        'paddlepaddle',
        'paddleocr',
    ]
)