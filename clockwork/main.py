import sys

from text_adventure.grammar import interpreter
from text_adventure import (
        inventory,
        exception as txt_exception)

'''
from text_adventure.grammar.interpreter import Interpreter
from text_adventure.inventory import displayPlayerInventory
from text_adventure.exception import \
    (CannotGoThatWay,
     DenyInput, 
     NotImplemented,
     PlayerDeath)
     '''

        
import clockwork
from clockwork import (
        rooms,
        agents,
        items,
        dictionary)

from clockwork.agents import player as clockwork_player


class Game(object):
    def run(self):
        self.player = clockwork_player.Player(name='Player')
        
        rooms.createRooms()
        agents.createAgents()
        items.createItems()
        clockwork.fillContainers()
        entityNouns = [x.lower() for x in self.getEntityNames()]
        dictionary.get('nouns').extend(entityNouns)
        interpreter = interpreter.Interpreter(
                dictionary=dictionary,
                thesaurus=thesaurus)
        
        self.player.changeOwner(Room.getRoom('Entrance'))
        print self.player.currentOwner.getDescription()
        
        while(True):
            actionText = raw_input('>')
            
            try:
                sentence = interpreter.evaluate(actionText)
                action = Action(sentence=sentence,
                                player=self.player)
                succeeded = action.act()
                if not succeeded:
                    raise txt_exception.CouldNotInterpret(
                        'I understood "{0}", but did not know what '
                        'to do with it.'.format(actionText))
            except DenyInput as e:
                print e
                continue
            except PlayerDeath:
                print "You have died"
                sys.exit()
    
    def getEntityNames(self):
        return clockwork.names
            
    
if __name__ == '__main__':
    game = Game()
    game.run()
