import mesop as me
import mesop.labs as mel
from agent import EmpamedAI
def on_load(e: me.LoadEvent):
  me.set_theme_mode("system")

@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/",
  title="EmpaMedAI",
  on_load=on_load
)
def page():
    mel.chat(chat_completion, title="EmpaMedAI", bot_user="EmpaMedAI")

def chat_completion(query: str, history: list[mel.ChatMessage]):
    print("history",history)
    for chunk in EmpamedAI.generate_chat_response(query=query,history=history):
       yield chunk
      