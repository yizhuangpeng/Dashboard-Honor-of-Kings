from streamlit_echarts import st_pyecharts
from streamlit_echarts import JsCode
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import pickle
from PIL import Image
import requests
from io import BytesIO
import seaborn as sns
import numpy as np

from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.commons.utils import JsCode
from pyecharts.charts import Pie
from pyecharts.charts import EffectScatter
from pyecharts.globals import SymbolType
from pyecharts.charts import Scatter3D
from pyecharts.globals import ThemeType
from pyecharts.charts import Radar
from pyecharts.charts import Line

from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import plot_tree
from dtreeviz.trees import dtreeviz
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis


audio_file = open('welcome.ogg', 'rb')
audio_bytes = audio_file.read()

st.markdown('# Dashboard for Honor of Kings')
with st.beta_expander("Group Member"):
    st.write('**_PENG YIZHUANG_**: A0220532X; **_LIU YUTAO_**: A0220421A;')
    st.write('**_YANGCHEN_**: A0220507U; **_ZHANG CHENGWEI_**: A0220362W; **_ZHANG FAN_**: A0220403A')
    st.audio(audio_bytes, format='audio/ogg')
    
@st.cache()
def return_image(link):
    response = requests.get(link)
    img = Image.open(BytesIO(response.content))
    return img


#Part 1 Introduction of Honor of Kings
st.markdown('- **Part 1: Introduction of Honor of Kings**')
st.sidebar.write('### Part 1: Introduction of Honor of Kings')
if st.sidebar.checkbox('Introduction of Honor of Kings'):
    st.image(return_image('http://p4.itc.cn/images01/20200624/5ac1c76409cc4f88b4e375c836dfaefc.jpeg'))
    st.write('Honor of Kings:sunglasses:, is a Multiplayer Online Battle Arena game developed by Tencent and launched in 2015. Five years after its launch, it still has 100 million average daily active users and maintains a position of China’s top1 mobile game.')
    st.write("Till now, there are 102 heroes in the game. They belong to six different positions, including Archer, Mage, Assassin, Support, Tank, and Warrior. All of these roles have special abilities and come handy in different fights.")
    st.write("In this game, you can firstly choose from both a variety of battle modes, such as 1v1, 3v3, 5v5, and multiplayer battles and a wide variety of heroes, all of which have special abilities, exclusive skins and a special backstory and then control the hero and kill non-player characters and opponents to gain more experience and gold that can be used to upgrade your hero and buy equipment to gain more power. The condition to win the game is that your team succeed to destroy the enemy's towers and crystal.")
    
@st.cache()

def return_data(csv_name):
    x=pd.read_csv(csv_name)
    return x
hero = return_data('Hero Attributes.csv')
radar = return_data('Radar.csv')
combat=return_data('combat.csv')




    
#Part 2 Visualization
st.markdown('- **Part 2: Overview of attributes to Heros in Honor of Kings**')Q
    st.sidebar.write('### Part 2: Overview of attributes to Heros in Honor of Kings')œq

#2.1
topic_list=st.sidebar.multiselect('2.1 Choose to see Topics',['Hero Postion','Radar Chart by Hero Position','Radar Chart by Hero'])

