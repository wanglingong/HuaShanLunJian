import random
from flask import Flask, request, jsonify
import copy

# damage_rate = 1.5
"""
    华山论剑-英雄类
    英雄属性：体力、内力、名谓、技能、攻击力、防御力等
    口才1：自报家门
    口才2：发表获胜感言和战败感言
    能力1：修炼，每次修炼会增加体力、内力、攻击力、防御力的其中几个
    技能1：普通攻击、防御
    技能2：带名字的技能,如：蛤蟆功等
"""

"""
    ************ 任务书 **************
    * 任务1:实现这个英雄类             *
    * 任务2:创建东邪和西毒             *
    * 任务3:打印各自的属性             *
    * 任务4:各自修炼十次后打印他的属性   *
    * 任务5:五招内看看胜负             *
    ********************************* 
"""
app = Flask(__name__)


class Hero:
    """
    任务1 实现英雄类
    """

    def __init__(self, name, title, life, energy, attack, defense, skills, introduction):
        # 英雄属性
        self.name = name
        self.title = title
        self.life = life
        self.energy = energy
        self.attack = attack
        self.defense = defense
        self.skills = skills
        self.introduction = introduction

    def __str__(self):
        # 打印英雄的属性
        return f"【{self.name}】{self.introduction}\n" \
               f"体力：{self.life}\n" \
               f"内力：{self.energy}\n" \
               f"攻击力：{self.attack}\n" \
               f"防御力：{self.defense}\n" \
               f"技能：{self.skills}\n"

    def introduce(self):
        # 口才1 自报家门
        return f"我{self.name}来也,{self.introduction}" + "\n"

    def speak(self, status_fight):
        # 口才2 发表获胜感言和战败感言
        mood, words = self.get_words(status_fight)
        return f"{self.name}【{mood}】地说:{words}" + "\n"

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

    def practice(self):
        # 能力1 修炼
        # 修炼后的属性变化
        """
            # "+=" 运算符等价于在自身加上数值
            # 即 a += 1 等价于  a = a + 1
            # random.randint(1, 10) 表示随机生成1到10之间的整数
        """
        self.life += random.randint(1, 10)
        self.energy += random.randint(1, 2)
        self.attack += random.randint(1, 10)
        self.defense += random.randint(1, 5)

    def attacker(self, opponent, skill_index=-1):
        attack_log = ""
        # 攻击
        # 技能的索引从0开始
        # 技能消耗是技能顺序的数倍
        if skill_index == -1:
            skill_index = random.randint(0, len(self.skills) - 1)
        skill = self.skills[skill_index]
        skill_cost = skill_index * 20
        if self.energy <= skill_cost:
            skill_index = 0
            skill2 = self.skills[skill_index]
            skill_cost = skill_index * 20
            attack_log += f"{self.name}的内力不足，无法使用{skill}, 只好【{skill2}】" + "\n"
        # 技能消耗 20 内力
        self.energy -= skill_cost
        # 技能效果统一为技能顺序的数倍
        damage = self.attack * (skill_index * 0.5 + 1) - opponent.defense
        attack_log += f"{self.name}对{opponent.name}使用{skill}。造成: {damage} 点伤害" + "\n"

        # 伤害反馈到对方身上
        opponent.life -= damage
        return attack_log

    def check_alive(self):
        if self.life <= 0:
            return True

    def challenge(self, opponent):
        challenge_log = []
        """
        # 挑战模式 五招内看看胜负
        """
        for i in range(5):
            round_log = {
                "title": "",
                "content": ""
            }
            arena = [self, opponent]
            # 随机打乱顺序
            random.shuffle(arena)
            # 谁先出招
            round_log["title"] = f"第{i+1}回合,{arena[0].name}先手"
            first = arena[0]
            second = arena[1]
            # 先手出招
            round_log["content"] += first.attacker(second, random.randint(0, len(first.skills) - 1))
            if second.check_alive():
                round_log += second.speak("lose")
                round_log += f"{second.name} 战败了……"
                round_log += first.speak("win")
                break
            # 后手出招
            round_log["content"] += second.attacker(first, random.randint(0, len(second.skills) - 1))
            if first.check_alive():
                round_log += first.speak("lose")
                round_log += f"{first.name} 战败了……"
                round_log += second.speak("win")
                break
            round_log["content"] += "【回合结束】"
            round_log["content"] += f"{self.name}剩余气血({self.life},{self.energy})|{opponent.name}剩余气血({opponent.life},{opponent.energy})" + "\n"
            challenge_log.append(round_log)

        end_log = {
            "title": "【点到即止】",
            "content": ""
        }
        end_log["content"] += self.speak("win")
        end_log["content"] += f"{self.name} 化解了 {opponent.name} 的攻势……" + "\n"
        end_log["content"] += opponent.speak("lose")
        challenge_log.append(end_log)
        return challenge_log


boss_dongxie = Hero("黄药师", "东邪", 100, 100, 15, 5, ["乱A", "落英神剑掌"], "桃花岛乃我一手所建，千树万花，迷人心智。")
boss_xi_du = Hero("欧阳锋", "西毒", 100, 100, 18, 3, ["乱A", "蛤蟆功"], "毒蛇为友，蛤蟆为伴，江湖谁人不知？谁人不晓？")
boss_list = [boss_dongxie, boss_xi_du]
users = {}


@app.route("/create_player", methods=["POST"])
def create_player():
    data = request.json
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id 是必须的"}), 400

    hero = Hero(
        name=data["hero"].get("name"),
        title=data["hero"].get("title"),
        life=data["hero"].get("life", 100),
        energy=data["hero"].get("energy", 50),
        attack=data["hero"].get("attack", 20),
        defense=data["hero"].get("defense", 10),
        skills=data["hero"].get("skills", ["普通攻击"]),
        introduction=data["hero"].get("introduction", "无")
    )
    users[user_id] = hero
    return jsonify({"message": f"用户 {user_id} 的角色创建成功", "hero": hero.__dict__})


@app.route("/create_boss", methods=["POST"])
def create_boss():
    data = request.json
    user_id = data.get("user_id")
    if user_id != "oulinko":
        return jsonify({"error": "该用户无法创建boss"}), 400

    hero = Hero(
        name=data.get("name"),
        title=data.get("title"),
        life=data.get("life", 100),
        energy=data.get("energy", 50),
        attack=data.get("attack", 20),
        defense=data.get("defense", 10),
        skills=data.get("skills", ["普通攻击"]),
        introduction=data.get("introduction", "无")
    )
    boss_list.append(hero)
    return jsonify({"message": f"新boss创建成功，欢迎体验", "hero": hero.__dict__})


@app.route("/get_boss_list", methods=["GET"])
def get_boss():
    return jsonify({"boss_list": [boss.name for boss in boss_list]})


@app.route("/attack/<user_id>/<boss_name>", methods=["GET"])
def attack_boss(user_id, boss_name):
    # 挑战模式 五招内看看胜负
    boss = next((boss for boss in boss_list if boss.name == boss_name), None)
    challenging_boss = copy.deepcopy(boss)
    challenging_boss.introduce()
    result = challenging_boss.attacker(users[user_id])
    return jsonify({"result": result})


@app.route("/challenge/<user_id>/<boss_name>", methods=["GET"])
def challenge_boss(user_id, boss_name):
    # 挑战模式 五招内看看胜负
    boss = next((boss for boss in boss_list if boss.name == boss_name), None)
    challenging_boss = copy.deepcopy(boss)
    challenging_boss.introduce()
    result = challenging_boss.challenge(users[user_id])
    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5050, debug=True)