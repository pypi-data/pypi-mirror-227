class DependenciesInstaller():
    def __init__(self):
        from hurllm.core import DependenciesInstaller
        self.__dependencies_installer = DependenciesInstaller()
    def install(self): self.__dependencies_installer.install()
    def uninstall(self): self.__dependencies_installer.uninstall()
    def describe(self): self.__dependencies_installer.describe()
class HurLLM:
    def __init__(self, API_KEY='', response_index=0, language='en-us', session_control=False):
        from hurllm.core import HurLLM
        self.__hurllm = HurLLM(API_KEY=API_KEY, response_index=response_index, language=language, session_control=session_control)
    def addFile(self, path=''): self.__hurllm.addFile(path=path)
    def conversation(self, prompt='', code_interpreter=False): return self.__hurllm.conversation(prompt=prompt, code_interpreter=code_interpreter)
    def getResponses(self): return self.__hurllm.getResponses()
    def __del__(self):
        try: self.__hurllm.__del__
        except: pass
