# Repository for the talk "Let the Right One In" at JupyterCon 2023

This repository contains the code examples shown at the talk for JupyterCon 2023, "Let the Right One In".

From the root of the repository, there are four folders each with example configuration for different authentication
mechanisms for JupyterHub. Prerequisites for running the code samples are:

 - git, to clone the repository. Alternatively you can download the repository as a zip file
 - docker and docker-compose, to be able to build and start the containers

For all the folders, the start-up command is the same:

```
docker-compose build
docker-compose up
```


Each folder has its own headline below

# jupyterhub-plain

A base-line jupyterhub, with the `dummy` authenticator and `DockerSpawner`. This folder is for easy experimentation
with the various configuration settings for authenticators and spawners.

Note that any username/password combination will log you in

# jupyterhub-ldap

This folder contains OpenLDAP as an additional docker service, providing a LDAP API to query against. The LDAP server
has been configured with some default users, username/passwords:

 - amy/amy
 - professor/professor
 - bender/bender

# jupyterhub-oauth2

This configuration requires you to setup an application in GitLab to handle the single sign-on process through OAuth2.
You'll need to set the call-back url to `http://localhost:8000/hub/oauth_callback` and copy the client id and client
secret from the web interface. Place these values in a `.env` file in the folder with the following variables set:

```
GITLAB_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GITLAB_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxx
```

# jupyterhub-saml

This repository contains some example code to get you started with a SAML provider
