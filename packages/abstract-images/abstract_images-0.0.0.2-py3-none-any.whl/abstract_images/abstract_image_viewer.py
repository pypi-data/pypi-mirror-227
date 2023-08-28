import os
import json
import webbrowser
from abstract_gui import get_gui_fun,expandable,create_row_of_buttons
from abstract_utilities.string_clean import eatAll
from abstract_utilities.path_utils import is_file
from abstract_utilities.read_write_utils import read_from_file, write_to_file
from abstract_utilities.compare_utils import get_lower
from abstract_gui import *
from .image_utils import read_image,get_image_bytes,resize_image,cv2_image_to_bytesio,image_to_bytes
def change_image_num(k:int=1):
    if k == 1:
        js_bridge["image_num"]+=k
    elif k == -1:
        js_bridge["image_num"]-=k
    if js_bridge["image_num"] <0:
        js_bridge["image_num"] = 0
    elif js_bridge["image_num"] > len(js_bridge["all_list"]):
        js_bridge["image_num"] = len(js_bridge["all_list"])
    return js_bridge["image_num"]
def event_while(event):
    print(event)
    if event in ["Download","Open Image","Previous","Next","Favorite","Remove","skip"]:
        if event == "Previous":
            change_image_num(k=-1)
        if event == "Next":
            change_image_num(k=1)
        if event == "-FRAME_INPUT-":
            val = window_mgr.get_values()["-FRAME_INPUT-"]
            if val > len(js_bridge["all_list"]):
                window_mgr.update_values(key="-FRAME_INPUT-",value=val)
            if val < 0:
                window_mgr.update_values(key="-FRAME_INPUT-",value=0)
        if event == "Open Image":
            webbrowser.open(js_bridge["all_list_n"][js_bridge["image_num"]]["image"], new=2)
        if event == "skip":
            js_bridge["image_num"] = int(window_mgr.get_values(window_mgr.get_last_window_method())["-FRAME_INPUT-"])
        if event == "Download":
            webbrowser.open(js_bridge["all_list_n"][js_bridge["image_num"]]["download"], new=2)
            change_image_num(k=1)
        if event in ["skip","Next","Previous","Download"]:
            window_mgr.update_values(key="-CURR_IMG-",args={"value":js_bridge["image_num"]})
            window_mgr.update_values(key="-IMAGE_TITLE-",args={"value":js_bridge["all_list_n"][js_bridge["image_num"]]["title"]})
            window_mgr.update_values(key="-IMAGE_AUTHOR-",args={"value":js_bridge["all_list_n"][js_bridge["image_num"]]["user"]})
            window_mgr.update_values(key="-IMAGE_PATH-",args={"value":js_bridge["all_list_n"][js_bridge["image_num"]]["download"]})
            window_mgr.update_values(key="-IMAGE_COMPONENT-", args={"data": resize_image(image_path=js_bridge["all_list_n"][js_bridge["image_num"]]["image_save"], max_width=800, max_height=450)})
def abstract_image_viewer_run(image_json_path:str=None):
    window_mgr,upload_bridge,script_name=create_window_manager(global_var=globals())
    js_bridge = upload_bridge.return_global_variables(script_name=script_name)
    js_bridge["image_num"] = 0
    js_bridge["all_list"]=json.loads(read_from_file(image_json_path))
    image_path = js_bridge["all_list"][0]["image_save"]
    layout = [[[[get_gui_fun("T",args={"text":"title","key":"-IMAGE_TITLE-"})],
        [get_gui_fun("T",args={"text":"author","key":"-IMAGE_AUTHOR-"})],
        [get_gui_fun("T",args={"text":"title","key":"-IMAGE_PATH-"})],
        [get_gui_fun("T",args={"text":"0","key":"-CURR_IMG-"}),get_gui_fun("T",args={"text":"of"}),get_gui_fun("T",args={"text":len(js_bridge["all_list_n"]),"key":"-MAX_IMG-"})]],
        [get_gui_fun("Image",args={"data":resize_image(image_path, max_width=800, max_height=450),"size":(None,None),"key":"-IMAGE_COMPONENT-"})],
        [create_row_of_buttons("Download","Open Image","Previous","Next","Favorite","Remove"),get_gui_fun("Frame",args={"title":"","layout":
                                   [[get_gui_fun("Input",args={"default_text":0,"size":(2,2),"key":"-FRAME_INPUT-","enable_events":True})]]})],create_row_of_buttons("skip"),]]
    window = window_mgr.get_new_window("Abstract Image Viewer",args={"layout":layout,"size": (600, 800),"event_function":"event_while",**expandable()})
    window_mgr.while_basic(window=window)

