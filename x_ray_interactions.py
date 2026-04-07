from vpython import *


scene=canvas(width =1024, height=480, center=vector(0,0,0), background=color.white, resizable=False, userzoom=False, userspin=False)
scene.lights=[]
distant_light(direction=vector( 0.22, 0.44, 0.88), color=color.white)
distant_light(direction=vector(-0.88, -0.22, -0.44), color=color.white)
#Moved down 100 affects below
my_bookImage = box(pos=vector(0,-100,0), length=scene.width, height=scene.height, texture="https://i.imgur.com/ipbI9jA.jpeg", shininess=0, visible = False, color=color.white)

#Variables
atoms_loc = scene.width/2
animation_speed=1000
remember_speed = animation_speed
E = 20 #Energy in keV
Z = 7.4 #Starting atomic number
theta = pi/15
text_size=15 
started = False #Set to true when simulation first starts (see Run())
started_atomic = False #Used if user hits switch to target view before simulation done and prints warning (see SwitchView() if and else lines)
propagating = False
running = False
is_atomic = False #Set to true when you switch to mechanistic view (see switchView)
has_run = False #Set to true after a full atomic/mechanistic run. Calls reset_atomic to reset visible stuff if don't change atomic mechanism. Check has_run.
remember_has_run=has_run
PE_dropElectronLoc = vector((-104/1025)*scene.width,(10/513)*scene.height,0)
PE_scatterElectronLoc = vector((-70/1025)*scene.width,(-31/513)*scene.height,0)
compton_electronLoc = vector((-63/1025)*scene.width,(-153/513)*scene.height,0)
pulse_list=[vector(0,34.625,0),vector(0.125,34.625,0),vector(0.25,34.5,0),vector(0.375,34.375,0),vector(0.5,34.25,0),vector(0.625,34.125,0),vector(0.75,34,0),vector(0.875,33.75,0),vector(1,33.625,0),vector(1.125,33.25,0),vector(1.25,33.125,0),vector(1.375,32.875,0),vector(1.5,32.75,0),vector(1.625,32.625,0),vector(1.75,32.5,0),vector(1.875,32.375,0),vector(2,32.375,0),vector(2.125,32.25,0),vector(2.25,32.375,0),vector(2.375,32.375,0),vector(2.5,32.5,0),vector(2.625,32.625,0),vector(2.75,32.75,0),vector(2.875,32.875,0),vector(3,33,0),vector(3.125,33.25,0),vector(3.25,33.625,0),vector(3.375,34,0),vector(3.5,34.375,0),vector(3.625,35,0),vector(3.75,35.5,0),vector(3.875,35.875,0),vector(4,36.375,0),vector(4.125,36.875,0),vector(4.25,37.125,0),vector(4.375,37.5,0),vector(4.5,37.875,0),vector(4.625,38.25,0),vector(4.75,38.5,0),vector(4.875,38.75,0),vector(5,38.875,0),vector(5.125,39,0),vector(5.25,39.125,0),vector(5.375,39.25,0),vector(5.5,39.375,0),vector(5.625,39.375,0),vector(5.75,39.5,0),vector(5.875,39.5,0),vector(6,39.5,0),vector(6.125,39.5,0),vector(6.25,39.375,0),vector(6.375,39.375,0),vector(6.5,39.25,0),vector(6.625,39.125,0),vector(6.75,39,0),vector(6.875,38.875,0),vector(7,38.75,0),vector(7.125,38.5,0),vector(7.25,38.125,0),vector(7.375,37.875,0),vector(7.5,37.625,0),vector(7.625,37.125,0),vector(7.75,36.625,0),vector(7.875,36.125,0),vector(8,35.625,0),vector(8.125,34.75,0),vector(8.25,34,0),vector(8.375,32.875,0),vector(8.5,31.75,0),vector(8.625,30.5,0),vector(8.75,29.25,0),vector(8.875,28.25,0),vector(9,27.375,0),vector(9.125,26.25,0),vector(9.25,25.375,0),vector(9.375,24.625,0),vector(9.5,23.875,0),vector(9.625,23.25,0),vector(9.75,22.625,0),vector(9.875,22.25,0),vector(10,21.875,0),vector(10.125,21.5,0),vector(10.25,21.375,0),vector(10.375,21.25,0),vector(10.5,21.25,0),vector(10.625,21.25,0),vector(10.75,21.25,0),vector(10.875,21.375,0),vector(11,21.625,0),vector(11.125,21.875,0),vector(11.25,22.5,0),vector(11.375,22.875,0),vector(11.5,23.375,0),vector(11.625,24.125,0),vector(11.75,24.875,0),vector(11.875,25.75,0),vector(12,26.5,0),vector(12.125,27.625,0),vector(12.25,28.75,0),vector(12.375,29.75,0),vector(12.5,30.75,0),vector(12.625,32.25,0),vector(12.75,33.75,0),vector(12.875,35,0),vector(13,36.25,0),vector(13.125,37.75,0),vector(13.25,39,0),vector(13.375,40,0),vector(13.5,41,0),vector(13.625,42.25,0),vector(13.75,43.25,0),vector(13.875,44,0),vector(14,44.75,0),vector(14.125,45.625,0),vector(14.25,46.25,0),vector(14.375,46.75,0),vector(14.5,47.125,0),vector(14.625,47.625,0),vector(14.75,47.875,0),vector(14.875,48,0),vector(15,48.125,0),vector(15.125,48.25,0),vector(15.25,48.125,0),vector(15.375,48,0),vector(15.5,47.875,0),vector(15.625,47.75,0),vector(15.75,47.375,0),vector(15.875,47,0),vector(16,46.625,0),vector(16.125,45.875,0),vector(16.25,45.25,0),vector(16.375,44.5,0),vector(16.5,43.75,0),vector(16.625,42.75,0),vector(16.75,41.75,0),vector(16.875,40.75,0),vector(17,39.625,0),vector(17.125,38,0),vector(17.25,35.875,0),vector(17.375,34.375,0),vector(17.5,32.625,0),vector(17.625,29.5,0),vector(17.75,26.625,0),vector(17.875,24.25,0),vector(18,21.75,0),vector(18.125,18.5,0),vector(18.25,15.875,0),vector(18.375,14,0),vector(18.5,12,0),vector(18.625,9.75,0),vector(18.75,8,0),vector(18.875,6.625,0),vector(19,5.375,0),vector(19.125,4,0),vector(19.25,2.875,0),vector(19.375,2.5,0),vector(19.5,2,0),vector(19.625,1.375,0),vector(19.75,1.25,0),vector(19.875,1.25,0),vector(20,1.625,0),vector(20.125,2.125,0),vector(20.25,2.75,0),vector(20.375,3.5,0),vector(20.5,4.375,0),vector(20.625,5.75,0),vector(20.75,7.375,0),vector(20.875,8.875,0),vector(21,10.375,0),vector(21.125,12.625,0),vector(21.25,15,0),vector(21.375,17.125,0),vector(21.5,19.5,0),vector(21.625,22.625,0),vector(21.75,25.875,0),vector(21.875,28.75,0),vector(22,32.125,0),vector(22.125,36.5,0),vector(22.25,40.5,0),vector(22.375,44.125,0),vector(22.5,48,0),vector(22.625,52.25,0),vector(22.75,56,0),vector(22.875,58.875,0),vector(23,61.75,0),vector(23.125,64.875,0),vector(23.25,67.5,0),vector(23.375,69.375,0),vector(23.5,71.375,0),vector(23.625,73.375,0),vector(23.75,75,0),vector(23.875,76.125,0),vector(24,76.875,0),vector(24.125,77.75,0),vector(24.25,78.125,0),vector(24.375,78.25,0),vector(24.5,78.125,0),vector(24.625,77.75,0),vector(24.75,76.875,0),vector(24.875,76.125,0),vector(25,75,0),vector(25.125,73.375,0),vector(25.25,71.375,0),vector(25.375,69.375,0),vector(25.5,67.5,0),vector(25.625,64.875,0),vector(25.75,61.75,0),vector(25.875,58.875,0),vector(26,56,0),vector(26.125,52.25,0),vector(26.25,48,0),vector(26.375,44.125,0),vector(26.5,40.5,0),vector(26.625,36.5,0),vector(26.75,32.125,0),vector(26.875,28.75,0),vector(27,25.875,0),vector(27.125,22.625,0),vector(27.25,19.5,0),vector(27.375,17.125,0),vector(27.5,15,0),vector(27.625,12.625,0),vector(27.75,10.375,0),vector(27.875,8.875,0),vector(28,7.375,0),vector(28.125,5.75,0),vector(28.25,4.375,0),vector(28.375,3.5,0),vector(28.5,2.75,0),vector(28.625,2.125,0),vector(28.75,1.625,0),vector(28.875,1.25,0),vector(29,1.25,0),vector(29.125,1.375,0),vector(29.25,2,0),vector(29.375,2.5,0),vector(29.5,2.875,0),vector(29.625,4,0),vector(29.75,5.375,0),vector(29.875,6.625,0),vector(30,8,0),vector(30.125,9.75,0),vector(30.25,12,0),vector(30.375,14,0),vector(30.5,15.875,0),vector(30.625,18.5,0),vector(30.75,21.75,0),vector(30.875,24.25,0),vector(31,26.625,0),vector(31.125,29.5,0),vector(31.25,32.625,0),vector(31.375,34.375,0),vector(31.5,35.875,0),vector(31.625,38,0),vector(31.75,39.625,0),vector(31.875,40.75,0),vector(32,41.75,0),vector(32.125,42.75,0),vector(32.25,43.75,0),vector(32.375,44.5,0),vector(32.5,45.25,0),vector(32.625,45.875,0),vector(32.75,46.625,0),vector(32.875,47,0),vector(33,47.375,0),vector(33.125,47.75,0),vector(33.25,47.875,0),vector(33.375,48,0),vector(33.5,48.125,0),vector(33.625,48.25,0),vector(33.75,48.125,0),vector(33.875,48,0),vector(34,47.875,0),vector(34.125,47.625,0),vector(34.25,47.125,0),vector(34.375,46.75,0),vector(34.5,46.25,0),vector(34.625,45.625,0),vector(34.75,44.75,0),vector(34.875,44,0),vector(35,43.25,0),vector(35.125,42.25,0),vector(35.25,41,0),vector(35.375,40,0),vector(35.5,39,0),vector(35.625,37.75,0),vector(35.75,36.25,0),vector(35.875,35,0),vector(36,33.75,0),vector(36.125,32.25,0),vector(36.25,30.75,0),vector(36.375,29.75,0),vector(36.5,28.75,0),vector(36.625,27.625,0),vector(36.75,26.5,0),vector(36.875,25.75,0),vector(37,24.875,0),vector(37.125,24.125,0),vector(37.25,23.375,0),vector(37.375,22.875,0),vector(37.5,22.5,0),vector(37.625,21.875,0),vector(37.75,21.625,0),vector(37.875,21.375,0),vector(38,21.25,0),vector(38.125,21.25,0),vector(38.25,21.25,0),vector(38.375,21.25,0),vector(38.5,21.375,0),vector(38.625,21.5,0),vector(38.75,21.875,0),vector(38.875,22.25,0),vector(39,22.625,0),vector(39.125,23.25,0),vector(39.25,23.875,0),vector(39.375,24.625,0),vector(39.5,25.375,0),vector(39.625,26.25,0),vector(39.75,27.375,0),vector(39.875,28.25,0),vector(40,29.25,0),vector(40.125,30.5,0),vector(40.25,31.75,0),vector(40.375,32.875,0),vector(40.5,34,0),vector(40.625,34.75,0),vector(40.75,35.625,0),vector(40.875,36.125,0),vector(41,36.625,0),vector(41.125,37.125,0),vector(41.25,37.625,0),vector(41.375,37.875,0),vector(41.5,38.125,0),vector(41.625,38.5,0),vector(41.75,38.75,0),vector(41.875,38.875,0),vector(42,39,0),vector(42.125,39.125,0),vector(42.25,39.25,0),vector(42.375,39.375,0),vector(42.5,39.375,0),vector(42.625,39.5,0),vector(42.75,39.5,0),vector(42.875,39.5,0),vector(43,39.5,0),vector(43.125,39.375,0),vector(43.25,39.375,0),vector(43.375,39.25,0),vector(43.5,39.125,0),vector(43.625,39,0),vector(43.75,38.875,0),vector(43.875,38.75,0),vector(44,38.5,0),vector(44.125,38.25,0),vector(44.25,37.875,0),vector(44.375,37.5,0),vector(44.5,37.125,0),vector(44.625,36.875,0),vector(44.75,36.375,0),vector(44.875,35.875,0),vector(45,35.5,0),vector(45.125,35,0),vector(45.25,34.375,0),vector(45.375,34,0),vector(45.5,33.625,0),vector(45.625,33.25,0),vector(45.75,33,0),vector(45.875,32.875,0),vector(46,32.75,0),vector(46.125,32.625,0),vector(46.25,32.5,0),vector(46.375,32.375,0),vector(46.5,32.375,0),vector(46.625,32.25,0),vector(46.75,32.375,0),vector(46.875,32.375,0),vector(47,32.5,0),vector(47.125,32.625,0),vector(47.25,32.75,0),vector(47.375,32.875,0),vector(47.5,33.125,0),vector(47.625,33.25,0),vector(47.75,33.625,0),vector(47.875,33.75,0),vector(48,34,0),vector(48.125,34.125,0),vector(48.25,34.25,0),vector(48.375,34.375,0),vector(48.5,34.5,0),vector(48.625,34.625,0),vector(48.75,34.625,0)]
#test_photon=curve(pos=pulse_list, color=vec(0,0.5,0), radius=1, canvas=scene, origin=vector(-110,-40,0))
message_list = []
num_PE=0
num_CS=0
N=0
num_trans=0
my_element_changed=False
remember_m_index=0

