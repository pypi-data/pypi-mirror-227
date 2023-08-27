from dataclasses import dataclass
from . import models

@dataclass
class Remap:
    data: dict
    def init(self, path: list[models.RemapData]):
        for item in path:
            key, value = self.get_data(item.from_path)
            tmp = self.get_path(item.to_path)
            if value is None or tmp is None:
                continue
            tmp[key if not item.new_name else item.new_name] = value
            self.data = tmp
            self.data = x if (x:= self.remove(item.from_path)) else self.data
        return self.remove_empty(self.data)
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
        return tmp
    def get_data(self, path: models.RemapUrl):
        arr = path.to_array()
        tmp = self.data
        if len(arr) == 1:
            if arr[0] in tmp:
                return (arr[0], tmp[arr[0]], )
        for url in arr[:-1]:
            if url in tmp:
                tmp = tmp[url]
                if not tmp:
                    return None, None
            else:
                return None, None
        return (arr[-1], tmp[arr[-1]],)
    
    def remove(self, path: models.RemapUrl):
        paths = path.to_array()
        i = len(paths) - 2
        while i >= 0:
            url = self.get_path(models.RemapUrl(".".join(paths[:i])))
            parent = url[paths[i]]
            field = parent[paths[i+1]]
            if isinstance(field, dict):
                keys = list(field.keys())
                for key in keys:
                    if field[key] is None:
                        del field[key]
            if not isinstance(field, dict) or len(field.keys()) == 0:
                del parent[paths[i+1]]
            if parent and isinstance(parent, dict) and len(parent.keys()) == 0:
                del url[paths[i]]
            i-=1
        return url
    def remove_empty(self, data: dict):
        for key in list(data.keys()):
            if isinstance(data[key], dict):
                if len(data[key].keys()) == 0:
                    del data[key]
                else:
                    data = self.remove_empty(data[key])            
            elif data[key] is None:
                del data[key]
        return data
    def set(self, data: dict):
        self.data = data
        return self