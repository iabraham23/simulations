#Web VPython 3.2
from vpython import *

#Create canvas. Set userspin=False, so image won't rotate.
scene=canvas(width =1024, height=480, center=vector(0,30,0), background=color.white, userspin=False, userzoom=False)
width_height=scene.width/scene.height
w = scene.width
h = scene.height
w_scale = w/1024
h_scale = h/480
pixel_D = 1.3

scene.lights=[]
distant_light(direction=vector( 0.22, 0.44, 0.88), color=color.white)
distant_light(direction=vector(-0.88, -0.22, -0.44), color=color.white)
#Set Camera Position
view_box = box(width=w/2, height=h/2, opacity=0)

#Variables
animation_speed = 100
text_size = 15*h_scale

isRunning = False
isStationary = True
isStarted = False
tilt_angle = pi/12

graph_h  = 150
axis_h = 175
mag_h = 150

B_mag = 1
B_dir = norm(vector(-1,-0.25882,0.96593)) #hat and norm give unit vectors
B = B_mag*B_dir

M_mag = 1
M_dir = norm(vector(0,0.96593,0.25882)) #starting M direction
#print('M_dir=', M_dir)
M = M_mag*M_dir

# energy = dot(-M,B)

drag=0.98
omega=0
torque = cross(M,B)
#print(torque)

#Assume resonance freq=100 MHz, (w=2*pi*10^8) scale down by a factor of ten million
w0=60
#Assume B1=10 microTesla, gamma = 2.68e8 >> w1=gammma*B1=2.68e3 (see HW 13.12 in text), scale down by factor of 10^3
w1=3

desync_time = 0.25

t=0
dt=0.005

MS_PER_SIM_UNIT = 2650.0
SEQUENCE_PRESETS = {
    "T1": {"TR_ms": 400, "TE_ms": 5},
    "T2": {"TR_ms": 4000, "TE_ms": 150},
}
sequence_mode = "T1"

T1 = 1 #This means 1 = 2650 ms
T2 = 0.106
mindex=0

TR = SEQUENCE_PRESETS[sequence_mode]["TR_ms"] / MS_PER_SIM_UNIT
TE = SEQUENCE_PRESETS[sequence_mode]["TE_ms"] / MS_PER_SIM_UNIT
t_final_1 = pi/(2*w1)
#t_final_2 = t_final_1 + 6*pi/(w0)
t_final_3 = t_final_1 + TR
#t_final_3 = t_final_2 + (T1*1.75)
#t_final_3 = t_final_2  #Same for all tissues t_final_3=0.884 t_final_3-t_final_1 (recovery time) = 0.36
initial_M_mag = 1
M_mag = initial_M_mag
M = M_mag*M_dir

#Objects
center = sphere(pos=vec(0,0,0), radius=6, color=norm(vec(141,101,197)), opacity=1)

Mvec = arrow(pos=vec(0,0,0), axis=pixel_D*mag_h*M, shaftwidth=8*w_scale*(mag_h/100), headwidth=15*w_scale*(mag_h/100), headlength=30*w_scale*(mag_h/100), color=vec(0.7,0,0.9), round=True, opacity=1)
Mvec_label=label(pos=Mvec.pos+1.1*Mvec.axis+vector(-100,0,0), text='Longitudinal\n Magnetization', color=Mvec.color, box=False, height=1.1*text_size, opacity=0)
Bvec = arrow(pos=-vec(-1,0,0), axis=pixel_D*mag_h*B, shaftwidth=7.5*w_scale*(mag_h/100), headwidth=15*w_scale*(mag_h/100), headlength=30*w_scale*(mag_h/100), color=color.cyan, round=True, visible=False)
torque_vec = arrow(pos=Mvec.pos+Mvec.axis, axis=pixel_D*mag_h/1.5*norm(cross(M,B)), shaftwidth=5*w_scale*(mag_h/100), headwidth=10*w_scale*(mag_h/100), headlength=20*w_scale*(mag_h/100), color=norm(vec(0,210,106)), round=True, visible=False)
Bvec_label = label(pos=Bvec.pos+0.5*Bvec.axis+vector(0,-3.5*text_size,0), text='RF Pulse On', color=color.cyan, box=False, height=1.1*text_size, opacity=0, visible=False)
torque_label = label(pos=torque_vec.pos + torque_vec.axis + vector(2*text_size,0,0), text='τ<sub>RF</sub>', height=1.3*text_size, box=False, color=color.green, opacity=0, visible=False)
M_vertical_vec = arrow(pos=vec(0,0,0), axis=pixel_D*mag_h*M, shaftwidth=7.5*w_scale*(mag_h/100), headwidth=15*w_scale*(mag_h/100), headlength=30*w_scale*(mag_h/100), color=vec(0.7,0,0), round=True, opacity=0.8, visible=True)
M_vert_dir=hat(M_vertical_vec.axis) #Use to start regrowth after RF pulse, same as M_dir above
M_horizontal_vec = arrow(pos=Mvec.pos, axis=pixel_D*mag_h*dot(M, norm(vector(1,-0.25882,0.96593)))*norm(vector(1,-0.25882,0.96593))*.99, shaftwidth=5*w_scale*(mag_h/100)*.9, headwidth=10*w_scale*(mag_h/100)*.9, headlength=20*w_scale*(mag_h/100)*.9, color=vec(0,0,0.9), round=True, opacity=0.8)
#print("M_hor_vec_ax=",M_horizontal_vec.axis) 
starting_shaftw = Mvec.shaftwidth
starting_headw = Mvec.headwidth
starting_headl = Mvec.headlength

