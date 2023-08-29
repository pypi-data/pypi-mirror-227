import logging
import pandas as pd
import sys
from threading import Thread
import uproot


logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(asctime)s %(name)s [%(levelname)s] (%(threadName)-10s) %(message)s',)
logger = logging.getLogger(__name__)

class Root_to_DataFrame_MT(Thread):
    """
    A class that uses MultiThreading to collect trees from a .root file
    and converts them to Pandas dataframe. 
    It inherits from threading.Thread class to perform multithreading.
    Methods have been implemented to save dataframes to and load dataframes from hdf5 files.
    """
    def __init__(self,file_name, get_sipm=False, tree_names = ['Tree_Laser','Tree_R11065','Tree_SiPM']):
        Thread.__init__(self)
        self.tree_names = tree_names
        self.get_sipm = get_sipm
        self.file_name = file_name
        self.file_type = 'root'
        if not get_sipm and "Tree_SiPM" in self.tree_names:
            tree_names.remove('Tree_SiPM')
            setattr(self, 'Tree_SiPM', None)

    def run(self):
        """
        Overridden method of threading.Thread class.
        Run when start() method is called on an instance of the class.
        """
        if self.file_type == 'root':
            with uproot.open(self.file_name) as file:
                logger.info(f"Opening {self.file_name}")
                workers = []
                for tree_name in self.tree_names:
                    workers.append(Thread(target=setattr,args=(self,tree_name,
                                                               self.get_tree(file, tree_name))))
                for worker in workers:
                    worker.start()
                for worker in workers:
                    worker.join()
        elif self.file_type == 'hdf5':
            logger.info(f"Opening {self.file_name}")
            workers = []
            for tree_name in self.tree_names:
                    workers.append(Thread(target=setattr,args=(self,tree_name,
                                                               pd.read_hdf(self.file_name,key=tree_name))))
            for worker in workers:
                worker.start()
            for worker in workers:
                worker.join()
        else:
            raise NotImplementedError(f"Loading {self.file_type} files is not supported")

    def get_tree(self, file, tree_name):
        """
        Get a specific tree from .root file currently open with uproot.
        _file_ argument must be instance of uproot.ReadOnlyFile class.

            Parameters:
                    file (uproot.ReadOnlyFile): file to extract trees from
                    tree_name (str): name of tree to extract

            Returns:
                    pandas.DataFrame containing tree data. Array entries have been converted into numpy.ndarray objects.
        
        """
        logger.info(f"Fetching {tree_name} from {self.file_name}")
        return pd.DataFrame(file[tree_name].arrays(library='np'))
        
    def to_dfs(self, save_as=None):
        """
        Saves stored dataframes in a hdf5 file format.
        DataFrame keys in the .h5 file will be the tree names.

            Parameters:
                    save_as (str): name of file to save to. If none and self.file_name ends in '.root',
                                    the extension will be substituted by '.h5'.
        """
        for tree_name in self.tree_names:
            df = getattr(self,tree_name)
            
            if not save_as and self.file_name.endswith(".root"):
                save_as = self.file_name.rstrip(".root") + ".h5"
            df.to_hdf(save_as,key=tree_name)
    
    @classmethod
    def from_hdf(cls, file_name, get_sipm=None, tree_names=None):
        """
        Create instance of class that extracts trees from .h5 file. Tree names must match keys in hdf5 file.
        Sets file_type to 'hdf5'.
        
            Parameters:
                    file_name (str): file name to extract trees from
                    get_sipm (bool): if Tree_SiPM in list of tree names (tree_names arg), 
                                     this bool determines whether to return the dataframe (True) or None (False)
                    tree_names (iterable of str): names of trees to extract 

            Returns:
                    instance (Root_to_DataFrame_MT): instance of class. DataFrames are not loaded yet.
        """
        _args = dict(get_sipm=get_sipm,tree_names=tree_names)
        args = {key:value for (key,value) in _args.items() if value}
        instance = cls(file_name,**args)
        instance.file_type = 'hdf5'
        return instance
    
if __name__=="__main__":
    """
    Run Example if executed as main
    """
    dfs = Root_to_DataFrame_MT("BC0174_SPE1500VLaserTrig_small.root")
    dfs_ups = Root_to_DataFrame_MT("BC0174_SPE1500VLaserTrigUPS_small.root")

    logger.info("Loading trees...")
    dfs.start()
    dfs_ups.start()
    
    dfs.join()
    dfs_ups.join()
    logger.info("Done")

    logger.info(dfs.Tree_Laser)
    logger.info(dfs_ups.Tree_R11065.RawWaveform)