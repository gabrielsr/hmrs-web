# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rails db:seed command (or created alongside the database with db:setup).
#
# Examples:
#
from dateutil import parser

_d = parser.parse

pwd_hash = "$2b$12$QLpUyPzW8PF6Kidk/fMXM.AQQSCI7UK7OsUr4k.2qVAbPq7yPdrhy" # pwd:asdasdasd
principals = [
    {"id": 1, "username": "alice"},
    {"id": 2, "username": "bod"},
    {"id": 3, "username": "carol"},
]

profiles = [
    {"id": 1,"principal_id": 1, "name": "Alice A."},
    {"id": 2, "principal_id": 2, "name": "Bob B."},
    {"id": 3, "principal_id": 3, "name": "Carol C."}
]

credentials = [
    {"principal_id": 1, "password": pwd_hash },
    {"principal_id": 2, "password": pwd_hash },
    {"principal_id": 3, "password": pwd_hash }
]
