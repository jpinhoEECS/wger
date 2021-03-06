# -*- coding: utf-8 -*-

# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License

# Standard Library
import json
import logging

# Third Party
from django.core import serializers
from django.http import (
    HttpResponse,
    HttpResponseForbidden,
    JsonResponse
)
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _


# wger
from wger.manager.helpers import render_workout_day
from wger.manager.models import Workout
from wger.utils.helpers import check_token


logger = logging.getLogger(__name__)


def workout_json(request, id, comments=False, uidb64=None, token=None):
    '''
    Generates a JSON with the contents of the given workout
    and allows user to download in browser
    '''

    # Load the workout
    if uidb64 is not None and token is not None:
        if check_token(uidb64, token):
            workout = get_object_or_404(Workout, pk=id)
        else:
            return HttpResponseForbidden()
    else:
        if request.user.is_anonymous():
            return HttpResponseForbidden()
        workout = get_object_or_404(Workout, pk=id, user=request.user)

    # package response and download file in browser
    response = HttpResponse(str(workout.canonical_representation), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename=Workout-{0}.json'.format(id)
    response['Content-Length'] = len(response.content)
    return response