#Objects
lbl_start1=label(pos=vector(0, scene.height/2,0), text="Click for mechanistic view!", font="helvetica", box=True, canvas=scene, color=vec(0.000, 0.360, 0.390), height=text_size, visible=True, opacity=0)
lbl_start2=label(pos=vector(0, scene.height/2,0), text="Return to target view!", font="helvetica", box=True, canvas=scene, color=vec(0.000, 0.360, 0.390), height=text_size, visible=False, opacity=0)
medium_box = box(pos=vector(atoms_loc/2,-2.5*text_size,0), height=scene.height/1.5, width=scene.width/10, length=scene.width/30, color=color.black, opacity=0.25, visible=False)
medium_label = text(pos=medium_box.pos + vector(-20,(medium_box.height/2.3),-50), text='Sample', font="sans", box=False, canvas=scene, axis=vector(5,0.1,10), color=vec(0.622, 0.779, 0.847), height=1.5*text_size, visible=False)
#BAS Source is a curve and box is invisible
my_CS_atomic= box(pos=vector(0,-2*text_size,0), height=scene.width/2, length=scene.width/2, width=1, texture="https://i.imgur.com/dpjuhGV.png", color=color.white, opacity=1, visible=False)
my_PE_atomic= box(pos=vector(0,-2*text_size,0), height=scene.width/2, length=scene.width/2, width=1, texture="https://i.imgur.com/Pc2apHh.png", color=color.white, opacity=1, visible=False)
my_trans_atomic= box(pos=vector(0,-2*text_size,0), height=scene.width/2, length=scene.width/2, width=1, texture="https://i.imgur.com/rhxqQqy.png", color=color.white, opacity=1, visible=False)
my_mech_atomic_list=[my_PE_atomic, my_CS_atomic, my_trans_atomic]
probability_list=[vector(350,-50,0), vector(750,-50,0), vector(750,50,0), vector(350,50,0), vector(350,-50,0)]
probability_box = curve(pos=probability_list, color=color.black, radius=2, visible=True, origin=vector(0,-50,0))
xray_source_list=[3*vector(-atoms_loc-180,0,0), 3*vector(-atoms_loc-190,0,0), 3*vector(-atoms_loc-190,-5,0), 3*vector(-atoms_loc-220,-5,0), 3*vector(-atoms_loc-220,10,0), 3*vector(-atoms_loc-190,10,0), 3*vector(-atoms_loc-190,5,0), 3*vector(-atoms_loc-180,5,0), 3*vector(-atoms_loc-180,0,0)] 
xray_source_new=curve(pos=xray_source_list, radius=2, color=color.black, origin=vector(1530,-50,0))
xray_source = box(pos=vector(-atoms_loc,0,0), height=scene.height/30, width=3*scene.width/50, length=scene.width/50, color=color.black, opacity=0)
xray_label = label(pos=xray_source.pos + vector(-100,xray_source.height,0), text='X-ray Source', font="helvetica", box=False, canvas=scene, color=color.black, height=text_size, opacity=0)
detector_box = box(pos=vector(medium_box.pos.x + medium_box.length + scene.width/2,0,0), height=scene.height, width=scene.width/5, length=1, color=vector(0.5,0.5,0.5), opacity=0.2, visible=False)
detector_label = text(pos=detector_box.pos+vector(0,detector_box.height/2.5,-50), text='Detector', font="sans", box=False, canvas=scene, axis=vector(0.5,0.1,5), color=vec(0.622, 0.779, 0.847), height=1.5*text_size, visible=False)
atomic_viewBox = box(pos=vector(0, scene.height/2,0), length=0.6*scene.width/4, height=0.6*scene.width/4, width=1, texture="https://webdev2.watzek.cloud/~nddill/scanningSims/images/projection_Radiography/PEmech_icon_small.png", opacity=1, shininess = 0, color=color.white, visible=False)
atomic_view_lbl = label(pos=atomic_viewBox.pos + vector(0,(atomic_viewBox.height/2-7*text_size),0), text='Atomic View', font="helvetica", box=False, canvas=scene, color=vector(0,0,0.8), height=text_size, opacity=0, visible=False)
PE_scatterElectron = sphere(pos=PE_scatterElectronLoc, radius=8, color=color.cyan, visible=False)
PE_dropElectron = sphere(pos=PE_dropElectronLoc, radius=8, color=color.magenta, visible=False)
atomic_label = label(pos=vector(0,(-scene.height/2) + text_size,0), text='Both the scattered electron and emited x-ray are absorbed by the medium', font="helvetica", box=False, canvas=scene, color=color.black, height=text_size, opacity=0, visible=False)
my_mech_lbl= label(pos=vector(-50,0,0), text="CHOOSE A MECHANISM FROM THE CONTROL PANEL\n FOLLOWED BY PLAY/PAUSE!", color=vector(0,0.36,0.39), box=False, opacity=0, visible=False)
my_error_lbl = label(pos=vector(-50,0,0), text="ERROR: CHOOSE A MECHANISM FROM THE CONTROL PANEL\n FOLLOWED BY PLAY/PAUSE!", color=vector(0,0.36,0.39), box=False, opacity=0, visible=False)
my_error2_lbl =label(pos=vector(-50,0,10), text="ERROR: SWITCH TO MECHANISTIC VIEW FIRST!", color=vector(0,0.36,0.39), box=False, opacity=0, visible=False)
my_secondary_abs_lbl = label(pos=vector(scene.width*(300/1024),100,0), text="💥", color=vector(0,0.36,0.39), box=False, opacity=0, height=3*text_size, visible=False)
my_secondary_abs_lbl2 = label(pos=vector(scene.width*(300/1024),100-4*text_size,0), text="Absorbed quickly!", color=vector(0,0.36,0.39), box=False, opacity=0, visible=False)
compton_electron = sphere(pos=compton_electronLoc, radius=8, color=color.cyan, visible=False)
my_electrons_list=[PE_scatterElectron, PE_dropElectron, compton_electron]
water = box(pos=vector(0,-2*text_size,0), length=scene.width/4, height=1596/1224*scene.width/4, width=1, texture="https://i.imgur.com/QZSxqxP.png", shininess=0, visible = True, color=color.white)
bone = box(pos=vector(0,-2*text_size,0), length=scene.width/4, height=scene.width/4, width=1, texture="https://i.imgur.com/yAuZARI.png", shininess=0, visible = False, color=color.white)
lead =  box(pos=vector(0,-2*text_size,0), length=scene.width/4, height=scene.width/4, width=1, texture="https://i.imgur.com/DkWsBWv.png", shininess=0, visible = False, color=color.white)
my_targets_list=[water,bone,lead]
my_water_lbl=label(pos=vector(0,water.height/2-text_size,0), text='<b>WATER<b>', box = False, opacity=0, color=vec(0,0.6,0.8), visible=True)
my_bone_lbl=label(pos=vector(0,water.height/2-text_size,0), text='<b>BONE<b>', box = False, opacity=0, color=vector(0.6,0.6,0.6), visible=False)
my_lead_lbl=label(pos=vector(0,water.height/2-text_size,0), text='<b>LEAD<b>', box = False, opacity=0, color=vector(0.3,0.3,0.3), visible=False)
my_prob_lbl = label(pos=vector(550, xray_label.pos.y+2*text_size,0), text="<b>NUMBER OF EVENTS<b>", color=vector(0,0.5,0.5), box=False, opacity=0)
my_PEtot_lbl = label(pos=vector(probability_list[0].x+62, my_prob_lbl.pos.y-2*text_size,0), text="<b>Photoelectric<b>", color=vector(0,0.5,0.5), height=0.85*text_size, box=False, opacity=0)
pe_tot_lbl = label(pos=vector(probability_list[0].x+62, my_prob_lbl.pos.y-6.5*text_size,0), color=vector(0,0.5,0.5), height = 1.5*text_size, box=False, opacity=0)
my_TRtot_lbl = label(pos=vector(probability_list[1].x-62, my_prob_lbl.pos.y-2*text_size,0), text="<b>Transmission<b>", height=0.85*text_size, color=vector(0,0.5,0.5), box=False, opacity=0)
tr_tot_lbl = label(pos=vector(probability_list[1].x-62, my_prob_lbl.pos.y-6.5*text_size,0), color=vector(0,0.5,0.5), height = 1.5*text_size, box=False, opacity=0)
my_CStot_lbl = label(pos=vector((probability_list[0].x+probability_list[1].x)/2,my_prob_lbl.pos.y-2*text_size,0), text="<b>Compton<b>", height=0.85*text_size, color=vector(0,0.5,0.5), box=False, opacity=0)
cs_tot_lbl = label(pos=vector((probability_list[0].x+probability_list[1].x)/2, my_prob_lbl.pos.y-6.5*text_size,0), color=vector(0,0.5,0.5), height = 1.5*text_size, box=False, opacity=0)
element_names_list = [my_water_lbl,my_bone_lbl,my_lead_lbl]
pe_schem = box(pos=vector(0,0,0), length=scene.width/2, height=scene.width/2, width=0.5, texture="https://webdev2.watzek.cloud/~nddill/scanningSims/images/projection_Radiography/PE.png", shininess=0, visible = False)
cs_schem = box(pos=vector(0,0,0), length=scene.width/2, height=scene.width/2, width=0.5, texture="https://webdev2.watzek.cloud/~nddill/scanningSims/images/projection_Radiography/Compton.png", shininess=0, visible = False, color=color.white)
trans_schem = box(pos=vector(0,0,0), length=scene.width/2, height=scene.width/2, width=0.5, texture="https://webdev2.watzek.cloud/~nddill/scanningSims/images/projection_Radiography/Atom.png", shininess=0, visible = False, color=color.white)
current_element = water
current_lbl=my_water_lbl
my_PE_label=label(pos=vector(0,-230,0), text="Photoelectric event!", box=False, color=vector(0,0.3,0.3), height=text_size, opacity=0, visible=False)
my_CS_label=label(pos=vector(0,-230,0), text="Compton scattering event!", box=False, color=vector(0,0.3,0.3), height=text_size, opacity=0, visible=False)
my_TR_label=label(pos=vector(0,-230,0), text="Transmission!", box=False, color=vector(0,0.3,0.3), height=text_size, opacity=0, visible=False)
my_mech_lbl_list=[my_PE_label, my_CS_label,my_TR_label]
my_target_lbl_list=[my_water_lbl,my_bone_lbl,my_lead_lbl]
#scaling_sphere = sphere(pos=vector(atoms_loc,0,0), radius=5, opacity=0)

