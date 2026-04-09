from asyncio import sleep
import random as rand

from vpython import *

#Create canvas. Set userspin=False, so image won't rotate.
scene=canvas(width =1024, height=480, center=vector(0,0,0), background=color.white, userspin=True, userzoom=False)
# background_box = box(pos=vector(0,0,0), height=scene.height, length=scene.width, width=1, opacity=0)
#background_box=box(pos=vector(500,0,0), length=scene.height, height=scene.height/2, width=0.25, texture='https://webdev2.watzek.cloud/~nddill/scanningSims/images/Nuclear/RN%20Picture%20(1025x513).jpg', shininess=0, opacity=0.9)


#Set lighting so not the default gray
scene.lights=[]
distant_light(direction=vector( 0.22, 0.44, 0.88), color=color.white)
distant_light(direction=vector(-0.88, -0.22, -0.44), color=color.white)



# Variables
text_size = scene.height*(15/480)
nucleon_number = 131 #BAS changed from 50 to make it I-131, make one nucleon type invisible and rotate to count
nucleon_radius = 2*text_size
nucleus_radius =  nucleon_number**(1/3)*nucleon_radius #Adjust nuclear radius so nucleons fill nucleus
animation_speed = 60
step_size = 3
proton_excess = False
neutron_excess = False
metastable_energy = False
propagating = False
finished = False
scale_sphere = sphere(pos=vector(0,scene.height/2,0), color=color.red, radius=3, opacity=0)

#Create Title
title = label(pos=vector(0,scene.height/2+3*text_size,0), text='Investigate Gamma Ray Production in Nuclear Medicine', font='helvetica', height=1.8*text_size, box=False, visible=True, color=color.black, opacity=0)
lbl_start=label(pos=vector(0,-scene.height/2,0), text="Start with Activities (link at top)!", font="helvetica", box=True, canvas=scene, color=vec(0.000, 0.360, 0.390), height=text_size, visible=False, opacity=0)
my_click = label(pos=vector(scene.width/1.6,-scene.height/1.8,0), text="Click to Advance", font="helvetica", box=False, canvas=scene, color=vec(0.000, 0.360, 0.390), height=text_size, visible=False, opacity=0)

# Objects
proton_list = []
neutron_list = []
cell=box(pos=vector(scene.width/2.1,-10,0.3), color=color.white, height = 0.7*320, length = 0.7*512, width = 0.5, opacity= 1, texture='https://medicalimaging.watzekdi.net/images/Nuclear_images/Activity2-Instability/Cancer_cells_crop2_small.png', visible = True)
#cell_nomid=box(pos=vector(scene.width/2.1,-10,0.3), color=color.white, height = 0.7*320, length = 0.7*512, width = 0.5, opacity= 1, texture='https://medicalimaging.watzekdi.net/images/Nuclear_images/Activity2-Instability/Cancer_cells_crop2_small_nomid.png', visible = False)

cell_lbl=label(pos=vector(scene.width/2.1,cell.height/2+4.5*text_size,0.3), color=vec(0,0.36,0.36), text = 'Cancerous Cells', height = 1.5*text_size, opacity = 0, box = False, visible = True)

lightningbolt = box(pos=vector(scene.width/2.1,0,0)+vector(0,cell.height/2+0.25*527,0.3), color=color.white, height = 0.5*527, length = 0.5*100, width = 0.5, opacity= 1, texture='https://i.imgur.com/z158BcH.png', visible = False)
tombstone = box(pos=vector(scene.width/2.1,cell.pos.y,0.3), color=color.white, height = 0.6*273, length = 0.6*240, width = 0.5, opacity= 1, texture='https://i.imgur.com/YZF3zwr.png', visible = False)
F18_lbl=label(pos=vector(0,scene.height/5,0), text='Fluorine-18', box=False, height=1.5*text_size, color=vec(0,0.36,0.36), opacity=0, visible=False)
O18_lbl=label(pos=vector(0,scene.height/5,0), text='Oxygen-18', box=False, height=1.5*text_size, color=vec(0,0.36,0.36), opacity=0, visible=False)
jiggle_lbl=label(pos=lbl_start.pos+vector(0,3*text_size,0), text='Gotta Jiggle!', box=False, height=1.5*text_size, color=vec(0,0.56,0.56), opacity=0, visible=False)

Tc_lbl=label(pos=vector(0,scene.height/3,0), text='Technetium-99m', box=False, height=1.5*text_size, color=vec(0,0.36,0.36), opacity=0, visible=False)
I131_lbl=label(pos=vector(0,scene.height/2.7,0), text='Iodine-131', box=False, height=1.5*text_size, color=vec(0,0.36,0.36), opacity=0, visible=True)
Xe131_lbl=label(pos=vector(0,scene.height/2.7,0), text='Xenon-131', box=False, height=1.5*text_size, color=vec(0,0.36,0.36), opacity=0, visible=False)

