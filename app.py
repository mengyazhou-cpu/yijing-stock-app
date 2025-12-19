import streamlit as st
import datetime

# --- 页面配置 (适配手机) ---
st.set_page_config(page_title="股市易经推演", page_icon="🔮", layout="centered")

# --- 核心逻辑: 获取北京时间 ---
def get_beijing_time():
    # 获取UTC时间并手动加8小时，确保不依赖服务器时区
    utc_now = datetime.datetime.utcnow()
    beijing_now = utc_now + datetime.timedelta(hours=8)
    return beijing_now

# --- 核心算法区 ---

# 1. 基础八卦对应
TRIGRAMS = {
    1: '乾 (天)', 2: '兑 (泽)', 3: '离 (火)', 4: '震 (雷)',
    5: '巽 (风)', 6: '坎 (水)', 7: '艮 (山)', 8: '坤 (地)'
}

def get_hexagram_name(upper, lower):
    # 简化的卦名生成，实际可扩展
    return f"{TRIGRAMS[upper].split(' ')[0]}{TRIGRAMS[lower].split(' ')[0]}" 

def calculate_time_hexagram():
    """时间起卦法 (针对板块) - 使用北京时间"""
    now = get_beijing_time()
    
    y, m, d = now.year, now.month, now.day
    h = now.hour if now.hour != 0 else 24
    
    # 年月日数之和
    date_sum = y + m + d
    
    upper_num = date_sum % 8 or 8
    lower_num = (date_sum + h) % 8 or 8
    change_line = (date_sum + h) % 6 or 6
    
    return upper_num, lower_num, change_line

def calculate_stock_hexagram(code):
    """股票代码起卦法 (针对个股)"""
    code_str = str(code).zfill(6)
    
    # 上卦：前三位
    sum_head = sum(int(digit) for digit in code_str[:3])
    upper_num = sum_head % 8 or 8
    
    # 下卦：后三位
    sum_tail = sum(int(digit) for digit in code_str[3:])
    lower_num = sum_tail % 8 or 8
    
    # 动爻：(上+下+时辰) % 6
    # 既然是个股代码起卦，动爻通常结合当前时辰，这里也用北京时间
    now = get_beijing_time()
    h = now.hour if now.hour != 0 else 24
    
    total_sum = sum_head + sum_tail + h
    change_line = total_sum % 6 or 6
    
    return upper_num, lower_num, change_line

def interpret_trend(upper, lower):
    """简单的吉凶判断逻辑"""
    # 五行: 金(1,2) 木(4,5) 水(6) 火(3) 土(7,8)
    elements = {1:'金', 2:'金', 3:'火', 4:'木', 5:'木', 6:'水', 7:'土', 8:'土'}
    u_e = elements[upper]
    l_e = elements[lower]
    
    trend = "震荡/中性"
    color = "grey"
    
    if u_e == l_e:
        trend = "比和 (盘整蓄势)"
        color = "blue"
    # 这里的生克逻辑仅做简单模拟
    elif (u_e == '火' and l_e == '金') or (u_e == '金' and l_e == '木') or (u_e == '土' and l_e == '水'): 
        trend = "相克 (压力较大)"
        color = "green" 
    elif (l_e == '火' and u_e == '木') or (u_e == '土' and l_e == '火') or (u_e == '金' and l_e == '土'):
        trend = "相生 (支撑较强)"
        color = "red" 
        
    return trend, color

# --- APP 界面构建 ---

current_time = get_beijing_time()
date_str = current_time.strftime('%Y-%m-%d')
time_str = current_time.strftime('%H:%M')

st.title("📈 每日易经·盘面推演")
st.caption(f"📅 北京时间：{date_str} {time_str}")

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

with st.expander("查看板块解读"):
    st.write("此卦象基于当前的【北京时间】推演。")
    st.write("若【相生】则板块内部合力强，容易出机会；若【相克】则分歧大，建议防守。")

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
    st.write("结合代码数理与当前时辰。重点观察关键价位。")
    st.write("提示：汉宇集团五行属金，若遇火克需谨慎，遇土生则持股。")

# --- 底部功能 ---
st.divider()
if st.button("🔄 刷新卦象 (更新时间)"):
    st.rerun()