#Rescaling original pulse and changing start point on y
for i in range(len(pulse_list)):
    #pulse_list[i] = pulse_list[i]/2 # Rescaling original pulse
    pulse_list[i].y -= scene.width*(70/1024) # changing start point on y, X-ray needs to head directly toward scattered electon in PE
    pulse_list[i].x -= scene.width*(110/1024)
    pulse_list[i].z += 2
    
#Create Title
scaling_sphere1=sphere(pos=vector(0,-300,0), opacity=0)
scaling_sphere2=sphere(pos=vector(0,-1*atomic_label.pos.y+7*text_size,0), opacity=0)
title = label(pos=vector(0,-1*atomic_label.pos.y+8*text_size,0), text='Explore Interactions Between Diagnostic X-rays and Matter', font='helvetica', height=1.5*text_size, box=False, visible=True, color=color.black, opacity=0)
lbl_start=label(pos=vector(0,-330,0), text="Start with Activities (link at top)!", font="helvetica", box=True, canvas=scene, color=vector(0,0.36,0.39), height=15, visible=True, opacity=0)

# Hyperlinks 
s = '''<font size=4> <font>'''
l= '''<font size=4> <font>'''
q = '''<font size=4> <font>'''
v = '''<font size=4> <font>'''
def link1(url, d):
    global s
    s += "<a href='https://webdev2.watzek.cloud/~nddill/scanningSims/images/projection_Radiography/%20Information-Interactions.png" + "' target='_blank'>" + url + "</a>"
    s += d
