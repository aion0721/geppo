import TkEasyGUI as eg

mail_dir = eg.popup_get_folder("EMLファイルが格納されているディレクトリを選んでください。")

eg.popup(mail_dir)