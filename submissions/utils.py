import psycopg2
from django.conf import settings

def log_to_redshift(username, file_name):
    try:
        conn = psycopg2.connect(
            dbname=settings.REDSHIFT_CONFIG['NAME'],
            user=settings.REDSHIFT_CONFIG['USER'],
            password=settings.REDSHIFT_CONFIG['PASSWORD'],
            host=settings.REDSHIFT_CONFIG['HOST'],
            port=settings.REDSHIFT_CONFIG['PORT']
        )
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO submissions (username, file_name, timestamp) VALUES (%s, %s, CURRENT_TIMESTAMP)",
            (username, file_name)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Redshift logging failed: {e}")
