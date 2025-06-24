class SearchController:
    def __init__(self, view):
        self.view = view
        self.view.search_btn.clicked.connect(self.on_search)
        self.view.search_edit.returnPressed.connect(self.on_search)  # 엔터키로도 검색

    def on_search(self):
        # 검색어와 관계없이 결과 화면으로 이동
        if self.view.parent() is not None:
            self.view.parent().setCurrentIndex(3)  # ResultView로 이동
