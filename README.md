# booking-system-pika
booking-system-pika created by GitHub Classroom

Databases Project (Sort of)

Currently, this app is in very early development. For instructors, please refer to the PDF folder located at the `documents` folder.

## Members of the Team:

    Ángel García | Frenzy (angel.garcia@upr.edu)
    Juan Gonzales (juan.gonzalez63@upr.edu)
    Franklin Sifre (franklin.sifre@upr.edu)
    

### TODO

- [x] Phase 1
- [ ] Phase 2
- [x] Get Flask Up and Running
- [x] Get Heroku boilerplate deployment
- [ ] Deploy flask app into the Heroku deployment
- [ ] Get Postman working



# Herkou Credentials [Important]

[Host:]
ec2-3-220-90-40.compute-1.amazonaws.com

[Database:]
d3ufj4hon9dtnd

[User:]
demmwnmoxjtnkk

[Port:]
5432

[Password:]
ac93f67b96c09f6278d475cb235576e6ba9055bedc85caacbce58a0fa91f6cd8

[URI:]
postgres://demmwnmoxjtnkk:ac93f67b96c09f6278d475cb235576e6ba9055bedc85caacbce58a0fa91f6cd8@ec2-3-220-90-40.compute-1.amazonaws.com:5432/d3ufj4hon9dtnd

[Heroku CLI:]
heroku pg:psql postgresql-corrugated-70019 --app booking-system-pika



1. Register a new user
2. Find available rooms (lab, classroom, study space, etc.) at a time frame given user role.
3. Find who appointed a room at a certain time
4. Give an all-day schedule for a room
5. Give an all-day schedule for a user
6. Find a time that is free for every user given.
7. Create a meeting with 2+ people in a room
8. Limit the access to rooms appointment, information and schedule according to person’s
authorization. (Just for highest role)
9. Allow user to mark time-space as “Unavailable”/ “Available” in his schedule(should
appear in user schedule and by default it is all marked as available)
10. Only highest can mark a time-space as “Unavailable”/ “Available” for any type of room
(should appear in room schedule and By default it is all marked as available)