keybox_list=[vector(70,70,0), vector(230,70,0), vector(230,-92,0), vector(70,-92,0), vector(70,70,0)]
keybox=curve(pos=keybox_list, radius=1, color = vec(0,0.36,0.36), origin = vector(-610,0,1))
keybox_lbl=label(pos=vector((keybox_list[0].x+keybox_list[1].x)/2,0.97*cell_lbl.pos.y,0) + keybox.origin, box = False, height=1.5*text_size, radius=1, text = 'Symbol Key', color = vec(0,0.36,0.36), opacity=0)
proton_key=ellipsoid(pos=(keybox_list[0]+vector(-490,-80,0)), height=1.9*nucleon_radius, length = 1.5*nucleon_radius, width = 1.5*nucleon_radius, color=color.magenta, opacity=0.2)
proton_key_lbl=label(pos=proton_key.pos, text='P', box=False, height=2*text_size, opacity=0, color=color.black)
neutron_key=ellipsoid(pos=(proton_key.pos+vector(-2.5*nucleon_radius,0,0)), length = proton_key.length, height = proton_key.height, width = proton_key.width, color=color.cyan, opacity=0.2)
neutron_key_lbl=label(pos=neutron_key.pos, text='N', box=False, height=2*text_size, opacity=0, color=color.black)
positron_key=ellipsoid(pos=(proton_key.pos+vector(0,2*nucleon_radius,0)), length = 0.4*proton_key.length, height = 0.4*proton_key.height, width = 0.4*proton_key.width, color=color.purple, opacity=0.3)
positron_key_lbl=label(pos=positron_key.pos, text='e<sup>+<sup>', box=False, height=text_size, opacity=0, color=color.black)
electron_key=ellipsoid(pos=(neutron_key.pos+vector(0,2*nucleon_radius,0)), length = 0.4*proton_key.length, height = 0.4*proton_key.height, width = 0.4*proton_key.width, color=color.cyan, opacity=0.2)
electron_key_lbl=label(pos=electron_key.pos, text='e<sup>-<sup>', box=False, height=text_size, opacity=0, color=color.black)
neutrino_key=ellipsoid(pos=(proton_key.pos+vector(0,-2*nucleon_radius,0)), length = 0.4*proton_key.length, height = 0.4*proton_key.height, width = 0.4*proton_key.width, color=color.red, opacity=0.3)
neutrino_key_lbl=label(pos=neutrino_key.pos, text='v', font = 'times', box=False, height=text_size, opacity=0, color=color.black)
antineutrino_key=ellipsoid(pos=(neutron_key.pos+vector(0,-2*nucleon_radius,0)), length = 0.4*proton_key.length, height = 0.4*proton_key.height, width = 0.4*proton_key.width, color=color.green, opacity=0.2)
antineutrino_key_lbl=label(pos=antineutrino_key.pos, text='v\u0305', font = 'times', box=False, height=text_size, opacity=0, color=color.black) #For overbar look at diacritical marks unicode https://en.wiktionary.org/wiki/%E2%97%8C%CC%85
nuclei_names_list = [F18_lbl,Tc_lbl,I131_lbl]
nucleus_sphere = sphere(pos=vector(0,0,0), radius=nucleus_radius, color=vec(0.7,0.7,0.7), opacity=0.2)

info_label = label(pos=vector(0,-scene.height/2+4*text_size,0), text='', height=text_size, box=False, opacity=0)

pulse_pos = [vector(-27.791,-1.773,0), vector(-25.791,-1.773,0), vector(-23.791,-1.773,0), vector(-21.791,-1.773,0), vector(-20.791,-3.773,0), vector(-18.791,-5.773,0), vector(-16.791,-3.773,0), vector(-15.791,-0.773,0), vector(-15.791,2.227,0), vector(-14.791,5.227,0), vector(-14.791,7.227,0), vector(-14.791,9.227,0), vector(-12.791,9.227,0), vector(-12.791,7.227,0), vector(-11.791,5.227,0), vector(-11.791,3.227,0), vector(-10.791,1.227,0), vector(-10.791,-0.773,0), vector(-10.791,-2.773,0), vector(-10.791,-4.773,0), vector(-10.791,-6.773,0), vector(-10.791,-8.773,0), vector(-9.791,-10.773,0), vector(-9.791,-12.773,0), vector(-7.791,-9.773,0), vector(-6.791,-7.773,0), vector(-6.791,-5.773,0), vector(-6.791,-3.773,0), vector(-6.791,-1.773,0), vector(-6.791,0.227,0), vector(-6.791,3.227,0), vector(-6.791,6.227,0), vector(-6.791,9.227,0), vector(-6.791,11.227,0), vector(-6.791,14.227,0), vector(-6.791,12.227,0), vector(-5.791,14.227,0), vector(-5.791,16.227,0), vector(-5.791,18.227,0), vector(-4.791,20.227,0), vector(-4.791,22.227,0), vector(-4.791,24.227,0), vector(-4.791,26.227,0), vector(-3.791,19.227,0), vector(-2.791,16.227,0), vector(-2.791,14.227,0), vector(-1.791,11.227,0), vector(-1.791,9.227,0), vector(-1.791,6.227,0), vector(-1.791,2.227,0), vector(-1.791,-2.773,0), vector(-1.791,-6.773,0), vector(-1.791,-10.773,0), vector(-1.791,-15.773,0), vector(-1.791,-19.773,0), vector(-1.791,-22.773,0), vector(-1.791,-25.773,0), vector(-1.791,-27.773,0), vector(-0.791,-30.773,0), vector(-0.791,-33.773,0), vector(0.209,-36.773,0), vector(0.209,-38.773,0), vector(2.209,-29.773,0), vector(2.209,-24.773,0), vector(3.209,-18.773,0), vector(3.209,-15.773,0), vector(3.209,-10.773,0), vector(3.209,-6.773,0), vector(3.209,-3.773,0), vector(3.209,0.227,0), vector(3.209,4.227,0), vector(3.209,8.227,0), vector(3.209,11.227,0), vector(3.209,15.227,0), vector(4.209,18.227,0), vector(4.209,21.227,0), vector(4.209,24.227,0), vector(5.209,26.227,0), vector(5.209,21.227,0), vector(6.209,16.227,0), vector(7.209,13.227,0), vector(7.209,10.227,0), vector(7.209,7.227,0), vector(7.209,3.227,0), vector(7.209,-0.773,0), vector(7.209,-3.773,0), vector(7.209,-6.773,0), vector(7.209,-9.773,0), vector(9.209,-10.773,0), vector(9.209,-13.773,0), vector(12.209,-8.773,0), vector(12.209,-3.773,0), vector(12.209,1.227,0), vector(12.209,5.227,0), vector(12.209,8.227,0), vector(14.209,10.227,0), vector(16.209,7.227,0), vector(16.209,5.227,0), vector(16.209,1.227,0), vector(16.209,-2.773,0), vector(16.209,-4.773,0), vector(18.209,-6.773,0), vector(21.209,-4.773,0), vector(21.209,-2.773,0), vector(21.209,0.227,0), vector(23.209,1.227,0), vector(24.209,-1.773,0), vector(27.209,-1.773,0), vector(30.209,-1.773,0), vector(31.209,-1.773,0)]
for i in range(len(pulse_pos)):
    pulse_pos[i].x = 2*(scene.width/1024)*pulse_pos[i].x
    pulse_pos[i].y =2*(scene.height/480)*pulse_pos[i].y

