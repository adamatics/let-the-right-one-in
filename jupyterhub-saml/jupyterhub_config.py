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

class ExtendedSAMLAuthenticator(samlauthenticator.SAMLAuthenticator):
    async def authenticate(self, handler, data):
        auth_state = await super().authenticate(handler, data)
        username = auth_state
        user_info = self.user_exists_or_create(username)

        user_info["name"] = username

        return user_info


c.JupyterHub.authenticator_class = ExtendedSAMLAuthenticator
c.SAMLAuthenticator.metadata_filepath = '/etc/jupyterhub/saml_metadata.xml'
c.SAMLAuthenticator.xpath_username_location = '//saml:Attribute[@Name="Username"]/saml:AttributeValue/text()'
c.SAMLAuthenticator.time_format_string = '%Y-%m-%dT%H:%M:%S.%fZ'
c.SAMLAuthenticator.shutdown_on_logout = True
c.SAMLAuthenticator.slo_forward_on_logout = False
c.SAMLAuthenticator.slo_forwad_on_logout = False
c.SAMLAuthenticator.create_system_users = False

c.Authenticator.enable_auth_state = True