def pie_base() -> Pie:
    position_name = list(hero['Position1'].value_counts().keys()) # Read column position 1 and count by groups to locate 
    position_value = [v for k,v in hero['Position1'].value_counts().items()] # make a sum
    c = (
        Pie()
        .add("", [list(z) for z in zip(position_name, position_value)])
        .set_global_opts(title_opts=opts.TitleOpts(title='Hero Postion'))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    return c

fig_2=pie_base()

#Radar_Positions

@st.cache

def return_index(hero,data):
    for i in range(len(data)):
        if data[i][0]['name']==hero:
            return i
        
c1_schema = [
    {"name": "Health points","min":3060,"max":3250},
    {"name": "Physical attack","min":160,"max":175},
    {"name": "Speed","min":350,"max":390},
    {"name": "Health regeneration","min":40,"max":55},
    {"name": "Physical defense","min":85,"max":105}
]

c1 = (
    Radar()
    .add_schema(schema=c1_schema, shape="circle")
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )

data_position=[[{'value':[3110,164.0,362,44,90], 'name': 'Mage'}],
              [{'value': [3229,170.0,381,49,92], 'name': 'Assassin'}],
              [{'value': [3150,171.0,354,40,89], 'name': 'Archer'}],
              [{'value': [3238,164.0,373,50,104], 'name': 'Support'}],
              [{'value': [3073,164.0,390,55,105], 'name': 'Tank'}],
              [{'value': [3217,164.5,380,54,98], 'name': 'Warrior'}]]

c_schema = [
    {"name": "Viability", "max": 10},
    {"name": "Attack damage", "max": 10},
    {"name": "Skill Effect", "max": 10},
    {"name": "Difficulty", "max": 10}
]
c = (
    Radar()
    .add_schema(schema=c_schema, shape="circle")
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )

data_Warrior=[[{'value': [5, 7, 6, 6], 'name': 'Yào'}], [{'value': [6, 9, 5, 5], 'name': 'Yunzhongjun'}], [{'value': [10, 8, 8, 6], 'name': 'Pangu'}], [{'value': [6, 6, 6, 5], 'name': 'Kuangtie'}], [{'value': [6, 4, 5, 6], 'name': 'Kai'}], [{'value': [9, 7, 7, 9], 'name': 'Nezha'}], [{'value': [8, 7, 6, 6], 'name': 'Yang Jian'}], [{'value': [3, 6, 8, 6], 'name': 'Athena'}], [{'value': [9, 5, 6, 7], 'name': 'Guan Yu'}], [{'value': [3, 9, 3, 7], 'name': 'Liu Bei'}], [{'value': [1, 4, 10, 8], 'name': 'Luna'}], [{'value': [3, 10, 4, 9], 'name': 'Miyamoto Musashi'}], [{'value': [2, 9, 5, 9], 'name': 'Hua Mulan'}], [{'value': [6, 6, 5, 6], 'name': 'Cao Cao'}], [{'value': [7, 6, 6, 5], 'name': 'Zhao Yun'}], [{'value': [9, 6, 2, 4], 'name': 'Da Mo'}], [{'value': [8, 7, 7, 6], 'name': 'Zhong Wuyan'}], [{'value': [6, 7, 3, 6], 'name': 'Laofuzi'}], [{'value': [6, 6, 3, 2], 'name': 'Dian Wei'}], [{'value': [8, 5, 8, 4], 'name': 'Sun Ce'}], [{'value': [5, 7, 7, 8], 'name': 'Ma Chao'}]]
data_mage=[[{'value': [6, 8, 8, 6], 'name': 'Xishi'}], [{'value': [5, 7, 8, 6], 'name': "Shangguan Wan'er"}], [{'value': [6, 8, 10, 6], 'name': 'Shen Mengxi'}], [{'value': [3, 2, 8, 4], 'name': 'Miledy'}], [{'value': [3, 5, 8, 7], 'name': 'Yixing'}], [{'value': [3, 7, 3, 6], 'name': 'Nvwa'}], [{'value': [3, 6, 8, 8], 'name': 'Zhuge Liang'}], [{'value': [3, 5, 9, 9], 'name': 'Mai Shiranui'}], [{'value': [2, 5, 9, 7], 'name': 'Zhou Yu'}], [{'value': [2, 6, 7, 6], 'name': 'Diao Chan'}], [{'value': [2, 3, 10, 8], 'name': 'Zhang Liang'}], [{'value': [8, 3, 5, 6], 'name': 'Mozi'}], [{'value': [4, 8, 7, 8], 'name': 'Wang Zhaojun'}], [{'value': [4, 9, 6, 6], 'name': 'Wu Zetian'}], [{'value': [6, 6, 7, 6], 'name': 'Yingzheng'}], [{'value': [4, 7, 3, 4], 'name': 'Bian Que'}], [{'value': [5, 9, 8, 6], 'name': 'Angela'}], [{'value': [1, 5, 8, 4], 'name': 'Xiaoqiao'}], [{'value': [1, 4, 9, 3], 'name': 'Daji'}], [{'value': [2, 5, 7, 3], 'name': 'Zhen Ji'}], [{'value': [5, 8, 7, 3], 'name': 'Gao Jianli'}], [{'value': [3, 6, 8, 9], 'name': 'Ganjiang Moye'}]]
data_Tank=[[{'value': [10, 10, 10, 5], 'name': "Chang'e"}], [{'value': [9, 5, 6, 6], 'name': 'Mengqi'}], [{'value': [9, 5, 5, 5], 'name': 'Su Lie'}], [{'value': [4, 6, 5, 4], 'name': 'Xiahou Dun'}], [{'value': [8, 4, 7, 5], 'name': 'Liu Bang'}], [{'value': [5, 8, 3, 5], 'name': 'Lv Bu'}], [{'value': [9, 4, 4, 3], 'name': 'Bai Qi'}], [{'value': [9, 4, 5, 4], 'name': 'Lian Po'}], [{'value': [8, 5, 7, 4], 'name': 'Xiang Yu'}], [{'value': [8, 6, 5, 3], 'name': 'Cheng Yaojin'}], [{'value': [7, 6, 5, 3], 'name': 'Arthur'}], [{'value': [5, 4, 7, 3], 'name': 'Miyue'}], [{'value': [10, 8, 10, 6], 'name': 'Zhu Bajie'}]]
data_Archer=[[{'value': [4, 10, 8, 5], 'name': 'Galo'}], [{'value': [3, 5, 8, 8], 'name': 'Gongsun Li'}], [{'value': [3, 6, 8, 6], 'name': 'Baili Shouyue'}], [{'value': [3, 6, 8, 6], 'name': 'Irene'}], [{'value': [2, 8, 4, 3], 'name': 'Huang Zhong'}], [{'value': [4, 8, 4, 7], 'name': 'Genghis Khan'}], [{'value': [7, 5, 6, 6], 'name': 'Marco Polo'}], [{'value': [3, 8, 5, 7], 'name': 'Yu Ji'}], [{'value': [4, 8, 4, 5], 'name': 'Li Yuanfang'}], [{'value': [3, 6, 8, 6], 'name': 'Houyi'}], [{'value': [5, 7, 6, 7], 'name': 'Sun Shangxiang'}], [{'value': [5, 7, 8, 6], 'name': 'Di Renjie'}], [{'value': [4, 7, 6, 6], 'name': 'Luban 7'}]]
data_Assassin=[[{'value': [4, 3, 8, 7], 'name': 'Sima Yi'}], [{'value': [5, 8, 6, 9], 'name': 'Pei Qinhu'}], [{'value': [5, 8, 8, 10], 'name': 'Baili Xuance'}], [{'value': [4, 6, 4, 4], 'name': 'Yuan Ge'}], [{'value': [6, 6, 5, 2], 'name': 'Tachibana Ukyo'}], [{'value': [2, 10, 4, 6], 'name': 'Lanlingwang'}], [{'value': [3, 7, 6, 5], 'name': 'Naklulu'}], [{'value': [3, 6, 8, 6], 'name': 'Li Bai'}], [{'value': [5, 5, 5, 4], 'name': 'Monkey King'}], [{'value': [2, 10, 4, 6], 'name': 'Ake'}], [{'value': [3, 6, 8, 8], 'name': 'Han Xin'}]]
data_Support=[[{'value': [10, 7, 8, 5], 'name': 'Yáo'}], [{'value': [10, 5, 10, 5], 'name': 'Dun Shan'}], [{'value': [7, 5, 8, 5], 'name': 'Yang Yuhuan'}], [{'value': [3, 4, 8, 5], 'name': 'Ming Shiyin'}], [{'value': [4, 7, 3, 4], 'name': 'Guiguzi'}], [{'value': [9, 5, 6, 6], 'name': 'Toho Taiichi'}], [{'value': [3, 3, 6, 8], 'name': 'Daqiao'}], [{'value': [8, 4, 5, 5], 'name': 'Taiyi Zhenren'}], [{'value': [6, 3, 5, 8], 'name': 'Cai Wenji'}], [{'value': [9, 2, 5, 7], 'name': 'Zhang Fei'}], [{'value': [9, 3, 7, 8], 'name': 'Zhong Kui'}], [{'value': [9, 2, 5, 7], 'name': 'Bull Demon'}], [{'value': [9, 2, 4, 4], 'name': 'Zhuang Zhou'}], [{'value': [7, 4, 6, 7], 'name': 'Sun Bin'}], [{'value': [8, 3, 5, 3], 'name': 'Liu Shan'}], [{'value': [1, 3, 8, 3], 'name': 'Jiang Ziya'}], [{'value': [8, 5, 7, 6], 'name': 'Master Luban'}]]

mark=0
for i in topic_list:
    if i=='Hero Postion':
        st.write('Till now, there are 102 heroes in the game. They belong to six different positions, including Archer, Mage, Assassin, Support, Tank, and Warrior. All of these roles have special abilities and come handy in different fights. Some of them are resilient to be attacked, some of them are born with huge damage and some of them control magic power.')
        st_pyecharts(fig_2,height=400,width=800)
        col1, col2= st.beta_columns([1,1.8])
        with col1:
            st.image(return_image('https://game.gtimg.cn/images/yxzj/img201606/heroimg/144/144-mobileskin-1.jpg'),width=200)
        with col2:
            st.write('Tank：Tank heroes have high health point and high defense. Their ability to survive is strong but perform normal on attack damage. They usually take a front row position in the battle and withstand enemy’s attacks.')
        col1, col2= st.beta_columns([1,1.8])
        with col1:
            st.image(return_image('https://game.gtimg.cn/images/yxzj/img201606/heroimg/193/193-mobileskin-1.jpg'),width=200)
        with col2:
            st.write('Warrior:  The warrior heroes are outstanding on both attack and defense. They usually stand behind a tank hero in the battle, undertaking a portion of enemy damage and fighting in the enemy lineup. Sometimes when there are no tank heroes in the team, warriors will also act as a pioneer.')
        col1, col2= st.beta_columns([1,1.8])
        with col1:
            st.image(return_image('https://game.gtimg.cn/images/yxzj/img201606/heroimg/109/109-mobileskin-1.jpg'),width=200)
        with col2:
            st.write('Mage: Mage heroes are weak on survival ability, but strong on attack output and control skills. They usually stand at back row position in the battle to attack and control enemy heroes.')
        col1, col2= st.beta_columns([1,1.8])
        with col1:
            st.image(return_image('https://game.gtimg.cn/images/yxzj/img201606/heroimg/116/116-mobileskin-1.jpg'),width=200)
        with col2:
            st.write('Assassin: Assassins are heroes with low survivability but explosive damage output. In the battle they usually move very agilely and can find the right time to kill the enemy’s core.')
        col1, col2= st.beta_columns([1,1.8])
        with col1:
            st.image(return_image('https://subao-web-admin.oss-cn-shanghai.aliyuncs.com/xunyou/detail/201908071020522890.jpg'), width=200)
        with col2:
            st.write('Archer: Archer heroes are heroes with high ranged damage output and control skills. In the battle, they can take advantage of "long hand" to stand in the rear row to attack and control enemies.')
        col1, col2= st.beta_columns([1,1.8])
        with col1:
            st.image(return_image('https://5b0988e595225.cdn.sohucs.com/images/20190310/c626efc9474146e99c440b87559e610c.png'), width=200)
        with col2:
            st.write('Support: support heroes are heroes with mediocre survivability and attacking abilities, and they rely on powerful skill effects and provide buff and other benefits to teammates or control enemies.')
    if i=='Radar Chart by Hero Position':
        position_show = st.sidebar.multiselect('Choose Hero Position',list(radar['position'].unique()))
        mark=1
        for i in position_show:
            k=return_index(i,data_position)
            c1.add(series_name=i,data=data_position[k])
        if len(position_show)>=1:
            st_pyecharts(c1,height=500) 
            
    if i=='Radar Chart by Hero':
        if mark!=1:
            position_show = st.sidebar.multiselect('Choose Hero Position',list(radar['position'].unique()))
        #Radar_hero
        selected_hero=[]
        for i in position_show:
            selected_hero=selected_hero+list(radar.loc[radar['position']==i]['name'])
        show_hero=st.sidebar.multiselect('Choose Hero',selected_hero)
        radar_data=[]
        for i in position_show:
            if i=='Warrior':
                radar_data=radar_data+data_Warrior
            if i=='Mage':
                radar_data=radar_data+data_mage
            if i=='Tank':
                radar_data=radar_data+data_Tank
            if i=='Archer':
                radar_data=radar_data+data_Archer
            if i=='Assassin':
                radar_data=radar_data+data_Assassin
            if i=='Support':
                radar_data=radar_data+data_Support
        for i in show_hero:
            k=return_index(i,radar_data)
            c.add(series_name=i,data=radar_data[k])

        if len(show_hero)>=1:
            st_pyecharts(c,height=500)       
    
#2.2                                  
## many pics in this part

fig_list = st.sidebar.multiselect('2.2 Choose to see Topics: ',
                                  ['Hero Speed','Hero-Health points','Hero-Health regeneration',
                                   'Hero-Physical defense','Hero-Physical Attack',])

# Moving fastest hero
def effectscatter_base() -> EffectScatter:
    c = (
        EffectScatter()
        .add_xaxis(list(hero['Hero']))
        .add_yaxis("", list(hero['Speed']))
        .set_global_opts(title_opts=opts.TitleOpts(title="Hero Speed"))
    )
    return c
fig_3=effectscatter_base()

# Highest health points

def bar_base1() -> Bar:
    c = (
        Bar({"width": "1024px", "height": "768px"})
        .add_xaxis(list(hero['Hero']))
        .add_yaxis("Health points",list(hero['Health points']),color='#61a0a8')
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Hero-Health points"),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")]
        )
        .set_series_opts(
        label_opts=opts.LabelOpts(is_show=False),
        markpoint_opts=opts.MarkPointOpts(
            data=[
                opts.MarkPointItem(type_="max", name="Maximun"),
                opts.MarkPointItem(type_="min", name="Minimum"),
                opts.MarkPointItem(type_="average", name="Average"),
            ]),
        markline_opts=opts.MarkLineOpts(
            data=[
                opts.MarkLineItem(type_="min", name="Maximun"),
                opts.MarkLineItem(type_="max", name="Minimum"),
                opts.MarkLineItem(type_="average", name="Average"),
            ]
        ),
            
            )
    )
    return c
