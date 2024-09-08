## Current tasks

https://rwwwrl.notion.site/1aa3f3f8c5a143f99683bf313bbbea2c?v=d4b6284348e140568404fe19c3b395f0

## Test stand

**url**: *https://myeshoponcontainers.site/docs/*
Test admin user login / password = admin / 1423

---

**Grafana**
**url**: *https://myeshoponcontainers.site:3000*
login / password = admin / 1423

## Deploy

1. create ssl sertificates:

   ```bash
   make create_or_renew_ssl_certificates
   ```

2. up services:
   ```bash
   make up_prod
   ```

## Updating ssl сертификатов

```bash
make create_or_renew_ssl_certificates
```

\*it will restart services
