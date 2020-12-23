#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Utils
from datetime import *
from SoundcloudService import get_activities, post_playlist, get_for_path
from requests import HTTPError


def createPlaylist(numero_semaine):
    # Initialization part
    datetimeFormat = "%Y/%m/%d %H:%M:%S %z"

    periodeDebut = Utils.getLundiAvecNumSemaine(date.today().year, numero_semaine)
    periodeFin = Utils.getDimancheAvecNumSemaine(date.today().year, numero_semaine)

    listSetsId = []
    listTracksId = []
    dateTimeLastActivitie = datetime.now()
    millisecondsInMinute = 60000

    print("Semaine n° %s" % numero_semaine)

    # Initialisation activities
    # create an array of track ids
    activities = get_activities(1)

    print(activities)

    while periodeDebut < dateTimeLastActivitie:
        for activitie in activities.collection:
            track = activitie.origin
            dateTimeLastActivitie = datetime.strptime(activitie.created_at, datetimeFormat).replace(tzinfo=None)
            if dateTimeLastActivitie < periodeFin:
                if (track.duration / millisecondsInMinute) > 10:
                    print("Set : %s - %s" % (dateTimeLastActivitie, activitie.origin.title))
                    listSetsId.append({'id': activitie.origin.id})
                else:  # Track de moins de 10 minutes
                    print("Track : %s - %s" % (dateTimeLastActivitie, activitie.origin.title))
                    listTracksId.append({'id': activitie.origin.id})

        # activities = client.get(activities.next_href)
        activities = retryOnInternalServerError(activities.next_href, 2)

    # create the playlist
    postSetsPlaylist(listSetsId, numero_semaine)
    postTacksPlaylist(listTracksId, numero_semaine)


def postSetsPlaylist(listSetsId, numeroSemaine):
    post_playlist(listSetsId, numeroSemaine, "Set semaine")


def postTacksPlaylist(listTracksId, numeroSemaine):
    post_playlist(listTracksId, numeroSemaine, "Track semaine")


def retryOnInternalServerError(nextHref, nbRetry):
    if nbRetry <= 0:
        raise Exception('CA PETE')

    try:
        return get_for_path(nextHref)
    except HTTPError as error:
        print("CA PETE")
        print(error)
        retryOnInternalServerError(nextHref, nbRetry - 1)
