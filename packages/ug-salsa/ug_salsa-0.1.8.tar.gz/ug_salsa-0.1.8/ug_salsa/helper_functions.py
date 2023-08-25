'''
File contains helper functions that may be used through multiple analysis modes or other scripts
'''

#%% Load Imports
import numpy as np
import pandas as pd
import scipy.io as sio
import traceback
import logging
import types
import functools
import time
import os
from datetime import datetime
import csv
from functools import wraps
import socket

import sys

#%% timing decorator
def timing(f):
    """
    Basic decorator for timing function calls and printing to stdout.
    """

    @wraps(f)
    def wrap(*args, **kw):
        ts = time.perf_counter()
        result = f(*args, **kw)
        te = time.perf_counter()
        print('func:%r args:[%r, %r] took: %2.4f sec' % (f.__name__, args, kw, te - ts))
        return result

    return wrap


#%% logging fn
def log(level: str, msg: str):
    time_str = time.strftime("%Y_%b_%d_%H_%M_%S", time.gmtime())
    level_dict = {'info': 20, 'warning': 30, 'exception': 40, 'critical': 50}
    lvl = level_dict[level]
    try:
        print(msg)
    except socket.error:
        # I think this only happens in Wing with remote dev, but it makes development harder.
        pass
    gen_logger = logging.getLogger('general_logger')
    gen_logger.log(lvl, msg)
    
    # logging.log(lvl, f"{time_str}: {msg}")

    if lvl >= 30:
        logger = logging.getLogger('exception_logger')
        logger.log(lvl, msg)
    return


#%% timing decorator
def report_runtime(num_layers: int = 0, log=False):
    '''
    Decorator to report function runtime.

    Notes:
    - When used with the exception_safeguard() decorator,
      report_runtime() should be called outside the exception decorator.
    '''

    def inner(func: types.FunctionType):
        padding = "    " * num_layers

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # args_repr = [repr(a) for a in args]
            # kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            # signature = ", ".join(args_repr + kwargs_repr)
            # print(f"{padding}Calling {func.__name__}({signature})")
            print(f"{padding}Calling {func.__name__}")
            if log:
                log('info', f"{padding}Calling {func.__name__}")
            start = time.perf_counter()
            results = func(*args, **kwargs)
            end = time.perf_counter()
            print(f"{padding}Finished running {func.__name__} in {end - start} seconds")
            if log:
                log(
                    'info',
                    f"{padding}Finished running {func.__name__} in {end - start} seconds",
                )
            return results

        return wrapper

    return inner


# class level timing decorator
def log_runtime_class_decorator(func: types.FunctionType):
    '''
    Decorator to log function runtime meant for use inside a class.

    Notes:
    - Class should have a params dict attr.
    - Should always be used on the outermost layer.
    '''

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        # get runtime
        start = time.perf_counter()
        results = func(self, *args, **kwargs)
        end = time.perf_counter()

        # log results
        new_row = [
            func.__qualname__,
            int(end - start) if (end - start) > 60 else np.round(end - start, 6),
        ]
        with open(f"{self.params['save_loc']}RunID{self.params['runid']}_rundmc_runtimes.csv", "a+") as file:
            writer = csv.writer(file)
            writer.writerow(new_row)
        return results

    return wrapper


#%% progress manager
class ProgressTracker:
    def __init__(self, runID, save_loc, total_analyses):
        self.runID = runID
        self.save_loc = save_loc
        self.completed = -1
        self.total = total_analyses

        start_time = datetime.timestamp(datetime.now())

        self.data = {
            'runID': self.runID,
            'total_analyses': self.total,
            'completed_analyses': self.completed,
            'progress': -1,
            'starttime': start_time,
            'timestamp': start_time,
            'Refbeads complete': False,
            'Templates complete': False,
            'TTEC complete': False,
            'Pipeline metrics complete': False,
            'Save complete': False,
        }

        return

    def update_progress(self):
        self.data['timestamp'] = datetime.timestamp(datetime.now())
        self.completed += 1
        self.data['completed_analyses'] = self.completed
        self.data['progress'] = np.round(100 * self.completed / self.total, 2)

        self.save_csv()
        return

    def Refbeads_completed(self):
        self.data['Refbeads complete'] = True
        self.update_progress()
        return

    def Templates_completed(self):
        self.data['Templates complete'] = True
        self.update_progress()
        return

    def TTEC_completed(self):
        self.data['TTEC complete'] = True
        self.update_progress()
        return

    def Pipeline_completed(self):
        self.data['Pipeline metrics complete'] = True
        self.update_progress()
        return

    def Save_completed(self):
        self.data['Save complete'] = True
        self.update_progress()
        return

    def save_csv(self):
        k = [k for k in self.data]
        v = [self.data[k] for k in self.data]
        df = pd.DataFrame().from_dict({"metric": k, "value": v})
        df.to_csv(f"{self.save_loc}progress.csv", header=False, index=False)
        return


