import datetime
now =  datetime.datetime.utcnow()
time = now.strftime("%Y-%m-%dT%H:%M:%S") + ".%03d" % (now.microsecond / 1000) + "Z"
print (time)
#add time stamp diye bir key oluşturup valueye bu verilecek