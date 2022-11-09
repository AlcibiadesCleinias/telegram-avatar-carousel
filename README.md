# telegram-avatar-carousel

With docker-compose you start using telethon and Redis (for session) with crontab task of rotating images 
from a [folder](telethon_user/src/data_avatars).

# Feature
- periodically **delete previous** photo about which app knows & **upload next** from the folder.
- store session in a file

# Start
- prepare `.env`
- start job with `docker-compose up -d`
- init telegram session from running docker container: 
`docker-compose run telethon_user sh -c "python main.py --init-session true"`
