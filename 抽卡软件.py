import random
import time

class GachaSimulator:
    def __init__(self):
        # 基础概率
        self.rate_fivestar = 0.006
        self.rate_fourstar = 0.051
        
        # 状态统计
        self.pity_4_star = 0      # 四星保底计数 (0-9)
        self.pity_5_star = 0      # 五星保底计数 (0-89)
        self.total_pulls = 0      # 总抽数
        self.num_fivestar = 0     # 五星数量
        self.num_fourstar = 0     # 四星数量
        self.up_count = 0         # 当期五星UP数量
        
        # 大小保底标记 (True表示大保底，False表示小保底)
        self.guarantee_5_star = False  
        self.guarantee_4_star = False 

        # 卡池数据(原神 4.2版本 上半卡池：芙宁娜)
        self.pool_3_star =["冷刃", "黎明神剑", "飞天御剑", "沐浴龙血的剑", "铁影阔剑", "以理服人", "黑缨枪", "讨龙英杰谭", "魔导绪论", "翡玉法球", "弹弓", "神射手之誓", "鸦羽弓"]
        # 四星池划分
        self.pool_4_star_up =["夏洛蒂", "柯莱", "北斗"]
        self.pool_4_star_std =["班尼特", "行秋", "香菱", "久岐忍", "芭芭拉", "凝光", "诺艾尔", "砂糖", "迪奥娜", "罗莎莉亚", "瑶瑶"]
        # 五星池划分
        self.pool_5_star_up = ["芙宁娜"]
        self.pool_5_star_std =[ "琴", "迪卢克", "七七", "莫娜", "刻晴", "提纳里", "迪希雅"]
    
    def pull_5_star(self):
        if self.guarantee_5_star or random.random() < 0.5:
            character = self.pool_5_star_up[0]
            self.guarantee_5_star = False  # 抽到UP，重新变为小保底
            self.up_count += 1
        else:
            character = random.choice(self.pool_5_star_std)
            self.guarantee_5_star = True   # 歪了，下次是大保底
            
        print(f"⭐⭐⭐⭐⭐ 恭喜你，抽到五星角色【{character}】！")
        self.pity_5_star = 0
        self.num_fivestar += 1
        # 注意：米哈游游戏的机制中，出5星不重置4星保底计数，所以不改动 pity_4_star

    def pull_4_star(self):
        if self.guarantee_4_star or random.random() < 0.5:
            character = random.choice(self.pool_4_star_up)
            self.guarantee_4_star = False
        else:
            character = random.choice(self.pool_4_star_std)
            self.guarantee_4_star = True
            
        print(f"⭐⭐⭐⭐ 获得四星角色【{character}】！")
        self.pity_4_star = 0  # 重置四星保底
        self.pity_5_star += 1
        self.num_fourstar += 1

    def pull_3_star(self):
        item = random.choice(self.pool_3_star)
        print(f"⭐⭐⭐ 获得三星物品【{item}】")
        self.pity_4_star += 1
        self.pity_5_star += 1

    def single_pull(self):
        self.total_pulls += 1
        
        # 计算当前五星出金率 (软保底：75抽之后概率线性增加)
        current_5_star_rate = self.rate_fivestar
        if self.pity_5_star >= 75:
            current_5_star_rate += (self.pity_5_star - 75) * 0.07

        # 随机抽取判断
        rand_val = random.random()
        
        if rand_val <= current_5_star_rate:
            self.pull_5_star()
        elif rand_val <= current_5_star_rate + self.rate_fourstar:
            self.pull_4_star()
        elif self.pity_4_star >= 9:
            # 触发四星保底
            self.pull_4_star()
        else:
            self.pull_3_star()

    def ten_pull(self):
        for _ in range(10):
            self.single_pull()
        print(f"--- 当前距离五星保底还剩 {90 - self.pity_5_star} 抽 ---")

    def show_statistics(self):
        print("\n" + "="*30)
        print("🎮 抽卡结束 🎮")
        print(f"共抽卡: {self.total_pulls} 次")
        print(f"五星总数: {self.num_fivestar} 个")
        print(f"四星总数: {self.num_fourstar} 个")
        
        if self.up_count > 0:
            avg_pulls = self.total_pulls / self.up_count
            print(f"UP五星数量: {self.up_count} 个")
            print(f"平均出UP金抽数: {avg_pulls:.2f} 抽/个")
        print("="*30 + "\n")
        time.sleep(2)

    def start(self):
        # 使用 while 循环替代递归，避免栈溢出
        while True:
            choice = input("\n请选择抽卡方式：[1]单抽 [2]十连抽 [0]退出系统: ").strip()
            
            if choice == '1':
                self.single_pull()
                print(f"--- 当前距离五星保底还剩 {90 - self.pity_5_star} 抽 ---")
            elif choice == '2':
                self.ten_pull()
            elif choice == '0':
                self.show_statistics()
                break
            else:
                print("输入无效，请重新输入！")

# 程序的标准入口
if __name__ == "__main__":
    print("欢迎来到 原神 4.2 芙宁娜 抽卡模拟器！")
    simulator = GachaSimulator()
    simulator.start()
    input("请按回车键退出程序...")