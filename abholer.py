#!/usr/bin/python
# E-Mail-Abholer
#
#
import imaplib,email,datetime,os,base64,quopri


M = imaplib.IMAP4("mail.jdhh.de")
M.login("blog@jandankert.de", "")
M.select("INBOX")
typ, data = M.search(None, 'ALL')

for num in data[0].split():

    now = datetime.datetime.now()
    dir =  os.path.dirname( os.path.realpath( __file__ ) )+'/../blog/'+str(now)+'/'
    os.mkdir(dir)
    
    f = open(dir+'title', 'w')
    typ, data = M.fetch(num, '(RFC822)')
    #print 'Message #'+num;
    src = data[0][1]
    msg = email.message_from_string(src)
    print "Subject: "+msg["Subject"]
    f.write(msg["Subject"])

    f = open(dir+'sender','w')
    #print "From: "+msg["From"]
    f.write(msg["From"])


    #for pl in get_flat_parts(msg):    
    for part in msg.walk():
    
	if part.is_multipart():
	    continue
	
	
	#print "     Typ:"+part.get_content_type()
	#print "  Inhalt:"+part.get_payload()
	
	if  part.get_content_type() == "text/plain":
	    f= open(dir+'text','w')
	    f.write( quopri.decodestring(part.get_payload()) )
	elif  part.get_content_type()[:6] == "image/":
	    f = open( dir + 'attachment-'+part.get_filename(),'w' )
	    f.write( base64.decodestring( part.get_payload() ) )
	else:
	    print "Unbekannter Typ: "+part.get_content_type()
	#print "\n"
	#print "\n\n"

    M.copy(num,"Archiv")
    M.store(num, '+FLAGS', r'(\Deleted)')
    M.expunge
M.close()
M.logout()