M_tip = sphere(pos=Mvec.pos+Mvec.axis, color=Mvec.color, make_trail=True, visible=True)


main_x_axis = arrow(pos=vector(0,0,0), axis=1.15*pixel_D*h_scale*axis_h*norm(vector(-1,-0.25882,0.96593)), shaftwidth=2.5*w_scale*(axis_h/100), headwidth=7*w_scale*(axis_h/100), headlength=15*w_scale*(axis_h/100), color=color.black, round=True)
main_y_axis = arrow(pos=vector(0,0,0), axis=1.15*pixel_D*h_scale*axis_h*norm(vector(1,-0.25882,0.96593)), shaftwidth=2.5*w_scale*(axis_h/100), headwidth=7*w_scale*(axis_h/100), headlength=15*w_scale*(axis_h/100), color=color.black, round=True)
main_z_axis = arrow(pos=vector(0,0,0), axis=1.15*pixel_D*h_scale*axis_h*norm(vector(0,0.96593,0.25882)), shaftwidth=3*w_scale*(axis_h/100), headwidth=7*w_scale*(axis_h/100), headlength=15*w_scale*(axis_h/100), color=color.black, round=True)

main_x_label = label(pos=main_x_axis.pos+main_x_axis.axis+vector(3*text_size,0,1.5*text_size), text='x', height=1.5*text_size, box=False, color=color.black, opacity=0)
main_y_label = label(pos=main_y_axis.pos+main_y_axis.axis+vector(-3*text_size,0,text_size), text='y', height=1.5*text_size, box=False, color=color.black, opacity=0)
main_z_label = label(pos=main_z_axis.pos+main_z_axis.axis+vector(1.5*text_size,-2*text_size,0), text='z', height=1.5*text_size, box=False, color=color.black, opacity=0)

main_xgraph_axis= arrow(pos=vector(-750,-2,0), axis=vector(300,0,0), shaftwidth=2.5*w_scale*(axis_h/100), headwidth=7*w_scale*(axis_h/100), headlength=15*w_scale*(axis_h/100), color=vec(0.000, 0.360, 0.390), round=True, opacity=1)
main_ygraph_axis = arrow(pos=vector(-750,-2,0), axis=vector(0,200,0), shaftwidth=2.5*w_scale*(axis_h/100), headwidth=7*w_scale*(axis_h/100), headlength=15*w_scale*(axis_h/100), color=vec(0.000, 0.360, 0.390), round=True, opacity=1)


coil_box = box(pos=main_y_label.pos+vec(w_scale*50+2*text_size,-1.20*text_size,0.5), length=w_scale*80, height=h_scale*80, width=0.5, color=color.white, texture='https://i.imgur.com/2gDRgGG.jpeg')
coil_box.rotate(angle=3.14159/8, axis=vector(0,0,-1))