#Quick Fix
LOR_arrow1 = arrow(pos = vector(0,0,0), axis = vector(0,0,0), round = True, headlength = 50, headwidth = 30, shaftwidth = 15, color = color.black, opacity=0.1, visable=False)
LOR_arrow2 = arrow(pos = vector(0,0,0), axis = vector(0,0,0), round = True, headlength = 50, headwidth = 30, shaftwidth = 15, color = color.black, opacity=0.1, visable=False)
neutrino_sphere = sphere(pos= vector(0,0,0) + nucleon_radius*hat(vector(0,0.5,0.5)), radius=0.2*nucleon_radius, color=color.green, opacity = 0.3, visible = False)
positron_sphere = sphere(pos=vector(0,0,0) + nucleon_radius*hat(vector(0,0.5,0.5)), radius=0.4*nucleon_radius, color=color.purple, opacity = 0.3, visible = False)
positron_label = label(pos=positron_sphere.pos, text='e<sup>+<sup>', height=text_size, color=color.black, box=False, opacity=0, visible = False)
neutrino_sphere = sphere(pos=vector(0,0,0) + nucleon_radius*hat(vector(0,0.5,0.5)), radius=0.2*nucleon_radius, color=color.green, opacity = 0.3, visible = False)
neutrino_label = label(pos=neutrino_sphere.pos, text='v', font ='times', height=0.8*text_size, color=color.black, box=False, opacity=0, visible = False)
antineutrino_sphere = sphere(pos=vector(0,0,0) + nucleon_radius*hat(vector(0,0.5,0.5)), radius=0.2*nucleon_radius, color=color.red, opacity = 0.3, visible = False)
antineutrino_label = label(pos=antineutrino_sphere.pos, text='v\u0305', font ='times', height=0.8*text_size, color=color.black, box=False, opacity=0, visible = False)
# Functions

# def click():
#     loc_b=scene.mouse.pos
#     control_panel.append_to_caption(str(loc_b)+'\n')

# scene.bind('mousedown', click)
def any(new_pos):
    for j in range(len(proton_list+neutron_list)):
        if find_distance(new_pos, (proton_list+neutron_list)[j].pos) < nucleon_radius/1.2:
            return True
    return False

def create_nucleus(atomic_mass): #randomly positioning neutrons and protons, make a function of atomic number
    while len(proton_list+neutron_list)<atomic_mass:
        theta = 2*pi*random()
        phi = pi*random()
        r = random()*(nucleus_radius-nucleon_radius)
        new_pos=r*vector(cos(theta)*sin(phi),sin(theta)*sin(phi),cos(phi))
        while any(new_pos):
            theta = 2*pi*random()
            phi = pi*random()
            r = random()*(nucleus_radius-nucleon_radius)
            new_pos=r*vector(cos(theta)*sin(phi),sin(theta)*sin(phi),cos(phi))
        proton_list.append(sphere(pos=new_pos, radius=nucleon_radius, color=color.magenta, opacity=0.3))
        while any(new_pos):
            theta = 2*pi*random()
            phi = pi*random()
            r = random()*(nucleus_radius-nucleon_radius)
            new_pos=r*vector(cos(theta)*sin(phi),sin(theta)*sin(phi),cos(phi))
        neutron_list.append(sphere(pos=new_pos, radius=nucleon_radius, color=color.cyan, opacity=0.3))

def find_distance(v1,v2):
    v3 = v1-v2
    d = sqrt(v3.x**2+v3.y**2+v3.z**2)
    return d

def Run():
    global propagating
    propagating = not propagating
    scene.autoscale=False
    # scene.select()
    if propagating:
        button_box_dict['Play/Pause'].color = color.green
        control_panel.unbind('mousedown', reset_button)
        
        # if not started:
        #     x=1
    else: 
        button_box_dict['Play/Pause'].color = vector(0.7,0.7,0.7)
        control_panel.bind('mousedown', reset_button)
    return

