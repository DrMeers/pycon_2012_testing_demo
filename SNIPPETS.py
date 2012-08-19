#---[ views ]------------------------------------------------

import uuid
from django.shortcuts import (
    get_object_or_404, redirect, render_to_response)
from .models import Attraction, UserRank

def get_uuid(request):
    return request.session.setdefault(
        'session_uuid', uuid.uuid4().hex)

def attraction_list(request):
    attractions = Attraction.objects.all()

    max_rank = len(attractions)
    for attraction in attractions:
        attraction.user_rank = None
        attraction.score = 0
        for user_rank in attraction.ranks.all():
            attraction.score += (max_rank - user_rank.rank)
            if user_rank.session_uuid == get_uuid(request):
                attraction.user_rank = user_rank.rank

    scores = sorted(
        map(lambda a: a.score, attractions), reverse=True
    )

    for attraction in attractions:
        attraction.overall_rank = scores.index(
            attraction.score
        )

    attractions = sorted(
        attractions, key=lambda a: (
            a.name if a.user_rank is None else a.user_rank
        )
    )

    return render_to_response(
        'mustsee/list.html',
        {'attractions': attractions}
    )

def promote(request, attraction_id):
    attraction = get_object_or_404(
        Attraction, id=attraction_id
    )
    user_rank, created = attraction.ranks.get_or_create(
        session_uuid=get_uuid(request)
    )
    if not created:
        user_rank.rank = max(user_rank.rank-1, 0)
        user_rank.save()
    return redirect('list')

#---[ tests ]------------------------------------------------

    def test_urls(self):
        URLS = (
            (reverse('list'),
             {'template_used': 'mustsee/list.html'}),
            (reverse('promote', args=(1,)),
             {'status_code': 302}),
            (reverse('promote', args=(9,)),
             {'status_code': 404}),
        )
        self._test_urls(URLS)

#---[ settings ]---------------------------------------------

LOGGING['handlers']['console'] = {
    'class': 'logging.StreamHandler'
}
LOGGING['loggers']['tests'] = {
    'handlers': ['console'],
    'level': 'INFO'
}

import sys
import dj_database_url

TESTING = (sys.argv[1:2] == ['test'])

SOUTH_TESTS_MIGRATE = False # don't migrate test database

if not TESTING:
    DATABASES = {
        'default': dj_database_url.config(
            default='postgres://localhost'
        )
    }

#---[ template ]---------------------------------------------

"""
{% extends "base.html" %}

{% block content %}
  <h1>Must See</h1>
  <table class="table table-striped">
    <tr>
      <th>Attraction</th>
      <th>User Rank</th>
      <th>Overall Rank</th>
    </tr>
    {% for attraction in attractions %}
      <tr>
        <td>

        </td>
        <td>

        </td>
        <td>

        </td>
      </tr>
    {% endfor %}
  </table>
{% endblock %}
"""

#---[ admin ]------------------------------------------------

from django.contrib import admin
from .models import Attraction, UserRank

class UserRankAdmin(admin.ModelAdmin):
    list_display = ('attraction', 'session_uuid', 'rank')
    list_filter = ('attraction', 'session_uuid')

admin.site.register(Attraction)
admin.site.register(UserRank, UserRankAdmin)

#---[ urls ]-------------------------------------------------

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'mustsee.views',
    url(r'^$', 'attraction_list', name='list'),
    url(r'^promote/(?P<attraction_id>\d+)$', 'promote',
        name='promote'
    ),
)
