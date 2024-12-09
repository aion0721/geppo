import TkEasyGUI as eg
from eml_processor import process_eml_files

class EMLProcessorApp:
    def __init__(self):
        self.eml_directory = ""
        self.layout = [
            [eg.Text("EMLファイル処理アプリ")],
            [eg.Button("ディレクトリ選択"), eg.Button("処理実行")],
            [eg.Text("", key="-DIR-")]
        ]
        self.window = eg.Window("EML Processor", self.layout)

    def run(self):
        while True:
            event, values = self.window.read()
            if event == eg.WINDOW_CLOSED:
                break
            elif event == "ディレクトリ選択":
                self.select_directory()
            elif event == "処理実行":
                self.process_files()
        self.window.close()

    def select_directory(self):
        self.eml_directory = eg.popup_get_folder("EMLファイルが格納されているディレクトリを選んでください。")
        self.window["-DIR-"].update(f"選択されたディレクトリ: {self.eml_directory}")

    def process_files(self):
        if not self.eml_directory:
            eg.popup_error("ディレクトリが選択されていません。")
            return
        output_file = "output.csv"
        process_eml_files(self.eml_directory, output_file)
        eg.popup(f"処理が完了しました。\n出力ファイル: {output_file}")

if __name__ == "__main__":
    app = EMLProcessorApp()
    app.run()
