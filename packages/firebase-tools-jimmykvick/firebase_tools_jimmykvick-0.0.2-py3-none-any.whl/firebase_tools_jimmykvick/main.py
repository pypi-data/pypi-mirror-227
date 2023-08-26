def firestore_instance():
  from google.cloud import firestore
  db = firestore.Client(project="my-budged-dev")
  return db

def add_document(body):
  db = firestore_instance()
  doc_ref = db.collection("spend").document()
  doc_ref.set(body)
  print(F"Insert new document {doc_ref.id}")