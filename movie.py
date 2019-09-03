import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel, QTextBrowser, QGridLayout
import requests
from bs4 import BeautifulSoup


class MyApp(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):


        self.tb = QTextBrowser()
        self.tb.setAcceptRichText(True)
        self.tb.setOpenExternalLinks(True)
        f = self.tb.font()
        f.setPointSize(10)
        self.tb.setFont(f)

        grid = QGridLayout()
        grid.addWidget(self.tb, 0, 0, 0, 0)
        self.setLayout(grid)

        self.setWindowTitle('네이버영화순위')
        self.setGeometry(800, 400, 400, 400)
        self.show()
        self.crawl_news()

    def crawl_news(self):

        url = 'https://movie.naver.com/movie/running/current.nhn?view=list&tab=normal&order=reserve'
        r = requests.get(url)
        html = r.content
        soup = BeautifulSoup(html, 'html.parser')

        html = soup.select('#content > div.article > div:nth-child(1) > div.lst_wrap > ul > li > dl')
        for i in range(10):
            title = html[i].select('dt > a')
            rate = html[i].select('dd.star > dl.info_exp > dd > div > span.num')
            star = html[i].select('dd.star > dl.info_star > dd > div > a > span.num')
            self.tb.append(str(i+1)+"  "+title[0].text +" *"+ star[0].text + " ///" + rate[0].text + " %")
            self.tb.append("")

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
