import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.ApplicationDefault()

firebase_admin.initialize_app(cred, {
    "projectId": os.environ.get("PROJECT_ID")
})


class FirestoreIO:

    def __init__(self):
        self.db = firestore.client()

    def list(self, collection):
        users_ref = self.db.collection(collection)
        docs = users_ref.stream()
        docs_dict = []
        for doc in docs:
            doc_dict = doc.to_dict()
            doc_dict['id'] = doc.id
            docs_dict.append(doc_dict)
        return docs_dict

    def get(self, collection, doc_id):
        doc = self.db.collection(collection).document(doc_id).get()
        doc_dict = doc.to_dict()
        if not doc_dict:
            return None
        doc_dict.update({'id': doc.id})
        return doc_dict

    def insert(self, collection, data, id=None):
        if id:
            doc_ref = self.db.collection(collection).document(id)
        else:
            doc_ref = self.db.collection(collection).document()
        doc_ref.set(data)
        doc_dict = doc_ref.get().to_dict()
        if not id:
            doc_dict.update({'id': doc_ref.id})
        return doc_dict

    def update(self, collection, doc_id, data):
        doc_ref = self.db.collection(collection).document(doc_id)
        doc_ref.update(data)
        doc_dict = doc_ref.get().to_dict()
        doc_dict.update({'id': doc_ref.id})
        return doc_dict

    def delete(self, collection, doc_id):
        doc_ref = self.db.collection(collection).document(doc_id)
        doc_ref.delete()
        return

    def search(self, collection, key, value):
        docs_dict = []
        docs = self.db.collection(collection).where(key, u'==', value).stream()
        for doc in docs:
            doc_dict = doc.to_dict()
            doc_dict['id'] = doc.id
            docs_dict.append(doc_dict)
        return docs_dict
