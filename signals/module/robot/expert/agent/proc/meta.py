from typing import List 
from langchain.docstore.document import Document
from module.pretzl.model.gpt.llm import MeteredLLM as Convey 

class MetadataService:

    def __init__(
            self
        ):    
        self.user_type="low awareness and out of town tourist"
    
    def GenerateMetadataForDocument(
            self,
            documents:List[Document],
    )->str:
        model=Convey()
        if type(documents).__name__=='list':
            content='\n'.join([doc.page_content for doc in documents])
        elif type(documents).__name__=='bytes':
            content='\n'.join([doc for doc in documents])
        prompt= f"""You are an expert in creating tags that relate to the content in a document, and it's ontological subject heading. 
            Look at the document to create tags that will help a {self.user_type} gain insight and value by using term labeling. 
            An output will be a list of 10 tags or labels with no other text. They should be in a comma separated string. 
            For example, if the material covers a car it might output: ["make,model,series,engine,style,color,interior,transmission,miles,factory"]. 
            These tags will then be attached to each page of the document to help flassify the document pages for vector search based on questions from users. 
            Please analyze and generate tags for this content: {content}
            """
        resp=model.invoke(prompt)
        print("Tags Generated: ", resp)
        return resp 
    

    def GetMetadataForPage(
            self, 
            chunk, 
            generated_metadata:List[str]=None
    ):
        model=Convey()
        page_content=chunk.page_content 
        prompt=f"""You are an expert in creating tags for data classification in documents.
        You are looking at a single page within the document and need to apply all the tags that relate to the data on this page
        You should output a list of 10 tags with no other text. The tags should be in a comma separated string. 
        For example if the material covers a cart the output should look like: ["make,model,series,engine,style,color,interior,transmission,miles,factory"]
        These tags would then be attached to each page of the document to help classify the document pages for vector serach based on questions from the users.
        Here is the page content: {page_content}"""
        result=model.invoke(prompt)
        print("Tags assigned to page: ", result)
        return result 