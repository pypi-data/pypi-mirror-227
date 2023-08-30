import requests

class Recording(object):
    def __init__(self,**d):
        self.__URL = d.get("url")
    
    @property
    def url(self):
        return self.__URL
    
    @property
    def audio_data(self):
        return requests.get(self.__URL).content

    def __repr__(self):
        return "<{0.__class__.__name__} {1} >".format(
            self,
            " ".join(
                f'{attr}={getattr(self, attr) if getattr(self, attr) != "" else "None"}'
                for attr in dir(self)
                if not attr.startswith('__')
                and isinstance(getattr(self, attr), str)
            )
        )