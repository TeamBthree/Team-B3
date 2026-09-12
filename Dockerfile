FROM odoo:19

COPY ./addons /mnt/extra-addons
COPY ./docker/start.sh /start.sh

USER root
RUN chmod +x /start.sh
USER odoo

ENTRYPOINT ["/start.sh"]