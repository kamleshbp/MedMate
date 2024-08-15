from tkinter import *

def draw_point(canvas,x,y,colour,size=5,text=''):
    x1, y1 = (220+x*20 - size), (240+y*20 - size)
    x2, y2 = (220+x*20 + size), (240+y*20 + size)
    canvas.create_oval(x1, y1, x2, y2, fill=colour)
    canvas.create_text(220+x*20,240+y*20,font=("Arial",20),text=text)

def draw_map(location_arr,canvas,image):
    canvas.place(relx=0.6,rely=0.2)
    canvas.create_image(10, 0, anchor=NW,image=image)
    for i in range(10,450):
        canvas.create_line(i,0,i,500,width=2,fill='white')
    '''
    for i in range(0,450,20):
        canvas.create_line(i,0,i,500,width=2)
    for i in range(0,500,20):
        canvas.create_line(0,i,450,i,width=2)
    '''
    if location_arr:
        all_locations=[]
        for location in location_arr.values():
            x=int(location['xCor'])
            y=int(location['yCor'])
            all_locations.append([x,y])
            if location['physicalName']!='Unknown':
                canvas.create_text(220+x*20+10,240+y*20+10,font=("Arial",5),text=location['physicalName'])
                canvas.update()
                draw_point(canvas,x,y,'red')
            for loc in all_locations:
                if [loc[0]+1,loc[1]] in all_locations:
                    canvas.create_line(220+loc[0]*20,240+loc[1]*20,220+(loc[0]+1)*20,240+loc[1]*20,fill='blue')
                if [loc[0],loc[1]+1] in all_locations:
                    canvas.create_line(220+loc[0]*20,240+loc[1]*20,220+loc[0]*20,240+(loc[1]+1)*20,fill='blue')