#%% try catch decorator
def exception_safeguard(message: str = ''):
    '''
    First level decorator to catch exceptions as they arise.
    Prevents exceptions from killing downstream analysis.
    '''

    def inner(func: types.FunctionType):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                result = func(self, *args, **kwargs)
                return result
            except Exception as e:
                traceback.print_exc()
                error_msg = f"{func.__name__} raised exception {e}{f': {message}'*bool(message)}"
                print(error_msg)
                log('exception', error_msg)
                log('exception', traceback.format_exc())
                return

        return wrapper

    return inner


#%% try catch decorator for templates, catches keyerrors specifically
def template_exception_safeguard(message: str = ''):
    '''
    First level decorator to catch exceptions as they arise.
    Prevents exceptions from killing downstream analysis.
    Handles case where templates not found.
    '''

    def inner(func: types.FunctionType):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                result = func(self, *args, **kwargs)
                return result
            except KeyError as e:
                error_msg = (
                    f"Template {e.args[0]} not found, skipping analysis {func.__name__}"
                )
                print(error_msg)
                log('warning', error_msg)
                log('warning', traceback.format_exc())
                return
            except Exception as e:
                traceback.print_exc()
                error_msg = f"{func.__name__} raised exception {e}{f': {message}'*bool(message)}"
                print(error_msg)
                log('exception', error_msg)
                log('exception', traceback.format_exc())
                return

        return wrapper

    return inner

#%%
def format_decays(rate):
    return -100 * (np.exp(rate) - 1)


#%%
def MAPE(y, predicted):
    """
    Calculates the Mean Absolute Percent Error (MAPE) given a dataset y and fit values.

    y, predicted: np.ndarray of shape (N,)

    """
    return 100 * np.sum(np.abs((y - predicted) / y)) / y.shape[0]


#%%
def clean_output_folder(out_folder: str):
    if os.path.exists(out_folder):
        _, _, file_list = next(os.walk(out_folder))
        for file in file_list:
            os.remove(out_folder + file)
    return


#%%
def plot_sanity_check(data, name):
    inds = np.random.choice(range(data.shape[0]), 10, replace=False)
    y = data[inds, :]
    fig = plt.figure()
    for i in range(10):
        plt.plot(range(1, data.shape[1] + 1), y[i, :])
    fig.savefig(f"plots/template_{name}_sample.png")
    plt.close()
    return


#%%
def exp_fit(x, y):

    # Fits y = A*exp(bx) over non-nan values of y
    results = dict()
    results['x'] = x
    results['y'] = y
    log_y = np.log(y)
    positive_inds = np.where(~np.isnan(log_y))[0]
    b, log_a = np.polyfit(x[positive_inds], log_y[positive_inds], 1)
    fit_params = dict()
    fit_params['A'] = np.exp(log_a)
    fit_params['b'] = b
    results['fit_params'] = fit_params

    results['predicted'] = np.exp(log_a) * (np.exp(b * x))
    results['residuals'] = y - results['predicted']
    return results


#%%
def logistic_fit( x, y ):
    
    def logistic( x, L, r, k):
        return L*np.exp(r*x) + k

    results = dict()
    results['x'] = x
    results['y'] = y

    L_0 = np.max(y)
    r_0 = -1.0
    k_0 = np.min(y)

    popt, _ = curve_fit(
        logistic,
        x,
        y,
        p0=(L_0, r_0, k_0),
        bounds=[[0, -np.inf, -1000], [np.inf, 0, np.inf]],
        maxfev=10000,
    )

    fit_params = dict()
    fit_params['L'] = popt[0]
    fit_params['r'] = popt[1]
    fit_params['k'] = popt[2]
    results["fit_params"] = fit_params
    results['predicted'] = logistic(x,
                                    fit_params['L'],
                                    fit_params['r'],
                                    fit_params['k'])


    results['residuals'] = y - results['predicted']
    return results


