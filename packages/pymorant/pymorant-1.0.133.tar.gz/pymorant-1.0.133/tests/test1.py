import sys
sys.path.append('/Users/artbrare/Documents/Morant/py_morant/src')

from pymorant import Chatbot, llm # noqa

llm.function_prueba()

chatbot = Chatbot("hola", "gpt-4", 2)
chatbot.vector_store_local(True)