Mz_x_axis_arrow = arrow(pos=vec(-w/1.8,h/4-graph_h/2,0), axis = vec(graph_h*w_scale,0,0), shaftwidth=2*w_scale*(graph_h/100), headwidth=5*w_scale*(graph_h/100), headlength=10*w_scale*(graph_h/100), color=color.black, round=True)
Mz_y_axis_arrow = arrow(pos=vec(-w/1.8,h/4-graph_h/2,0), axis = vec(0,graph_h*h_scale,0), shaftwidth=2*w_scale*(graph_h/100), headwidth=5*w_scale*(graph_h/100), headlength=10*w_scale*(graph_h/100), color=color.black, round=True)
Mz_x_label = label(pos=Mz_x_axis_arrow.pos+vec(graph_h/2,-text_size,0), text='t', height=text_size, box=False, color=color.black, opacity=0, visible=False)
Mz_y_label = label(pos=Mz_x_axis_arrow.pos+vec(-2*text_size,graph_h,0), text='M<sub>z<sub>', height=text_size, box=False, color=color.black, visible=False, opacity=0)
Mz_label = label(pos=vector(2*text_size,text_size,0), text='M<sub>z</sub>', height=1.3*text_size, box=False, color=M_vertical_vec.color, opacity=0, visible=False)

Mz_graph_title = label(pos=Mz_x_axis_arrow.pos+vec(graph_h/2,graph_h+2*text_size,0), text='Vertical Magnetization', height=text_size, box=False, color=color.magenta, visible=False,opacity=0)
Mz_graph_line_sphere = sphere(pos=Mz_y_axis_arrow.pos+vec(Mz_y_axis_arrow.shaftwidth,Mz_x_axis_arrow.shaftwidth+graph_h/1.3,0), radius=1, color=M_vertical_vec.color, make_trail=True, visible=False)

Mz_graph = compound([Mz_x_axis_arrow,Mz_y_axis_arrow])
Mz_x_axis_arrow.visible=False
Mz_y_axis_arrow.visible=False
Mz_graph.visible=False

Mxy_x_axis_arrow = arrow(pos=vec(-w/1.8,-h/4-graph_h/2,0), axis = vec(graph_h*w_scale,0,0), shaftwidth=2*w_scale*(graph_h/100), headwidth=5*w_scale*(graph_h/100), headlength=10*w_scale*(graph_h/100), color=color.black, round=True)
Mxy_y_axis_arrow = arrow(pos=vec(-w/1.8,-h/4-graph_h/2,0), axis = vec(0,graph_h*h_scale,0), shaftwidth=2*w_scale*(graph_h/100), headwidth=5*w_scale*(graph_h/100), headlength=10*w_scale*(graph_h/100), color=color.black, round=True)
Mxy_x_label = label(pos=Mxy_x_axis_arrow.pos+vec(graph_h/2,-text_size,0), text='t', height=text_size, box=False, color=color.black, visible=False, opacity=0)
Mxy_y_label = label(pos=Mxy_x_axis_arrow.pos+vec(-text_size*2,graph_h,0), text='M<sub>xy</sub>', height=text_size, box=False, color=color.black, opacity=0, visible=False)
#Mxy_label = label(pos=main_y_label.pos+vector(0,2.5*text_size,0), text='M<sub>xy</sub>', height=1.3*text_size, box=False, color=color.blue, opacity=0, visible=False)
Mxy_label = label(pos=vector(0,2.5*text_size,0), text='M<sub>xy</sub>', height=1.3*text_size, box=False, color=color.blue, opacity=0, visible=False)

