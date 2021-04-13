import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

def text_table_content(sqldata:list):
    table = '<table border = 1>'
    keylist = []
    if sqldata:
        s = sqldata[0]
        table += '<tr>'
        for key in s.keys():
            keylist.append(key)
            table += f'<th>{key}</th>'
        table += '</tr>'
        for a in sqldata:
            table += '<tr>'
            for b in keylist:
                table += f'<td>{a[b]}</td>'
            table += '</tr>'
        table += '</table>'
    return table

def format_mail_addr(addrlist):
    if addrlist:
        if len(addrlist) == 1:
            return addrlist[0]
        else:
            return ";".join(addrlist)
    else:
        return ""

def mail(content,my_sender,my_pass,to_receiver,cc_receiver,subject,host = "smtp.exmail.qq.com",port = 465,annex = None):
    ret = True
    try:
        msg = MIMEText(content, 'html')
        if annex:
            msg = MIMEMultipart()
            att1 = MIMEText(open(annex, 'rb').read(), 'base64', 'utf-8-sig')
            att1["Content-Type"] = 'application/octet-stream'
            # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
            att1.add_header('Content-Disposition', 'attachment', filename=f'{annex}')
            msg.attach(att1)
            msg.attach(MIMEText(content, 'html'))
        msg['From'] = formataddr(["simmsshu", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['Subject'] = subject  # 邮件的主题，也可以说是标题
        msg['To']   =   format_mail_addr(to_receiver)
        msg['Cc']   =   format_mail_addr(cc_receiver)
        receiver = to_receiver + cc_receiver
        server = smtplib.SMTP_SSL(host,port)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, receiver, msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception as f:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
        raise f
    return ret


