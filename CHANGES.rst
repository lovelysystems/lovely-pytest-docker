================================
Changes for Lovely Pytest Docker
================================

unreleased
==========

- allow to set the timeout and retry interval when waiting for services
- added explicit dependency to six, which is no more required in newer pytest versions
- add support for `docker-compose stop`

2021/08/05 0.2.1
================

- explicitly set the project-directory in compose executors to allow older
  compose versions to find ".env" files
  see https://docs.docker.com/compose/environment-variables/#the-env-file

2020/10/06 0.2.0
================

- added url_checker method to create an url_checker for a specific path

2019/08/27 0.1.0
================

 - added ``docker_services_project_name`` fixture in order to override the container
   name prefix for started services.

2019/01/22 0.0.5
================

 - python 2 runtime compatibility

2018/12/20 0.0.4
================

 - make docker_ip a fixture to make it possible to override it per project

2018/01/21 0.0.3
================

 - fixed wrong error handling when polling for docker up state

2018/01/10 0.0.2
================

 - added exec method in Services class
 - added possibility to use custom checker for wait_for_service method

2018/01/09 0.0.1
================

 - initial version
