#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys

args = sys.argv
# 0 为脚本本身 1 为第一个参数
if (len(args) == 1):
    print('参数错误')
    exit

#switch (args[1]):
# wc py竟然没switch
if(args[1] == 'detail'):
    import controller.runDetail
elif(args[1] == 'detailQueue'):
    import controller.detailQueue
elif(args[1] == 'zjw'):
    import controller.zjwBeijing
elif(args[1] == '-h'):
    # import controller.zjwBeijing
    if (len(args) >=3 and args[2] == 'city'):
        print(' bj 北京 sh 上海 sz 深圳 aq 安庆 hf 合肥 mas 马鞍山 wuhu 芜湖 bj 北京 cq 重庆 fz 福州 quanzhou 泉州 xm 厦门 zhangzhou 漳州 dg 东莞 fs 佛山 gz 广州 hui 惠州 jiangmen 江门 qy 清远 sz 深圳 zh 珠海 zhanjiang 湛江 zs 中山 gy 贵阳 bh 北海 fcg 防城港 gl 桂林 liuzhou 柳州 nn 南宁 lz 兰州 ez 鄂州 huangshi 黄石 wh 武汉 xy 襄阳 yichang 宜昌 cs 长沙 changde 常德 yy 岳阳 zhuzhou 株洲 bd 保定 lf 廊坊 sjz 石家庄 ts 唐山 zjk 张家口 hk 海口 san 三亚 kf 开封 luoyang 洛阳 xinxiang 新乡 xc 许昌 zz 郑州 zk 周口 hrb 哈尔滨 changzhou 常州 haimen 海门 ha 淮安 jy 江阴 ks 昆山 nj 南京 nt 南通 su 苏州 wx 无锡 xz 徐州 yc 盐城 zj 镇江 cc 长春 jl 吉林 ganzhou 赣州 jiujiang 九江 jian 吉安 nc 南昌 sr 上饶 dl 大连 dd 丹东 sy 沈阳 baotou 包头 hhht 呼和浩特 yinchuan 银川 sh 上海 cd 成都 dy 德阳 dazhou 达州 liangshan 凉山 mianyang 绵阳 nanchong 南充 heze 菏泽 jn 济南 jining 济宁 linyi 临沂 qd 青岛 ta 泰安 wf 潍坊 weihai 威海 yt 烟台 zb 淄博 baoji 宝鸡 hanzhong 汉中 xa 西安 xianyang 咸阳 jz 晋中 ty 太原 tj 天津 dali 大理 km 昆明 hz 杭州 huzhou 湖州 jx 嘉兴 jh 金华 nb 宁波 sx 绍兴 taizhou 台州 wz 温州 yw 义乌')
    else:
        print('这里是帮助页面 参数city显示所有城市列表')
# 初始化列表任务
elif(args[1] == 'initListJob'):
    import controller.initListJob as initListJobController
    initListJobController.run(args[2])
# 运行列表任务
elif(args[1] == 'runListJob'):
    import controller.runListJob as runListJobController
    runListJobController.run()
else:
    print('参数错误 请运行 list detail')

