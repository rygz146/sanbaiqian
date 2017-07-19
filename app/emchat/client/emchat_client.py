#!/usr/bin/python
# -*- coding: utf-8 -*-

from ..utils.types import service_users, service_chatfiles, service_messages
from ..services.emchat_service import EMIMUsersService, EMChatFilesService, EMMessagesService
from ..utils.confs import org, app


def get_instance(service_type):
    if service_type == service_users:
        return EMIMUsersService(org, app)
    if service_type == service_chatfiles:
        return EMChatFilesService(org, app)
    if service_type == service_messages:
        return EMMessagesService(org, app)


