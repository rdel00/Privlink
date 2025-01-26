from app import db, URL
from datetime import datetime

# Delete all expired URLs
def cleanup_expired_urls():
    now = datetime.now()
    expired_urls = URL.query.filter(URL.expiration_date < now).all()

    for url in expired_urls:
        db.session.delete(url)

    db.session.commit()

if __name__ == '__main__':
    cleanup_expired_urls()

