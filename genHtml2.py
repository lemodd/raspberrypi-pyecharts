#!/usr/bin/python3

from pyecharts import Line,Page
import platform
import sqlite3
import util




def gen():
    cn = sqlite3.connect('weather.db')
    cu = cn.cursor()

    textsize = 32
    time_st = []
    room_t = []
    out_t = []
    room_h = []
    cpu_t = []
    cpu_load = []
    bat_volt = []

    sql = "SELECT *  FROM record order by id desc limit 100 "
    rec = cu.execute(sql)
    # print(type(list(rec)))
    lst = list(rec)
    lst.reverse()

    for line in lst:
        tm_st = line[1][5:].replace("/","-") +" "+line[2]
        time_st.append(tm_st)
        room_t.append(line[3])
        out_t.append(line[4])
        room_h.append(line[5])
        cpu_t.append(line[6])
        cpu_load.append(line[7])
        bat_volt.append(line[8])

    page = Page(page_title="My RPi Center")

    #数据总个数
    amount = len(time_st)
    #需要显示的个数(24小时)
    display = 72
    #display range
    dis_range = int((1-display/amount)*100)
#    print(amount)

    line_room_t = Line("气温  %s/%s℃"%(str(room_t[-1]),str(out_t[-1])),
			title_pos='center',
			title_text_size=textsize,
			title_top='5%')
    line_room_t.add("室温", time_st, room_t,
             xaxis_name='时间',
             yaxis_name='温度(℃)',
             yaxis_name_pos='end',
             xaxis_name_pos='end',
             xaxis_label_textsize=textsize,
             yaxis_label_textsize=textsize,
	            label_text_size=textsize,
                    label_emphasis_textsize=textsize,
                    tooltip_font_size=textsize,
                    mark_point_textsize=10,
             is_label_show=True,
             line_width = 3,
             line_curve = 0.5,
             is_datazoom_show=True,
             datazoom_type='slider',
                    datazoom_range=[80,100],
             is_more_utils=True,
             xaxis_force_interval=50,
             yaxis_min=min(room_t)-5,
             yaxis_max=max(room_t)+5,
             tooltip_tragger='axis',
             mark_point=['min','max'],
             mark_line=['average'])



    line_room_t.add("外温", time_st, out_t,
             xaxis_name='时间',
             yaxis_name='温度(℃)',
             yaxis_name_pos='end',
             xaxis_name_pos='end',
             xaxis_label_textsize=textsize,
             yaxis_label_textsize=textsize,
	            label_text_size=textsize,
                    label_emphasis_textsize=textsize,
                    tooltip_font_size=textsize,
                    mark_point_textsize=10,
             is_label_show=True,
             line_width = 3,
             line_curve = 0.5,
             is_datazoom_show=True,
             datazoom_type='slider',
                    datazoom_range=[dis_range,100],
             is_more_utils=True,
             xaxis_force_interval=50,
             yaxis_min=min(min(room_t),min(out_t))-3,
             yaxis_max=max(max(room_t),max(out_t))+7,
             tooltip_tragger='axis',
             mark_point=['min','max'],
             mark_line=['average'])

    page.add(line_room_t)


    line_room_h = Line("湿度  "+str(room_h[-1])+'%',
                       title_pos='center',
                       title_text_size=textsize,
                       title_top='5%')
    line_room_h.add("", time_st, room_h,
             xaxis_name='时间',
             yaxis_name='湿度(%)',
             yaxis_name_pos='end',
             xaxis_name_pos='end',
             xaxis_label_textsize=textsize,
             yaxis_label_textsize=textsize,
                    label_text_size=textsize,
                    label_emphasis_textsize=textsize,
                    tooltip_font_size=textsize,
                    mark_point_textsize=10,
             is_label_show=True,
             line_width = 3,
             line_curve = 0.5,
             is_datazoom_show=True,
             datazoom_type='slider',
                    datazoom_range=[dis_range,100],
             is_more_utils=True,
             xaxis_force_interval=50,
             yaxis_min=min(room_h)-5,
             yaxis_max=max(room_h)+5,
             tooltip_tragger='axis',
             mark_point=['min','max'],
             mark_line=['average'])
    page.add(line_room_h)

   
    line_cpu_t = Line("CPU温度 %s℃"%(str(cpu_t[-1])),title_text_size=textsize, title_pos='center', title_top='5%')
    line_cpu_t.add("", time_st, cpu_t,
                  xaxis_name='时间',
                  yaxis_name='温度(℃)',
                  yaxis_name_pos='end',
                  xaxis_name_pos='end',
                  xaxis_label_textsize=14,
                  yaxis_label_textsize=14,
                  is_label_show=True,
                  line_width=3,
                  line_curve=0.5,
                  is_datazoom_show=True,
                  datazoom_type='slider',
                   datazoom_range=[dis_range,100],
                  is_more_utils=True,
                  xaxis_force_interval=50,
                  yaxis_min=min(cpu_t) - 3,
                  yaxis_max=max(cpu_t) + 3,
                  tooltip_tragger='axis',
                  mark_point=['min', 'max'],
                  mark_line=['average'])

    page.add(line_cpu_t)

    line_cpu_load = Line("CPU负载 %s%%"%(str(cpu_load[-1])),title_text_size=textsize, title_pos='center', title_top='5%')
    line_cpu_load.add("", time_st, cpu_load,
                   xaxis_name='时间',
                   yaxis_name='负载(%)',
                   yaxis_name_pos='end',
                   xaxis_name_pos='end',
                   xaxis_label_textsize=14,
                   yaxis_label_textsize=14,
                   is_label_show=True,
                   line_width=3,
                   line_curve=0.5,
                   is_datazoom_show=True,
                   datazoom_type='slider',
                      datazoom_range=[dis_range,100],
                   is_more_utils=True,
                   xaxis_force_interval=50,
                   yaxis_min=0,
                   yaxis_max=max(cpu_load) + 3,
                   tooltip_tragger='axis',
                   mark_point=['min', 'max'],
                   mark_line=['average'])

    page.add(line_cpu_load)

    line_bat_volt = Line("电池电压 %sV"%(str(bat_volt[-1])), 
			title_text_size=textsize,
			title_pos='center', 
			title_top='5%')
    line_bat_volt.add("", time_st, bat_volt,
                   xaxis_name='时间',
                   yaxis_name='电压(V)',
                   yaxis_name_pos='end',
                   xaxis_name_pos='end',
                   xaxis_label_textsize=14,
                   yaxis_label_textsize=14,
                   is_label_show=True,
                   line_width=3,
                   line_curve=0.5,
                   is_datazoom_show=True,
                   datazoom_type='slider',
                      datazoom_range=[dis_range,100],
                   is_more_utils=True,
                   xaxis_force_interval=50,
                   yaxis_min=3.3,
                   yaxis_max=4.3,
                   tooltip_tragger='axis',
                   mark_point=['min', 'max'],
                   mark_line=['average'])

    page.add(line_bat_volt)

    if platform.system()=="Linux":
        page.render('/home/pi/www/index.html')
    else:
        page.render('index.html')

    with open('/home/pi/www/wea.html','w') as f:
        f.write(str(room_t[-1])+'\n')
        f.write(str(room_h[-1])+'\n')
        f.write(str(out_t[-1]))


if __name__ == "__main__":
    gen()


