from . import cons, errors

from configparser import ConfigParser 

import os, configparser, json

import logging
def log(): return logging.getLogger(__name__)

class ConfigFileParser(ConfigParser):
    
    def __init__(self, filename):
        ConfigParser.__init__(self)
        self.filename = filename
        
    def read(self):
        return ConfigParser.read(self, self.filename)
    
    def write(self):
        try: os.makedirs(os.path.dirname(self.filename))
        except: pass
        
        with open(self.filename, "w") as f:
            return ConfigParser.write(self, f)

class Status(ConfigFileParser):
    
    def __init__(self):
        ConfigFileParser.__init__(self, cons.CONFIG_STATUS)
        
    def read(self):
        ConfigFileParser.read(self)
        try: self.add_section("status")
        except: pass

    def get(self, eurl):
        try: return int(ConfigFileParser.get(self, "status", eurl))
        except: return None
        
    def get_all(self):
        d = {}
        for s in self.items("status"):
            d[s[0]] = int(s[1])
        return d
    
    def set(self, eurl, status):
        ConfigFileParser.set(self, "status", eurl, str(status))
        
    def remove(self, eurl):
        self.remove_option("status", eurl)
    

class Main(ConfigFileParser):
    
    def __init__(self):
        ConfigFileParser.__init__(self, cons.CONFIG_MAIN)
        
    def read(self):
        ConfigFileParser.read(self)
        try: self.add_section("general")
        except: pass
        
    def get_shows(self):
        l = []
        for s in self.get("general", "shows", fallback="").split(","):
            s = s.strip()
            if len(s) > 0: l.append(s)
        return l
        
    def get_formats(self):
        l = []
        for s in self.get("general", "formats", fallback="").split(","):
            s = s.strip()
            if len(s) > 0: l.append(s)
        return l
        
    def get_source(self):
        _source = self.get("general", "source", fallback="thetvdb")
        if _source not in ["thetvdb", "tvrage"]:
             raise errors.ConfigError("Invalid source: %s" %(_source))
        return _source

class Cache(dict):
    
    def __init__(self):
        self._filename = cons.CACHE_EPISODES
    
    def read(self):
        self.clear()
        try:
            with open(self._filename) as f:
                self.update(json.load(f))
        except Exception as ex:
            pass
            
    def write(self):
        try: os.makedirs(os.path.dirname(self._filename))
        except: pass
        
        with open(self._filename, "w") as f:
            return json.dump(dict(self), f, indent=2, separators=(',', ': '))