Mxy_graph_title = label(pos=Mxy_x_axis_arrow.pos+vec(graph_h/2,graph_h+2*text_size,0), text='Tangential Magnetization', height=text_size, box=False, color=color.blue, visible=False, opacity=0)
Mxy_graph_line_sphere = sphere(pos=Mxy_y_axis_arrow.pos+vec(Mxy_y_axis_arrow.shaftwidth,Mxy_x_axis_arrow.shaftwidth,0), radius=1, color=M_horizontal_vec.color, make_trail=True, visible=False)
voltage_graph=curve()
recoveredMz_graph=curve()
mri_signal_label=label(pos=vector(-610,230,0), text="⎯ Decaying MRI Signal", color=color.blue, height=text_size, box=False, opacity=0, visible=False)
recoverMz_label=label(pos=mri_signal_label.pos+vector(27,-2*text_size,0), text="⎯ Recovering Magnetization", height = text_size, box=False, opacity=0, color=vec(0.9,0,0.7), visible=False)
timescale_label=label(pos=vector(mri_signal_label.pos.x+55,-25,0), text="", height = text_size, box=False, opacity=0, color=color.black, visible=True)
sequence_label=label(pos=timescale_label.pos+vector(0,-2.2*text_size,0), text="", height = text_size, box=False, opacity=0, color=vec(0.000, 0.360, 0.390), visible=True)
te_marker=sphere(pos=vector(0,0,0), radius=5, color=vec(1,0.55,0), visible=False)
te_marker_label=label(pos=vector(0,0,0), text="TE sample", height=0.9*text_size, box=False, opacity=0, color=te_marker.color, visible=False)
Mxy_graph = compound([Mxy_x_axis_arrow,Mxy_y_axis_arrow])
Mxy_graph.visible=False
Mxy_x_axis_arrow.visible=False
Mxy_y_axis_arrow.visible=False
my_tissuedata=box(pos=vector(530,95,0), height=0.22*917, length=0.22*1930, width=0.5, color=color.white, texture='https://i.imgur.com/87DxlTP.png', shininess=0, opacity=1) #Try 0 to 1 opacity for T1 while keeping T2 at opacity = 1 to transition from T2 to T1
csfgraphlabel1=label(pos=vector(-450,40,0), text='CS Fluid', height=text_size, box=False, opacity=0, align='left', color=color.magenta, visible=False)
csfgraphlabel2=label(pos=csfgraphlabel1.pos+vector(-260,95,0), text='CS Fluid', height=text_size, box=False, opacity=0, align='left', color=color.blue, visible=False)
cbgraphlabel1=label(pos=csfgraphlabel1.pos+vector(0,100,0), text='Bone', height=text_size, box=False, opacity=0, align='left', color=color.magenta, visible=False)
cbgraphlabel2=label(pos=csfgraphlabel2.pos+vector(0,-125,0), text='Bone', height=text_size, box=False, opacity=0, align='left', color=color.blue, visible=False)
fatgraphlabel1=label(pos=cbgraphlabel1.pos+vector(0,20,0), text='Fat', height=text_size, box=False, opacity=0, align='left', color=color.magenta, visible=False)
fatgraphlabel2=label(pos=csfgraphlabel2.pos+vector(0,-85,0), text='Fat', height=text_size, box=False, opacity=0, align='left', color=color.blue, visible=False)

info_label = label(pos=vector(0,-h/2,0), text='', height=1.2*text_size, box=False, opacity=0, color=vec(0,0.5,0.5))
te_marker_shown = False
GRAPH_X_START = main_xgraph_axis.pos.x
GRAPH_X_WIDTH = main_xgraph_axis.axis.x
GRAPH_Y_BASE = main_xgraph_axis.pos.y
GRAPH_SIGNAL_SCALE = 170

def update_sequence_timing():
    global TR, TE, t_final_3
    preset = SEQUENCE_PRESETS[sequence_mode]
    TR = preset["TR_ms"] / MS_PER_SIM_UNIT
    TE = preset["TE_ms"] / MS_PER_SIM_UNIT
    t_final_3 = t_final_1 + TR

def graph_x(elapsed_after_pulse):
    return GRAPH_X_START + GRAPH_X_WIDTH*(elapsed_after_pulse/TR)

def graph_y(normalized_signal):
    return GRAPH_Y_BASE + GRAPH_SIGNAL_SCALE*normalized_signal

def update_sequence_ui():
    preset = SEQUENCE_PRESETS[sequence_mode]
    button_box_dict['T1'].color = color.green if sequence_mode == "T1" else vec(0.7,0.7,0.7)
    button_box_dict['T2'].color = color.green if sequence_mode == "T2" else vec(0.7,0.7,0.7)
    timescale_label.text = f"0    time (after RF pulse)     {preset['TR_ms']} (ms)"
    sequence_label.text = f"{sequence_mode}-weighted: TR {preset['TR_ms']} ms, TE {preset['TE_ms']} ms"

