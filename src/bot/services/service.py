from abc import ABC 
from ..utils.logger import Logger

class Service(ABC):
    def __init__(self):
         

        self.logger = Logger(self.__class__.__name__)
    