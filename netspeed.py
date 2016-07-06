import sys
import random

if sys.version_info[0] == 2:
    import httplib2_python2 as httplib2
elif sys.version_info[0] == 3:
    import httplib2_python3 as httplib2
else:
    assert False

from bs4 import BeautifulSoup


class NetSpeed(object):
    def __init__(self):
        self.get_info()

    def parse_info(self, html):
        def clean_html(html):
            soup = BeautifulSoup(html, "html.parser")
            result = soup.find(id="webcode").string

            # Remove unexcepted ";" under OS X.
            return result.replace(";", "")

        html = clean_html(html)
        html = html.split('&')
        info = {}
        for i in html:
            tag, value = i.split('=')
            info[tag] = value

        return info

    def speed_up(self):
        h = httplib2.Http()
        resp, content = \
                h.request("http://bj.wokuan.cn/web/improvespeed.php?ContractNo=%s&up=%s&old=%s&round=%s"
                        % (self.id, self.new_speed_id, self.old_speed_id, random.randint(0, 100)))

        self.get_info()
        content = content.decode("utf-8")
        return "success&00000000" in content

    def speed_down(self):
        h = httplib2.Http()
        resp, content = \
                h.request("http://bj.wokuan.cn/web/lowerspeed.php?ContractNo=%s&round=%s"
                        % (self.id, random.randint(0, 100)))

        self.get_info()
        content = content.decode("utf-8")
        return "success&00000000" in content

    def get_info(self):
        h = httplib2.Http()
        resp, content = h.request("http://bj.wokuan.cn/web/startenrequest.php")

        content = content.decode("utf-8")
        info = self.parse_info(content)

        self.id = info['cn']
        self.status = int(info['stu'])
        self.old_speed = info['os']
        self.old_speed_id = info['old']
        self.new_speed = info['up']
        self.new_speed_id = info['gus']
        self.hours = float(info['glst'])

        if self.old_speed == "512":
            self.old_speed_unit_name = "Kbps"
        else:
            self.old_speed_unit_name = "Mbps"
            assert self.new_speed != "512"
