import pickle
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

    def __init__(self):
        self.player = clockwork_player.Player(name='Player')
        
        agents.create_agents()
        items.create_items()
        self.rooms = rooms.create_rooms()
        clockwork.fill_containers()
        entity_nouns = [x.lower() for x in self.get_entity_names()]
        dictionary.dictionary.get('nouns').extend(entity_nouns)
        self.interpreter = interpreter.Interpreter(
                dictionary=dictionary.dictionary,
                thesaurus=dictionary.thesaurus)
        
        self.player.change_owner(self.rooms.get('room1'))
        print self.player.owner.getDescription()
        
    def step(self):
        actionText = raw_input('>')
        
        try:
            evaluation = self.interpreter.evaluate(actionText)
            if isinstance(evaluation, sentence.Command):
                if evaluation.command == 'save':
                    save(evaluation.arguments[0])
                elif evaluation.command == 'restore':
                    restore(evaluation.arguments[0])
                else:
                    raise NotImplementedError()
            else:
                action = Action(sentence=evaluation,
                                player=self.player)
            succeeded = action.act()
            if not succeeded:
                raise txt_exception.CouldNotInterpret(
                    'I understood "{0}", but did not know what '
                    'to do with it.'.format(actionText))
        except DenyInput as e:
            print e
            return
        except NotImplementedError as e:
            print "That command is not implemented"
            return
        except PlayerDeath:
            print "You have died"
            sys.exit()
    
    def get_entity_names(self):
        return clockwork.names

game = Game()

def run():
    while True:
        game.step()

def save(filename):
    with open(filename, 'w') as savefile:
        pickle.dump(game, savefile)

def restore(filename):
    global game
    with open(filename, 'r') as savefile:
        game = pickle.load(savefile)
    
if __name__ == '__main__':
    run()
