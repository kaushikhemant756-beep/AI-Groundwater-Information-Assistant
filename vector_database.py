
import faiss
import pickle
import os

from sklearn.feature_extraction.text import TfidfVectorizer


class GroundwaterDatabase:

    def __init__(self):

        self.vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        self.index = None
        self.chunks = []

    def create_database(self, chunks):

        if not chunks:
            raise ValueError("No PDF chunks available.")

        self.chunks = chunks

        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        vectors = self.vectorizer.fit_transform(
            texts
        ).toarray()

        vectors = vectors.astype("float32")

        self.index = faiss.IndexFlatL2(
            vectors.shape[1]
        )

        self.index.add(vectors)

        return len(chunks)

    def search(self, question, top_k=3):

        if self.index is None:
            raise ValueError(
                "Please create database first."
            )

        query_vector = self.vectorizer.transform(
            [question]
        ).toarray().astype("float32")

        if query_vector.sum() == 0:
            return []

        top_k = min(top_k, len(self.chunks))

        distances, indices = self.index.search(
            query_vector, top_k
        )

        results = []

        for index in indices[0]:

            if index >= 0:

                results.append(
                    self.chunks[index]
                )

        return results

    def save_database(self, folder="data/database"):

        os.makedirs(folder, exist_ok=True)

        faiss.write_index(
            self.index,
            os.path.join(folder, "groundwater.index")
        )

        with open(
            os.path.join(folder, "groundwater.pkl"),
            "wb"
        ) as file:

            pickle.dump(
                {
                    "vectorizer": self.vectorizer,
                    "chunks": self.chunks
                },
                file
            )

    def load_database(self, folder="data/database"):

        self.index = faiss.read_index(
            os.path.join(folder, "groundwater.index")
        )

        with open(
            os.path.join(folder, "groundwater.pkl"),
            "rb"
        ) as file:

            saved_data = pickle.load(file)

        self.vectorizer = saved_data["vectorizer"]
        self.chunks = saved_data["chunks"]
