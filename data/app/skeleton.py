import uuid

import chromadb


class Skeleton:
    # this creates a folder on your local machine to store embeedings safely
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.client.get_or_create_collection(name="user_resume")

    def remember(self, resume_content):  # saves the cv into the database
        """Adds your resume to the memory"""
        # giving each memory a unique fingerprint so they never get lost
        unique_id = str(uuid.uuid4())
        self.collection.add(documents=[resume_content], ids=[unique_id])

    def recall(self):  # fetches the cv from the database
        """Bring back the most recent version of your story"""
        memories = self.collection.get()  # gets the most recent cv from the database
        if memories["documents"]:  # return the first document you found
            return memories["documents"][0]
        return "The skeleton has no memory of your resume. Sorry!"
