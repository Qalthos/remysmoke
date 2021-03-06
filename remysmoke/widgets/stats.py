from __future__ import division, print_function, unicode_literals
from datetime import datetime, timedelta
import difflib
import random

from remysmoke.model import DBSession
from remysmoke.model.auth import User
from remysmoke.model.smoke import Cigarette
from remysmoke.model.unsmoke import Unsmoke


def smoke_stats(user):
    """Produce a dictionary of statistics for each user."""
    now = datetime.today()
    smoke_data = DBSession.query(Cigarette).filter_by(user=user.user_name) \
                          .order_by(Cigarette.date)
    unsmoke_data = DBSession.query(Unsmoke).filter_by(user=user.user_name) \
                            .order_by(Unsmoke.date).all()
    user = user.display_name

    year = smoke_data.filter(Cigarette.date >= now - timedelta(days=365)).all()
    month = smoke_data.filter(Cigarette.date >= now - timedelta(days=28)).all()
    week = smoke_data.filter(Cigarette.date >= now - timedelta(days=7)).all()
    smoke_data = smoke_data.all()
    if not smoke_data:
        return dict()

    # Complex calculations get their own function
    streak = calculate_streak(unsmoke_data)
    latest_excuses, random_excuses, top_excuses = get_excuses(smoke_data)
    score = smoke_score((smoke_data, year, month, week))

    # Other simple stats
    newest_data = smoke_data[-1].date
    oldest_data = smoke_data[0].date
    timespan = max((datetime.today() - oldest_data).days + 1, 1)
    dpp = 1.0 * timespan * 20 / len(smoke_data)
    cpm = len(smoke_data) * 10.50 * 30 / (20 * timespan)

    return dict(score=score, lifespan=dpp, cost=cpm,
                now=(now - newest_data), best=streak, top=top_excuses,
                latest=latest_excuses, random=random_excuses)


def calculate_streak(unsmoke_data):
    """Given a list of unsmoke records, calculate longest consecutive streak."""
    streak = timedelta()
    if unsmoke_data:
        start = last = unsmoke_data[0].date
        tomorrow = timedelta(days=1)
        for datum in unsmoke_data:
            if datum.date == (last + tomorrow):
                # Update the current streak and check for length
                current_streak = datum.date - start
                if current_streak > streak:
                    streak = current_streak
            else:
                # Reset the start date
                start = datum.date
            last = datum.date

    return streak


def get_excuses(smoke_data):
    """Given smoke data, get the 5 latest, 5 most popular, and 5 random excuses."""
    excuses = [(smoke_point.justification,
                smoke_point.date.strftime('%d %b %Y %H:%M'))
               for smoke_point in smoke_data]

    latest_excuses = reversed(excuses[-5:])
    random_excuses = random.sample(excuses, 5 if len(excuses) >= 5 else len(excuses))

    counts = list()
    for (excuse, _) in excuses:
        excuse = excuse.lower().strip()
        for merge_pair in counts:
            if difflib.get_close_matches(excuse, merge_pair[0], 1, .8):
                if excuse not in merge_pair[0]:
                    merge_pair[0].append(excuse)
                merge_pair[1] += 1
                break
        else:
            counts.append([[excuse], 1])
    top_excuses = sorted([(count, similar) for similar, count
                          in counts], reverse=True)[:5]

    return (latest_excuses, random_excuses, top_excuses)


def smoke_score(smoke_data):
    """Takes smoking stats and reduces those stats to a number."""
    delta = 0
    score = 0
    weights = [.01, .1, .5, 1]
    for collection, weight in zip(smoke_data, weights):
        if not collection:
            continue
        timespan = (collection[-1].date - collection[0].date).days
        for datum in collection:
            # Score is reduced by 1 for each hour difference
            # Indulgences count as negative too
            #delta += abs(datum.date - datum.submit_date).total_seconds() / 3600.
            this_delta = abs(datum.date - datum.submit_date)
            delta += this_delta.seconds / 3600. + this_delta.days / 24.

        # Score is [days of history] / [# of smokes] - delta
        score += weight * (24.0 * timespan / len(collection) - delta)
    return score
