# ChatWithLocalAI

## How to use
1. Install and run OLLAMA
2. Run a redis docker container.
* sudo docker run -d --rm -p 6378:6379 redis:8
3. Run a Django Application
* source DjangoChannel/.venv/bin/activate
* cd ./DjangoChannel
* python manage.py runserver
4. Run npm dev server
* cd Djangochannel/React/FrondEnd
* npm run dev
5. Access to the page
* Open a browser and type "localhost:5173"