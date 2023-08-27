from setuptools import setup, find_packages
from setuptools.command.install import install
from os import environ, path, listdir, remove, rename
from subprocess import call
from shutil import move

class CustomInstall(install):
    def run(self):
        try:
            if 'COLAB_GPU' not in environ and 'KAGGLE_KERNEL_RUN_TYPE' not in environ:
                install.run(self)
                install_dir = self.install_lib
                core_file_path = path.join(install_dir, 'hurllm', 'core.py')
                call(['python', '-m', 'compileall', core_file_path])
                pycache_dir = path.join(install_dir, 'hurllm', '__pycache__')
                for filename in listdir(pycache_dir):
                    if filename.startswith('core'):
                        pycache_file = path.join(pycache_dir, filename)
                        new_file_path = path.join(install_dir, 'hurllm', filename)
                        move(pycache_file, new_file_path)
                        new_file_name = path.join(install_dir, 'hurllm', 'core.pyc')
                        rename(new_file_path, new_file_name)
                        remove(core_file_path)
                        break
            else: install.run(self)
        except Exception as error:
            print(f'ERROR while compiling the installation core: {error}')
            install.run(self)
 
setup(
    name = 'hurllm',
    version = '1.0.7',
    author = 'hurdotcom',
    packages=find_packages(),
    install_requires=[
        'deep-translator>=1.11.4',
        'browser-cookie3>=0.19.1',
        'google-cloud-translate>=3.12.0',
        'requests>=2.31.0',
        'youtube-search-python>=1.6.6',
        'youtube-transcript-api>=0.6.1',
        'PyPDF2>=3.0.1',
        'beautifulsoup4>=4.11.1',
        'pdfplumber>=0.7.4',
        'docx2txt>=0.8',
        'pandas>=1.4.3',
        'python-pptx>=0.6.21',
        'ultralytics>=8.0.158',
        'opencv-python>=4.8.0.76',
        'numpy>=1.23.1',
        'scikit-learn>=1.3.0',
        'webcolors>=1.13',
        'matplotlib>=3.5.2',
        'easyocr>=1.7.0',
        'SpeechRecognition>=3.8.1',
        'pydub>=0.25.1',
        'moviepy>=1.0.3',
        'imageio>=2.31.1'
    ],
    description = 'Closed source LLM model.',
    long_description = 'HurLLM is a proprietary pre-trained Artificial Intelligence model for LLM (Large Language Model) with Transformers technology. It uses a parameter base trained through August 2023 and has fine-tuning added monthly thereafter. The HurLLM code library algorithm splits its processing between the local machine and the remote server hosting the model parameters. Floating point weights are read remotely via API and interpreted locally on your local machine, making it possible to run the code on any machine with 4 Gigabytes or more of RAM memory without using GPU and maintaining the privacy of the data of the user that are processed on the client hardware. It is a closed source model with thirty free messages to test in the trial version. The paid version has no usage or availability limitations, allowing the user to make as many requests as he wants without changing the license price, which is fixed at $2.50 (two dollars and fifty cents/month) without readjustments.\n\n'+
    'from hurllm import HurLLM\n\n'+
    "hurllm = HurLLM(API_KEY='YOUR_API_KEY')\n"+
    "answer = hurllm.conversation(prompt='Your question here.')\n"+
    'print(answer)',
    url = 'https://hurllm.web.app',
    project_urls = {
        'Source code': 'https://github.com/hurllm/hurllm1.0.0',
        'Download': 'https://github.com/hurllm/hurllm1.0.0/archive/refs/heads/main.zip'
    },
        package_data={
        'hurllm': ['yolov8m.pt'],
    },
    license = 'Proprietary Software',
    keywords = 'LLM, Transformers, Artificial Intelligence, NLP, GPT',
    cmdclass={'install': CustomInstall}
)