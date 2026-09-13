FROM odoo:19

COPY ./addons /mnt/extra-addons
COPY ./docker/start.sh /start.sh

USER root

RUN chmod +x /start.sh \
    && mkdir -p /home/odoo/.ssh \
    && chown -R odoo:odoo /home/odoo \
    && chmod 700 /home/odoo/.ssh \
    && chsh -s /bin/bash odoo

ENV HOME=/home/odoo

USER odoo

ENTRYPOINT ["/start.sh"]