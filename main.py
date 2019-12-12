import sys

import core, config_core
import ui, config_ui
import random


def main():
    config_core.map = core.Map()
    config_ui.app = ui.QApplication(sys.argv)
    ui.Window()
    config_ui.window.show()
    config_core.turn = random.randint(1,2)
    if config_core.turn == 2:
        ui.ai_turn()
    sys.exit(config_ui.app.exec_())

if __name__ == "__main__":
    main()