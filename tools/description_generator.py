from langchain_community.tools import DuckDuckGoSearchResults
from langchain.tools.base import BaseTool

class Query2Description(BaseTool):
    name: str = "Query2Description"
    description: str = """Use this tool when you have to Identify and Explain Health Terms:
    When a user mentions a health-related term or condition, provide a clear and concise explanation of it.
    Offer additional relevant information, such as common symptoms, causes, treatment options, and any preventive measures if applicable."""
    

    def _run(self, query: str) -> str:
        print("in query to description")
        try:
            search = DuckDuckGoSearchResults()
            return search.run(query)
        except Exception as e:
            print("An error occurred:", e)
            return str(e)

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError()
