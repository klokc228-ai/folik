Production DB & deploy notes

1) Backup existing production data (mandatory)

# on production server, in project dir:
python manage.py dumpdata --natural-foreign --natural-primary --exclude auth.permission --exclude contenttypes > /tmp/folik_prod_backup.json

Download `/tmp/folik_prod_backup.json` to safe location.

2) Remove SQLite from repo (already done): `.gitignore` includes `db.sqlite3` and it has been removed from git index.

3) Use environment DATABASE_URL on production

Set `DATABASE_URL` env var on production, e.g. for Postgres:

DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/DBNAME

4) Apply migrations on production (after pull and env configured):

python manage.py migrate

5) Restore data if needed:

python manage.py loaddata /tmp/folik_prod_backup.json

6) Notes for Cloudinary

Ensure `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET` are set in prod env.

7) Rollback plan

Keep the JSON backup and don't remove it until you confirm site works and data is present.
