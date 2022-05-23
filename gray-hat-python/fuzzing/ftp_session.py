from boofuzz import Session, Target, s_get
from boofuzz.monitors import pedrpc


def recieve_ftp_banner(sock):
    sock.recv(1024)


sess = Session(session_filename="audits/warftpd.session")
target = Target("192.168.244.133", 21)
target.netmon = pedrpc.Client("192.168.244.133", 26001)
target.procmon = pedrpc.Client("192.168.244.133", 26002)
target.procmon_options = {"proc_name": "war-ftpd.exe"}

sess.pre_send = recieve_ftp_banner
sess.add_target(target)

sess.connect(s_get("user"))
sess.connect(s_get("user"), s_get("pass"))
sess.connect(s_get("pass"), s_get("cwd"))
sess.connect(s_get("pass"), s_get("dele"))
sess.connect(s_get("pass"), s_get("mdtm"))
sess.connect(s_get("pass"), s_get("mkd"))

sess.fuzz()
