from abc import ABC, abstractmethod

class DirectoryManager(ABC):
    def __init__(self, base_url):
        self.base_url = base_url

    @abstractmethod
    def get_input_r1_path(self):
        pass

    @abstractmethod
    def get_input_r2_path(self):
        pass

    @abstractmethod
    def get_input_ref_path(self):
        pass

    @abstractmethod
    def get_input_dada2_path(self):
        pass

    @abstractmethod
    def get_input_merger_path(self):
        pass

    @abstractmethod
    def get_output_denoise_path(self):
        pass

    @abstractmethod
    def get_output_merge_path(self):
        pass

    @abstractmethod
    def get_output_all_path(self):
        pass

    @abstractmethod
    def get_output_best_path(self):
        pass

    @abstractmethod
    def get_qc_report_path(self):
        pass

class QcDirectoryManager(DirectoryManager):
    def get_input_r1_path(self):
        return f'{self.base_url}denoiseResult/r1/'

    def get_input_r2_path(self):
        return f'{self.base_url}denoiseResult/r2/'

    def get_input_ref_path(self):
        return f'{self.base_url}mergeResult/merger/r1Ref/'

    def get_input_dada2_path(self):
        return f'{self.base_url}mergeResult/dada2/merged/'

    def get_input_merger_path(self):
        return f'{self.base_url}mergeResult/merger/merged/'

    def get_output_denoise_path(self):
        return f'{self.base_url}qcResult/validator/denoise/'

    def get_output_merge_path(self):
        return f'{self.base_url}qcResult/validator/merge/'

    def get_output_all_path(self):
        return f'{self.base_url}qcResult/validator/all/'

    def get_output_best_path(self):
        return f'{self.base_url}qcResult/validator/best/'

    def get_qc_report_path(self):
        return f'{self.base_url}qcResult/qcReport/'

    def get_qc_report_root_path(self):
        return f'{self.base_url}qcResult/'


