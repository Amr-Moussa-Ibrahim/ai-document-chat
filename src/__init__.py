"""AI Document Chat - source package.

This folder holds the 'brain' of the app, split into small, easy-to-read files:
    document_loader.py -> reads your files and cuts them into small chunks
    embeddings.py      -> turns text chunks into numbers the AI understands
    vector_store.py    -> stores those numbers and finds the most relevant ones
    chatbot.py         -> ties it all together and writes the final answer
"""
