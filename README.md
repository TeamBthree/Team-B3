# B3agric ERP

Agriculture ERP system built with Odoo.

## Technology Stack

- Odoo: 19
- PostgreSQL: 15
- Containerization: Docker
- Local Development: Docker Compose
- Cloud Deployment: Render

## Custom Module

The project includes the custom `agri_farm` module for managing agricultural operations.

## Database

The ERP database is:

`B3agric.erp`

## Local Development

The Odoo application runs on port `8069`.

Database credentials are stored in `.env` and are not committed to GitHub.

See `.env.example` for the required environment variables.

## Cloud Deployment

The ERP was deployed to Render using Docker.

Cloud components:
- Web Service: Render
- Database: Render PostgreSQL
- Containerization: Docker
- Persistent Storage: Render Persistent Disk

Live ERP:
https://b3agric-odoo.onrender.com

## Database Migration

The local B3agric.erp PostgreSQL database was backed up and restored into the Render PostgreSQL database.

The cloud database uses the name:

`b3agric_erp`

The database name was changed because the Render PostgreSQL service does not allow the same naming format used locally.

Database credentials are stored as environment variables and are not committed to the repository.

## Filestore Migration

The Odoo filestore from the local ERP was transferred to the cloud persistent disk.

The filestore was placed in:

`/var/lib/odoo/filestore/b3agric_erp`

The migrated filestore was verified after deployment to ensure that ERP attachments and images were available.

## Environment Variables

The deployment uses environment variables for database configuration.

Required variables include:

- `HOST`
- `USER`
- `PASSWORD`

A template is provided in `.env.example`.

Actual passwords and other sensitive credentials are not stored in GitHub.

## Testing

After deployment, the ERP was tested by:

- Creating and testing two user accounts
- Creating three sample ERP records
- Testing the assessor account
- Checking ERP functionality
- Verifying migrated data and attachments
- Restarting the cloud service to confirm data persistence