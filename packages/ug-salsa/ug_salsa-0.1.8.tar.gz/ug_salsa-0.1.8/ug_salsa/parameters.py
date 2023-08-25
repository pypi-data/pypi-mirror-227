#%% Load imports
import numpy as np
import os
import configparser
import argparse
import logging
from collections import UserDict

#%% helper fns
class ExtraKeyError(Exception): pass

def ends_in_slash(path: str):
    return path + '/'*(not path.endswith('/'))   

#%% Shared parameters class
class Parameters(UserDict):
    
    _params = {}
    
    def __new__(cls): #singleton functionality
        if not hasattr(cls, 'instance'):
            cls.instance = super(Parameters, cls).__new__(cls)
            cls.instance.parse_arguments()
            cls.data = cls._params
        return cls.instance
    
    def __init__(self):
        self.data = self._params
        return

    def parse_arguments(self):
        # Command line arguments, highest priority
        parser = self.get_ArgParser()
        args = parser.parse_args()
        args = vars(args)
        
        # file arguments, medium priority
        file_args = self.read_params_file(args.get('paramsFile'))
        for key in ['base_in', 'base_out', 'save_loc']:
            if not args[key]:
                args[key] = file_args.get(key, '')
        
        # default params, low priority
        defaults = {}
        defaults.update(self.get_static_defaults())
        defaults.update(self.get_dynamic_defaults(args['runid'],
                                                  base_in = args.get('base_in'),
                                                  base_out = args.get('base_out'),
                                                  save_loc = args.get('save_loc')))
        
        # verify and clean args
        bad_keys = [key for key in file_args if key not in defaults]
        if bad_keys:
            raise ExtraKeyError(f"Unrecognized keys in paramsFile: {bad_keys}")
        args = {k:v for k,v in args.items() if (v != '') and (v is not None)}
        
        # Update params in order of importance
        self._params.update(defaults)
        self._params.update(file_args)
        self._params.update(args)
        
        # Verify folder paths end in slash
        self._params['base_in'] = ends_in_slash(self._params['base_in'])
        self._params['base_out'] = ends_in_slash(self._params['base_out'])
        self._params['save_loc'] = ends_in_slash(self._params['save_loc'])
        
        return
    
    def set_up_logging(self):
        formatter = logging.Formatter('%(asctime)s: %(levelname)s - %(message)s')
        
        handler = logging.FileHandler(self._params['save_loc'] + f"RunID{self._params['runid']}_rundmc_log.txt")
        handler.setFormatter(formatter)
        logger = logging.getLogger('general_logger')
        logger.setLevel(level=logging.INFO)
        logger.addHandler(handler)        
        
        error_handler = logging.FileHandler(self._params['save_loc'] + f"RunID{self._params['runid']}_rundmc_log_exceptions.txt")
        error_handler.setFormatter(formatter)
        logger = logging.getLogger('exception_logger')
        logger.setLevel(level=logging.WARNING)
        logger.addHandler(error_handler)
        return
    
    def get_ArgParser(self):
        dynamic_params = self.get_dynamic_defaults('')
        static_params = self.get_static_defaults()
        
        parser = argparse.ArgumentParser()
        
        for key in static_params:
            parser.add_argument(f"--{key}", type = type(static_params[key]),
                                required = False)
        
        for key in dynamic_params:

            parser.add_argument(f"--{key}", type = type(dynamic_params[key]),
                                required = False, default = '')
            
        return parser    

    def read_params_file(self,filepath: str):
        if filepath is None or not os.path.isfile(filepath):
            return {}
        
        config = configparser.ConfigParser(allow_no_value=True)
        config.optionxform = str
        config.read(filepath)
        config.sections()
        section='RunDMC'
        
        file_params = {}
        try:
            for key, value in config.items(section):
                if str(value).isdigit():
                    value = int(value)
                else:
                    try:
                        value = float(value)
                    except ValueError:
                        pass
                file_params[key] = value
        except configparser.NoSectionError:
            raise configparser.NoSectionError("WARNING: Params file found, but section 'RunDMC' does not exist.")
        return file_params    
    
    def load_defaults(self, runID: str, base_in: str = '', base_out: str = '', save_loc: str = ''):
        defaults = {}
        defaults.update(self.get_static_defaults())
        defaults.update(self.get_dynamic_defaults(runID,
                                                  base_in = base_in,
                                                  base_out = base_out,
                                                  save_loc = save_loc))
        self._params.update(defaults)
        return
    
    def get_static_defaults(self):
        '''
        
        '''
        params = {}
        

        params["do_rb_analysis"] = True
        params["do_tmpl_analysis"] = True
        params["do_ec_analysis"] = True
        params["do_fwhm_analysis"] = True
                
        # Ref bead params
        params['max_refbead_cv'] = 0.15 # max CV for reference beads
        params['min_preamble_mean'] = 1000
        params['refbeads_nflows'] = [1,200]
        params['find_all_refbeads'] = 0 # set to 1 for entire binary file 
        params['refbeads_nsamples'] = int(1.5e8) # should be ~ 1.5e8 during actuial implementation 
        params['bead_loss_threshold'] = 500
        params['beadLoss_min_gradient'] = 1000
        params['flicker_count_threshold'] = 40
        params['tile_CV_threshold'] = 0.15
        params['tile_var_threshold'] = 0.2 # max fraction of flow/flow change in signal per tile 
        params['pixel_size'] = 0.319552849057432 # only for V's # NOTE: this value is in microns. load in pixel size from file in the future.
        #params['pixel_size'] = 0.43 # only for W's # NOTE: this value is in microns. load in pixel size from file in the future.
        #params['pixel_size'] = 5/16 # only for X's # NOTE: this value is in microns. load in pixel size from file in the future.
        params['min_bead_density'] = 1e5, # low/no loading threshold for loading density (in beads/mm2)
        params['s3_bucket'] = 'ultimagen-rundmc'
        params['paramsFile'] = ''
        params['send_nexus_html'] = False
        #params['skip_plots'] = False
        
        # data loading experimental
        params['refbead_max_flow'] = 'max'
        
        # Template params
        params['flow_order'] = 'TGCA'
        params['load_template_assignments'] = True
        params['Nbead_sample_templates'] = 10**6
        params['TemplateCorrLength'] = 444
        params['TemplateCorrThresh'] = [0.7, 0.8] # threshold for correlation against template, [against TK, against med]
        params['signal_dtype'] = np.float16
        params['bead_size_dtype'] = np.int8
        params['standard_templates'] = ['TFSA1', 'TFSA2'] # New templates will be TFSA1 and TFSA2
        params['STS_benchmark_flows'] = [136, 200, 300, 400]
        params['floor_template'] = 'TFSA1'
        params['desert_template'] = 'TFSA1'
       
        params['template_list_file'] = os.path.join(os.path.dirname(__file__),'templates_names.csv')
        params['TNS_templates'] = ['TFSA1',"TFSA2"]
        params['tool_noise_length'] = 136
        params['tool_noise_RMS_fraction'] = 0.8
        params['tool_noise_low_std_percentile'] = 30
        params['rundmc_path'] = os.path.dirname(__file__)
        
        # TTEC params
        params["linearity_max_hmer"] = 6
        params["linearity_count_thresh"] = 200
        params['Nbead_sample_ec'] = 4 * 10**6
        params["ttec_phasing_sample_size"] = 2 * 10**6
        params["ttec_phasing_nbeads_for_phasing"] = 30_000
        params["ttec_phasing_min_beads_per_tile"] = 20
        params["ttec_phasing_enrichment_threshold"] = 0.32
        
        # config params
        params['nexus_conf'] = '/home/pyphot/.nexus.conf'
        
        return params
    
    def get_dynamic_defaults(self,
                             runID: str,
                             base_in: str = '',
                             base_out: str = '',
                             save_loc: str = ''):
        params = {}
        params['runid'] = runID
        params['base_in'] = ends_in_slash(f"/data/Runs/{runID}/sam/input/"*(not base_in) + base_in)
        params['base_out'] = ends_in_slash(f"/data/Runs/{runID}/sam/output/"*(not base_out) + base_out)
        params['save_loc'] = ends_in_slash(params['base_out']*(not save_loc) + save_loc)
        
        params['tile_csv']= params['base_in'] + 'FolderInfoZP_tilesDescription.csv'
        params['full_tile_csv']= params['base_in'] + 'FolderInfoZP_tilesDescription_full.csv'
        params['phot_file'] = params['base_in'] + 'photometry_misc.txt'
        params['aggregate_html'] = params['save_loc'] + f"RunID{params['runid']}_plots.html"

        return params
    
#%% Testing block
if __name__ == "__main__":
    from pprint import pprint
    p = Parameters()
    p.parse_arguments()
    pprint(p._params)
    print()