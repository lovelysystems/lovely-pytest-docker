================================
Changes for Lovely Pytest Docker
================================

Unreleased
==========

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
