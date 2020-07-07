from os.path import join

builtins = {"yaz": print,
            "oku": input,
            "sayı": int,
            "kesir": float,
            "uzunluk": len,
            "yazı": str,
            "aç": open,
            "mantıksal": bool,
            "mutlak_değer": abs}

##print(*(i for i in sys.__dict__.keys() if not i.startswith("__")), sep = "\n")

class dotdict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setattr__

class Module():

    def __init__(self, name, module_name, name_mapping):
        self.name = name
        self.module = module_name
        self.mapping = name_mapping

    @classmethod
    def from_file(cls, name):
        with open(join("lib", name + ".txt"), "r", encoding = "utf-8") as f:
            data = f.read()
        module_name, data = data.split("\n", 1)
        data = [i for i in data.split("\n") if i]
        name_mapping = dict((i.replace(" ", "").split(":") for i in data))
        return cls(name, module_name, name_mapping)
    
    def create(self):
        self.module = __import__(self.module)
        m = dotdict()
        for alias, name in self.mapping.items():
            m[alias] = getattr(self.module, name)
        return m

modules = {}

def loadmodule(module_name):
    try:
        return modules[module_name].create()
    except KeyError:
        return Module.from_file(module_name).create()