#Functions
def reset():
    global isRunning, isStarted, B_mag, B_dir, B,B_vec, M_dir, M, M_tip, Mvec, M_mag, t, torque_vec, torque_label, M_vertical_vec, M_horizontal_vec, voltage_list, voltage_graph, dt, mindex, recoveredMz_list, recoveredMz_graph, initial_M_mag, te_marker_shown, Bvec
    isRunning = False
    isStarted = False
    B_mag = 1
    B_dir = norm(vector(-1,-0.25882,0.96593))
    B = B_mag*B_dir
    omega=0
    
    initial_M_mag = 1
    M_mag = initial_M_mag
    M_dir = norm(vector(0,0.96593,0.25882))
    M = M_mag*M_dir
    torque = cross(M,B)

    Mvec.visible=False
    M_vertical_vec.visible=False
    M_horizontal_vec.visible=False
    Bvec.visible=False
    torque_vec.visible=False
    torque_label.visible=False
    Bvec_label.visible=False

    Mz_label.visible=False
    Mxy_label.visible=False
    mri_signal_label.visible=False
    recoverMz_label.visible=False
    reset_label.visible=False
    inactive_button_label.visible=False
    te_marker.visible=False
    te_marker_label.visible=False
    te_marker_shown = False
    voltage_graph.visible=False
    recoveredMz_graph.visible=False
    csfgraphlabel1.visible=False
    csfgraphlabel2.visible=False
    cbgraphlabel1.visible=False
    cbgraphlabel2.visible=False
    fatgraphlabel1.visible=False
    fatgraphlabel2.visible=False
    Bvec = arrow(pos=-vec(-1,0,0), axis=pixel_D*mag_h*B, shaftwidth=7.5*w_scale*(mag_h/100), headwidth=15*w_scale*(mag_h/100), headlength=30*w_scale*(mag_h/100), color=color.cyan, round=True, visible=False)
    torque_vec = arrow(pos=Mvec.pos+Mvec.axis, axis=pixel_D*mag_h/1.5*norm(cross(M,B)), shaftwidth=5*w_scale*(mag_h/100), headwidth=10*w_scale*(mag_h/100), headlength=20*w_scale*(mag_h/100), color=norm(vec(0,210,106)), round=True, visible=False)
    torque_label = label(pos=torque_vec.pos + torque_vec.axis + vector(2*text_size,0,0), text='τ<sub>RF</sub>', height=1.3*text_size, box=False, color=color.green, opacity=0, visible=False)
    #Hidden under Mvec
    M_vertical_vec = arrow(pos=vec(0,0,1), axis=pixel_D*mag_h*M, shaftwidth=7.5*w_scale*(mag_h/100), headwidth=15*w_scale*(mag_h/100), headlength=30*w_scale*(mag_h/100), color=vec(0.7,0,0), round=True, opacity=0.8)    
    M_vertical_vec.opacity=0.2
    Mvec = arrow(pos=vec(0,0,0), axis=pixel_D*mag_h*M, shaftwidth=8*w_scale*(mag_h/100), headwidth=15*w_scale*(mag_h/100), headlength=30*w_scale*(mag_h/100), color=vec(0.7,0,0.9), round=True, opacity=1, visible=True)
    Mvec_label.visible=True
    Mvec_label.pos = Mvec.pos+1.1*Mvec.axis+vector(-100,0,0)
    M_horizontal_vec = arrow(pos=Mvec.pos, axis=pixel_D*mag_h*dot(M, norm(vector(1,-0.25882,0.96593)))*norm(vector(1,-0.25882,0.96593))*.99, shaftwidth=5*w_scale*(mag_h/100)*.9, headwidth=10*w_scale*(mag_h/100)*.9, headlength=20*w_scale*(mag_h/100)*.9, color=vec(0,0,0.9), round=True, opacity=0.8)
    Mz_label.color=M_vertical_vec.color
    M_tip.clear_trail()
    M_tip.visible=False
    M_tip = sphere(pos=Mvec.pos+Mvec.axis, color=Mvec.color, make_trail=True, visible=True)
    voltage_list=[]
    recoveredMz_list=[]
    reset_label.text="Hit Reset Before Changing Tissue!"
    #if csfdone==True and cbdone==True and fatdone==True:
        
    t=0
    button_box_dict['Play/Pause'].color = vector(0.7,0.7,0.7)
    control_panel.unbind('mousedown', reset_button)
    control_panel.bind('mousedown', reset_button)
    update_sequence_ui()
    #print(animation_speed)

#Create Title
title = label(pos=vector(0,scene.height/2+9*text_size,0), text='Explore Signal Generation and Decay\n(Classical Description)', font='helvetica', height=1.8*text_size, box=False, visible=True, color=color.black, opacity=0)
lbl_start=label(pos=vector(0,-h/2-4*text_size,0), text="Start with Activities: (link at top)!", font="helvetica", box=False, linewidth=2, canvas=scene, color=vec(0.000, 0.360, 0.390), height=0, visible=True, opacity=0)
reset_label=label(pos=lbl_start.pos+vector(0,95,0), text="Hit Reset Before Changing Tissue!", color=lbl_start.color, height=1.5*text_size, box=False, opacity=0, visible=False)