fig_4=bar_base1()

# Health regeneration
def bar_base2() -> Bar:
    c = (
        Bar({"width": "1024px", "height": "768px"})
        .add_xaxis(list(hero['Hero']))
        .add_yaxis("Health regeneration",list(hero['Health regeneration']),color='#ca8622')
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Hero-Health regeneration"),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")]
        )
        .set_series_opts(
        label_opts=opts.LabelOpts(is_show=False),
        markpoint_opts=opts.MarkPointOpts(
            data=[
                opts.MarkPointItem(type_="max", name="Maximun"),
                opts.MarkPointItem(type_="min", name="Minimum"),
                opts.MarkPointItem(type_="average", name="Average"),
            ]),
        markline_opts=opts.MarkLineOpts(
            data=[
                opts.MarkLineItem(type_="min", name="Maximun"),
                opts.MarkLineItem(type_="max", name="Minimum"),
                opts.MarkLineItem(type_="average", name="Average"),
            ]
        ),
            
            )
        
    )
    return c
fig_5=bar_base2()

# Physical Defense
def bar_base() -> Bar:
    c = (
        Bar({"width": "1024px", "height": "768px"})
        .add_xaxis(list(hero['Hero']))
        .add_yaxis("Physical defense",list(hero['Physical defense']),color='#444693')
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Hero-Physical defense"),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")]
        )
        .set_series_opts(
        label_opts=opts.LabelOpts(is_show=False),
        markpoint_opts=opts.MarkPointOpts(
            data=[
                opts.MarkPointItem(type_="max", name="Maximun"),
                opts.MarkPointItem(type_="min", name="Minimum"),
                opts.MarkPointItem(type_="average", name="Average"),
            ]),
        markline_opts=opts.MarkLineOpts(
            data=[
                opts.MarkLineItem(type_="min", name="Maximun"),
                opts.MarkLineItem(type_="max", name="Minimum"),
                opts.MarkLineItem(type_="average", name="Average"),
            ]
        ),
            
            )
    )
    return c
