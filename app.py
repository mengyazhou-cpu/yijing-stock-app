import streamlit as st
import datetime
import lunarcalendar # 需要 pip install lunarcalendar
from sxtwl import Lunar # 备选，或者直接用简单算法，这里为了通用性使用简化算法模拟易经逻辑

# --- 页面配置 (适配手机) ---
st.set_page_config(page_title="股市易经推演", page_icon="🔮", layout="centered")

# --- 核心算法区 (简化模拟版，确保逻辑自洽) ---

# 1. 基础八卦对应
TRIGRAMS = {
    1: '乾 (天)', 2: '兑 (泽)', 3: '离 (火)', 4: '震 (雷)',
    5: '巽 (风)', 6: '坎 (水)', 7: '艮 (山)', 8: '坤 (地)'
}
HEXAGRAM_NAMES = {
    # 简化的64卦名查询字典 (此处仅列出部分示例逻辑，实际需完整字典，为节省篇幅用通用逻辑生成)
    (1,1): "乾为天", (3,4): "火雷噬嗑", (2,4): "泽雷随", (3,1): "火天大有",
    (3,7): "火山旅", (3,5): "火风鼎", (1,1): "乾为天"
    # ... 实际代码建议引入完整库，这里用算法生成描述
}

def get_hexagram_name(upper, lower):
    # 这里为了演示，返回卦象结构描述
    return f"{TRIGRAMS[upper].split(' ')[0]}{TRIGRAMS[lower].split(' ')[0]}" 

def calculate_time_hexagram():
    """时间起卦法 (针对板块)"""
    now = datetime.datetime.now()
    # 农历转换简化逻辑：取年月日时之和
    # 实际上应调用农历库，这里用公历模拟随机性但保持每日固定
    y, m, d = now.year, now.month, now.day
    h = now.hour if now.hour != 0 else 24
    
    upper_num = (y + m + d) % 8 or 8
    lower_num = (y + m + d + h) % 8 or 8
    change_line = (y + m + d + h) % 6 or 6
    
    return upper_num, lower_num, change_line

def calculate_stock_hexagram(code):
    """股票代码起卦法 (针对个股)"""
    # 补全6位代码
    code_str = str(code).zfill(6)
    head = int(code_str[:3])
    tail = int(code_str[3:])
    
    # 上卦：前三位之和 % 8
    sum_head = sum(int(digit) for digit in code_str[:3])
    upper_num = sum_head % 8 or 8
    
    # 下卦：后三位之和 % 8
    sum_tail = sum(int(digit) for digit in code_str[3:])
    lower_num = sum_tail % 8 or 8
    
    # 动爻：(上和+下和+时辰) % 6
    # 默认取午盘时间(12点)作为定数
    total_sum = sum_head + sum_tail + 6 
    change_line = total_sum % 6 or 6
    
    return upper_num, lower_num, change_line

def interpret_trend(upper, lower):
    """简单的吉凶判断逻辑"""
    # 生克关系 (简化)
    # 金:1,2 | 木:4,5 | 水:6 | 火:3 | 土:7,8
    elements = {1:'金', 2:'金', 3:'火', 4:'木', 5:'木', 6:'水', 7:'土', 8:'土'}
    u_e = elements[upper]
    l_e = elements[lower]
    
    trend = "震荡/中性"
    color = "grey"
    
    if u_e == l_e:
        trend = "比和 (盘整蓄势)"
        color = "blue"
    elif (u_e == '火' and l_e == '金') or (u_e == '金' and l_e == '木'): 
        trend = "相克 (震荡调整)"
        color = "green" # 跌
    elif (l_e == '火' and u_e == '木') or (u_e == '土' and l_e == '火'):
        trend = "相生 (趋势向上)"
        color = "red" # 涨
        
    return trend, color

# --- APP 界面构建 ---

st.title("📈 每日易经·盘面推演")
st.caption(f"📅 {datetime.date.today().strftime('%Y-%m-%d')} | 仅供娱乐参考")

st.divider()

# Tab 1: 机器人板块
st.subheader("🤖 机器人板块")
u1, l1, c1 = calculate_time_hexagram()
trend1, color1 = interpret_trend(u1, l1)

col1, col2 = st.columns([1, 2])
with col1:
    st.markdown(f"## {TRIGRAMS[u1]}")
    st.markdown("---")
    st.markdown(f"## {TRIGRAMS[l1]}")
with col2:
    st.markdown(f"**本卦：** {get_hexagram_name(u1, l1)}")
    st.markdown(f"**动爻：** 第 {c1} 爻")
    st.markdown(f"**趋势判定：** :{color1}[{trend1}]")

with st.expander("查看详细解读"):
    st.write("根据今日时间起卦，上卦为体，下卦为用。需结合开盘量能判断。若动爻在上位，关注高位股风险；若动爻在下位，关注补涨机会。")

st.divider()

# Tab 2: 汉宇集团
st.subheader("🏭 汉宇集团 (300403)")
u2, l2, c2 = calculate_stock_hexagram(300403)
trend2, color2 = interpret_trend(u2, l2)

col3, col4 = st.columns([1, 2])
with col3:
    st.markdown(f"## {TRIGRAMS[u2]}")
    st.markdown("---")
    st.markdown(f"## {TRIGRAMS[l2]}")
with col4:
    st.markdown(f"**本卦：** {get_hexagram_name(u2, l2)}")
    st.markdown(f"**动爻：** 第 {c2} 爻")
    st.markdown(f"**趋势判定：** :{color2}[{trend2}]")

with st.expander("查看个股策略"):
    st.write("基于代码数理起卦。重点观察关键价位支撑。若出现相生卦象，建议持股；若相克，建议做T降本。")

# --- 底部功能 ---
st.divider()
if st.button("🔄 刷新卦象"):
    st.rerun()

st.info("💡 提示：点击浏览器分享按钮，选择“添加到主屏幕”，即可像App一样使用。")