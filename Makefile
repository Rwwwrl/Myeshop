# DEV
build_dev:
	docker-compose -p dev -f docker-compose.dev.yml build

up_dev:
	docker-compose -p dev -f docker-compose.dev.yml up -d

down_dev:
	docker-compose -p dev -f docker-compose.dev.yml down



# LOCAL PROD
build_local_prod:
	docker-compose -p local_prod -f docker-compose.base_prod.yml -f docker-compose.local_prod.yml build

up_local_prod:
	docker-compose -p local_prod -f docker-compose.base_prod.yml -f docker-compose.local_prod.yml up -d

down_local_prod:
	docker-compose -p local_prod -f docker-compose.base_prod.yml -f docker-compose.local_prod.yml down



# PROD
dpull:
	docker-compose -p prod -f docker-compose.base_prod.yml docker-compose.prod.yml pull

up_prod:
	docker-compose -p prod -f docker-compose.base_prod.yml -f docker-compose.prod.yml up -d

down_prod:
	docker-compose -p prod -f docker-compose.base_prod.yml -f docker-compose.prod.yml down



# TESTS
build_tests:
	docker-compose -p tests -f docker-compose.tests.yml build

up_tests:
	docker-compose -p tests -f docker-compose.tests.yml up

down_tests:
	docker-compose -p tests -f docker-compose.tests.yml down


# UTILS
create_or_renew_ssl_certificates:
	$(MAKE) down_prod
	docker-compose -p ssl_certificates -f docker-compose.ssl_certificates.yml up -d
	@sleep 4
	@echo
	@echo "INFO: certbot logs:"
	@docker logs certbot
	@echo
	docker-compose -p ssl_certificates -f docker-compose.ssl_certificates.yml down
	$(MAKE) up_prod
