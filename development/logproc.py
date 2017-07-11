import sqlite3
conn = sqlite3.connect('logproc.db')
c = conn.cursor()
if conn != None:
   print "Connection succesful"
c.execute("INSERT INTO experimentation(architecture, mapper, mode, run,threads, time, outputNumber) VALUES ('amd','aln','interleave',1,8,20,2384563)")
conn.commit()

c.execute('SELECT * FROM experimentation')
print c.fetchone()



