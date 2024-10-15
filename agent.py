from langchain_together import ChatTogether
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.agents.initialize import initialize_agent
from tools.pubmed_tool import Get_PubMed_Papers
from tools.description_generator import Query2Description
from tools.emotion_detector import EmotionDetector
from dotenv import load_dotenv
import os
load_dotenv()
os.environ["TOGETHER_API_KEY"]=os.environ.get("TOGETHER_API_KEY")
class EmpamedAI:
    chat = ChatTogether(
        model="mistralai/Mixtral-8x22B-Instruct-v0.1",
        streaming=True, 
        callbacks=[StreamingStdOutCallbackHandler()])
    tools=[
        Query2Description(),
        EmotionDetector(),
        Get_PubMed_Papers()
        ]
    agent=initialize_agent(
        tools,
        chat,
        agent="structured-chat-zero-shot-react-description",verbose=True)
    
    
    @staticmethod
    def generate_chat_response(query,history):
        messages=[
                {"role": msg.role, "content": query if msg.role == "user" else msg.content}
                for msg in history
            ]
        yield EmpamedAI.agent.run(messages)
        
