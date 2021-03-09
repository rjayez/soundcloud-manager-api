#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import time
from datetime import *

from requests import HTTPError

import Utils
from SoundcloudService import get_activities, post_playlist, get_activities_with_cursor


def createPlaylist(numero_semaine, annee=None):
    # Initialization part
    datetimeFormat = "%Y/%m/%d %H:%M:%S %z"

    if annee is None:
        annee = date.today().year

    periodeDebut = Utils.getLundiAvecNumSemaine(annee, numero_semaine)
    periodeFin = Utils.getDimancheAvecNumSemaine(annee, numero_semaine)

    listSetsId = []
    listTracksId = []
    dateTimeLastActivitie = datetime.now()
    millisecondsInMinute = 60000

    print("Semaine n° %s" % numero_semaine)

    # Initialisation activities
    # create an array of track ids
    activities = get_activities(1)

    print(activities)

    if activities is None:
        raise Exception("L'objet des activities est vide :'(")

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
        activities = retryOnInternalServerError(activities.next_href, 3)

    # create the playlist
    postTacksPlaylist(listTracksId, numero_semaine)
    postSetsPlaylist(listSetsId, numero_semaine)

    return {
        "setsNumber": len(listSetsId),
        "tracksNumber": len(listTracksId)
    }


def postSetsPlaylist(listSetsId, numeroSemaine):
    post_playlist(listSetsId, numeroSemaine, "Set semaine")


def postTacksPlaylist(listTracksId, numeroSemaine):
    post_playlist(listTracksId, numeroSemaine, "Track semaine")


def retryOnInternalServerError(nextHref, nbRetry):
    if nbRetry <= 0:
        raise Exception('CA PETE')

    cursor = extract_cursor(nextHref)

    try:
        return get_activities_with_cursor(1, cursor)
    except HTTPError as error:
        print("CA PETE")
        print(error)
        time.sleep(2)
        retryOnInternalServerError(nextHref, nbRetry - 1)


def extract_cursor(nextHref):
    regex = re.compile(r'.+cursor=([\d\w-]+)')
    cursor = regex.match(nextHref).group(1)
    return cursor
