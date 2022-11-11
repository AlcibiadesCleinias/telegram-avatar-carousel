# telegram-avatar-carousel

With docker-compose you start using telethon and Redis (for session) with crontab task of rotating images 
from a [folder](telethon_user/src/data_avatars).

# Feature
- periodically **delete previous** photo about which app knows & **upload next** from the folder.
- store session in a file
- telegram ecology: use telegram file id if already uploaded to telegram (checks via Redis)
- container with task rotation will not restart automatically to prevent ddos to login with fail. 

# Start
- prepare `.env` (you will need telegram API & hash from https://my.telegram.org/auth)
- start job with `docker-compose up -d`
- init telegram session from running docker container: 
`docker-compose run telethon_user --init-session true`

# Env
- TASK_RANDOM_DELAY_PERIOD: to prevent ban on telegram it makes some random delay after actual crontab task execution.

# Suggestion & Ban Warning
I experienced a ban after using 3 images to be rotated each minute. 
Thus, choose crontab accurately and access your risk deliberately.
