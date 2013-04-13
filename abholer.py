#!/usr/bin/python
# E-Mail-Abholer
#
#
import imaplib,email


M = imaplib.IMAP4("mail.jdhh.de")
M.login("blog@jandankert.de", "blogmaschine")
M.select("INBOX")
typ, data = M.search(None, 'ALL')
for num in data[0].split():
    typ, data = M.fetch(num, '(RFC822)')
    print 'Message #'+num;
    src = data[0][1]
    msg = email.message_from_string(src)
    print "Subject: "+msg["Subject"]


    #for pl in get_flat_parts(msg):    
    for part in msg.walk():
    
	if part.is_multipart():
	    continue
	    
	print "     Typ:"+part.get_content_type()
	print "  Inhalt:"+part.get_payload()
	#print "Filename:"+part.get_filename()
	print "\n"
	print "\n\n"

    M.copy(num,"Archiv")
    M.store(num, '+FLAGS', r'(\Deleted)')
    M.expunge
M.close()
M.logout()


