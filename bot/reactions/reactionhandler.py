import abc


class ReactionHandler(abc.ABC):
    def __init__(self, name, unicode):
        self.name = name
        self.unicode = unicode

    @abc.abstractmethod
    async def handle_reaction(self, event_id, reaction_context):
        pass
