# Meridian Catalog

Order details and product search API.

Part of the Meridian document workspace. Configuration is supplied through environment variables. SERVICE_KEY authenticates internal requests. The edge resolves sessions through accounts and forwards X-User-Id and X-Tenant-Id to downstream services. Internal services are reachable only on the application network.

## Service peers

- [edge](https://github.com/sainath1204/meridian-edge)
- [accounts](https://github.com/sainath1204/meridian-accounts)
- [query](https://github.com/sainath1204/meridian-query)
