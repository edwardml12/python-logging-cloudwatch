from services.logger import logger

class Item:
    def __init__(self, name: str = None, description: str = None):
        self.name = name
        self.description = description
    
    def update_item(self, name: str, description: str):
        if name:
            self.name = name
        if description:
            self.description = description

    def get_item(self) -> 'Item':
        logger.info('Esta é uma mensagem informativa.')
        return {"name": self.name, "description": self.description}