fig_6=bar_base()

#Physical attack
#@st.cache()
def bar_base() -> Bar:
    c = (
        Bar({"width": "1024px", "height": "768px"})
        .add_xaxis(list(hero['Hero']))
        .add_yaxis("Physical attack",list(hero['Physical attack']),color='#6d8346')
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Hero-Physical Attack"),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")]
        )
        .set_series_opts(
        label_opts=opts.LabelOpts(is_show=False),
        markpoint_opts=opts.MarkPointOpts(
            data=[
                opts.MarkPointItem(type_="max", name="Maximun"),
                opts.MarkPointItem(type_="min", name="Minimum"),
                opts.MarkPointItem(type_="average", name="Average"),
            ]),
        markline_opts=opts.MarkLineOpts(
            data=[
                opts.MarkLineItem(type_="min", name="Maximun"),
                opts.MarkLineItem(type_="max", name="Minimum"),
                opts.MarkLineItem(type_="average", name="Average"),
            ]
        ),
            
            )
    )
    return c
fig_7=bar_base()
        
        
for i in fig_list:
    if i=='Hero Speed':
        st_pyecharts(fig_3,height=400)
        col1, col2, col3= st.beta_columns([1,1,2])
        with col1:
            st.image(return_image('https://game.gtimg.cn/images/yxzj/img201606/heroimg/198/198-mobileskin-1.jpg'),width=150)
        with col2:
            st.image(return_image('https://subao-web-admin.oss-cn-shanghai.aliyuncs.com/xunyou/detail/201911181035074327.jpg'), width=150)
        with col3:
            st.write('We find it interesting that without equipments, heroes who move faster are not archers or mages, a group which is considered to be the agilest, but Mengqi and Dun Shan. These  two cumbersome heroes stand out.')
    if i=='Hero-Health points':
        st_pyecharts(fig_4,height=400)
        col1, col2= st.beta_columns([1,2])
        with col1:
            st.image(return_image('https://game.gtimg.cn/images/yxzj/img201606/heroimg/166/166-mobileskin-1.jpg'),width=200)
        with col2:
            st.write('Arthur has the highest health points among all the heroes. This hero presented at the first introduction of the game. After 5 years development, Arthur is still very popular. This strength allows Arthur to help his teammates resist damage in the early game stage and helps himself to grow better.')
    if i=='Hero-Health regeneration':
        st_pyecharts(fig_5,height=400)
        col1, col2= st.beta_columns([1,2])
        with col1:
            st.image(return_image('https://game.gtimg.cn/images/yxzj/img201606/heroimg/525/525-mobileskin-1.jpg'),width=200)
        with col2:
            st.write('Top 1 is Master Luban. He is a helpful support in the game. He can provide strong protection to teammates and help them get into the right position.')
        col3, col4= st.beta_columns([1,2])
        with col3:
            st.image(return_image('https://game.gtimg.cn/images/yxzj/coming/v2/adjust/image/20191015/d0dbfa902a7e16464eddd3e5e048086f.jpg'),width=200)
        with col4:
            st.write('The Lowest is Yuji, she is an ADC in the team, so health regeneration is not her strength.')
    if i=='Hero-Physical defense':
        st_pyecharts(fig_6,height=400)
        col1, col2= st.beta_columns([1,2])
        with col1:
            st.image(return_image('https://game.gtimg.cn/images/yxzj/img201606/heroimg/113/113-mobileskin-1.jpg'),width=200)
        with col2:
            st.write('Top 1 is Zhuang Zhou. He is a very good support and rise ‘Kun’, which is considered to be  a Mythical Animal in Chinese fairy tale. And thus,  his viability is very strong.')
        col3, col4= st.beta_columns([1,2])
        with col3:
            st.image(return_image('https://images.saiyu.com/img/2019/09/17/6370431554868609657609782.jpg'),width=200)
        with col4:
            st.write('The lowest are Dun Shan, Mengqi and Shangguan Waner. Since Menqi and Dun Shan have the highest speeds, they can take this advantage to avoid attack.')
            st.write('As for Shangguan Waner, although she is week on defense, her agility can offset the negative effects.')
    if i=='Hero-Physical Attack':
        st_pyecharts(fig_7,height=400)
        col1, col2= st.beta_columns([1,2])
        with col1:
            st.image(return_image('https://game.gtimg.cn/images/yxzj/img201606/heroimg/508/508-mobileskin-1.jpg'),width=200)
        with col2:
            st.write('Galo has the highest physical attack among all the heroes. Surely, the highest physical attack makes her a very strong archer. She is also enabled to have the largest range of attack. There is no surprising that the ban rate of Galo is high.')
        col3, col4= st.beta_columns([1,2])
        with col3:
            st.image(return_image('https://game.gtimg.cn/images/yxzj/img201606/heroimg/522/522-mobileskin-1.jpg'),width=200)
        with col4:
            st.write('At the same time, Yào’s physical attack is the lowest. He is a very special warrior, mastering both magical damage and physical damage.')



