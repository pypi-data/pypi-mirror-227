# -*- coding: utf-8 -*-
# ****************************************************************
# IDE:          PyCharm
# Developed by: Mario Cerón Charry
# Date:         19/08/23 15:09
# Project:      Zibanu - Django
# Module Name:  auth
# Description:  
# ****************************************************************
from rest_framework import status
from rest_framework.response import Response
from zibanu.django.rest_framework.viewsets import ViewSet


class LogoutUser:
    """
    ViewSet to perform logout actions and remove cached tokens.
    """

    def logout(self, request, *args, **kwargs) -> Response:
        user = request.data("user")
        return Response()