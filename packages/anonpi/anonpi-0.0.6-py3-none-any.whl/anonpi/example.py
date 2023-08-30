from anonpi import AnonApi


anon = AnonApi("wf0vR-t#d8Ux.N0wFFloMk0#jrUOo7Lh8D7uyDOdSBrm-1Gw!inrrG5ux2jlDYWWAdsfbyphLvc6WAee")

# Shoud be digits pending datatype
call = anon.create_call(
    from_number="sa213",
    to_number="00",
    callback_url="https://anonpi.co",
)

