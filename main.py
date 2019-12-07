import sys

import core, config_core
import ui, config_ui


def main():
    config_core.map = core.Map()
    config_ui.app = ui.QApplication(sys.argv)
    ui.Window()
    config_ui.window.show()
    sys.exit(config_ui.app.exec_())

if __name__ == "__main__":
    main()