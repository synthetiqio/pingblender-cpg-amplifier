from langchain.text_splitter import CharacterTextSplitter 

class CharacterSplitter:
    @staticmethod
    def split(
        document, 
        chunk_size, 
        chunk_overlap
    ):
        runner = CharacterTextSplitter(
            separator="\n\n",
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap, 
            length_function=len, 
            is_separator_regex=False,
        )
        all_split=runner.split_documents(documents=document)
        return all_split