#%%
# def merge_tilesDescriptions(params):
# if ('full_tile_csv' not in params) or ('tile_csv' not in params):
# raise FileNotFoundError

# full_td = pd.read_csv(params['full_tile_csv'])[['Theta','BeadsPerTile']]
# full_td.rename(columns={'BeadsPerTile':'FullBeadsPerTile'}, inplace = True)
# sampled_td = pd.read_csv(params['tile_csv'])

# merged_td = sampled_td.merge(full_td, how="left", on='Theta')
# return merged_td

#%%
class jupyter_io:
    def __init__(self, params, fname=None, save_loc=None, folder_path=None):
        self.params = params
        self.save_loc = (save_loc is not None) * (str(save_loc)) + (
            save_loc is None
        ) * (self.params['save_loc'])
        self.fname = (fname is not None) * (str(fname)) + (fname is None) * (
            'output_plots.ipynb'
        )
        self.converted_name = None
        self.folder_path = folder_path

        self.nb = nbf.v4.new_notebook()
        self.nb['cells'] = []
        return

    def add_text_cell(self, text):
        self.nb['cells'].append(nbf.v4.new_markdown_cell(text))
        return

    def add_code_cell(self, code):
        self.nb['cells'].append(nbf.v4.new_code_cell(code))
        return

    def create_ipynb(self):
        with open(self.save_loc + self.fname, 'w+') as f:
            nbf.write(self.nb, f)
        return

    def run_ipynb(self):
        result = os.system(
            f'jupyter nbconvert --to notebook --execute {self.save_loc + self.fname}'
        )
        self.converted_name = self.fname.split(".ipynb")[0] + ".nbconvert.ipynb"
        return result

    def to_html(self):
        if self.converted_name is None:
            self.run_ipynb()
        result = os.system(
            f'jupyter nbconvert {self.save_loc + self.converted_name} --to=html --TemplateExporter.exclude_input=False'
        )
        return result

    def clean_up(self):
        if os.path.exists(self.save_loc + self.converted_name):
            os.remove(self.save_loc + self.converted_name)
            self.converted_name = None
        if os.path.exists(self.save_loc + self.fname):
            os.remove(self.save_loc + self.fname)
        return

    def folder_to_html(self):
        if self.folder_path is None:
            log('info', "jupyter_io: No folder passed")
            return
        if not os.path.exists(self.folder_path):
            log('info', "jupyter_io: Folder does not exist")
            return

        _, _, fileList = next(os.walk(self.folder_path))
        fileList = [file for file in fileList if file.endswith(".png")]
        self.add_text_cell(f"""# Generated Plots for run {self.params['runid']}""")
        self.add_code_cell(f"""from IPython.display import Image""")
        for filename in fileList:
            self.add_code_cell(f"""Image(filename='{self.folder_path + filename}')""")

        self.create_ipynb()
        self.run_ipynb()
        self.to_html()
        self.clean_up()
        os.system(f'rm -rf {self.folder_path}')  # Linux
        return


#%%
class WriteData:
    def __init__(self, params):
        self.params = params
        return

    # takes a dictionary and writes to a csv
    def to_csv(self, input_data: dict, fname: str):
        # print("Saving CSV to " + params['save_loc'] + fname)
        if type(input_data) is dict:
            with open(self.params['save_loc'] + fname, 'w') as f:
                for key in input_data.keys():
                    f.write("%s,%s\n" % (key, input_data[key]))
        return

    # TODO unused?
    def to_s3(self, local_fname, upload_fname=''):

        if len(upload_fname) == 0:
            upload_fname = local_fname

        s3 = boto3.client('s3')
        try:
            logging.info(
                f"Uploading: {local_fname} -> {params['s3_bucket']+upload_fname}"
            )
            with open(local_fname, "rb") as f:
                s3.upload_fileobj(f, self.params['s3_bucket'], upload_fname)
                logging.info("Upload Successful")
            return True

        except FileNotFoundError:
            logging.info("The file was not found")
            return False

    def to_matfile(self, input_dict, filename, save_loc=None):
        if save_loc is None:
            save_loc = self.params['save_loc']
        try:
            sio.savemat(save_loc + filename, input_dict, appendmat=True)
        except:
            logging.info('WARNING: Unable to save ' + filename + ' intermediate file.')


#%%
