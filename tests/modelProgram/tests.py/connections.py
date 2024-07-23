import sys

from PyQt5.QtCore import QCoreApplication, QUrl
from PyQt5.QtNetwork import QNetworkCookie
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import (
    QWebEnginePage,
    QWebEngineProfile,
    QWebEngineSettings,
    QWebEngineView,
)


class OpenconnectSamlAuth(QMainWindow):
    def __init__(self, parent=None):
        super(OpenconnectSamlAuth, self).__init__(parent)

        self._cookie = None

        self.webview = QWebEngineView()

        self.profile = QWebEngineProfile("storage", self.webview)
        self.cookie_store = self.profile.cookieStore()
        self.cookie_store.cookieAdded.connect(self.handle_cookie_added)

        self.profile.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)

        webpage = QWebEnginePage(self.profile, self)
        self.webview.setPage(webpage)
        self.webview.titleChanged.connect(self.update_title)

        self.setCentralWidget(self.webview)
        self.resize(1024, 768)

    @property
    def cookie(self):
        return self._cookie

    def login(self, url):
        self.webview.load(QUrl.fromUserInput(url))
        self.webview.setWindowTitle("Loading...")

    def update_title(self):
        self.webview.setWindowTitle(self.webview.title())

    def handle_cookie_added(self, cookie):
        print("added {name} : {value}".format(name=cookie.name(), value=cookie.value()))
        if cookie.name() == b"name_of_cookie":
            self._cookie = QNetworkCookie(cookie)
            QCoreApplication.quit()


# main loop
def main():
    app = QApplication(sys.argv)

    openconnect_webobj = OpenconnectSamlAuth()
    openconnect_webobj.login("http://169.254.230.238")
    openconnect_webobj.show()

    ret = app.exec_()

    cookie = openconnect_webobj.cookie
    if cookie is not None:
        print("results:", cookie.name(), cookie.value(), cookie.toRawForm())

    sys.exit(ret)


if __name__ == "__main__":
    main()