#Hyperlinks - figure this out better from Bruce Sherwood email on 1/12/2024
x= '''<font size=4> <font>'''
y = '''<font size=4> <font>'''
z = '''<font size=4> <font>'''
def link4(url, d):
    global z
    z += "<a href='https://medicalimaging.watzekdi.net/images/mri_images/Classical%20Signal/Information-ClassicalSignal.png" + "' target='_blank'>" + url + "</a>"
    z += d
def link3(url, d):
    global y
    y += "<a href='https://medicalimaging.watzekdi.net/images/mri_images/Classical%20Signal/BACKGROUND-ClassicalSignal.png" + "' target='_blank'>" + url + "</a>"
    y += d
def link2(url, d):
    global x
    x += "<a href='https://medicalimaging.watzekdi.net/images/mri_images/Classical%20Signal/Activities_ClassicalSignal.png" + "' target='_blank'>" + url + "</a>"
    x += d

link2("Activities", "&nbsp &nbsp &nbsp")
print(x)
link3("Background", "&nbsp &nbsp &nbsp")
print(y)
link4("Information", "&nbsp &nbsp &nbsp")
print(z)

#-------------------------------New canvas with control panel ---------------------------------------------------------------------------------------------------------------------------------------------------
# Set up Control Panel
control_panel=canvas(width=scene.width, height=scene.height/5 , center = vector(0,0,0), background=vec(0.622, 0.779, 0.847), userspin=False, userzoom=False, resizable=False)
title_cp=label(pos=vector(0,(control_panel.height/2)-text_size,0), text='Control Panel', font='helvetica', height=control_panel.height*(20/100), box=False, visible=True, color=color.black, opacity=0)

# Create Buttons
button_box_dict = {}
button_icon_list = []
button_text_list = []
voltage_list = []
recoveredMz_list=[]
button_size = control_panel.height/2

def create_buttons(chosen_canvas, text_list, icon_list):
    side_buffer = chosen_canvas.width/100
    if len(text_list) > 1:
        step = (chosen_canvas.width-2*side_buffer)/(len(text_list)-1)
    for i in range(len(text_list)):
        button_box_dict.setdefault(text_list[i], box(pos=vector((-chosen_canvas.width/2)+side_buffer+(i*step), -text_size/2, 0), length=button_size, height=button_size, width=0.01, color=vec(0.7,0.7,0.7), shininess=0))
        button_icon_list.append(label(pos=button_box_dict[text_list[i]].pos, text=icon_list[i], height=button_box_dict[text_list[i]].height/1.7, color=color.black, box=False, opacity=0))
        button_text_list.append(label(pos=button_box_dict[text_list[i]].pos-vector(0,button_box_dict[text_list[i]].height/2+text_size,0), text=text_list[i], height=text_size, color=color.black, box=False, opacity=0))

create_buttons(control_panel, ['Play/Pause', 'Reset', 'T1', 'T2'], ['⏯','↻','',''])
inactive_button_label=label(pos=button_box_dict['Reset'].pos, text='x', color=color.red, box=False, height=3*text_size, opacity=0, visible=False)
def pause_play_button():
    global isStarted, isRunning, M_tip
    loc_m = control_panel.mouse.pos
    if abs(loc_m.x-button_box_dict['Play/Pause'].pos.x)<=button_box_dict['Play/Pause'].length/2 and abs(loc_m.y-button_box_dict['Play/Pause'].pos.y)<=button_box_dict['Play/Pause'].height/2:
        # if M_tip.pos.y<=0:
        #     reset()
        # else:
        if button_box_dict['Play/Pause'].color == color.green:
            button_box_dict['Play/Pause'].color = vec(0.7,0.7,0.7)
            isRunning = False
            M_tip.make_trail = False
        else:
            button_box_dict['Play/Pause'].color = color.green
            control_panel.unbind('mousedown', reset_button)
            isRunning = True
            isStarted = True
            M_tip.make_trail = True

        
control_panel.bind('mousedown', pause_play_button)




def reset_button():
    loc_m = control_panel.mouse.pos
    if abs(loc_m.x-button_box_dict['Reset'].pos.x)<=button_box_dict['Reset'].length/2 and abs(loc_m.y-button_box_dict['Reset'].pos.y)<=button_box_dict['Reset'].height/2:
        button_box_dict['Reset'].color = color.green
        reset()
        #sleep(1)
        #reset()
        button_box_dict['Reset'].color = vector(0.7,0.7,0.7)

control_panel.bind('mousedown', reset_button)

