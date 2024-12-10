# action/Action.py

class Action:
    def execute(self, *args, **kwargs):
        raise NotImplementedError("Subclasses should implement this method.")
