run-local:
	docker build -t my-python-app .
	docker run -it --rm --name my-running-app my-python-app
test-local:
	docker build -f test/Dockerfile -t my-python-app-test .
	docker run -it my-python-app-test