#Part 3
st.sidebar.write('### Part 3: Analysis of single and double heros winning rates in King Pro League Fall 2020')        
st.markdown('- **Part 3: Analysis of single and double heros winning rates in King Pro League Fall 2020**')

df = return_data('combat.csv')

winning = st.sidebar.multiselect('Table of Contents: ',[
    "3.1 Single Hero's Winning Rate",'3.2 Ranking of Single Winning Rate',"3.3 Two Hero's Winning Rate",
    "3.4 Heat map of Two Hero's Winning Rate","3.5 Ranking of Two Hero's Winning Rate","3.6 Recommendations on 5v5 hero combination for KPL"])

#1.1
@st.cache(suppress_st_warning=True)
def one_hero_win(name):
    df_1 = df[(df['hero1'] == name)|(df['hero2'] == name)|(df['hero3'] == name)|(df['hero4'] == name)|(df['hero5'] == name)]
    win_rate = df_1.mean()['win'] #get win rate
    return win_rate
#1.2
a=return_data('hero_winning_rate.csv')
#2.1
@st.cache(suppress_st_warning=True)
def two_hero_win(name1,name2):
    df_2 = df[((df['hero1'] == name1)|(df['hero2'] == name1)|(df['hero3'] == name1)|(df['hero4'] == name1)|(df['hero5'] == name1))&((df['hero1'] == name2)|(df['hero2'] == name2)|(df['hero3'] == name2)|(df['hero4'] == name2)|(df['hero5'] == name2))]
    win_rate = df_2.mean()['win']
    return win_rate