def sequence_button():
    global sequence_mode
    loc_m = control_panel.mouse.pos
    for mode in ("T1", "T2"):
        if abs(loc_m.x-button_box_dict[mode].pos.x)<=button_box_dict[mode].length/2 and abs(loc_m.y-button_box_dict[mode].pos.y)<=button_box_dict[mode].height/2:
            if sequence_mode != mode:
                sequence_mode = mode
                update_sequence_timing()
                reset()
            else:
                update_sequence_ui()
            return

control_panel.bind('mousedown', sequence_button)
update_sequence_ui()


# Menu from Lane
def change_tissue(m):
    global T1,T2, t_final_3, mindex
    scene.autoscale = False
    mindex=m.index
    if m.index == 0:
        T1 = 1
        T2 = 1/10
        
    if m.index == 1:
        T1 = 0.151
        #T2 = 0.00038
        T2 = 5*0.00038
        
    if m.index == 2:
        T1 = 0.094
        T2 = 0.026
        
    #t_final_3 = t_final_2 + T1
    my_element_changed=True
wtext(text="                                                            <font size=4>Signal-Generating Tissue = <font>")
menu_text = ["Cerebrospinal Fluid","Cortical Bone","Fat"]  #Center numbers better

bg_menu = menu(bind=change_tissue, choices = menu_text)


