from abc import ABC, abstractmethod

class BaseModule(ABC):
    """
    Abstract base class for all modules in PySploitX.
    """
    def __init__(self):
        self.options = self.get_options()

    @abstractmethod
    def get_options(self):
        """
        Returns a dictionary of options that the module requires.
        Example: {'RHOST': ('127.0.0.1', 'The target host'), 'RPORT': (80, 'The target port')}
        """
        pass

    @abstractmethod
    def run(self, options):
        """
        The main function of the module that executes its logic.
        """
        pass

    def get_info(self):
        """
        Returns a dictionary containing information about the module.
        This can be overridden by subclasses to provide more details.
        """
        return {
            "Name": self.__class__.__name__,
            "Description": self.__doc__ or "No description provided."
        }