def link2(url, d):
    global l
    l += "<a href='https://i.imgur.com/xhjl1AH.png" + "' target='_blank'>" + url + "</a>"
    l += d
def link3(url, d):
    global q
    q += "<a href='https://i.imgur.com/HroYa7s.png" + "' target='_blank'>" + url + "</a>"
    q += d
def link4(url, d):
    global v
    v += "<a href='https://webdev2.watzek.cloud/~nddill/scanningSims/images/projection_Radiography/%20Information-Interactions.png" + "' target='_blank'>" + url + "</a>"
    v += d
    
link4("Information", "&nbsp &nbsp &nbsp")
#scene.append_to_title(v)
link3("Background", "&nbsp &nbsp &nbsp")
scene.append_to_title(q)
link2("Activities", "&nbsp &nbsp &nbsp")
scene.append_to_title(l)

# Functions

def event_type_print(type):
    global event_type, num_CS, num_trans, num_PE, N
    event_type=type
    if event_type==1:
        my_PE_label.visible=True
        num_PE=num_PE+1
    if event_type==2:
        my_CS_label.visible=True
        num_CS=num_CS+1
    if event_type==3:
        my_TR_label.visible=True
        num_trans=num_trans+1
    N=num_PE+num_CS+num_trans
   
    
def caption_print(text): 
    global message_list
    if len(message_list) < 10:
        control_panel.append_to_caption(text)
        message_list.append(text)
    else:
        control_panel.caption=''
        for i in range(len(message_list)-1):
            message_list[i] = message_list[i+1]
        message_list[9] = text
        for i in message_list:
            control_panel.append_to_caption(i)   

