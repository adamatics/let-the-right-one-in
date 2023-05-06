# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import sys
import os
from oauthenticator.generic import GenericOAuthenticator
c = get_config()  # noqa: F821

#############################################################################
#
# AUTHENTICATOR CONFIGURATION
#
#############################################################################

from oauthenticator.gitlab import GitLabOAuthenticator
c.GitLabOAuthenticator.client_id = os.environ.get('GITLAB_CLIENT_ID')
c.GitLabOAuthenticator.client_secret = os.environ.get('GITLAB_CLIENT_SECRET')
c.GitLabOAuthenticator.oauth_callback_url = "http://localhost:8000/hub/oauth_callback"
c.GitLabOAuthenticator.scope = ['read_user']
c.Authenticator.enable_auth_state = True
#############################################################################
#
# DOCKER SPAWNER CONFIGURATION
#
#############################################################################

# Spawn single-user servers as Docker containers
c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"

# Spawn containers from this image
c.DockerSpawner.image = os.environ["DOCKER_NOTEBOOK_IMAGE"]

# JupyterHub requires a single-user instance of the Notebook server, so we
# default to using the `start-singleuser.sh` script included in the
# jupyter/docker-stacks *-notebook images as the Docker run command when
# spawning containers.  Optionally, you can override the Docker run command
# using the DOCKER_SPAWN_CMD environment variable.
spawn_cmd = os.environ.get("DOCKER_SPAWN_CMD", "start-singleuser.sh")
c.DockerSpawner.cmd = spawn_cmd

# Connect containers to this Docker network
network_name = os.environ["DOCKER_NETWORK_NAME"]
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name

# Explicitly set notebook directory because we'll be mounting a volume to it.
# Most `jupyter/docker-stacks` *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
notebook_dir = os.environ.get("DOCKER_NOTEBOOK_DIR", "/home/jovyan/work")
c.DockerSpawner.notebook_dir = notebook_dir

# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
c.DockerSpawner.volumes = {"jupyterhub-user-{username}": notebook_dir}

# Remove containers once they are stopped
c.DockerSpawner.remove = True

# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True

## JupyterHub configuration related to Dockerspawning
# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = "jupyterhub"
c.JupyterHub.hub_port = 8081

# Persist hub data on volume mounted inside container
c.JupyterHub.cookie_secret_file = "/data/jupyterhub_cookie_secret"
c.JupyterHub.db_url = "sqlite:////data/jupyterhub.sqlite"


class ExpGitLabOAuthenticator(GitLabOAuthenticator):
    async def pre_spawn_start(self, user, spawner):
        """Pass upstream_token to spawner via environment variable"""
        auth_state = await user.get_auth_state()

        if not auth_state:
            # auth_state not enabled
            return
        try:
            spawner.environment['GITLAB_ACCESS_TOKEN'] = auth_state['access_token']
            spawner.environment['GITLAB_USERNAME'] = auth_state['gitlab_user']['username']
            spawner.environment['GITLAB_FULLNAME'] = auth_state['gitlab_user']['name']
        except Exception as e:
            print('ERROR setting env vars from auth_state')
            print(str(e))
        try:
            spawner.environment['UWS_AUTH_TOKEN'] = hashlib.sha1(bytes(f'{auth_state["gitlab_user"]["username"]}-secret-salt-string', 'utf-8')).hexdigest()
        except Exception as e:
            print('ERROR setting UWS_AUTH_TOKEN from GitLab auth_state: {}'.format(str(e)))

c.JupyterHub.authenticator_class = ExpGitLabOAuthenticator
