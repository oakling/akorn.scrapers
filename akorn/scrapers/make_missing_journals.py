from akorn.celery.couch import db_store, db_journals

print "Hello"

journal_id_map = {}

def make_journal(journal_name):
  doc = {'name': journal_name,
         'aliases': [journal_name],}

  doc_id, doc_rev = db_journals.save(doc)

  journal_id_map[journal_name] = doc_id

  return doc_id

for row in db_store.view('missing/journal_id', include_docs=True).rows:
  doc = row.doc
  if 'journal' in doc:
    print doc['journal']

    if doc['journal'] in journal_id_map:
      doc['journal_id'] = journal_id_map[doc['journal']]
      print "Re-using"
    else:
      doc['journal_id'] = make_journal(doc['journal'])
      print "Making new"

    db_store.save(doc)
