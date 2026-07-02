import chromadb


class Skeleton:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.client.get_or_create_collection(name="user_resume")

    def remember(self, resume_content):
        """Saves CV into ChromaDB"""
        self.collection.upsert(  # Changed from add to upsert
            documents=[resume_content], ids=["my_resume"]
        )

    def recall(self):
        result = self.collection.get(ids=["my_resume"])

        print(result)

        if not result or not result["documents"]:
            print("No resume data found!")
            return ""

        return result["documents"][0]

    def stitch(self, template, summary, skills, experience):
        """Final assembly of LaTeX strings"""
        final_cv = template.replace("[SUMMARY]", summary)
        final_cv = final_cv.replace("[SKILLS]", skills)
        final_cv = final_cv.replace("[EXPERIENCE]", experience)

        # Emergency backup fix for common LaTeX breakers - as this happens when ai generates content
        final_cv = final_cv.replace("C#", "C\\#").replace(" %", " \\%")
        return final_cv