def create_photon(loc): #Fix photons not all starting at source
    new_photon=curve(pos=pulse_list, color=vec(0,0.5,0), radius=1, canvas=scene, origin=loc)
    return new_photon
    
def move_objects(objects, directions, ends, speed=3): #objects is a list (e.g., x_ray or x_ray and sphere)
    travel_vector = vector(1,0,0)
    remember_view = is_atomic 
    number_done = 0
    while number_done < len(objects):
        rate(animation_speed)
        if is_atomic != remember_view:
            break
        if propagating:
            for i in range(len(objects)):
                if isinstance(objects[i], sphere): #checks an electron
                    if objects[i].pos.x <= ends[i].x:
                        objects[i].pos += speed*hat(directions[i]) #hat() function gives unit vector along the direction of the vector argument 
                        objects[i].opacity -=(i+1)*0.003
                        if objects[i].pos.x >= ends[i].x:
                            number_done += 1
                elif isinstance(objects[i], curve): #checks a photon
                    if objects[i].origin.x <= ends[i].x:
                        objects[i].origin += speed*hat(directions[i])
                        if objects[i].origin.x >= ends[i].x:
                            number_done += 1
    
def interaction(photon, in_vector):
    global PE, CS, TR
    rand = random()
    probComp = 0.25 #see 32186.pdf
    if Z==7.4: #from text page 217, check how mu's depend on energy to get rand (transmission) right
        if E==20:
            if rand>=0.9: # for mu=0.78 x=3 cm page 240 of text > 10% transmission
                event_type_print(3)
                return in_vector  
            elif rand>=0.585:#probPE=0.65 .9*0.65=0.585 
                event_type_print(2)
                return (hat(vector(sqrt(2)/2 + random()*(1-sqrt(2)/2), -sqrt(2)/2 + random()*(sqrt(2)), 0)))
            else: 
                event_type_print(1)
                photon.visible = False
                return vector(1,0,0)            
        if E==60:
            if rand>=0.45: #see text page 240 for different mu's > 55% at 60 KeV
                event_type_print(3)
                return in_vector  
            elif rand>=0.0315: #probPE=0.07
                event_type_print(2)
                return (hat(vector(sqrt(2)/2 + random()*(1-sqrt(2)/2), -sqrt(2)/2 + random()*(sqrt(2)), 0)))
            else:
                event_type_print(1)
                photon.visible = False
                return vector(1,0,0)
        if E==100:
            if rand>=0.39: #mu=0.167 (61% trans) from https://www.nuclear-power.com/nuclear-power/reactor-physics/atomic-nuclear-physics/radiation/x-rays-roentgen-radiation/linear-and-mass-attenuation-coefficient-x-rays/
                event_type_print(3)
                return in_vector  
            elif rand>=0.008: #0.39*0.02  probPE=0.02
                event_type_print(2)
                return (hat(vector(sqrt(2)/2 + random()*(1-sqrt(2)/2), -sqrt(2)/2 + random()*(sqrt(2)), 0)))
            else:
                event_type_print(1)
                photon.visible = False
                return vector(1,0,0)          
    if Z==13.8: 
        if E==20:
            if rand>=1.0: # for mu=4.8 x=3 cm page 240 of text > no transmission
                event_type_print(3)
                return in_vector  
            elif rand>=0.89: #probPE=0.89 #from text page 217
                event_type_print(2)
                return (hat(vector(sqrt(2)/2 + random()*(1-sqrt(2)/2), -sqrt(2)/2 + random()*(sqrt(2)), 0)))
            else: 
                event_type_print(1)
                photon.visible = False
                return vector(1,0,0) 
        if E==60:# for mu=0.55 x=3 cm page 240 of text > 19% transmission
            if rand>=0.81: # for mu=4.8 x=3 cm page 240 of text > no transmission
                event_type_print(3)
                return in_vector  
            elif rand>=0.25: #0.81*(probPE=0.31) #from text page 217
                event_type_print(2)
                return (hat(vector(sqrt(2)/2 + random()*(1-sqrt(2)/2), -sqrt(2)/2 + random()*(sqrt(2)), 0)))
            else: 
                event_type_print(1)
                photon.visible = False
                return vector(1,0,0)
        if E==100:
            if rand>=0.64: #for mu=0.34 x=3 cm from Calculated-linear-attenuation-coefficients-cm-1-for-biodegradable-implant-materials.png
                event_type_print(3)
                return in_vector  
            elif rand>=0.06: #0.64*0.09  probPE=0.09
                event_type_print(2)
                return (hat(vector(sqrt(2)/2 + random()*(1-sqrt(2)/2), -sqrt(2)/2 + random()*(sqrt(2)), 0)))
            else:
                event_type_print(1)
                photon.visible = False
                return vector(1,0,0)
    if Z==82: 
        probPE=1.00 #Nearly all PE for iodine Z=49.8 (88% at 100 KeV) so lead is basicallly all PE (82/49.8)^3 > 4
        event_type_print(1)
        photon.visible = False
        return vector(1,0,0)

