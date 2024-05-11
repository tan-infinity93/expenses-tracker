build:
	sudo docker build --no-cache --tag flask-expenses .;

run:
	sudo docker run --name flask-expenses -d -p 5000:5000 flask-expenses;

remove:
	sudo docker rm -f flask-expenses;

rebuild:
	sudo docker build --no-cache --tag flask-expenses .;
	sudo docker rm -f flask-expenses || true;
	sudo docker run --name flask-expenses -d -p 5005:5000 flask-expenses;

show-logs:
	sudo docker logs flask-expenses;

show-running-logs:
	sudo docker logs -f flask-expenses;

show-app:
	sudo docker ps -a | grep 'flask-expenses'

