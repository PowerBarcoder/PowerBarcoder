"""
@file directory_manager.py
@brief This module defines abstract and concrete classes for managing directories
related to the QC process.
"""
from abc import ABC, abstractmethod

class DirectoryManager(ABC):
    """
    Abstract base class for directory managers.
    """
    def __init__(self, base_url):
        """
        Initialize the DirectoryManager with a base URL.

        :param base_url: The base URL for constructing directory paths.
        :type base_url: str
        """
        self.base_url = base_url

    @abstractmethod
    def get_input_r1_path(self):
        """
        Abstract method to get the input R1 path.

        :return: The input R1 path.
        :rtype: str
        """
        pass

    @abstractmethod
    def get_input_r2_path(self):
        """
        Abstract method to get the input R2 path.

        :return: The input R2 path.
        :rtype: str
        """
        pass

    @abstractmethod
    def get_input_ref_path(self):
        """
        Abstract method to get the input reference path.

        :return: The input reference path.
        :rtype: str
        """
        pass

    @abstractmethod
    def get_input_dada2_path(self):
        """
        Abstract method to get the input DADA2 path.

        :return: The input DADA2 path.
        :rtype: str
        """
        pass

    @abstractmethod
    def get_input_merger_path(self):
        """
        Abstract method to get the input merger path.

        :return: The input merger path.
        :rtype: str
        """
        pass

    @abstractmethod
    def get_output_denoise_path(self):
        """
        Abstract method to get the output denoise path.

        :return: The output denoise path.
        :rtype: str
        """
        pass

    @abstractmethod
    def get_output_merge_path(self):
        """
        Abstract method to get the output merge path.

        :return: The output merge path.
        :rtype: str
        """
        pass

    @abstractmethod
    def get_output_all_path(self):
        """
        Abstract method to get the output all path.

        :return: The output all path.
        :rtype: str
        """
        pass

    @abstractmethod
    def get_output_best_path(self):
        """
        Abstract method to get the output best path.

        :return: The output best path.
        :rtype: str
        """
        pass

    @abstractmethod
    def get_qc_report_path(self):
        """
        Abstract method to get the QC report path.

        :return: The QC report path.
        :rtype: str
        """
        pass

class QcDirectoryManager(DirectoryManager):
    """
    Concrete implementation of DirectoryManager for QC directories.
    """
    def get_input_r1_path(self):
        """
        Get the input R1 path.

        :return: The input R1 path.
        :rtype: str
        """
        return f'{self.base_url}denoiseResult/r1/'

    def get_input_r2_path(self):
        """
        Get the input R2 path.

        :return: The input R2 path.
        :rtype: str
        """
        return f'{self.base_url}denoiseResult/r2/'

    def get_input_ref_path(self):
        """
        Get the input reference path.

        :return: The input reference path.
        :rtype: str
        """
        return f'{self.base_url}mergeResult/merger/r1Ref/'

    def get_input_dada2_path(self):
        """
        Get the input DADA2 path.

        :return: The input DADA2 path.
        :rtype: str
        """
        return f'{self.base_url}mergeResult/dada2/merged/'

    def get_input_merger_path(self):
        """
        Get the input merger path.

        :return: The input merger path.
        :rtype: str
        """
        return f'{self.base_url}mergeResult/merger/merged/'

    def get_output_denoise_path(self):
        """
        Get the output denoise path.

        :return: The output denoise path.
        :rtype: str
        """
        return f'{self.base_url}qcResult/validator/denoise/'

    def get_output_merge_path(self):
        """
        Get the output merge path.

        :return: The output merge path.
        :rtype: str
        """
        return f'{self.base_url}qcResult/validator/merge/'

    def get_output_all_path(self):
        """
        Get the output all path.

        :return: The output all path.
        :rtype: str
        """
        return f'{self.base_url}qcResult/validator/all/'

    def get_output_best_path(self):
        """
        Get the output best path.

        :return: The output best path.
        :rtype: str
        """
        return f'{self.base_url}qcResult/validator/best/'

    def get_qc_report_path(self):
        """
        Get the QC report path.

        :return: The QC report path.
        :rtype: str
        """
        return f'{self.base_url}qcResult/qcReport/'

    def get_qc_report_root_path(self):
        """
        Get the QC report root path.

        :return: The QC report root path.
        :rtype: str
        """
        return f'{self.base_url}qcResult/'


