# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Configuration file for JupyterHub
import os

c = get_config()  # noqa: F821

# We rely on environment variables to configure JupyterHub so that we
# avoid having to rebuild the JupyterHub container every time we change a
# configuration parameter.

#############################################################################
#
# DOCKER SPAWNER CONFIGURATION
#
#############################################################################

c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"
c.DockerSpawner.image = os.environ["DOCKER_NOTEBOOK_IMAGE"]
spawn_cmd = os.environ.get("DOCKER_SPAWN_CMD", "start-singleuser.sh")
c.DockerSpawner.cmd = spawn_cmd
network_name = os.environ["DOCKER_NETWORK_NAME"]
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name
notebook_dir = os.environ.get("DOCKER_NOTEBOOK_DIR", "/home/jovyan/work")
c.DockerSpawner.notebook_dir = notebook_dir
c.DockerSpawner.volumes = {"jupyterhub-user-{username}": notebook_dir}
c.DockerSpawner.remove = True
c.DockerSpawner.debug = True

## JupyterHub configuration related to Dockerspawning
# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = "jupyterhub-ldap"
c.JupyterHub.hub_port = 8080
# Persist hub data on volume mounted inside container
c.JupyterHub.cookie_secret_file = "/data/jupyterhub_cookie_secret"
c.JupyterHub.db_url = "sqlite:////data/jupyterhub.sqlite"



#############################################################################
#
# AUTHENTICATOR CONFIGURATION
#
#############################################################################

c.JupyterHub.authenticator_class = "ldapauthenticator.LDAPAuthenticator"
c.LDAPAuthenticator.server_address = "ldap://ldap:10389"
c.LDAPAuthenticator.bind_dn_template = [
    "cn={username},ou=people,dc=planetexpress,dc=com",
]
