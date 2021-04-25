docker-build:
	DOCKER_BUILDKIT=0 docker build --tag eu.gcr.io/trial-shop/api:latest .

docker-run:
	docker run --publish 5000:8080 --publish 5001:9191 -d --name trial-shop-api eu.gcr.io/trial-shop/api:latest

docker-push:
	docker push eu.gcr.io/trial-shop/api

docker-clean:
	docker stop trial-shop-api
	docker rm trial-shop-api
	docker rmi eu.gcr.io/trial-shop/api:latest