#2.2
matrix=return_data('matrix.csv')
def return_heatmap(color):
    cm = sns.light_palette(color, as_cmap=True)
    return cm
#2.3
b=return_data('winning_rate_list.csv')

#3.1
c=return_data('team_structure.csv')

for i in winning:
    if i=="3.1 Single Hero's Winning Rate":
        st.write('''**_1.1 Single Hero's Winning Rate_**''')
        hero_1=st.selectbox('Select A Hero',list(radar['name'].unique()))
        st.write(format(one_hero_win(hero_1),'.3f'))
    if i=='3.2 Ranking of Single Winning Rate':
        st.write('''**_1.2 Ranking of Single Winning Rate_**''')
        st.write(a.iloc[:,1:])
    if i=="3.3 Two Hero's Winning Rate":
        st.write("**_2.1 Two Hero's Winning Rate_**")
        hero_2=st.multiselect('Select Two Heros',list(radar['name'].unique()))
        if len(hero_2)!=2:
            st.write('Please select **2** heros.')
        elif format(two_hero_win(hero_2[0],hero_2[1]),'.3f')=='nan':
            st.write('No combat data for these two heros')
        else:
            st.write(format(two_hero_win(hero_2[0],hero_2[1]),'.3f'))
    if i=="3.4 Heat map of Two Hero's Winning Rate":
        st.write("**_2.2 Heat map of Two Hero's Winning Rate_**")
        st.write(matrix.style.background_gradient(cmap=return_heatmap("green")))
    if i=="3.5 Ranking of Two Hero's Winning Rate":
        st.write("**_2.3 Ranking of Two Hero's Winning Rate_**")
        st.write(b.iloc[:,1:])
    if i=="3.6 Recommendations on 5v5 hero combination for KPL":
        st.write("**_3.6 Recommendations on 5v5 hero combination for KPL_**")
        st.write(c)

    
