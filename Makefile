# DEV
build_dev:
	docker-compose -f docker-compose.dev.yml build

up_dev:
	docker-compose -f docker-compose.dev.yml up -d

down_dev:
	docker-compose -f docker-compose.dev.yml down



# LOCAL PROD
build_local_prod:
	docker-compose -f docker-compose.prod.yml -f docker-compose.local_prod.yml build

up_local_prod:
	docker-compose -f docker-compose.prod.yml -f docker-compose.local_prod.yml up -d

down_local_prod:
	docker-compose -f docker-compose.prod.yml -f docker-compose.local_prod.yml down



# PROD
dpull:
	docker-compose -f docker-compose.prod.yml pull

up_prod:
	docker-compose -f docker-compose.prod.yml up -d

down_prod:
	docker-compose -f docker-compose.prod.yml down



# TESTS
build_tests:
	docker-compose -f docker-compose.tests.yml build

up_tests:
	docker-compose -f docker-compose.tests.yml up

down_tests:
	docker-compose -f docker-compose.tests.yml down