def resetAtomic():
    global has_run, started, PE_scatteredElectron, PE_dropElectron, compton_electron
    PE_scatterElectron.pos = PE_scatterElectronLoc
    PE_dropElectron.pos = PE_dropElectronLoc
    compton_electron.pos = compton_electronLoc
    PE_scatterElectron.opacity = 1
    PE_dropElectron.opacity = 1
    if has_run:
        for i in range(0,3):
            my_electrons_list[i].visible=False
        for i in range(1,4):
            if button_box_list[i].color==vector(0.7,0.7,0.7):
                my_mech_atomic_list[i-1].visible=False
        for i in range(1,4):
            if button_box_list[i].color==color.green and i==1:
                    my_electrons_list[i-1].visible=True
                    my_electrons_list[i].visible=True
            elif button_box_list[i].color==color.green and i==2:
                my_electrons_list[i].visible=True
                my_electrons_list[i].opacity=1
    has_run = False
    started = False
    #animation_speed=1000

def switchView():
    global is_atomic, running, propagating, started, has_run, my_evt, num_PE, num_CS, num_trans, my_mech_lbl
    loc_b=scene.mouse.pos
    if abs(loc_b.x-lbl_start1.pos.x)<=100 and abs(loc_b.y-lbl_start1.pos.y)<=text_size:
        if not started_atomic:
            is_atomic = not is_atomic
            my_error2_lbl.visible=False
            button_box_list[0].color = vector(0.7,0.7,0.7)
            if started:
                xray.visible=False
            if is_atomic:
                for i in range(0,3):
                    my_target_lbl_list[i].visible=False
                current_element.visible=False
                bg_menu.disabled=True
                E_slider.disabled=True
                control_panel.bind("mousedown", pe_but)
                control_panel.bind("mousedown", cs_but)
                control_panel.bind("mousedown", trans_but)
                atomic_viewBox.visible=False
                lbl_start1.visible=False
                my_mech_lbl.visible=True
                my_evt=control_panel.waitfor('mousedown') #wait until mouse event chooses mechanism. Specify canvas.
                caption_print("Switched to mechanistic view\n")
                control_panel.bind("mousedown", Run)
                medium_box.visible = False
                medium_label.visible = False
                detector_box.visible = False
                detector_label.visible = False
                lbl_start2.visible=True        
                probability_box.visible=False
                my_water_lbl.visible=False
                my_bone_lbl.visible=False
                my_lead_lbl.visible=False
                my_prob_lbl.visible=False
                my_PEtot_lbl.visible=False
                my_TRtot_lbl.visible=False
                my_CStot_lbl.visible=False
            else:
                caption_print("Switched to target view\n")
                E_slider.disabled=False
                bg_menu.disabled=False
                animation_speed=1000
                for i in range(0,3):
                    my_mech_atomic_list[i].visible=False
                    my_mech_lbl_list[i].visible=False
                    if i==remember_m_index:
                        my_targets_list[i].visible=True                      
                my_mech_atomic_list[i-1].visible=False
                for i in range(1,4):
                    button_box_list[i].color=vector(0.7,0.7,0.7)
                num_PE=0
                num_CS=0
                num_trans=0
                control_panel.bind("mousedown", Run)
                control_panel.unbind("mousedown", pe_but)
                control_panel.unbind("mousedown", cs_but)
                control_panel.unbind("mousedown", trans_but)
                lbl_start2.visible=False
                lbl_start1.visible=True
                my_mech_lbl.visible=False
                PE_scatterElectron.visible = False
                PE_dropElectron.visible = False
                atomic_label.visible = False
                compton_electron.visible = False
                atomic_label.visible = False
                probability_box.visible=True
                my_prob_lbl.visible=True
                my_PEtot_lbl.visible=True
                my_TRtot_lbl.visible=True
                my_CStot_lbl.visible=True
            sleep(1/(2*animation_speed))
            started = False
            running = False
            propagating = False
        else:
            caption_print("Wait until the animation is over to switch views\n")

scene.bind("mousedown", switchView)

def adjust_E(s):
    global E, num_CS, num_PE, num_trans
    E=s.value #E is slider value
    E_caption.text="<font size=4> E = <font>"+ str(E) + "keV"
    num_PE=0
    num_CS=0
    num_trans=0
    pe_tot_lbl.visible=False
    cs_tot_lbl.visible=False
    tr_tot_lbl.visible=False  
E_slider = slider(bind=adjust_E, min=20, max=100, step=40, value=E, length=200, width=10) #Set these so could use PE percentages from page 217 of text (Table 11.1)
E_caption = wtext(text="<font size=4> E<font> =<font>"+ str(E) + "keV   ")
#Create element menu

