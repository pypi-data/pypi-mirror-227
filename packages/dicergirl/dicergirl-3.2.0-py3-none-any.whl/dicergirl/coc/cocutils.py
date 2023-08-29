from typing import Optional
try:
    from ..utils.docimasy import expr
    from ..utils.messages import temporary_madness, madness_end, phobias, manias
    from ..utils.dicer import Dice
    from ..utils.multilogging import multilogger
    from .coccards import coc_cards, coc_attrs_dict
    from .investigator import Investigator
except ImportError:
    from dicergirl.utils.docimasy import expr
    from dicergirl.utils.messages import temporary_madness, madness_end, phobias, manias
    from dicergirl.utils.dicer import Dice
    from dicergirl.utils.multilogging import multilogger
    from dicergirl.coc.coccards import coc_cards, coc_attrs_dict
    from dicergirl.coc.investigator import Investigator

import random
import re

logger = multilogger(name="Dicer Girl", payload="COCUtil")

def sc(arg, event):
    """ COC 疯狂检定 """
    reply = []
    try:
        args = arg.split(" ")
        args = list(filter(None, args))
        using_card = False
        s_and_f = args[0].split("/")
        success = Dice().parse(s_and_f[0])
        success.roll()
        success = success.calc()
        failure = Dice().parse(s_and_f[1])
        failure.roll()
        failure = failure.calc()
        if len(args) > 1:
            card = {"san": int(args[1]), "name": "未指定调查员"}
            reply.append("[Oracle] 用户指定了应当检定的 SAN 值, 这会使得本次检定不会被记录.")
            using_card = False
        else:
            card = coc_cards.get(event)
            using_card = True
        r = Dice().roll().calc()
        s = f"[Oracle] 调查员: {card['name']}\n"
        s += f"检定精神状态: {card['san']}\n"
        s += f"理智检定值: {r}, "
        if r <= card["san"]:
            down = success
            s += "检定成功.\n"
        else:
            down = failure
            s += "检定失败.\n"
        s += f"{card['name']} 理智降低了 {down} 点, "
        if down >= card["san"]:
            s += "陷入了永久性疯狂.\n"
        elif down >= (card["san"] // 5):
            s += "陷入了不定性疯狂.\n"
        elif down >= 5:
            s += "陷入了临时性疯狂.\n"
        else:
            s += "未受到严重影响.\n"
        card["san"] -= down
        if card["san"] <= 0:
            card["san"] = 0
        s += f"当前 {card['name']} 的 SAN 值为: {card['san']}"
        reply.append(s)
        if using_card:
            coc_cards.update(event, card)
        return reply
    except:
        return "[Oracle] 产生了未知的错误, 你可以使用`.help ra`指令查看指令使用方法.\n如果你确信这是一个错误, 建议联系开发者获得更多帮助.\n如果你是具有管理员权限, 你可以使用`.debug on`获得更多信息."

def st():
    """ COC 射击检定 """
    result = random.randint(1, 20)
    if result < 4:
        rstr = "右腿"
    elif result < 7:
        rstr = "左腿"
    elif result < 11:
        rstr = "腹部"
    elif result < 16:
        rstr = "胸部"
    elif result < 18:
        rstr = "右臂"
    elif result < 20:
        rstr = "左臂"
    elif result < 21:
        rstr = "头部"
    return "D20=%d: 命中了%s" % (result, rstr)

def coc_at(args, event):
    """ COC 伤害检定 """
    inv = Investigator().load(coc_cards.get(event))
    method = "+"

    if args:
        d = Dice().parse(args).roll()
    else:
        d = Dice().parse("1d6").roll()

    if "d" in inv.db():
        db = Dice(inv.db()).roll()
        dbtotal = db.total
        db = db.db
    else:
        db = int(inv.db())
        dbtotal = db
        if db < 0:
            method = ""

    return f"[Oracle] 投掷 {d.db}{method}{db}=({d.total}+{dbtotal})\n造成了 {d.total+dbtotal}点 伤害."

def coc_dam(args, message):
    """ COC 承伤检定 """
    card = coc_cards.get(message)
    if not card:
        return "[Oracle] 未找到缓存数据, 请先使用`.coc`指令进行车卡生成角色卡并`.set`进行保存."
    max_hp = card["con"] + card["siz"]
    try:
        arg = int(args[0])
        card["hp"] -= arg
        r = f"[Orcale] {card['name']} 失去了 {arg}点 生命"
    except:
        d = Dice().parse("1d6").roll()
        card["hp"] -= d.total
        r = "[Oracle] 投掷 1D6={d}\n受到了 {d}点 伤害".format(d=d.calc())
    if card["hp"] <= 0:
        card["hp"] = 0
        r += f", 调查员 {card['name']} 已死亡."
    elif (max_hp * 0.8) <= card["hp"] and (card["hp"] < max_hp):
        r += f", 调查员 {card['name']} 具有轻微伤."
    elif (max_hp * 0.6 <= card["hp"]) and (card["hp"] <= max_hp * 0.8):
        r += f", 调查员 {card['name']} 进入轻伤状态."
    elif (max_hp * 0.2 <= card["hp"]) and (card["hp"] <= max_hp * 0.6):
        r += f", 调查员 {card['name']} 身负重伤."
    elif max_hp * 0.2 >= card["hp"]:
        r += f", 调查员 {card['name']} 濒死."
    else:
        r += "."
    coc_cards.update(message, card)
    return r

def coc_ra(args, event):
    """ COC 技能检定 """
    if len(args) == 0:
        return "[Oracle] 错误: 检定技能需要给入技能名称.\n使用`.help ra`指令查看指令使用方法."
    if len(args) > 2:
        return "[Oracle] 错误: 参数过多(最多2需要但%d给予)." % len(args)

    card_data = coc_cards.get(event)
    if not card_data:
        if len(args) == 1:
            return "[Oracle] 你尚未保存人物卡, 请先执行`.coc`车卡并执行`.set`保存.\n如果你希望快速检定, 请执行`.ra [str: 技能名] [int: 技能值]`."

        return str(expr(Dice(), args[1]))

    inv = Investigator().load(card_data)

    is_base = False
    exp = None
    for _, alias in coc_attrs_dict.items():
        if args[0] in alias:
            exp = int(getattr(inv, alias[0]))
            is_base = True
            break

    if not is_base:
        for skill in inv.skills:
            if args[0] == skill:
                exp = inv.skills[skill]
                break
            else:
                exp = False

    if not exp:
        if len(args) == 1:
            return "[Oracle] 你没有这个技能, 如果你希望快速检定, 请执行`.ra [str: 技能名] [int: 技能值]`."

        if not args[1].isdigit():
            return "[Oracle] 技能值应当为整型数, 使用`.help ra`查看技能检定指令使用帮助."

        return str(expr(Dice(), int(args[1])))
    elif exp and len(args) > 1:
        if not args[1].isdigit():
            return "[Oracle] 技能值应当为整型数, 使用`.help ra`查看技能检定指令使用帮助."

        reply = [f"[Oracle] 你已经设置了技能 {args[0]} 为 {exp}, 但你指定了检定值, 使用指定检定值作为替代."]
        reply.append(str(expr(Dice(), int(args[1]))))
        return reply

    time = 1
    r = expr(Dice(), exp)

    for _ in range(time-1):
        r += expr(Dice(), exp)

    return r.detail

def ti():
    """ COC 临时疯狂检定 """
    i = random.randint(1, 10)
    r = "临时疯狂判定1D10=%d\n" % i
    r += temporary_madness[i-1]
    if i == 9:
        j = random.randint(1, 100)
        r += "\n恐惧症状为: \n"
        r += phobias[j-1]
    elif i == 10:
        j = random.randint(1, 100)
        r += "\n狂躁症状为: \n"
        r += manias[j-1]
    r += "\n该症状将会持续1D10=%d" % random.randint(1, 10)
    return r

def li():
    """ COC 总结疯狂检定 """
    i = random.randint(1, 10)
    r = "总结疯狂判定1D10=%d\n" % i
    r += madness_end[i-1]
    if i in [2, 3, 6, 9, 10]:
        r += "\n调查员将在1D10=%d小时后醒来" % random.randint(1, 10)
    if i == 9:
        j = random.randint(1, 100)
        r += "\n恐惧症状为: \n"
        r += phobias[j-1]
    elif i == 10:
        j = random.randint(1, 100)
        r += "\n狂躁症状为: \n"
        r += manias[j-1]
    return r

def rb(args):
    """ COC 奖励骰 """
    if args:
        match = re.match(r'([0-9]{1,2})([a-zA-Z\u4e00-\u9fa5]*)', args)
    else:
        match = None
    ten = []
    if match:
        t = int(match[1]) if match[1] else 1
        reason = f"由于 {match[2]}:\n" if match[2] else ""
    else:
        reason = ""
        t = 1
    for _ in range(t):
        _ = Dice("1d10").roll().calc()
        _ = _ if _ != 10 else 0
        ten.append(_)
    result = Dice("1d100").roll().calc()
    ten.append(result//10)
    ften = min(ten)
    ten.remove(result//10)
    return f"{reason}奖励骰:\nB{t}=(1D100={result}, {ten})={ften}{str(result)[-1]}"

def rp(args):
    """ COC 惩罚骰 """
    if args:
        match = re.match(r'([0-9]{1,2})([a-zA-Z\u4e00-\u9fa5]*)', args)
    else:
        match = None
    ten = []
    if match:
        t = int(match[1]) if match[1] else 1
        reason = f"由于 {match[2]}:\n" if match[2] else ""
    else:
        reason = ""
        t = 1
    for _ in range(t):
        _ = Dice("1d10").roll().calc()
        _ = _ if _ != 10 else 0
        ten.append(_)
    result = Dice("1d100").roll().calc()
    ten.append(result//10)
    ften = max(ten)
    ten.remove(result//10)
    return f"{reason}惩罚骰:\nB{t}=(1D100={result}, {ten})={ften}{str(result)[-1]}"

def coc_en(event, args):
    """ COC 技能成长检定 """
    if not args:
        return "[Oracle] 错误: 检定技能需要给入技能名称.\n使用`.help ra`指令查看指令使用方法."

    try:
        arg = int(args[1])
    except ValueError:
        return "[Oracle] 错误: 给定需要消耗的激励点应当为整型数.\n使用`.help ra`指令查看指令使用方法."

    check = random.randint(1, 100)

    if check > arg or check > 95:
        plus = random.randint(1, 10)
        r = "判定值%d, 判定成功, 技能成长%d+%d=%d" % (check, arg, plus, arg+plus)
        return r + "\n温馨提示: 如果技能提高到90%或更高, 增加2D6理智点数。"
    else:
        return "判定值%d, 判定失败, 技能无成长。" % check
