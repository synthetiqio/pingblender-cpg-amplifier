from langchain.text_splitter import RecursiveCharacterTextSplitter

class RecursiveSplitter:
    
    
    @staticmethod
    def split(
        document, 
        chunk_size, 
        chunk_overlap
    ):
        runner= RecursiveCharacterTextSplitter(
            #separators=separators, 
            #keep_separator=False,
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap
        )
        allsplits=runner.split_documents(document)
        return allsplits 
    

    @staticmethod
    def afr_split(
        document,
        chunk_size, 
        chunk_overap,
    ):
        print('RECURSE AFR Running')
        return document