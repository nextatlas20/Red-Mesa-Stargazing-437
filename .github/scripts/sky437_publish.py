#!/usr/bin/env python3
from pathlib import Path
import re


def write(path, text):
    p = Path(path)
    if str(p.parent) != '.':
        p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')


config = Path('_config.yml').read_text(encoding='utf-8')
out = []
seen_title = False
seen_description = False
seen_email = False
for line in config.splitlines(keepends=True):
    if re.match(r'^title\s*:', line):
        out.append('title: Red Mesa Public Stargazing\n')
        seen_title = True
    elif re.match(r'^description\s*:', line):
        out.append('description: Public session times and capacity summary for the Red Mesa sky night\n')
        seen_description = True
    elif re.match(r'^[ \t]*email\s*:', line) and not seen_email:
        out.append('email: sky@redmesa.example\n')
        seen_email = True
    else:
        out.append(line)
if not (seen_title and seen_description and seen_email):
    raise SystemExit('Expected one title, description, and email line in _config.yml')
write('_config.yml', ''.join(out))

about = '''---
title: "Red Mesa Public Stargazing"
permalink: /
layout: single
---

## Sky night
Three public viewing sessions take place on 2045-11-08.

## Booking status
All 12 available seats are booked. Seven requests were accepted and two were waitlisted without splitting parties.

## Session topics
The evening covers Moon craters, Saturn rings, and the Pleiades cluster.

## Contact
Bookings: sky@redmesa.example
'''
write('_pages/about.md', about.rstrip('\n') + '\n')

capacity = '''{"event_id":"SKY-437","title":"Red Mesa Public Stargazing","event_date":"2045-11-08","booking_cutoff":"2045-11-01T17:00:00Z","contact_email":"sky@redmesa.example","valid_session_count":3,"booking_candidate_count":9,"accepted_request_count":7,"waitlisted_request_count":2,"booked_seat_count":12,"remaining_seat_count":0,"sessions":[{"session_id":"S-MOON","topic":"Moon craters","starts_at":"2045-11-08T19:00:00Z","ends_at":"2045-11-08T19:40:00Z","capacity":4,"booked_seats":4,"remaining_seats":0,"accepted_request_count":3,"waitlisted_request_count":1},{"session_id":"S-RINGS","topic":"Saturn rings","starts_at":"2045-11-08T20:00:00Z","ends_at":"2045-11-08T20:40:00Z","capacity":3,"booked_seats":3,"remaining_seats":0,"accepted_request_count":2,"waitlisted_request_count":0},{"session_id":"S-CLUSTER","topic":"Pleiades cluster","starts_at":"2045-11-08T21:00:00Z","ends_at":"2045-11-08T21:40:00Z","capacity":5,"booked_seats":5,"remaining_seats":0,"accepted_request_count":2,"waitlisted_request_count":1}]}'''
write('_data/sky-437-capacity.json', capacity.rstrip('\n') + '\n')

sessions_csv = '''session_id,topic,starts_at,ends_at,capacity,booked_seats,remaining_seats,accepted_request_count,waitlisted_request_count
S-MOON,Moon craters,2045-11-08T19:00:00Z,2045-11-08T19:40:00Z,4,4,0,3,1
S-RINGS,Saturn rings,2045-11-08T20:00:00Z,2045-11-08T20:40:00Z,3,3,0,2,0
S-CLUSTER,Pleiades cluster,2045-11-08T21:00:00Z,2045-11-08T21:40:00Z,5,5,0,2,1
'''
write('downloads/sky-437-sessions.csv', sessions_csv.rstrip('\n') + '\n')

summary = '''# Red Mesa stargazing bookings

Event date: 2045-11-08
Booking cutoff: 2045-11-01T17:00:00Z

## Capacity summary
All 12 seats across three public sessions are booked. Seven requests were accepted and two were waitlisted.

- 19:00 UTC — Moon craters: 4 of 4 seats booked
- 20:00 UTC — Saturn rings: 3 of 3 seats booked
- 21:00 UTC — Pleiades cluster: 5 of 5 seats booked

## Contact
Bookings: sky@redmesa.example
'''
write('downloads/sky-437-booking-summary.md', summary.rstrip('\n') + '\n')

print('SKY-437 files written')
