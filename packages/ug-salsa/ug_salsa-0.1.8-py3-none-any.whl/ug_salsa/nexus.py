#%% Load imports
import numpy as np
import traceback
import json

from salsa.parameters import Parameters
from salsa.helper_functions import log
try:
    import nexusutils as nx
except ImportError as e:
    log('exception', f'Encountered exception while loading nx: {e}')

#%% Helper functions and class
class NexusReturnsFalse(Exception):
    pass

def metaclass(cls):
    class Nexus(metaclass=cls):
        pass
    return Nexus

#%% main nexus class
@metaclass
class Nexus(type):
    
    _api = None
    params: Parameters = None
    runID: str = None
    
    @classmethod
    def initialize( cls ) -> None:
        cls.params = Parameters()
        cls.runID = cls.params['runid']
        
        try:
            cls._api = nx.ApiSession(config = cls.params['nexus_conf'])
        except Exception as e:
            log('warning', f"Nexus connection cannot be established. Error: {e}")
        return
    
    @classmethod
    def get_nexus_details(cls) -> str:
        cls.params = Parameters()
        cls.runID = cls.params['runid']
        # run, cam = cls.runID.split("_")
        try:
            status, result_str = cls._api.get_run(cls.runID)
            if not status:
                return ''
            result_list = json.loads(result_str)
            if not result_list:
                return ''
            return result_list[0].get("details", "")
        except Exception as e:
            log('warning', f"Nexus connection cannot be established. Error: {e}")
        return ''
    
    @classmethod
    def send_html( cls, filename ) -> None:
        if not cls.params['send_nexus_html']:
            return
        status, message = cls._api.upload_file(cls.runID, filename)
        if not status:
            log("exception", f"Failed to send plots.html to nexus, got response {message}")
    
    @classmethod
    def update_report(cls, key, value) -> None:

        #if theres any null, return
        if(cls.catch_null(key, value)):
            return
        
        #if no report exists, create report (this condition is handled in create_report)
        if(cls.create_report(key,value)):
            return
        
        #otherwise, updates existing report
        try:
            log('info',f'Updating report with data key = {key}, value = {value}')
            cls._api.update_report(cls.runID, {key:value})
        except Exception as e:
            log('warning',f"Failed to update Nexus reports table with {dict({key: value})}. Error: {e}")
            log("warning",traceback.format_exc())
        return
    
    @classmethod
    def create_report(cls, key, value) -> bool:
        try:
            status, report = cls._api.get_report(cls.runID)
            if not status:
                raise NexusReturnsFalse
            if report == '[]':
                log('info',f'Creating report with data key = {key}, value = {value}')
                cls._api.create_report(cls.runID, {key:value})
                return True #a report was created
        except Exception as e:
            log("warning",f"Unable to create Nexus report entry with {dict({key: value})}. Error: {e}")
            log("warning",traceback.format_exc())
        return False

    @classmethod
    def catch_null(cls, key, value) -> bool:
        if value in ['null', 'NULL', '', None] or np.isnan(value):
            log('info',f'update_report function received a value of {value} for key {key}. Skipping update.')
            return True
        return False

    @classmethod
    def update_metrics(cls, *args, **kwargs):
        '''
        Updates Nexus metrics using the Nexus API
        '''
        return cls._api.update_metrics(*args, **kwargs)    
    
    @classmethod
    def __getattr__( cls, name ):
        '''
        Get attributes for a Nexus object, if there are no attributes an exception is raised in that case
        '''
        try:
            return getattr(cls._api, name)
        except:
            print(f"type object 'Nexus' has no attribute '{name}'")
    
        return
