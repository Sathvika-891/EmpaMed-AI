import pickle
from langchain.tools import BaseTool
import os
class EmotionDetector(BaseTool):
    name: str= "EmotionDetector"
    description:str ="""Use this tool to analyze the user's messages and accurately detect their emotions. The primary emotions to identify include joy, sadness, anger, fear, and love.Follow the instructions given below

    Emotion Detection:
    Carefully analyze the user's language for emotional cues.
    Identify the predominant emotion from the following: joy, sadness, anger, fear, and love.

    Model Prediction:
    Respond empathetically based on the emotion predicted by the machine learning model.
    If the predicted emotion aligns with the context of the user's message, proceed with the suggested response.

    Verification:
    Recognize that as a machine learning model, predictions may occasionally be incorrect.
    Verify the predicted emotion against the user's message context. If they match, proceed. If there is a discrepancy, use your judgment to detect the accurate emotion.

    Responding with Empathy:
    Offer responses that demonstrate empathy and understanding.
    Provide emotional support tailored to the detected emotion.
    Use comforting words, encouragement, or advice to help the user feel supported and heard.
    After the tool completes these steps, you should use the retrieved information to generate a detailed and coherent response, including the results from the thought action and observation"""

    def __init__(
        self,
    ):
        super(EmotionDetector, self).__init__()

    def _run(self, emotion: str) -> str:
        print("in meotion detection")
        try:
            model_path=os.path.join(os.path.dirname(__file__), "../models", "SVM_Emotion_Detection_Model.pkl")
            with open(model_path,"rb") as f:
                model=pickle.load(f)
            vectoriser_path=os.path.join(os.path.dirname(__file__), "../models", "SVM_Emotion_Detection_Vectoriser.pkl")
            with open(vectoriser_path,"rb") as f:
                vectorizer=pickle.load(f)
            pred=model.predict(vectorizer.transform([emotion]))[0]
            print("Predicted emotion:{}".format(pred))
            return pred

        except Exception as e:
            print("An error occurred:", e)
            return e

    async def _arun(self, smiles: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError()
