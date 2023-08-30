from anonpi import AnonApi , __version__    



anon = AnonApi("wf0vR-t#d8Ux.N0wFFloMk0#jrUOo7Lh8D7uyDOdSBrm-1Gw!inrrG5ux2jlDYWWAdsfbyphLvc6WAee")

# Shoud be digits pending datatype
call = anon.get_call("calluuid")
call.get_recording()