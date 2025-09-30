from typing import List
from langchain.docstore.document import Document 
from module.robot.control import LLM

class Human:


    def __init__(
            self
        ):
        return 
    

    def metaForDocument(
            self, 
            docs: List[Document]
        )->str:
        mod = LLM

        if type(docs).__name__ == "list":
            content = "\n".join([doc.page_content for doc in docs])
        elif type(docs).__name__ == "bytes":
            content = "\n".join([doc for doc in docs])

        prompt = f"""You have cultivated precise expertise in generating tags to help label and categorized documents \
              based on their use in special capacities for communicating to individuals, small businesses, US federal \
              government agencies, and enterprise commercial entities about the value or status of a transaction, or updated \
              information related to the status of a transaction. For example, in order to submit tax information to \
              the US Government about my individual income tax calculations, and expected payment or refund, I need \
              to supply the IRS with a complete US Standard IRS Form 1040. You should output a list of 10 tags without any \
              additional text. Tags should be separated by a comma. For example, if this document is about a restaurant \
              transaction, list each of the itemized meals in a comma separated output, with each item enclosed in single\
              quotation marks, and the whole list encapsulated in a sigle pair of brackets,  which resembles: \
              ['burger', 'fries', 'drink', 'hot dog', 'ice cream sundae', 'cheese sticks']. 
              The list will then be attached to each page to help classify the document pages for vector searches with \
              inputs provided by users for streamlining semantic procedures to provide better answers. 
              Please analyze and create these tags based on this: {content}"""
        
        response = mod.invoke(prompt)
        print(f'Received these DOCUMENT tags as a response from robot : {str(response)}')
        return response
    

    def metaForPage(
            self, 
            chunk, 
            gen_meta : List[str] = None
        )->str:
        mod = LLM
        page = chunk.page_content
        prompt = f"""

        """
        response = mod.invoke(prompt)
        print(f'Received these PAGE tags as a response from robot : {str(response)}')
        return response

            