from akorn.celery.couch import db_journals, db_store

for journal_id in db_journals:
  rows = db_store.view('index/journal_id', key=journal_id).rows

  if len(rows) == 0:
    journal = db_journals[journal_id]
    try:
      print "No articles for {}".format(journal['name'])
    except:
      print journal

