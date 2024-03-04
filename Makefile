run-local:
	docker build -t concurrent-queue .
	docker run -it --rm --name concurrent-queue concurrent-queue
test-local:
	docker build -f test/Dockerfile -t concurrent-queue-test .
	docker run -it concurrent-queue-test
