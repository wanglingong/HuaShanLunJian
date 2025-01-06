# 2024/12/31
# python实战分析培训班(第三期)
import requests
import random
from rich.console import Console
from rich.panel import Panel

console = Console()

BASE_URL = "http://127.0.0.1:5050"
"""
    华山论剑-第一课-英雄类
    英雄属性：出自哪一部小说、体力、内力、名谓、技能、攻击力、防御力等
    能力1：自报家门
    能力2：发表获胜感言和战败感言
"""

"""
    ************ 任务书 **************
    * 任务1:实现基础英雄类             *
    * 要求1:包含上述的属性             *
    * 要求2:实现上述的能力             *
    ********************************* 
"""


class Hero:
    """
    任务1 实现基础英雄类
    """
    from_novel = "射雕三部曲"

    def __init__(self, name, title, life, energy, attack, defense, skills, introduction):
        """
        实现 : __init__ 构造函数,该函数会在创建类实例时自动执行
        提示 1: 完成构造函数的参数设计,名字、名谓、体力、内力 …………等等
        提示 2: 完成类中对象属性的赋值完成初始化,如下方的self.name=name
        """
        # 英雄属性
        self.name = name
        self.title = title
        self.life = life
        self.energy = energy
        self.attack = attack
        self.defense = defense
        self.skills = skills
        self.introduction = introduction

    def introduce(self, emotion):
        """
        实现 : introduce 自报家门函数,该函数可通过 类实例.introduce()进行调用
        提示 1: 自报家门的内容通过 print("xxxx")打印
        提示 2: 在类的内部函数中,默认第一个参数传递是类自身(也是实例自身),于是可通过 self.name来获取类(实例)的属性
        提示 3: f"{}" 表示一个格式化的字符串{}中为带补充填写的属性名
        """
        # 补完打印内容
        print(f"我{self.name}来也,{self.title} 舍我其谁 体力是{self.life},内力是{self.energy}")
        print(f"我现在的心情是~{emotion}")

    def speak(self, status):
        """
        实现 : speak 发表感言函数,该函数可通过 类实例.speak()进行调用
        提示 1: 发表感言的内容通过 print("xxxx")打印
        提示 2: 感言内容可以通过 self.get_words(status)来获取(该函数以写好)，status传入"win"或"lose"
        提示 3: 在类的内部函数中,全局变量、局部变量、临时变量直接使用变量名获取其值如 status
        """
        mood, words = self.get_words(status)
        # 补完打印内容
        print(f"{self.name}【{mood}】地说:{words}")

    # @staticmethod 表示这个函数是静态函数
    # 静态函数不跟对象挂钩,也就是说不需要访问对象的任何属性及方法
    # 因此不写出self，也无法访问self
    @staticmethod
    def get_words(result):
        # 胜利的喊话
        victory_words = [
            "哈哈哈，果然是技高一筹，承让了！",
            "这等武艺也敢来挑战我？回去再练十年吧！",
            "江湖中今日又多了一段我胜你败的传奇！",
            "武道至高，今日你算是见识到了！",
            "来者不善，善者不来，你也不过如此！"
        ]

        # 失败的喊话
        defeat_words = [
            "今日技不如人，他日再来讨教！",
            "哼，青山不改，绿水长流，我们来日再战！",
            "大侠果然身手不凡，我甘拜下风！",
            "江湖路远，后会有期，来日再比高低！",
            "败也无妨，武者在于永不言弃！"
        ]

        # random 是一个随机数库, random.choice表示随机选择列表中的喊话词
        if result == "win":
            mood = "神气"
            words = random.choice(victory_words)
        else:
            mood = "遗憾"
            words = random.choice(defeat_words)

        return mood, words

    def create_my_hero(self, user_name):
        json_data = {
            "user_id": user_name,
            "hero": self.__dict__
        }
        response = requests.post(f"{BASE_URL}/create_player", json=json_data)
        if response.status_code == 200:
            print("角色创建成功！")
            print(response.json())
            return True
        else:
            print("角色创建失败！")
            print(response.json())
            return False

    @staticmethod
    def choose_opponent():
        response = requests.get(f"{BASE_URL}/get_boss_list")
        if response.status_code == 200:
            print(response.json())
            return response.json()["boss_list"]
        else:
            print("没找到对手~！")
            print(response.json())
            return False

    @staticmethod
    def challenge(user_name, boss_name):
        response = requests.get(f"{BASE_URL}/challenge/{user_name}/{boss_name}")
        return response.json()


"""
    英雄类的实例化测试:
    1、实例初始化传入了name="张无忌", name_title="剑宗剑神", life=100, energy=100四个参数,你可也实现更多
    2、实例调用了hero.introduce() 做自我介绍
    3、实例调用了hero.speak("win") 做胜利发言,你也可以尝试失败感言
"""
if __name__ == "__main__":
    user = input("请输入你的名字:")
    my_Hero = Hero("黄蓉", "", 100, 100, 15, 5, ["乱A", "落英神剑掌"],
                   "桃花岛乃我父亲所建，我从小就住在桃花岛，你能奈我何？")
    if my_Hero.create_my_hero(user):
        my_Hero.introduce("神气")
        print("华山论剑,多路英雄已到达战场！")
        opponent = my_Hero.choose_opponent()
        choice = input("请选择你的对手:")
        while choice not in opponent:
            print("没有这个对手！")
            choice = input("请选择你的对手:")
        else:
            print("战斗一触即发,请做好准备！！！")
            start_fight = input("是否开始战斗?[y/n]") or "y"
            if start_fight == "y":
                result = my_Hero.challenge(user, choice)
                # print(result["result"])
                contents = result["result"]
                for content in contents:
                    console.print(Panel(content["content"].rstrip("\n"), title=content["title"], title_align="center", style="bold red"))
            else:
                print("你干嘛~哎哟~，战斗取消！")
