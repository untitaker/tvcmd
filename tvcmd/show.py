import logging
def log(): return logging.getLogger(__name__)

#
# Shows and episodes are handled separately because that way is
# easier to filter episodes, in tvcmd a show is not a group of episodes,
# it is only a set of name and id used to get episodes lists from a source
# shows are represented in low case and _ charaters, ex:
# steins_gate, how_i_met_your_mother, the_office_us
#
class Item():
    
    def __init__(self, id, name):
        self.id = id
        self.name = name
    
    def __eq__(self, other):
        return (self.url() == other.url())
    
    def url(self):
        return self.name.replace("(","").replace(")","").replace(" ", "_").lower()
    
    def print_str(self):
        return "[ %s ]: %s" % (self.id, self.url())
    
class List(list):
    
    def clear(self):
        while len(self) > 0 : self.pop()
    
    def print_str(self):
        return "\n".join([ s.print_str() for s in self ])
        
    def filter(self, function):
        return List(item for item in self if function(item))