# Menu from Lane
def change_element(m):
    global current_element, Z, current_lbl, num_CS, num_PE, num_trans, my_element_changed, remember_m_index
    my_element_changed = not my_element_changed
    scene.autoscale = False
    current_element.visible=False
    current_lbl.visible=False 
    current_element=menu_elements[m.index]
    remember_m_index=m.index
    #print('m.index=', remember_m_index)
    current_lbl= element_names_list[m.index]
    Z = float(menu_text[m.index]) #Use this to calculate probabilities in interaction()
    current_element.visible=True
    current_lbl.visible=True
    num_PE=0
    num_CS=0
    num_trans=0
    N=0
    pe_tot_lbl.visible=False
    cs_tot_lbl.visible=False
    tr_tot_lbl.visible=False
    my_element_changed=True
wtext(text="               <font size=4>Atomic Number (Z) = <font>")
menu_text = ["7.4","13.8","82"]  #Center numbers better
menu_elements = [ water, bone, lead ]
bg_menu = menu(bind=change_element, choices = menu_text)


def adjust_speed(s):
    global animation_speed #animation_speed is slider value
    animation_speed = s.value
    speed_caption.text="<font size=4> Speed<font> =<font>"+ str(animation_speed)
wtext(text="                 ")
speed_slider = slider(bind=adjust_speed, min=500, max=2000, step=100, value=animation_speed, length=200, width=10)
speed_caption = wtext(text="<font size=4> Speed<font> =<font>"+ str(animation_speed))

    
#-------------------------------New canvas with control panel ---------------------------------------------------------------------------------------------------------------------------------------------------
control_panel=canvas(width =1024, height=100, center = vector(0,0,0), background=vec(0.622, 0.779, 0.847), userspin=False, userzoom=False, resizable=False)
title_cp=label(pos=vector(0,(control_panel.height/2)-text_size,0), text='Control Panel', font='helvetica', height=control_panel.height*(20/100), box=False, visible=True, color=color.black, opacity=0)

button_box_list = []
button_icon_list = []
button_text_list = []
button_greenbox_list = []
button_size = 50
def create_buttons(chosen_canvas, text_list, icon_list): #Positioning buttons uniformly from -512 +side_buffer to 512 -side_buffer
    global side_buffer, step
    side_buffer = chosen_canvas.width/100
    step = (chosen_canvas.width-2*side_buffer)/(len(text_list)-1)
    for i in range(len(text_list)):
        button_box_list.append(box(pos=vector((-chosen_canvas.width/2)+side_buffer+(i*step), -text_size/2, 0), length=control_panel.width*(button_size/1024), height=control_panel.height*(button_size/100), width=1, color=vec(0.5,0.5,0.5), shininess=0, opacity=0.3))
        button_icon_list.append(label(pos=button_box_list[i].pos, text=icon_list[i], height=button_box_list[i].height/1.7, color=color.black, box=False, opacity=0))
        button_text_list.append(label(pos=button_box_list[i].pos-vector(0,button_box_list[i].height/2+text_size,0), text=text_list[i], height=text_size, color=color.black, box=False, opacity=0))

create_buttons(control_panel, ['Play/Pause', 'PE', 'Compton', 'Transmitted'], ['⏯','⚛️','📈','📡'])

loc_b=vector(0,0,0)
def Run():
    global started, propagating, running, started_atomic, my_element_changed, num_CS, num_PE, num_trans, N, my_error_lbl, my_mech_lbl, N
    loc_b=control_panel.mouse.pos
    if abs(loc_b.x-button_box_list[0].pos.x)<=button_box_list[0].length/2 and abs(loc_b.y-button_box_list[0].pos.y)<=button_box_list[0].height/2: 
        scene.autoscale=False
        if N==100:
            N=0
        if my_mech_lbl.visible==True:
            my_error_lbl.visible=True
            my_mech_lbl.visible=False
            return
        running = not running
        if my_element_changed==True:
            my_element_changed = not my_element_changed
            num_PE=0
            num_CS=0
            num_trans=0 
            N=0
        if running:
            if not started and not remember_has_run:
                caption_print("Emiting X-rays!\n") #Appears in legend below control panel
                caption_print("PE, Compton, and Transmitted buttons active only in Mechanistic View!\n")
                started=True
            propagating = True
            button_box_list[0].color = color.green
            if not is_atomic:
                pe_tot_lbl.visible=True
                cs_tot_lbl.visible=True
                tr_tot_lbl.visible=True
                E_slider.disabled=True
                bg_menu.disabled=True
            if is_atomic:
                pe_tot_lbl.visible=False
                cs_tot_lbl.visible=False
                tr_tot_lbl.visible=False
                started_atomic = True
                if has_run:   #Check             
                    resetAtomic()
        elif not running: #just elif?
            propagating=False
            button_box_list[0].color = vector(0.7,0.7,0.7)
            if not is_atomic:
                E_slider.disabled=False
                bg_menu.disabled=False
            else: 
                E_slider.disabled=True
                bg_menu.disabled=True
control_panel.bind("mousedown", Run)
#------------------------------
#Create level buttons
def pe_but():
    global PE_scatterElectron, PE_dropElectron, compton_electron
    loc_b=control_panel.mouse.pos   
    if abs(loc_b.x-button_box_list[1].pos.x)<=button_box_list[0].length/2 and abs(loc_b.y-button_box_list[1].pos.y)<=button_box_list[0].height/2:
        my_electrons_list[0].visible=True
        my_electrons_list[0].opacity=1
        my_electrons_list[1].opacity=1
        my_electrons_list[1].visible=True
        PE_scatterElectron.visible=True
        PE_scatterElectron.pos=PE_scatterElectronLoc
        PE_dropElectron.pos=PE_dropElectronLoc
        PE_scatterElectron.opacity=1
        PE_dropElectron.opacity=1
        PE_dropElectron.visible=True
        my_error_lbl.visible=False
        compton_electron.visible=False
        my_PE_atomic.visible=True
        my_CS_atomic.visible=False
        my_trans_atomic.visible=False
        pe_tot_lbl.visible=False
        cs_tot_lbl.visible=False
        tr_tot_lbl.visible=False
        probability_box.visible=False
        my_bone_lbl.visible=False
        my_water_lbl.visible=False
        my_lead_lbl.visible=False
        my_prob_lbl.visible=False
        my_CStot_lbl.visible=False
        my_PEtot_lbl.visible=False
        my_TRtot_lbl.visible=False
        bg_menu.disabled=True
        my_mech_lbl.visible=False
        button_box_list[1].color = color.green
        button_box_list[2].color = vector(0.7,0.7,0.7)
        button_box_list[3].color = vector(0.7,0.7,0.7)
