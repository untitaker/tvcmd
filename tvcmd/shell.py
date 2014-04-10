import readline, cmd
from . import commands, manager, io, cons

from . import __version__

import logging
def log(): return logging.getLogger(__name__)

readline.set_completer_delims(" ")

class CommandContainer():
    def __init__(self):
        self.reload = commands.Reload()
        self.update = commands.Update()
        self.save = commands.Save()
        self.shows = commands.Shows()
        self.search = commands.Search()
        self.new = commands.New()
        self.adquire = commands.Adquire()
        self.see = commands.See()
        self.format = commands.Format()
        self.ls = commands.Ls()

class Shell(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        
        self.prompt = "tvcmd:> "
        self.cmds = CommandContainer()
    
    #
    # bypass command handling to each command class
    #
    def do_reload(self, line):
        return self.cmds.reload.do(line)
    
    def do_update(self, line):
        return self.cmds.update.do(line)
    
    def do_save(self, line):
        return self.cmds.save.do(line)
    
    def do_shows(self, line):
        return self.cmds.shows.do(line)
    
    def do_search(self, line):
        return self.cmds.search.do(line)
    
    def do_format(self, line):
        return self.cmds.format.do(line)
        
    def complete_format(self, text, line, start_index, end_index):
        return self.cmds.format.complete(text, line, start_index, end_index)
                
    def do_adquire(self, line):
        return self.cmds.adquire.do(line)
        
    def complete_adquire(self, text, line, start_index, end_index):
        return self.cmds.adquire.complete(text, line, start_index, end_index)
    
    def do_new(self, line):
        return self.cmds.new.do(line)
        
    def complete_new(self, text, line, start_index, end_index):
        return self.cmds.new.complete(text, line, start_index, end_index)
    
    def do_see(self, line):
        return self.cmds.see.do(line)
        
    def complete_see(self, text, line, start_index, end_index):
        return self.cmds.see.complete(text, line, start_index, end_index)
        
    def do_ls(self,line):
        return self.cmds.ls.do(line)
        
    def complete_ls(self, text, line, start_index, end_index):
        return self.cmds.ls.complete(text, line, start_index, end_index)
    
    
    #
    # basic commands
    #
    def do_version(self, line):
        io.msg(__version__)
    
    def do_help(self, line):
        sep = "\n   "
        help = (
                "** COMMANDS **\n"
                "To get specific help type: COMMAND --help\n"
                "Auxiliary commands: version, exit, quit, help\n"
                "DB commands: update, save, reload\n"
                "Episodes commands: new, adquire, see, format, ls\n"
                "Shows commands: shows, search\n"
                
                "\n** PATHS **\n"
                "config: %s\n"
                "status-db: %s\n"
                "cache: %s\n"
                
                "\n** Example Config **\n"
                "[general]\n"
                "shows = an_idiot_abroad, the_office_us, lost\n"
                "formats = https://torrentz.eu/verified?f=${show+}+s${season}e${episode}\n"
                "source = tvrage"
        )
        print(help %(cons.MAINCONFIGFILE, cons.STATUSDBFILE, cons.CACHEFILE))
        return
    
    def emptyline(self):
        pass
    
    def do_exit(self, line):
        if manager.instance.modified:
            answer = io.ask_yn("Database has been modified. Do you want to save it before closing?")
            if answer: self.onecmd("save")
        return True
    
    do_quit = do_exit
    
    def default(self, line):
        if line == "EOF":
            io.msg("")
            return self.onecmd("exit")
        
        io.msg("Invalid command: %s"%(line.split(" ")[0]))
        self.onecmd("help")
    
    def cmdloop(self):
        try:
            return cmd.Cmd.cmdloop(self)
        except KeyboardInterrupt:
            io.msg("^C")
            return self.cmdloop()