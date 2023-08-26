from dataclasses import dataclass
from . import models

@dataclass
class Remap:
    data: dict
    def init(self, path: list[models.RemapData]):
        for item in path:
            key, value = self.get_data(item.from_path)
            print(f"{value=}")
            tmp = self.get_path(item.to_path)
            print(f"{tmp=}")
            if value is None or tmp is None:
                continue
            tmp[key] = value
            print(f"{tmp=}")
            self.data = tmp
            self.data = x if (x:= self.remove(item.from_path)) else self.data
        return self.data
    def get_path(self, path: models.RemapUrl):
        arr = path.to_array()
        tmp = self.data
        if len(arr) == 1 and arr[0] == "":
            return self.data
        for url in arr:
            if url in tmp:
                tmp = tmp[url]
            else:
                return None
        return tmp,
    def get_data(self, path: models.RemapUrl):
        arr = path.to_array()
        tmp = self.data
        if len(arr) == 1:
            if arr[0] in tmp:
                return (arr[0], tmp[arr[0]], )
        for url in arr[:-1]:
            if url in tmp:
                tmp = tmp[url]
            else:
                return None
        return (arr[-1], tmp[arr[-1]],)
    
    def remove(self, path: models.RemapUrl):
        paths = path.to_array()
        i = len(paths) - 2
        while i >= 0:
            url = self.get_path(models.RemapUrl(".".join(paths[:i])))
            if len(url[paths[i]].keys()) == 1:
                del url[paths[i]]
            i-=1
        return url
        
    def set(self, data: dict):
        self.data = data
        return self