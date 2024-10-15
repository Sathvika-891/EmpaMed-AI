from Bio import Entrez
from langchain.tools.base import BaseTool
from pydantic import BaseModel, Field
from typing import Optional, Type
from dotenv import load_dotenv
from langchain.callbacks.manager import AsyncCallbackManagerForToolRun, CallbackManagerForToolRun
class Get_PubMed_Papers(BaseTool):
    name: str = "Get_PubMed_Papers" 
    description: str = """
    Use this tool when you need to retrieve relevant research papers or resources related to specific medical queries from the PubMed database.
    The tool performs the following steps:
    1. Searches the PubMed database for the top relevant articles based on the given query.
    2. Retrieves detailed information about each article, including the title, abstract, and various identifiers.
    3. Constructs URLs for accessing the articles directly through DOI, PMC, and PubMed IDs.
    4. After the tool completes these steps, you should use the retrieved information to generate a detailed and coherent response, including the results from the thought action and observation

    """

    def search(self, query):
        mail = "abc@gmail.com"
        Entrez.email = mail  # Use your email address here
        handle = Entrez.esearch(db='pubmed',
                                sort='relevance',
                                retmax=5,
                                retmode='xml',
                                term=query)
        results = Entrez.read(handle)
        return results

    def fetch_details(self, id_list):
        ids = ','.join(id_list)
        mail = "abc@gmail.com"
        Entrez.email = mail  # Use your email address here
        handle = Entrez.efetch(db='pubmed',
                               retmode='xml',
                               id=ids)
        results = Entrez.read(handle)
        return results

    def get_urls(self, paper):
        urls = {}

        # Extract DOI if available
        if 'ELocationID' in paper['MedlineCitation']['Article']:
            for elocation in paper['MedlineCitation']['Article']['ELocationID']:
                if elocation.attributes.get('EIdType') == 'doi':
                    doi = elocation
                    urls['DOI'] = f"https://doi.org/{doi}"

        # Extract PMC ID if available
        if 'PubmedData' in paper and 'ArticleIdList' in paper['PubmedData']:
            for article_id in paper['PubmedData']['ArticleIdList']:
                if article_id.attributes.get('IdType') == 'pmc':
                    pmc_id = article_id
                    urls['PMC'] = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmc_id}"

        # Extract PubMed ID if available
        if 'PMID' in paper['MedlineCitation']:
            pmid = paper['MedlineCitation']['PMID']
            urls['PubMed'] = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}"

        return urls

    def _run(self, query: str) -> str:
        try:
            print("in pubmed tool")
            
            results = self.search(query)
            id_list = results['IdList']
            papers = self.fetch_details(id_list)
            articles = {}
            for i, paper in enumerate(papers['PubmedArticle']):
                if "Abstract" in paper['MedlineCitation']['Article']:
                    title = paper['MedlineCitation']['Article']['ArticleTitle']
                    abstract = paper['MedlineCitation']['Article']['Abstract']['AbstractText']
                    urls = self.get_urls(paper)
                    articles[i + 1] = {
                        "Title": title,
                        "Abstract": abstract,
                        "URLs": urls
                    }
            return articles
        except Exception as e:
            return str(e)

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError()
