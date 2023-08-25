
# monkstools/top_module.py
from .person_group import PersonGroup
from .secondary_preference import SecondaryPreference
# 从其他子模块中导入所需的类

class TopModule:
    def __init__(self, data):
        self.person_group = PersonGroup(data['person_group'])
        self.secondary_preference = SecondaryPreference(data['secondary_preference'])
        # 初始化其他子模块

    def calculate_roi(self):
        # 计算ROI的方法
        pass

    def display_results(self):
        # 展示结果的方法
        pass