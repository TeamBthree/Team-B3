FROM odoo:19

COPY ./addons /mnt/extra-addons
COPY ./docker/start.sh /start.sh

USER root

RUN chmod +x /start.sh \
    && mkdir -p /home/odoo/.ssh \
    && usermod -d /home/odoo -s /bin/bash odoo \
    && chown -R odoo:odoo /home/odoo \
    && chmod 700 /home/odoo/.ssh

ENV HOME=/home/odoo

USER odoo

ENTRYPOINT ["/start.sh"]