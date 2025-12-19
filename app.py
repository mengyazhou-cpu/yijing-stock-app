import streamlit as st
import datetime
import random

# --- 页面设置 ---
st.set_page_config(page_title="易经实盘 V3.0", page_icon="⚡", layout="centered")

# --- 核心工具 ---
def get_beijing_time():
    utc_now = datetime.datetime.utcnow()
    return utc_now + datetime.timedelta(hours=8)

def get_interpretation(u_val, l_val, context="sector"):
    """
    u_val: 上卦 (1-8)
    l_val: 下卦 (1-8)
    context: 'sector' (板块) 或 'stock' (个股)
    """
    elements = {1:'金', 2:'金', 3:'火', 4:'木', 5:'木', 6:'水', 7:'土', 8:'土'}
    u_e = elements[u_val]
    l_e = elements[l_val]
    
    # 基础分
    score = 50
    signal = "横盘震荡"
    color = "orange"
    advice = "观望"
    comment = "多空平衡。"

    # --- 逻辑判定 ---
    
    # 1. 比和 (同五行)
    if u_e == l_e:
        score = 55
        signal = "⚖️ 蓄势整固"
        comment = "主力高度控盘，正在清洗浮筹。"
        advice = "【持股】只要不破位，继续持有。"

    # 2. 相生 (大吉)
    # 木生火 (3,4/5)
    elif (u_e == '火' and l_e in ['木']) or (l_e == '火' and u_e in ['木']):
        score = 95
        signal = "🔥 主升浪启动"
        color = "red"
        comment = "木火通明，题材爆发，买盘汹涌。"
        advice = "【猛干】趋势确立，积极做多。"
        
    # 土金相生 (1/2, 7/8)
    elif (u_e in ['土'] and l_e in ['金']) or (l_e in ['土'] and u_e in ['金']):
        score = 85
        signal = "📈 稳步推升"
        color = "red"
        comment = "底部筹码锁定良好，价升量增。"
        advice = "【低吸】回踩5日线是绝佳买点。"

    # 其他相生
    elif (u_e in ['水'] and l_e in ['木']) or (l_e in ['水'] and u_e in ['木']):
        score = 75
        signal = "🌤️ 温和反弹"
        color = "red"
        comment = "有资金呵护，走势强于大盘。"
        advice = "【持有】耐心等待拉升。"

    # 3. 相克 (凶/调整)
    # 火克金 (3, 1/2) - 汉宇最怕这个
    elif (u_e == '火' and l_e in ['金']) or (l_e == '火' and u_e in ['金']):
        score = 25
        signal = "📉 抛压沉重"
        color = "green"
        comment = "上方套牢盘巨大，主力拉高出货。"
        advice = "【快跑】趁反弹减仓，切勿追高。"
        
    # 其它相克
    else:
        score = 40
        signal = "🌧️ 震荡下行"
        color = "green"
        comment = "分歧加大，承接乏力。"
        advice = "【防守】不要轻易补仓，观察支撑。"

    return signal, color, comment, advice, score

# --- 动态算卦函数 ---

def calculate_sector_hex():
    """板块：基于日期+小时 (宏观趋势)"""
    now = get_beijing_time()
    # 算法：日期和 vs 日期+小时
    date_sum = now.year + now.month + now.day
    u = date_sum % 8 or 8
    l = (date_sum + now.hour) % 8 or 8
    return u, l

def calculate_stock_hex(code):
    """个股：基于代码+分钟 (微观波动)"""
    now = get_beijing_time()
    code_str = str(code)
    
    # 基础数理
    base_head = sum(int(x) for x in code_str[:3])
    base_tail = sum(int(x) for x in code_str[3:])
    
    # !!! 关键修改：加入分钟级扰动，模拟盘中实时波动 !!!
    # 分钟数如果是偶数，对上卦产生影响；奇数对下卦产生影响
    minute_factor = now.minute % 3 
    
    u = (base_head + now.hour) % 8 or 8
    l = (base_tail + now.minute) % 8 or 8 # 下卦随分钟剧烈变动
    
    return u, l

# --- 界面渲染 ---

now_bj = get_beijing_time()
st.title("⚡ 易经实盘 V3.0")
st.caption(f"📅 北京时间：{now_bj.strftime('%H:%M:%S')} (每分钟刷新)")

# 1. 机器人板块
st.divider()
st.subheader("🤖 机器人板块 (宏观)")
u1, l1 = calculate_sector_hex()
sig1, col1, com1, adv1, sc1 = get_interpretation(u1, l1)

if col1 == 'red':
    st.error(f"### {sig1}")
elif col1 == 'green':
    st.success(f"### {sig1}")
else:
    st.warning(f"### {sig1}")
    
st.write(f"**分析：** {com1}")
st.write(f"**策略：** {adv1}")
st.caption(f"🔢 卦象底层数据：{u1} / {l1}") # 显示数据证明不同

# 2. 汉宇集团
st.divider()
st.subheader(f"🏭 汉宇集团 (300403)")
u2, l2 = calculate_stock_hex(300403)
sig2, col2, com2, adv2, sc2 = get_interpretation(u2, l2, context="stock")

# 强行对比逻辑：如果个股分数高于板块
strength = ""
if sc2 > sc1:
    strength = "🔥 强于板块 (龙头相)"
elif sc2 < sc1:
    strength = "🐢 弱于板块 (跟风)"
else:
    strength = "🤝 同步大盘"

st.info(f"**当前状态：{strength}**")

if col2 == 'red':
    st.error(f"### {sig2}")
elif col2 == 'green':
    st.success(f"### {sig2}")
else:
    st.warning(f"### {sig2}")

st.write(f"**分析：** {com2}")
st.write(f"**策略：** {adv2}")
st.caption(f"🔢 卦象底层数据：{u2} / {l2} (随分钟变化)")

# --- 刷新 ---
st.divider()
if st.button("🔄 点我刷新 (模拟盘中异动)"):
    st.rerun()