# Setup
scene.select()
create_nucleus(nucleon_number)


s = '''<font size=4> <font>'''
l= '''<font size=4> <font>'''
q = '''<font size=4> <font>'''
v = '''<font size=4> <font>'''
def link1(url, d):
    global s
    s += "<a href='https://medicalimaging.watzekdi.net/images/Nuclear_images/Activity2-Instability/Information-NuclearDecay.png" + "' target='_blank'>" + url + "</a>"
    s += d
def link2(url, d):
    global l
    l += "<a href='https://medicalimaging.watzekdi.net/images/Nuclear_images/Activity2-Instability/Activities-NuclearDecay.png" + "' target='_blank'>" + url + "</a>"
    l += d
def link3(url, d):
    global q
    q += "<a href='https://medicalimaging.watzekdi.net/images/Nuclear_images/Activity2-Instability/Background-NuclearDecay.jpg" + "' target='_blank'>" + url + "</a>"
    q += d
def link4(url, d):
    global v
    v += "<a href='https://medicalimaging.watzekdi.net/images/Nuclear_images/Activity2-Instability/Information-NuclearDecay.png" + "' target='_blank'>" + url + "</a>"
    v += d
 
link4("Information", "&nbsp &nbsp &nbsp")
scene.append_to_title(v)
link3("Background", "&nbsp &nbsp &nbsp")
scene.append_to_title(q)
link2("Activities", "&nbsp &nbsp &nbsp")
scene.append_to_title(l)




# Set up Control Panel
control_panel=canvas(width=1024, height=100, center = vector(0,0,0), background=vec(0.622, 0.779, 0.847), userspin=False, userzoom=False, resizable=False)
title_cp=label(pos=vector(0,(control_panel.height/2)-text_size,0), text='Control Panel', font='helvetica', height=control_panel.height*(20/100), box=False, visible=True, color=color.black, opacity=0)

# Create Buttons
button_box_dict = {}
button_icon_list = []
button_text_list = []
button_size = 50

def create_buttons(chosen_canvas, text_list, icon_list):
    side_buffer = chosen_canvas.width/100
    if len(text_list) > 1:
        step = (chosen_canvas.width-2*side_buffer)/(len(text_list)-1)
    for i in range(len(text_list)):
        button_box_dict.setdefault(text_list[i], box(pos=vector((-chosen_canvas.width/2)+side_buffer+(i*step), -text_size/2, 0), length=control_panel.width*(button_size/1024), height=control_panel.height*(button_size/100), width=0.01, color=vec(0.7,0.7,0.7), shininess=0))
        button_icon_list.append(label(pos=button_box_dict[text_list[i]].pos, text=icon_list[i], height=button_box_dict[text_list[i]].height/1.7, color=color.black, box=False, opacity=0))
        button_text_list.append(label(pos=button_box_dict[text_list[i]].pos-vector(0,button_box_dict[text_list[i]].height/2+text_size,0), text=text_list[i], height=text_size, color=color.black, box=False, opacity=0))
create_buttons(control_panel, ['Play/Pause', 'Proton Excess', 'Neutron Excess', 'Metastable State', 'Reset'], ['⏯', 'P', 'N', '⚡', '↻'])

# Button Functionality

def pause_play_button():
    global proton_excess, neutron_excess
    loc_m = control_panel.mouse.pos
    if abs(loc_m.x-button_box_dict['Play/Pause'].pos.x)<=button_box_dict['Play/Pause'].length/2 and abs(loc_m.y-button_box_dict['Play/Pause'].pos.y)<=button_box_dict['Play/Pause'].height/2:
        if finished:
            info_label.text = 'Click reset to restart the simulation'
        else:
            if neutron_excess or proton_excess or metastable_energy:
                Run()
            else:
                info_label.text = 'Select proton excess, neutron excess, or metastable first'
                sleep(5)
                info_label.text = ''

control_panel.bind('mousedown', pause_play_button)

def proton_button():
    global proton_excess, neutron_excess, metastable_energy, nucleon_number, nucleus_radius, proton_list, neutron_list
    loc_m = control_panel.mouse.pos
    if abs(loc_m.x-button_box_dict['Proton Excess'].pos.x)<=button_box_dict['Proton Excess'].length/2 and abs(loc_m.y-button_box_dict['Proton Excess'].pos.y)<=button_box_dict['Proton Excess'].height/2:
        scene.autoscale = False
        nucleon_number=18 #for fluorine-18
        nucleus_radius =  nucleon_number**(1/3)*nucleon_radius
        nucleus_sphere.radius = nucleus_radius
        cell.visible = False
        cell_lbl.visible = False
        info_label.text = ''
        for p in proton_list:
            #print(p)
            p.visible = False
        for n in neutron_list:
            n.visible = False
        proton_list=[]
        neutron_list=[]
        create_nucleus(nucleon_number)
        if finished:
            info_label.text = 'Click reset to restart the simulation'
        elif button_box_dict['Proton Excess'].color == vector(0.7,0.7,0.7):
            button_box_dict['Proton Excess'].color = color.green
            button_box_dict['Neutron Excess'].color = vector(0.7,0.7,0.7)
            button_box_dict['Metastable State'].color = vector(0.7,0.7,0.7)
            proton_excess = True
            neutron_excess = False
            metastable_energy = False
            F18_lbl.visible=True
            I131_lbl.visible=False
            Tc_lbl.visible=False
            Xe131_lbl.visible = False
            O18_lbl.visible = False
            for p in proton_list:
                p.color = color.magenta
            for n in neutron_list:
                n.color = color.cyan
            indexes = list(range(len(neutron_list)))
            switch_indexes = []
            for i in range(round(len(neutron_list)*0.3)):
                rand_index = floor(random()*len(indexes))
                switch_indexes.append(indexes[rand_index])
                indexes.remove(indexes[rand_index])
            for i in switch_indexes:
                neutron_list[i].color = color.magenta