#Part 4
st.sidebar.write('### Part 4: Predict win/lose for a KPL team based on decision tree') 
st.sidebar.write('#### Please input how many heroes in each position as below')

st.markdown('- **Part 4: Predict win/lose for a KPL team based on decision tree**')
#st.markdown('_**Goal**: Use 5 heroes’ position and their related ‘Money’, ‘Output’, ‘Intake’ to predict win / lose_')
st.markdown('#### Step1: Get decision tree:')

step1 = st.sidebar.selectbox('Assasin',[0,1,2])
step2 = st.sidebar.selectbox('Archer',[0,1,2])
step3 = st.sidebar.selectbox('Support',[0,1,2])
step4 = st.sidebar.selectbox('Tank',[0,1,2])
step5 = st.sidebar.selectbox('Warrior',[0,1,2])
step6 = st.sidebar.selectbox('Mage',[0,1,2])
position_list = str([step1, step2, step3, step4, step5, step6])

dft = pd.read_csv('train.csv')

if (position_list in list(dft['position_list'])):

    dft_tree=dft.loc[dft['position_list']==position_list]
    x = dft_tree[['ass-mon','ass-out','ass-int','arc-mon','arc-out','arc-int','sup-mon','sup-out','sup-int','tan-mon','tan-out','tan-int','war-mon','war-out','war-int','mag-mon','mag-out','mag-int']]
    y = dft_tree['win']

    tree = DecisionTreeClassifier(max_depth=3, max_leaf_nodes=5)
    tree.fit(x,y)
    
    
    
    plt.figure(figsize=(100,60))                     # Adjust figure ratio for better display
    plot_tree(tree,                                 # Tree classifier
          filled=True,                          # Fill nodes with different colors
          rounded=True,                         # Rounded conner of nodes
          feature_names=x.columns,              # Feature names
          class_names=y.unique().astype(str),   # Class names
          fontsize=60)                          # Font size
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()
    
    st.markdown('#### Step2: Get the prediction result:')
    
    ass1=''
    ass2=''
    ass3=''
    arc1=''
    arc2=''
    arc3=''
    sup1=''
    sup2=''
    sup3=''
    tan1=''
    tan2=''
    tan3=''
    war1=''
    war2=''
    war3=''
    mag1=''
    mag2=''
    mag3=''

    st.write('Please input the performance of each position following the structure of [money output intake]')
    
    
    col1, col2, col3, col4, col5, col6= st.beta_columns([1,1,1,1,1,1])
    with col1:
        ass1 = st.text_input("assasin-money", ass1)
    with col2:
        arc1 = st.text_input("archer-money", arc1)
    with col3:
        sup1 = st.text_input("support-money", sup1)
    with col4:
        tan1 = st.text_input("tank-money", tan1)
    with col5:
        war1 = st.text_input("warrior-money", war1)
    with col6:
        mag1 = st.text_input("mage-money", mag1)
    
    col1, col2, col3, col4, col5, col6= st.beta_columns([1,1,1,1,1,1])
    with col1:
        ass2 = st.text_input("assasin-output", ass2)
    with col2:
        arc2 = st.text_input("archer-output", arc2)
    with col3:
        sup2 = st.text_input("support-output", sup2)
    with col4:
        tan2 = st.text_input("tank-output", tan2)
    with col5:
        war2 = st.text_input("warrior-output", war2)
    with col6:
        mag2 = st.text_input("mage-output", mag2)
    
    col1, col2, col3, col4, col5, col6= st.beta_columns([1,1,1,1,1,1])
    with col1:
        ass3 = st.text_input("assasin-intake", ass3)
    with col2:
        arc3 = st.text_input("archer-intake", arc3)
    with col3:
        sup3 = st.text_input("support-intake", sup3)
    with col4:
        tan3 = st.text_input("tank-intake", tan3)
    with col5:
        war3 = st.text_input("warrior-intake", war3)
    with col6:
        mag3 = st.text_input("mage-intake", mag3)
    

    performance=[]

    performance.extend(ass1.split())
    performance.extend(ass2.split())
    performance.extend(ass3.split())
    
    performance.extend(arc1.split())
    performance.extend(arc2.split())
    performance.extend(arc3.split())
    
    performance.extend(sup1.split())
    performance.extend(sup2.split())
    performance.extend(sup3.split())
    
    performance.extend(tan1.split())
    performance.extend(tan2.split())
    performance.extend(tan3.split())
    
    performance.extend(war1.split())
    performance.extend(war2.split())
    performance.extend(war3.split())
    
    performance.extend(mag1.split())
    performance.extend(mag2.split())
    performance.extend(mag3.split())
    
    
    st.write(' Perdiction result:')
    
    if len(performance)==18:
        if tree.predict(np.array([performance]))[0]==0:
            st.write('This game probably will lose')
        else:
            st.write('This game probably will win')
    else:
        st.write('Error, please input the performance of each position')
    
else:
    st.write('')
    st.write('Error, please change another team structure.')
    st.write('Posible reasons:     1. sum of each position != 5.     2.we do not have data under this structure')
