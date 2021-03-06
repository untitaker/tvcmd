import urllib.parse

import xml.parsers.expat

from .. import errors
from . import base
from ..lib import xmltodict

import logging
def log(): return logging.getLogger(__name__)

class TVRage(base.Base):
    def get_shows(self, pattern):
        url = "http://services.tvrage.com/feeds/search.php?show=%s" % (urllib.parse.quote(pattern))
        
        try:
            xml_content = self._get_url(url)
            xml_content_dict = xmltodict.parse(xml_content)
            
            shows = xml_content_dict["Results"]["show"]
            if (not isinstance(shows, list)): shows = [shows]
            
            return [{"id": s["showid"], "name": s["name"]} for s in shows]
            
        except (xml.parsers.expat.ExpatError, KeyError):
            raise errors.SourceError("Error listing shows: unexpected source response")
        except:
            raise
    
    def get_episodes(self, show_id):
        url = "http://services.tvrage.com/feeds/episode_list.php?sid=%s" % (show_id)
        
        try:
            xml_content = self._get_url(url)
            xml_content_dict = xmltodict.parse(xml_content)
            
            seasons = xml_content_dict["Show"]["Episodelist"]["Season"]
            if (not isinstance(seasons, list)): seasons = [seasons]
            
            l = []
            for s in seasons:
                episodes = s["episode"]
                
                # hack: xmltodict doesn't create lists on singleitems
                if (not isinstance(episodes, list)): episodes = [episodes]
                for e in episodes:
                    l.append({
                        "name": e["title"],
                        "episode": int(e["seasonnum"]),
                        "season": int(s["@no"]),
                        "date": e["airdate"]
                    })
            return l
        except (xml.parsers.expat.ExpatError, KeyError):
            raise errors.SourceError("Error listing episodes: unexpected source response")
        except:
            raise
