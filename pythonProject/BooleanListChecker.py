class BooleanListChecker:
    def __init__(self, bool_list):
        self.bool_list = bool_list

    def check_all_true(self):
        if all(self.bool_list):
            # print("流程结束")
            return True
        # else:
        #     # print("流程未结束")


class BooleanMirror:
    def __init__(self, source_list, mirror_list):
        self.source_list = source_list
        self.mirror_list = mirror_list

    def update(self):
        for i, value in enumerate(self.source_list):
            if value:
                self.mirror_list[i] = True