control_panel.bind('mousedown', proton_button)

def neutron_button():
    global proton_excess, neutron_excess, metastable_energy, nucleon_number, nucleus_radius, proton_list, neutron_list
    loc_m = control_panel.mouse.pos
    if abs(loc_m.x-button_box_dict['Neutron Excess'].pos.x)<=button_box_dict['Neutron Excess'].length/2 and abs(loc_m.y-button_box_dict['Neutron Excess'].pos.y)<=button_box_dict['Neutron Excess'].height/2:
        scene.autoscale = False
        nucleon_number=131 #for iodine-131
        nucleus_radius =  nucleon_number**(1/3)*nucleon_radius
        nucleus_sphere.radius = nucleus_radius
        cell.visible=True
        cell_lbl.visible = True
        info_label.text = ''
        for p in proton_list:
            p.visible = False
        for n in neutron_list:
            n.visible = False
        proton_list=[]
        neutron_list=[]
        create_nucleus(nucleon_number)
        if finished:
            info_label.text = 'Click reset to restart the simulation'
        elif button_box_dict['Neutron Excess'].color == vector(0.7,0.7,0.7):
            button_box_dict['Proton Excess'].color = vector(0.7,0.7,0.7)
            button_box_dict['Neutron Excess'].color = color.green
            button_box_dict['Metastable State'].color = vector(0.7,0.7,0.7)
            proton_excess = False
            neutron_excess = True
            metastable_energy = False
            I131_lbl.visible=True
            F18_lbl.visible=False
            Tc_lbl.visible=False
            Xe131_lbl.visible = False
            O18_lbl.visible = False
            for p in proton_list:
                p.color = color.magenta
            for n in neutron_list:
                n.color = color.cyan
            indexes = list(range(len(proton_list)))
            switch_indexes = []
            for i in range(round(len(proton_list)*0.3)):
                rand_index = floor(random()*len(indexes))
                switch_indexes.append(indexes[rand_index])
                indexes.remove(indexes[rand_index])
            for i in switch_indexes:
                proton_list[i].color = color.cyan

control_panel.bind('mousedown', neutron_button)

def metastable_button():
    global proton_excess, neutron_excess, metastable_energy, nucleon_number, nucleus_radius,  proton_list, neutron_list
    loc_m = control_panel.mouse.pos
    if abs(loc_m.x-button_box_dict['Metastable State'].pos.x)<=button_box_dict['Metastable State'].length/2 and abs(loc_m.y-button_box_dict['Metastable State'].pos.y)<=button_box_dict['Metastable State'].height/2:
        info_label.text = ''
        scene.autoscale = False
        nucleon_number=99 #for Tc-99m
        nucleus_radius =  nucleon_number**(1/3)*nucleon_radius
        nucleus_sphere.radius = nucleus_radius
        cell.visible = False
        cell_lbl.visible = False
        for p in proton_list:
            p.visible = False
        for n in neutron_list:
            n.visible = False
        proton_list=[]
        neutron_list=[]
        create_nucleus(nucleon_number)
        if finished:
            info_label.text = 'Click reset to restart the simulation'
        elif button_box_dict['Metastable State'].color == vector(0.7,0.7,0.7):
            button_box_dict['Proton Excess'].color = vector(0.7,0.7,0.7)
            button_box_dict['Neutron Excess'].color = vector(0.7,0.7,0.7)
            button_box_dict['Metastable State'].color = color.green
            proton_excess = False
            neutron_excess = False
            metastable_energy = True
            Tc_lbl.visible=True
            F18_lbl.visible=False
            I131_lbl.visible=False
            Xe131_lbl.visible = False
            O18_lbl.visible = False
            for p in proton_list:
                p.color = color.magenta
            for n in neutron_list:
                n.color = color.cyan
        
control_panel.bind('mousedown', metastable_button)

def reset_button():
    global propagating, proton_excess, neutron_excess, metastable_energy, finished
    loc_m = control_panel.mouse.pos
    if abs(loc_m.x-button_box_dict['Reset'].pos.x)<=button_box_dict['Reset'].length/2 and abs(loc_m.y-button_box_dict['Reset'].pos.y)<=button_box_dict['Reset'].height/2:
        button_box_dict['Reset'].color = color.green
        if propagating:
            Run()
        button_box_dict['Proton Excess'].color = vector(0.7,0.7,0.7)
        button_box_dict['Neutron Excess'].color = vector(0.7,0.7,0.7)
        button_box_dict['Metastable State'].color = vector(0.7,0.7,0.7)
        tombstone.visible = False
        cell.visible = False
        proton_excess = False
        neutron_excess = False
        metastable_energy = False
        finished = False
        LOR_arrow1.visible = False
        LOR_arrow2.visible = False
        cell.visible = False
        tombstone.visible = False
        cell_lbl.visible = False
        neutrino_sphere.visible = False
        antineutrino_label.visible = False
        antineutrino_sphere.visible = False
        neutrino_label.visible = False
        info_label.text = ''
        for p in proton_list:
            p.color = color.magenta
        for n in neutron_list:
            n.color = color.cyan
        sleep(0.1)
        button_box_dict['Reset'].color = vector(0.7,0.7,0.7)
        

