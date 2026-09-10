# B3agric ERP — Deployment Documentation

## Current Environment

- Odoo version: 19
- PostgreSQL version: 15
- Deployment method: Docker Compose
- Odoo container: `odoo-odoo-1`
- PostgreSQL container: `odoo-db-1`
- Odoo port: `8069`

## Database

The Agriculture ERP database is:

`B3agric.erp`

The database has been backed up before migration.

The backup was successfully restored into a temporary test database to verify that the backup is readable.

## Docker Volumes

PostgreSQL data:

`odoo_odoo-db-data`

Odoo data and filestore:

`odoo_odoo-web-data`

The Odoo filestore contains the files required by the ERP database.

## Custom Addon

The project contains the custom Odoo module:

`agri_farm`

Location:

`addons/agri_farm/`

## Environment Variables

Sensitive database credentials are stored in `.env`.

The `.env` file must not be committed to GitHub.

A `.env.example` file is provided as a template for team members and deployment.

## Backups

Database and filestore backups are kept outside the Git repository.

They must not be uploaded to GitHub because they may contain sensitive ERP data.

## Deployment Overview

The cloud deployment will use:

1. GitHub for project files and version control.
2. Docker Compose to run Odoo and PostgreSQL.
3. Environment variables for database credentials.
4. PostgreSQL backup to restore the ERP database.
5. Odoo filestore backup to restore uploaded files and attachments.

## Important

The `rumbit_erp` database is a separate ERP database and must not be modified or included in the B3agric migration.