scene.select()
scene.autoscale=False
while True:
    rate(0.3*animation_speed)
    while isRunning and t<t_final_1:
        rate(0.3*animation_speed)
        inactive_button_label.visible=True
        Bvec.visible=True
        torque_vec.visible=True
        torque_label.visible=True
        Mvec_label.visible=False
        Bvec_label.visible=True
        Mz_label.visible=True
        Mxy_label.visible=True
        if isRunning: #redundant
            torque = cross(M,B)
            energy = dot(-M,B)
            M_dir = M_dir.rotate(angle=(-pi/2)/(t_final_1/dt), axis=main_x_axis.axis)
            M=M_mag*M_dir
            Mvec.axis = pixel_D*mag_h*M
            M_tip.pos = Mvec.pos + Mvec.axis
            M_vertical_vec.opacity=0.8
            M_vertical_vec.axis = pixel_D*mag_h*dot(M, norm(vector(0,0.96593,0.25882)))*norm(vector(0,0.96593,0.25882))*.99
            M_vertical_vec.headwidth = starting_headw*mag(M_vertical_vec.axis)/mag_h*.9
            M_vertical_vec.headlength = starting_headl*mag(M_vertical_vec.axis)/mag_h*.9
            M_vertical_vec.shaftwidth = starting_shaftw*mag(M_vertical_vec.axis)/mag_h*.9
            Mz_label.pos=M_vertical_vec.axis+vector(-40,0,0)
           
            M_horizontal_vec.axis = pixel_D*mag_h*(dot(M, norm(vector(1,-0.25882,0.96593)))*norm(vector(1,-0.25882,0.96593)) + dot(M, norm(vector(-1,-0.25882,0.96593)))*norm(vector(-1,-0.25882,0.96593)))*.99
            M_horizontal_vec.headwidth = starting_headw*mag(M_horizontal_vec.axis)/mag_h*.9
            M_horizontal_vec.headlength = starting_headl*mag(M_horizontal_vec.axis)/mag_h*.9
            M_horizontal_vec.shaftwidth = starting_shaftw*mag(M_horizontal_vec.axis)/mag_h*.9
            Mxy_label.pos= M_horizontal_vec.axis+vector(0,2*text_size,0)
            torque_vec.pos = Mvec.pos+Mvec.axis
            torque_vec.axis = pixel_D*mag_h/1.5*norm(cross(M,B))
            torque_label.pos=torque_vec.pos + torque_vec.axis + vector(2*text_size,0,0)
            t=t+dt  
    if isRunning and abs(t-t_final_1)<=2*dt:
        sleep(1)
        M_horizontal_vec_after_pulse=M_horizontal_vec.axis #start horizontal signal with this
        M_tip.clear_trail()
        M_tip.make_trail = False
        Mvec.visible=False
        Bvec.visible=False
        Mvec_label.visible=False
        Bvec_label.visible=False
        torque_vec.visible=False
        torque_label.visible=False
        #isRunning = False
        Mz_label.visible=False
        info_label.text = ''
        #t=t_final_1
        


    while isRunning and t>=t_final_1 and t<t_final_3:
        rate(0.2*animation_speed)
        if isRunning: #redundant?
            if mindex==0:
                csfgraphlabel1.visible=True
                csfgraphlabel2.visible=True
            if mindex==1:
                cbgraphlabel1.visible=True
                cbgraphlabel2.visible=True
            if mindex==2:
                fatgraphlabel1.visible=True
                fatgraphlabel2.visible=True
            elapsed_after_pulse = t-t_final_1
            M_mag = initial_M_mag*exp(-elapsed_after_pulse/T2)
            M=M_mag*M_dir
            Mxy_label.visible=True
            mri_signal_label.visible=True
            M_vertical_vec.color=vec(0.7,0,0.9)
            M_vertical_vec.opacity=1
            M_horizontal_vec.axis=M_horizontal_vec_after_pulse*exp(-elapsed_after_pulse/T2)
            voltage=vector(graph_x(elapsed_after_pulse), graph_y(M_mag), 0)
            voltage_list.append(voltage)
            voltage_graph.visible=False
            voltage_graph=curve(canvas=scene, pos=voltage_list, radius=2, color=color.blue)
            M_horizontal_vec.headwidth = starting_headw*mag(M_horizontal_vec.axis)/mag_h*.9
            M_horizontal_vec.headlength = starting_headl*mag(M_horizontal_vec.axis)/mag_h*.9
            M_horizontal_vec.shaftwidth = starting_shaftw*mag(M_horizontal_vec.axis)/mag_h*.9
            Mxy_label.pos=M_horizontal_vec.pos+M_horizontal_vec.axis+vector(0,2*text_size,0)
            if (mindex==1 or mindex==2) and t>=t_final_1+0.05:
                Mxy_label.visible=False
            if mindex==0 and t>=t_final_1+0.15:
                Mxy_label.visible=False
            if (not te_marker_shown) and elapsed_after_pulse >= TE:
                te_signal = initial_M_mag*exp(-TE/T2)
                te_marker.pos = vector(graph_x(TE), graph_y(te_signal), 0)
                te_marker.visible = True
                te_marker_label.pos = te_marker.pos + vector(35,1.5*text_size,0)
                te_marker_label.visible = True
                te_marker_shown = True
            M = norm(vector(0,0.96593,0.25882))
            M_vertical_vec.axis = pixel_D*mag_h*M*(1-exp(-elapsed_after_pulse/T1))+vector(0,starting_headl*exp(-elapsed_after_pulse/T1),0) 
            M_vertical_vec.headwidth = starting_headw
            M_vertical_vec.headlength = starting_headl
            M_vertical_vec.shaftwidth = starting_shaftw
            Mz_label.visible=True
            Mz_label.color=Mvec.color
            recoverMz_label.visible=True
            #timescale_label.visible=True
            recoveredMz_list.append(vector(graph_x(elapsed_after_pulse), graph_y(1-exp(-elapsed_after_pulse/T1)), 0))
            recoveredMz_graph.visible=False
            recoveredMz_graph=curve(canvas=scene, pos=recoveredMz_list, radius=2, color=vec(0.9,0,0.7))
            Mz_label.pos = M_vertical_vec.pos + M_vertical_vec.axis+vector(-40,0,0)
            Mz_graph_line_sphere.pos = Mz_y_axis_arrow.pos+vec(Mz_y_axis_arrow.shaftwidth+(t/t_final_3)*graph_h/1.3,Mz_x_axis_arrow.shaftwidth+((dot(Mvec.axis,norm(vector(0,0.96593,0.25882))))/(M_mag*mag_h*pixel_D))*graph_h/1.3,0)
            Mxy_graph_line_sphere.pos = Mxy_y_axis_arrow.pos+vec(Mxy_y_axis_arrow.shaftwidth+(t/t_final_3)*graph_h/1.3,Mxy_x_axis_arrow.shaftwidth+(sqrt(dot(Mvec.axis,norm(vector(1,-0.25882,0.96593)))**2 + dot(Mvec.axis,norm(vector(-1,-0.25882,0.96593)))**2)/(M_mag*mag_h*pixel_D))*graph_h/1.3,0)
            t = t+dt

    if isRunning and t>=t_final_3:
        button_box_dict['Play/Pause'].color = vec(0.7,0.7,0.7)
        isRunning = False
        isStarted = False
        control_panel.bind('mousedown', reset_button)
        reset_label.visible=True
        inactive_button_label.visible=False
    if csfgraphlabel1.visible==True and cbgraphlabel1.visible==True and fatgraphlabel1.visible==True:
        reset_label.text="Reload Page to Start Over!"
