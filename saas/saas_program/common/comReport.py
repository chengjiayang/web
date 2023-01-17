
# from bs4 import BeautifulSoup

import os
# with open(r"./testFile/result_test_activity_create.py.html",encoding='utf-8') as report:
from lxml import etree
import re
import logging
import chardet
import html
import time
from concurrent.futures import  ThreadPoolExecutor
from jinja2 import Environment, PackageLoader
logging.basicConfig(level=logging.INFO)



#替换文件，保留
# with open(r"./testFile/result_test_user_get_down.py.html",'r',encoding='utf-8') as file:

class Report():
    datas=[]


    def datas_processing(self):
        def get_report_data(report):

            htmlElement = etree.parse(report, parser=etree.HTMLParser(encoding='utf-8'))
            # print(etree.tostring(htmlElement, pretty_print=True, encoding="utf-8").decode("utf-8"))
            try:
                if htmlElement.xpath("//tr[@id='pt1_1']/preceding-sibling::tr[1]"):
                    Element1 = htmlElement.xpath("//tr[@id='pt1_1']/preceding-sibling::tr[1]")[0]
                    Element2 = htmlElement.xpath("//tr[@id='pt1_1']")[0]

                    Element2_email = Element2
                    Element2 = etree.tostring(Element2, pretty_print=True, encoding="utf-8").decode("utf-8")
                    # Element2 = Element2.replace('''pt1_1''', '''pt2_1''')
                elif htmlElement.xpath("//tr[@id='ft1_1']/preceding-sibling::tr[1]"):
                    Element1 = htmlElement.xpath("//tr[@id='ft1_1']/preceding-sibling::tr[1]")[0]
                    Element2 = htmlElement.xpath("//tr[@id='ft1_1']")[0]

                    Element2_email = Element2
                    Element2 = etree.tostring(Element2, pretty_print=True, encoding="utf-8").decode("utf-8")
                    # Element2 = Element2.replace('''ft1_1''', '''ft2_1''')
                elif htmlElement.xpath("//tr[@id='et1_1']/preceding-sibling::tr[1]"):
                    Element1 = htmlElement.xpath("//tr[@id='et1_1']/preceding-sibling::tr[1]")[0]
                    Element2 = htmlElement.xpath("//tr[@id='et1_1']")[0]

                    Element2_email = Element2
                    Element2 = etree.tostring(Element2, pretty_print=True, encoding="utf-8").decode("utf-8")
                    # Element2 = Element2.replace('''et1_1''', '''et2_1''')
            except:
                print(report)


            Element1_email = Element1
            Element1 = etree.tostring(Element1, pretty_print=True, encoding="utf-8").decode("utf-8")

            #
            # Element1 = Element1.replace('''href="javascript:showClassDetail('c1',1)"''',
            #                             '''href="javascript:showClassDetail('c2',1)"''')
            # Element1 = Element1.replace('''id="c1"''', '''id="c2"''')

            element = Element1 + Element2

            if Element1_email.get("class") == 'success':
                Element1_email.set("class", 'passClass')
            elif Element1_email.get("class") == 'danger':
                Element1_email.set("class", 'failClass')
            elif Element1_email.get("class") == 'warning':
                Element1_email.set("class", 'errorClass')
            Element1_email = etree.tostring(Element1_email, pretty_print=True, encoding="utf-8").decode("utf-8")
            Element2_email.xpath("./td[2]")[0].remove(Element2_email.xpath("./td[2]/div")[0])
            Element2_email = etree.tostring(Element2_email, pretty_print=True, encoding="utf-8").decode("utf-8")
            element_email = Element1_email + Element2_email
            # print(element)
            try:
                Element_pass_count = htmlElement.xpath("//tr[@id='total_row']/td[3]")[0].text
            except:
                print(etree.tostring(htmlElement, pretty_print=True, encoding="utf-8").decode("utf-8"))

            Element_fail_count = htmlElement.xpath("//tr[@id='total_row']/td[4]")[0].text
            Element_error_count = htmlElement.xpath("//tr[@id='total_row']/td[5]")[0].text

            return [element, Element_pass_count, Element_fail_count, Element_error_count, element_email]

        reports = []
        for file in os.listdir(r'./saas/saas_program/testFile'):
            # print(file)
            if file.startswith('result_test_'):
                file = os.path.join(r'./saas/saas_program/testFile/', file)
                if os.path.isfile(file):
                    # print(file)
                    reports.append(file)

        datalist = []
        pool = ThreadPoolExecutor(max_workers=len(reports))
        # print("报告文件数%d"%len(reports))
        for report in reports:
            datalist.append(pool.submit(get_report_data, report).result())

        element = '\n'
        pass_counts = 0
        fail_counts = 0
        error_counts = 0
        element_email = ''

        for data in datalist:
            element = element + data[0]
            pass_counts = pass_counts + int(data[1])
            fail_counts = fail_counts + int(data[2])
            error_counts = error_counts + int(data[3])
            element_email = element_email + data[4]

        tests_counts = pass_counts + fail_counts + error_counts
        pass_rate = '{:.2f}%'.format((pass_counts / tests_counts) * 100)
        # print(element)
        tests_counts = str(tests_counts)
        pass_counts = str(pass_counts)
        fail_counts = str(fail_counts)
        error_counts = str(error_counts)
        pass_rate = str(pass_rate)

        # 删除单用例测试报告文件
        for file in reports:
            os.remove(file)

        return [element, tests_counts, pass_counts, fail_counts, error_counts, pass_rate, element_email]

    def merge_reports(self,start_time, duration):

        [element, tests_counts, pass_counts, fail_counts, error_counts, pass_rate, element_email] =Report.datas


        htmlElement_report = etree.parse(r'./saas/saas_program/testFile/report_template/test_model.html', parser=etree.HTMLParser(encoding='utf-8'))
        Element_start_time = htmlElement_report.xpath("//div[@class='heading']/p[1]")[0]
        Element_start_time.text = '开始时间 : %s' % start_time
        Element_run_time = htmlElement_report.xpath("//div[@class='heading']/p[2]")[0]
        Element_run_time.text = '合计耗时 : %s' % duration
        Element_result = htmlElement_report.xpath("//div[@class='heading']/p[3]")[0]
        Element_result.text = '测试结果 : 共 %s，通过 %s，通过率= %s' % (str(tests_counts), str(pass_counts), str(pass_rate))

        Element_pass_rate = htmlElement_report.xpath("//a[@class='btn btn-primary']")[0]
        Element_pass_rate.text = '概要{ %s }' % pass_rate
        Element_pass = htmlElement_report.xpath("//a[@class='btn btn-success']")[0]
        Element_pass.text = "通过{ %s }" % pass_counts
        Element_fail = htmlElement_report.xpath("//a[@class='btn btn-danger']")[0]
        Element_fail.text = "失败{ %s }" % fail_counts
        Element_error = htmlElement_report.xpath("//a[@class='btn btn-warning']")[0]
        Element_error.text = "错误{ %s }" % error_counts
        Element_total = htmlElement_report.xpath("//a[@class='btn btn-info']")[0]
        Element_total.text = "所有{ %s }" % tests_counts
        Element_total1 = htmlElement_report.xpath("//tr[@id='total_row']/td[2]")[0]
        Element_total1.text = tests_counts
        # Element_total.text='100'.encode('utf-8')
        Element_pass1 = htmlElement_report.xpath("//tr[@id='total_row']/td[3]")[0]
        Element_pass1.text = pass_counts
        Element_fail1 = htmlElement_report.xpath("//tr[@id='total_row']/td[4]")[0]
        Element_fail1.text = fail_counts
        Element_error1 = htmlElement_report.xpath("//tr[@id='total_row']/td[5]")[0]
        Element_error1.text = error_counts
        Element_pass_rate1 = htmlElement_report.xpath("//tr[@id='total_row']/td[6]")[0]
        Element_pass_rate1.text = "通过率：%s" % pass_rate

        element1 = htmlElement_report.xpath("//tr[@id='pt1_1']/preceding-sibling::tr[1]")[0]
        element2 = htmlElement_report.xpath("//tr[@id='pt1_1']")[0]
        element1.getparent().remove(element1)
        element2.getparent().remove(element2)

        now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
        nowtime=now
        # report_ending_log= r"./saas/saas_program/testFile/Report_log.html"
        report_ending_log = r"./templates/Report_log.html"

        with open(report_ending_log, "w+", encoding='utf-8') as file_test:
            a = etree.tostring(htmlElement_report, pretty_print=True, encoding="utf-8").decode("utf-8")
            # print()
            file_test.write(html.unescape(a))



        file = open(report_ending_log, "r", encoding="utf-8")

        content = file.read()
        # print(chardet.detect(content))
        # print(content)
        position_strint = '''<tr id="total_row" class="text-center info">'''
        pos = content.index(position_strint)
        #
        # print(pos)
        # print(content[pos:])
        contentadd = element
        # print(pos)
        if pos != -1:
            content = content[:pos] + '\n' + contentadd + content[pos:]
            file_report = open(report_ending_log, "w", encoding='utf-8')
            # print(content)
            file_report.write(html.unescape(content))
            file_report.close()

        # with open(report_ending_log,'r',encoding='utf-8') as file:
        #     print(file.read())




        html_report = etree.parse(report_ending_log, parser=etree.HTMLParser(encoding='utf-8'))
        # print(etree.tostring(html_report, pretty_print=True, encoding="utf-8").decode("utf-8"))
        Elements = html_report.xpath("//a[@class='detail']")
        i = 1
        for element in Elements:
            element2 = element.xpath("./../../following-sibling::tr[1]")[0]
            element3 = element2.xpath("./td[2]/button")[0]
            element4 = element2.xpath("./td[2]/div")[0]

            element.set("href", "javascript:showClassDetail('c%d',1)" % i)
            element.set("id", 'c%d' % i)
            element2.set("id", element2.get("id").replace('1_1', '%d_1' % i))
            element3.set("id", element3.get("id").replace('1_1', '%d_1' % i))
            element3.set("data-target", element3.get("data-target").replace('1_1', '%d_1' % i))
            element4.set("id", element4.get("id").replace('1_1', '%d_1' % i))
            i = i + 1


        with open(report_ending_log, "w+", encoding='utf-8') as file_test:
            a = etree.tostring(html_report, pretty_print=True, encoding="utf-8").decode("utf-8")
            file_test.write(html.unescape(a))



    def create_report_email(self,start_time, duration):
        [element, tests_counts, pass_counts, fail_counts, error_counts, pass_rate, element_email] = Report.datas



        env = Environment(loader=PackageLoader('saas.saas_program.testFile', 'report_template'))
        template = env.get_template('report_email_model.html')
        html_content = template.render(start_time=start_time,
                                       duration=duration,
                                       pass_counts=pass_counts,
                                       element_email=element_email,
                                       tests_counts=tests_counts,
                                       fail_counts=fail_counts,
                error_counts=error_counts)
        now=time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
        nowtime=now
        report_ending_email = r"./saas/saas_program/testFile/Report_email%s.html" % (nowtime)
        with open(report_ending_email, "w+", encoding='utf-8') as file_test:
            file_test.write(html_content)



        html_report = etree.parse(report_ending_email, parser=etree.HTMLParser(encoding='utf-8'))
        # print(etree.tostring(html_report, pretty_print=True, encoding="utf-8").decode("utf-8"))
        Elements = html_report.xpath("//a[@class='detail']")
        # print(Elements)
        i = 1
        for element in Elements:
            element2 = element.xpath("./../../following-sibling::tr[1]")[0]
            element3 = element2.xpath("./td[2]/button")[0]
            element4 = element2.xpath("./td[1]")[0]

            element.set("href", "javascript:showClassDetail('c%d',1)" % i)
            element.set("id", 'c%d' % i)
            element2.set("id", element2.get("id").replace('1_1', '%d.1' % i))
            element3.set("id", element3.get("id").replace('1_1', '%d.1' % i))
            element3.set("data-target", element3.get("data-target").replace('1_1', '%d.1' % i))
            # element3.set("tag",'a')
            element4.set('class','none')


            # element4.set("id", element4.get("id").replace('1_1', '%d_1' % i))
            i = i + 1
            # print(element.attrib)
            # print(element2.attrib)
            # print(element3.attrib)

        with open(report_ending_email, "w+", encoding='utf-8') as file_test:
            a = etree.tostring(html_report, pretty_print=True, encoding="utf-8").decode("utf-8")
            file_test.write(html.unescape(a))



# report1=Report()
# report1.datas























