import pandas as pd 
class Helper:

    @staticmethod
    def read_datafile(
        file_path,
        file_format,
    ):
        if file_format=='CSV':
            datafile=pd.read_csv(file_path)
            return datafile
    
    @staticmethod
    def get_confidenceindex(confidence):
        ALL_CONFIDENCE= ['Unknown', 'Low', 'Medium', 'High']
        return ALL_CONFIDENCE.index(confidence)