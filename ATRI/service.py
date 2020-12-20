import json
from pathlib import Path
from typing import Optional

SERVICE_SWITCH_PATH = Path('.') / 'ATRI' / 'data' / 'service' / 'switch.service.json'
SERVICE_BANLIST_PATH = Path('.') / 'ATRI' / 'data' / 'service' / 'banlist.service.json'

state = 0


class Service():
    class Switch():
        if not SERVICE_SWITCH_PATH.is_file:
            SERVICE_SWITCH_PATH.write_text(json.dumps({}))
            data = {}
        else:
            data = json.loads(SERVICE_SWITCH_PATH.read_bytes())

        def get_service(self) -> dict:
            return self.data
        
        def auth_service(self, service: str, group: Optional[int]) -> bool:
            try:
                self.data['global']
            except:
                self.data['global'] = {}
                SERVICE_SWITCH_PATH.write_text(json.dumps(self.data))
            
            try:
                self.data[group]
            except:
                self.data[group] = {}
                SERVICE_SWITCH_PATH.write_text(json.dumps(self.data))
            
            if (not self.data['global'].get('service', None)
                or not self.data[group][service].get('service', None)):
                self.data['global'][service] = True
                self.data[group][service] = True
                SERVICE_SWITCH_PATH.write_text(json.dumps(self.data))
            else:
                pass
            
            if self.data['global'][service]:
                return True if self.data[group][service] else False
            else:
                return False
        
        def control_service(self, service: str, _type: bool, group: Optional[int]) -> bool:
            if service not in self.data:
                self.data['global'][service] = True
                self.data[group][service] = True
                SERVICE_SWITCH_PATH.write_text(json.dumps(self.data))
            
            if group:
                try:
                    self.data[group][service] = _type
                    SERVICE_SWITCH_PATH.write_text(json.dumps(self.data))
                    return True
                except:
                    return False
            else:
                try:
                    self.data['global'][service] = _type
                    SERVICE_SWITCH_PATH.write_text(json.dumps(self.data))
                    return True
                except:
                    return False
    
    class BanList():
        if not SERVICE_BANLIST_PATH.is_file():
            SERVICE_BANLIST_PATH.write_text(json.dumps({}))
            data = {}
        else:
            data = json.loads(SERVICE_BANLIST_PATH.read_bytes())
        
        def get_banlist(self) -> dict:
            return self.data
        
        def is_in_list(self, user: Optional[int]) -> bool:
            return False if user in self.data else True

        def add_list(self, user: Optional[int]) -> bool:
            try:
                self.data[user] = user
                SERVICE_BANLIST_PATH.write_text(json.dumps(self.data))
                return True
            except:
                return False

        def del_list(self, user: Optional[int]) -> bool:
            try:
                del self.data[user]
                SERVICE_BANLIST_PATH.write_text(json.dumps(self.data))
                return True
            except:
                return False
    
    class Dormant():
    
        def is_sleep(self) -> bool:
            return True if state != 1 else False
        
        def cont_wake(self, _type: bool) -> bool:
            global state
            try:
                if _type:
                    state = 0
                else:
                    state = 1
                return True
            except:
                return False