control_panel.bind('mousedown', reset_button)

# Running Code
scene.select()
while True:
    rate(animation_speed)
    if propagating:
        if proton_excess:
            control_panel.unbind('mousedown', proton_button)
            control_panel.unbind('mousedown', neutron_button)
            control_panel.unbind('mousedown', metastable_button)
            decay_proton = proton_list[0]
            for particle in proton_list:
                if particle.pos.z > decay_proton.pos.z:
                    decay_proton=particle
            #info_label.text = 'Due to an excess of protons, the nucleus becomes unstable as the coulumb potential overtakes the strong force'
            remember_pos=decay_proton.pos
            switch_value = 3
            for i in range(150):
                jiggle_lbl.visible = True
                rate(animation_speed)
                if propagating:
                    decay_proton.pos += switch_value*hat(vector(1,1,1))
                    if i % 3 == 1:
                        switch_value *= -1
            decay_proton.pos = remember_pos
            jiggle_lbl.visible = False
            decay_proton.color = color.cyan
            F18_lbl.visible = False
            O18_lbl.visible = True
            positron_sphere = sphere(pos=remember_pos + nucleon_radius*hat(vector(0,0.5,0.5)), radius=0.4*nucleon_radius, color=color.purple, opacity = 0.3, visible = True)
            positron_label = label(pos=positron_sphere.pos, text='e<sup>+<sup>', height=text_size, color=color.black, box=False, opacity=0)
            neutrino_sphere = sphere(pos=remember_pos + nucleon_radius*hat(vector(0,0.5,0.5)), radius=0.2*nucleon_radius, color=color.red, opacity = 0.3, visible = True)
            neutrino_label = label(pos=neutrino_sphere.pos, text='v', font ='times', height=0.8*text_size, color=color.black, box=False, opacity=0)
            end_pos = vector(nucleus_radius,0,0) + 0.9*nucleon_radius*hat(vector(1,0,0)) #This determines collision point. Want close to nucleus
            choose_plusminus = random()
            if choose_plusminus > 0.5:
                randang=choose_plusminus*pi/2
            else:
                randang=-choose_plusminus*pi/2
            end_pos_n = vector(nucleus_radius,0,0) + nucleon_radius*20*hat(vector(cos(randang),sin(randang),0))
            while find_distance(positron_sphere.pos, end_pos/2) > 2*step_size:
                rate(animation_speed)
                if propagating:
                    travel_vector = hat(end_pos/2 - positron_sphere.pos)
                    positron_sphere.pos += step_size*travel_vector
                    positron_label.pos = positron_sphere.pos
                    travel_vector_n = hat(end_pos_n - neutrino_sphere.pos)
                    neutrino_sphere.pos += step_size*travel_vector_n
                    neutrino_label.pos = neutrino_sphere.pos
            electron_sphere = sphere(pos=end_pos + vector(find_distance(end_pos, positron_sphere.pos),0,0), radius=electron_key.length, color=color.cyan, visible=True, opacity=0.2)
            electron_label = label(pos=electron_sphere.pos, text='e<sup>-<sup>', height=text_size, color=color.black, box=False, opacity=0, visible=True)
            while find_distance(positron_sphere.pos, end_pos) > 2*step_size or find_distance(electron_sphere.pos, end_pos) > 2*step_size:
                rate(animation_speed)
                if propagating:
                    travel_vector_p = hat(end_pos - positron_sphere.pos)
                    travel_vector_e = hat(end_pos - electron_sphere.pos)
                    positron_sphere.pos += step_size*travel_vector_p
                    positron_label.pos = positron_sphere.pos
                    electron_sphere.pos += step_size*travel_vector_e
                    electron_label.pos = electron_sphere.pos
                    neutrino_sphere.pos += 3*step_size*travel_vector_n
                    neutrino_label.pos = neutrino_sphere.pos
            my_click.visible = True
            scene.pause()
            #sleep(0.1)
            my_click.visible = False
            positron_sphere.visible = False
            positron_label.visible = False
            electron_sphere.visible = False
            electron_label.visible = False
            explotion_sphere = sphere(pos=end_pos, radius=0, color=color.orange, visible=True)
            
            while explotion_sphere.radius < nucleon_radius:
                rate(animation_speed)
                if propagating:
                    explotion_sphere.radius += nucleon_radius/10
            while explotion_sphere.radius > 0:
                rate(animation_speed)
                if propagating:
                    if explotion_sphere.radius - nucleon_radius/10 > 0:
                        explotion_sphere.radius -= nucleon_radius/10
                    else:
                        break
            explotion_sphere.visible = False
            info_label.text = 'If both gamma rays are transmitted and detected, they generate \na line of response (arrow) that helps to localize the decay event.'
            gamma_ray_1 = curve(pos=pulse_pos, origin=end_pos, size=0.5*vector(1,1,1), color=color.black)
            gamma_ray_2 = curve(pos=pulse_pos, origin=end_pos, size=0.5*vector(1,1,1), color=color.black)
            for i in range(85):
                rate(animation_speed)
                gamma_ray_1.origin += step_size*hat(vector(0.5,1,0))
                gamma_ray_2.origin += step_size*hat(vector(-0.5,-1,0))
                neutrino_sphere.pos += step_size*travel_vector_n
                neutrino_label.pos = neutrino_sphere.pos
            gamma_ray_1.visible = False
            gamma_ray_2.visible = False
            LOR_arrow1 = arrow(pos = gamma_ray_2.origin, axis = 1.05*(gamma_ray_1.origin - gamma_ray_2.origin), round = True, headlength = 50, headwidth = 30, shaftwidth = 15, color = color.black, opacity=0.1)
            LOR_arrow2 = arrow(pos = gamma_ray_1.origin, axis = -1.05*(gamma_ray_1.origin - gamma_ray_2.origin), round = True, headlength = 50, headwidth = 30, shaftwidth = 15, color = color.black, opacity=0.1)
            sleep(2)
            #info_label.text = ''

            if propagating:
                Run()
            finished = True
            control_panel.bind('mousedown', proton_button)
            control_panel.bind('mousedown', neutron_button)
            control_panel.bind('mousedown', metastable_button)
        
        elif neutron_excess:
            control_panel.unbind('mousedown', proton_button)
            control_panel.unbind('mousedown', neutron_button)
            control_panel.unbind('mousedown', metastable_button)
            note = label(pos=vector(0,-scene.height/2-text_size,0), text='', height=text_size, box=False, opacity=0)
            note.text = 'Beta particles are used to destroy cancerous cells.\nGamma rays are used for imaging.'
            
            cell_nomid1=box(pos=vector(scene.width/2.1,-10,0.3), color=color.white, height = 0.7*320, length = 0.7*512, width = 0.5, opacity= 1, texture='https://medicalimaging.watzekdi.net/images/Nuclear_images/Activity2-Instability/Cancer_cells_crop2_small_nomid.png', visible = False)
            cell_nomid2=box(pos=vector(scene.width/2.1,-10,0.3), color=color.white, height = 0.7*320, length = 0.7*512, width = 0.5, opacity= 1, texture='https://i.natgeofe.com/n/548467d8-c5f1-4551-9f58-6817a8d2c45e/NationalGeographic_2572187_16x9.jpg?w=1200', visible = False)
            cell_nomid3=box(pos=vector(scene.width/2.1,-10,0.3), color=color.white, height = 0.7*320, length = 0.7*512, width = 0.5, opacity= 1, texture='https://images.squarespace-cdn.com/content/66ec3b49803ab81bf84f89e4/1726785641222-1BBJMO12LECPNQ5GWYZ2/image-asset.jpeg?content-type=image%2Fjpeg', visible = False)
            
            cell_nomid_list = [cell, cell, cell_nomid1, cell_nomid2, cell_nomid3]   # List of images to iterate through as target are hit/cells are destroyed
            cell_counter = 1
            for j in range(5):
                decay_neutron = neutron_list[j]
                
                # lightning bolt shifts right to target different cell each iteration 
                lightningbolt = box(pos=vector(scene.width/2.1,0,-110+((cell_counter-1)*110))+vector(0,cell.height/2+0.25*527,0.3), color=color.white, height = 0.5*527, length = 0.5*100, width = 0.5, opacity= 1, texture='https://i.imgur.com/z158BcH.png', visible = False)
                for particle in neutron_list:
                    if particle.pos.z > decay_neutron.pos.z:
                        decay_neutron=particle
                    remember_pos=decay_neutron.pos
                remember_pos=decay_neutron.pos
                switch_value = 3
                for i in range(150):
                    rate(animation_speed)
                    jiggle_lbl.visible = True
                    if propagating:
                        decay_neutron.pos += switch_value*hat(vector(1,1,1))
                        if i % 4 == 1:
                            switch_value *= -1
                decay_neutron.pos = remember_pos
                # sleep(3)  # Unncessery pause?
                jiggle_lbl.visible = False
                info_label.text = ''
                # sleep(0.3)    # Unncessery pause?
                #info_label.text = 'To become more stable, the neutron releases a electron to become a proton'
                decay_neutron.color = color.magenta
                I131_lbl.visible = False
                Xe131_lbl.visible = True
                electron_sphere = sphere(pos=remember_pos + nucleon_radius*hat(vector(0,0.5,0.5)), radius=0.4*nucleon_radius, color=color.cyan, opacity=0.2)
                electron_label = label(pos=electron_sphere.pos, text='e<sup>-<sup>', height=electron_sphere.radius*2.5, color=color.black, box=False, opacity=0)
                antineutrino_sphere = sphere(pos=remember_pos + nucleon_radius*hat(vector(0,0.5,0.5)), radius=0.2*nucleon_radius, color=color.green, opacity = 0.3)
                antineutrino_label = label(pos=antineutrino_sphere.pos, text='v\u0305', font ='times', height=0.8*text_size, color=color.black, box=False, opacity=0)
                #end_pos = vector(nucleus_radius,0,0) + nucleon_radius*5*hat(vector(1,0,0))
                gamma_ray = curve(pos=pulse_pos, origin=vector(nucleus_radius,0,0), size=0.5*vector(1,1,1), color=color.black)
                choose_plusminus = random()
                if choose_plusminus > 0.5:
                    randang=choose_plusminus*pi/2
                else:
                    randang=-choose_plusminus*pi/2
                end_pos_g = vector(nucleus_radius,0,0) + nucleon_radius*20*hat(vector(cos(randang),sin(randang),0))
                
                # Electrons that hit target vs miss in random directions
                end_pos_e_hit = vector(nucleus_radius,0,0) + nucleon_radius*20*hat(vector(1,0,0))
                r = rand.choice([i for i in range(-5,5) if i != 0])
                end_pos_e_miss = vector(nucleus_radius,0,0) + nucleon_radius*20*hat(vector(1,-r,0))
                
                end_pos_e = end_pos_e_miss
                if j % 2 == 0:  # Hits target on even iterations, misses on odd iterations
                    end_pos_e = end_pos_e_hit
                    cell_counter += 1   # Switches to next image in list if the target is hit
                cell_nomid = cell_nomid_list[cell_counter]
                
                choose_plusminus = random()
                if choose_plusminus > 0.5:
                    randang=choose_plusminus*pi/2
                else:
                    randang=-choose_plusminus*pi/2
                end_pos_an = vector(nucleus_radius,0,0) + nucleon_radius*20*hat(vector(cos(randang),sin(randang),0))
                while find_distance(electron_sphere.pos, end_pos_e) > 2*step_size:
                    rate(animation_speed)
                    if propagating:
                        i = 110
                        travel_vector_e = hat(end_pos_e - electron_sphere.pos)
                        travel_vector_an = hat(end_pos_an - antineutrino_sphere.pos)
                        if electron_sphere.pos.x >= 0.9*cell.pos.x:
                            electron_sphere.visible = False
                            electron_label.visible = False
                            if j % 2 == 0:
                                lightningbolt.visible = True
                        electron_sphere.pos += step_size*travel_vector_e
                        electron_label.pos = electron_sphere.pos
                        antineutrino_sphere.pos += step_size*travel_vector_an
                        antineutrino_label.pos = antineutrino_sphere.pos
                        travel_vector_g = hat(end_pos_g - gamma_ray.origin)
                        gamma_ray.origin += step_size*travel_vector_g
            
                # Remove leftover particles from prev. iteration
                antineutrino_sphere.visible = False
                antineutrino_label.visible = False
                gamma_ray.visible = False

                #while electron_sphere.pos.x < scene.width/2 + nucleon_radius:
                #    rate(animation_speed)
                #    if propagating:
                #        electron_sphere.pos += step_size*travel_vector
                 
                cell_nomid_list[cell_counter-1].visible = False # Previous cells disappear as the image updates
                lightningbolt.visible = False
                cell_nomid.visible=True
                sleep(1.5)  # Time for final image with all cells killed to be visible before tombstone appears
                
            cell_nomid.visible = False
            tombstone.visible = True
            if propagating:
                Run()
            finished = True
            control_panel.bind('mousedown', proton_button)
            control_panel.bind('mousedown', neutron_button)
            control_panel.bind('mousedown', metastable_button)

        elif metastable_energy:
            control_panel.unbind('mousedown', proton_button)
            control_panel.unbind('mousedown', neutron_button)
            control_panel.unbind('mousedown', metastable_button)
            #info_label.text = 'Since the nucleus is in a high energy state, it is ustable'
            remember_proton_pos_list = []
            remember_neutron_pos_list = []
            for i in range(len(proton_list)):
                remember_proton_pos_list.append(proton_list[i].pos)
                remember_neutron_pos_list.append(neutron_list[i].pos)
            switch_value = 3
            for i in range(150):
                rate(animation_speed)
                if propagating:
                    jiggle_lbl.visible = True
                    for particle in proton_list+neutron_list:
                        particle.pos += switch_value*hat(vector(1,1,1))
                    nucleus_sphere.pos += switch_value*hat(vector(1,1,1))
                    if i % 4 == 1:
                        switch_value *= -1
            for i in range(len(proton_list)):
                proton_list[i].pos = remember_proton_pos_list[i]
                neutron_list[i].pos = remember_neutron_pos_list[i]
            nucleus_sphere.pos = vector(0,0,0)
            jiggle_lbl.visible = False
            #sleep(1)
            #info_label.text = ''
            #sleep(0.3)
            #info_label.text = 'To become more stable, the nucleus releases a gamma ray lowering its energy'
            gamma_ray = curve(pos=pulse_pos, origin=vector(nucleus_radius,0,0), size=0.5*vector(1,1,1), color=color.black)
            choose_plusminus = random()
            if choose_plusminus > 0.5:
                randang=choose_plusminus*pi/2
            else:
                randang=-choose_plusminus*pi/2
            end_pos = vector(nucleus_radius,0,0) + nucleon_radius*20*hat(vector(cos(randang),sin(randang),0))
            while find_distance(gamma_ray.origin, end_pos) > 2*step_size:
                rate(animation_speed)
                if propagating:
                    travel_vector = hat(end_pos - gamma_ray.origin)
                    gamma_ray.origin += step_size*travel_vector
            #sleep(2)
            info_label.text = 'The emitted gamma ray may escape the body and be detected.'
            while gamma_ray.origin.x < scene.width/2 + nucleon_radius:
                rate(animation_speed)
                if propagating:
                    gamma_ray.origin += step_size*travel_vector
            sleep(3)
            info_label.text = ''
            gamma_ray.visible = False

            if propagating:
                Run()
            finished = True
            control_panel.bind('mousedown', proton_button)
            control_panel.bind('mousedown', neutron_button)
            control_panel.bind('mousedown', metastable_button)