#control_panel.bind("mousedown", pe_but)
control_panel.unbind("mousedown", pe_but)


def cs_but():
    global PE_scatterElectron, PE_dropElectron, compton_electron
    loc_b=control_panel.mouse.pos
    if abs(loc_b.x-button_box_list[2].pos.x)<=button_box_list[0].length/2 and abs(loc_b.y-button_box_list[2].pos.y)<=button_box_list[0].height/2:
        compton_electron.visible=True
        compton_electron.opacity=1
        compton_electron.pos=compton_electronLoc
        my_electrons_list[2].visible=True
        my_electrons_list[2].opacity=1
        has_run=True
        PE_scatterElectron.visible=False
        PE_dropElectron.visible=False
        my_CS_atomic.visible=True
        my_PE_atomic.visible=False
        my_trans_atomic.visible=False
        my_error_lbl.visible=False
        pe_tot_lbl.visible=False
        cs_tot_lbl.visible=False
        tr_tot_lbl.visible=False
        probability_box.visible=False
        my_bone_lbl.visible=False
        my_water_lbl.visible=False
        my_lead_lbl.visible=False
        my_prob_lbl.visible=False
        my_CStot_lbl.visible=False
        my_PEtot_lbl.visible=False
        my_TRtot_lbl.visible=False
        bg_menu.disabled=True
        my_mech_lbl.visible=False
        button_box_list[1].color = vector(0.7,0.7,0.7)
        button_box_list[2].color = color.green
        button_box_list[3].color = vector(0.7,0.7,0.7)
#control_panel.bind("mousedown", cs_but)
control_panel.unbind("mousedown", cs_but)

def trans_but(): #Make lead
    loc_b=control_panel.mouse.pos
    if abs(loc_b.x-button_box_list[3].pos.x)<=button_box_list[0].length/2 and abs(loc_b.y-button_box_list[3].pos.y)<=button_box_list[0].height/2:
        my_trans_atomic.visible=True
        my_CS_atomic.visible=False
        my_PE_atomic.visible=False
        has_run=True
        pe_tot_lbl.visible=False
        cs_tot_lbl.visible=False
        tr_tot_lbl.visible=False
        my_error_lbl.visible=False
        probability_box.visible=False
        my_bone_lbl.visible=False
        my_water_lbl.visible=False
        my_lead_lbl.visible=False
        my_prob_lbl.visible=False
        my_CStot_lbl.visible=False
        my_PEtot_lbl.visible=False
        my_TRtot_lbl.visible=False
        bg_menu.disabled=True
        my_mech_lbl.visible=False
        button_box_list[1].color = vector(0.7,0.7,0.7)
        button_box_list[2].color = vector(0.7,0.7,0.7)
        button_box_list[3].color = color.green
        for i in range(0,3):
            my_electrons_list[i].visible=False
#control_panel.bind("mousedown", trans_but)
control_panel.unbind("mousedown", trans_but)

#Running
while True:
    rate(animation_speed)
    if propagating and not is_atomic and N<=99:
        xray = create_photon(xray_source.pos+vector(xray_source.length/2,0,0))
        initial_traj=hat(vector(cos(theta) + random()*(1-cos(theta)), -sin(theta) + random()*(2*sin(theta)), 0))
        move_objects([xray], [initial_traj], [vector(0,0,0)], 3) #changed from medium_box.pos
        move_objects([xray], [interaction(xray, initial_traj)], [detector_box.pos-vector(detector_box.length/2,0,0)], 3) #interaction calls event_type
        xray.visible = False
        my_PE_label.visible=False
        my_CS_label.visible=False
        my_TR_label.visible=False
        pe_tot_lbl.text = "{:.0f}".format(num_PE)
        cs_tot_lbl.text = "{:.0f}".format(num_CS)
        tr_tot_lbl.text = "{:.0f}".format(num_trans)
    elif propagating and is_atomic and not has_run:
        started_atomic = True
        animation_speed=300
        xray = create_photon(xray_source.pos+vector(xray_source.length/2,0,0))
        if button_box_list[1].color == color.green: #PE is on
            move_objects([xray], [vector(1,0,0)], [PE_scatterElectron.pos+vector(50,0,0)], 2) #added extra 50 to ending position along to get closer to scattered
            xray.visible = False
            move_objects([PE_scatterElectron], [vector(1,-0.3,0)], [vector(scene.width*(1000/1024),0,0)], 2)    
            xray=create_photon(vector(-10,20,0)) #This origin puts pulse in right place
            move_objects([xray, PE_dropElectron], [vector(1,0.2,0), PE_scatterElectron.pos-PE_dropElectron.pos-vector(0,750,0)], [vector(scene.width*(300/1024),0,0), PE_scatterElectronLoc], 2) #Secondary X-ray doesn't go far
            xray.visible = False
            my_secondary_abs_lbl.visible=True
            my_secondary_abs_lbl2.visible=True
        sleep(0.1)
        if button_box_list[2].color == color.green: #Compton is on
            move_objects([xray], [vector(1,-0.2,0)], [compton_electron.pos+vector(50,0,0)], 2)
            move_objects([xray, compton_electron], [vector(1,0.2,0), vector(1,-0.2,0)], [vector(scene.width*(1000/1024),0,0), vector(scene.width*(1000/1024),0,0)], 2)
        #sleep(0.1)
        if button_box_list[3].color == color.green: #Trans is on
            rand2=random()
            if rand2>=0.5:
                rand2=0.25*rand2
            else:
                rand2=-0.25*rand2
            move_objects([xray], [vector(1,rand2,0)], [vector(scene.width*(1000/1024),0,0)], 2)
        xray.visible = False
        if my_secondary_abs_lbl.visible==True:
            sleep(2)
            my_secondary_abs_lbl.visible=False
            my_secondary_abs_lbl2.visible=False
        button_box_list[0].color = vector(0.7,0.7,0.7)
        control_panel.bind("mousedown", pe_but)
        control_panel.bind("mousedown", cs_but)
        control_panel.bind("mousedown", trans_but)
        propagating = False
        running = False
        has_run = True
        remember_has_run = True
        started_atomic = False
        control_panel.caption
            