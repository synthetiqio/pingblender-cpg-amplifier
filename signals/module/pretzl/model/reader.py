from module.pretzl.control import PRETZL as ControlToggles
class Router:

    def get(
            ft: str
            ):
        isHealth:bool= ControlToggles.ToggleController().getSector(sector="HEALTH")
        print(f"READER : Router -- system reads filetype : {ft}")
        try:
            parse_set : dict = {}
            if ft == "vnd.openxmlformats-officedocument.spreadsheet.sheet" :
                parse_set = {
                    'dataformat' : 'EXCEL_10', 
                    'datareader' : 'PRETZL'            
                    }
            elif ft == "vnd.openxmlformats-officedocument.wordprocessingml.document":
                parse_set = {
                    'dataformat' : 'WORD_10', 
                    'datareader' : 'DocIntel'
                }
            elif ft == "vnd.familysearch.gedcom":
                parse_set = {
                    'dataformat':"GRIMM_GED", 
                    'datareader':"Mimeograph"
                }
            elif ft == "octet-stream":
                parse_set = {
                    'dataformat' : 'CODE_BODY', 
                    'datareader' : 'TextLoader'
                }
            elif ft == "pdf":
                parse_set = {
                    'dataformat' : 'PDF_PARSABLE', 
                    'datareader' : 'AFR'
                }
            elif ft == "msword":
                parse_set = {
                    'dataformat' : 'WORD_LEGACY', 
                    'datareader' : 'AFR'
                }
            elif ft == "vnd.ms-excel":
                parse_set = {
                    'dataformat' : 'EXCEL_9', 
                    'datareader' : 'PRETZL'
                }
            elif ft == "plain":
                parse_set = {
                    'dataformat' : 'TXT_TXT', 
                    'datareader' : 'TextLoader'
                }
            elif ft == "csv":
                parse_set = {
                    'dataformat' : 'CSV_TEXT', 
                    'datareader' : 'TextLoader'
                }
            elif ft == "json":
                parse_set = {
                    'dataformat' : 'JSON_TXT', 
                    'datareader' : 'TextLoader'
                }
            elif ft == "jpeg":
                parse_set = {
                    'dataformat' : 'IMG_JPEG', 
                    'datareader' : 'DocIntel'
                }
            elif ft == "png":
                parse_set = {
                    'dataformat' : 'IMG_PNG', 
                    'datareader' : 'DocIntel'
                }
            elif ft == "zip":
                parse_set = {
                    'dataformat' : 'ZIP_DOC',
                    'datareader' : 'PRETZL'
                }
                '''
                added conditional logic to separate and treat the use of the 
                EDI file formats for the healthcare industry. 
                resource:
                '''
            if isHealth is True and ft == "octet-stream":
                print("[PRETZL]: System Identfied EDI Form Data (State 0)")
                parse_set = {
                    'dataformat':'EDI', 
                    'datareader':'PRETZL'
                }
            print(parse_set)
            return parse_set
        except:
            raise TypeError("[PRETZL] - File type is unable to be processed.")
        
        
class Loader:

    pass