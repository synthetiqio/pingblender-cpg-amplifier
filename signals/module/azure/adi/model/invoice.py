import logging
from core.auth.control import MeterController as ModelControl
import ast, json

class SummaryChatQuestions:
    """
    @summaryChatQuestions: runs the prompt to assure that the data which is analyzed understands the outcomes summarily.
    """
    
    key_points = """
                The list of columns is {columns}. Exclude columns with similar prefix like table_items that have multiple records in a single document.
                Task: Write 3 simple questions, include column names, that woudl summarize the invoice statements. No Explanation.
                Example: Unique, Count, Sum, top etc based questions. 
                Response: JSON Structure {{"Short Title of the Key Point": "Generated Question"}}
                """
    summarize= """
                Exclude information about any dataframe cleaning or issues occured. Only Summarize the useful facts in less than 3 sentences: {key_points}
               """
    
    

    def __init__( 
            self, 
            agent, 
            columns,
    ):
        self.agent= agent
        self.columns= columns

    def get_agent_response(
            self, 
            query
    ):
        response= self.agent.invoke(query)
        output= response['output']
        return output
    

    def get_graffiti_chat_response(
            self, 
            query
    ):
        output = ModelControl.llmjson.invoke(query)
        return json.loads(output.dict()['content'])
    
    def get_key_points(
            self
    ):
        prompt= SummaryChatQuestions.key_points.format(
            columns=self.columns
            )
        generated_questions= self.get_graffiti_chat_response(prompt)
        key_points= {}
        for key, question in generated_questions.items():
            key_points[key] = self.get_agent_response(question)
        return key_points
    

    def get_summary_response(
            self,
    ):
        key_points= self.get_key_points()
        summarization_prompt= SummaryChatQuestions.summarize.format(
            key_points=", ".join(key_points.values()))
        response = ModelControl.llm.invoke(summarization_prompt)
        output= response.dict()['content']
        return output
    

class SummaryDocQuestions:

    title="Invoice Summary Document"
    key_points= """
                List of columns as {columns}. Exclude columns with similar prefix like table_items are table details with multiple records.
                Task: Write 3 informational questions that generate aggregated metrics. No Explanation. 
                Example: Invoice Total, No. of Invoice IDs, Total Tax
                Response: JSON structure {{"Short Title of the Key Point": "Generated Question"}}

                """
    table_items= """
                LIst Columns as {columns}. Exclude company_name, Columns with similar prefix like table_items that have multiple records in a single document.
                Task: Write 1 question that would generate aggregated tabular information. No Explanation."
                Response: JSON structure with key table_items - {{"table_items": "Generated Question"}}
                """
    agent_prompt= """If unable to solve or error appears, say - Error"""

    def __init__(
            self, 
            agent, 
            columns
    ):
        self.agent = agent
        self.columns = columns

    def get_agent_response(
            self, 
            query
    ):
        response= self.agent.invoke('{}'.format(query))
        output= response['output']
        return output
    

    def get_graffiti_chat_response(
            self, 
            query
    ):
        output = ModelControl.llmjson.invoke(query)
        response = json.loads(output.dict()['content'])
        logging.info(response)
        return response
    
    def get_title(self):
        return SummaryDocQuestions.title
    
    def get_key_points(
            self
    ):
        prompt= SummaryDocQuestions.key_points.format(
            columns=self.columns
        )
        generated_questions= self.get_graffiti_chat_response(prompt)
        key_points={}
        for key, question in generated_questions.items():
            key_points[key]= self.get_agent_response(question)
        return key_points
    
    def get_table_items(
            self
    ):
        prompt = SummaryDocQuestions.table_items.format(
            columns=self.columns
            )
        generated_question= self.get_graffiti_chat_response(
            prompt
            )
        question = generated_question['table_items']
        prompt= f"Output: List of List only with the first record as \
            the name of the field headers followed by real records."
        return self.get_agent_response(query=f'{question}{prompt}')
    
    
    def get_summary_response(
            self,
    ):
        output={}
        output['title']= self.get_title()
        output['key_points'] = self.get_key_points()
        output['table_items']= self.get_table_items()
        logging.info(output)
        return output


class SourceSummaryDocQuestions:
    title=  "Summary Document - {title}"
    key_points= """
            List of coulumns as {columns}. Exlude columns with similar prefix like the table_items that have multiple records in a single document.
            Task: Write 5 informational questions which generate important summary metrics, like Key Performance Indicators. No Explanation. 
            Response: JSON structure {{'Short Tile of the Key Point': "Generated Question"}}
            """
    agent_prompt= """If unable to solve or error appears, say - Error"""

    def __init__(
        self, 
        agent, 
        columns, 
        file_name
    ):
        self.agent = agent
        self.columns = columns
        self.file_name = file_name

    def get_agent_response(
            self, 
            query
    ):
        response= self.agent.invoke('{}. {}'.format(
            query, 
            SummaryDocQuestions.agent_prompt)
        )
        output= response['output']
        return output
    
    def get_graffiti_chat_response(
            self, 
            query
    ):
        output = ModelControl.llmjson.invoke(query)
        return json.loads(output.dict()['content'])
    
    def get_title(
            self
    ):
        return SourceSummaryDocQuestions.title.format(title=self.file_name)
    
    def get_key_points(
            self
    ):
        prompt= SourceSummaryDocQuestions.key_points.format(columns=self.columns)
        generated_questions = self.get_graffiti_chat_response(prompt)
        key_points={}
        prompt= "Output: Under 20 words. In case of computation errors say - Error"
        for key, question in generated_questions.items():
            query= prompt + '\n' + question
            key_points[key]= self.get_agent_response(query)
        return key_points
    
    def get_summary_response(
            self
    ):
        output= {}
        output['title']= self.get_title()
        output['key_points']= self.get_key_points()
        return output