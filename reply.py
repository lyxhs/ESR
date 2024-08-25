import flet as ft
import asyncio
import os
import shutil
import sys
from pathlib import Path
from functools import partial
from flet import AppBar, ElevatedButton, Page, Text, View, colors

class Sentencevo:
    def __init__(self, en, cn, audiourl):
        self.en = en
        self.cn = cn
        self.audiourl = audiourl
        self.index = 0

async def play_audio(audio: ft.Audio):
    audio.play()

def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    audio1 = ft.Audio(
        src='typing.mp3',
        autoplay=False,
    )
    page.overlay.append(audio1)

    audio2 = ft.Audio(
        src='right.mp3',
        autoplay=False,
    )
    page.overlay.append(audio2)

    audio3 = ft.Audio(
        src='error.mp3',
        autoplay=False
    )
    page.overlay.append(audio3)

    sentencevos = []
    nowfilepath = os.path.dirname(sys.argv[0])

    lastroute="/"
    backbutton = ft.FilledButton(text="Back",on_click=lambda _:goany())
    button_row = ft.Row(
        controls = [backbutton]
    )

    sa = os.path.join(nowfilepath,"disposition")
    s1 = os.path.join(sa,"Typographica.ttf").replace("\\","/")
    s2 = os.path.join(sa,"站酷庆科黄油体.ttf").replace("\\","/")
    s3 = os.path.join(sa,"GenJyuuGothicL-Bold.ttf").replace("\\","/")
    s4 = os.path.join(sa,"方正楷体简体.ttf").replace("\\","/")
    s5 = os.path.join(sa,"OPPOSans-H.ttf").replace("\\","/")
    s6 = os.path.join(sa,"OugkehRoundRegular-ARRnL.otf").replace("\\","/")

    page.fonts = {
        "Typographica":s1,
        "zkhyt":s2,
        "genyu":s3,
        "fzkt":s4,
        "oppo":s5,
        "oug":s6
    }

    #page.theme = ft.Theme(font_family="Typographica")

    ######first page

    def on_change(e):
        text_field.value = e.control.value
        page.update()

    filename = ft.TextField(
        label="Enter your file name",
        hint_text="Type here...",
        on_change=on_change,
        max_lines=1,
        width=page.width-100
    )

    text_field = ft.TextField(
        label="Enter with your writings",
        hint_text="Type here...",
        on_change=on_change,
        max_lines=20,
        min_lines=5,
        multiline=True,
        width=page.width-100
    )

    def save_file():
        nonlocal ph,phe,wh,phv,nowfilepath
        file_name = str(filename.value)
        full_path = os.path.join(nowfilepath, "articles", file_name)
        wh=full_path
        if os.path.exists(full_path)==False:
            os.makedirs(full_path, exist_ok=True)
        textname = "en"
        full_path = os.path.join(nowfilepath, "articles", file_name,textname)
        phe=full_path
        textname = "cn"
        ph = os.path.join(nowfilepath, "articles", file_name,textname)
        textname = "voice"
        phv = os.path.join(nowfilepath, "articles", file_name,textname)

    ph:str
    phe:str
    phv:str
    texts = []

    def s(value:str):
        nonlocal texts,nowfilepath
        save_file()
        texts = value.split('.')
        gotomodifications()

    begin = View(
        "/Customized",
        [
            button_row,
            filename,
            text_field,
            ElevatedButton("Submit", on_click=lambda _: s(text_field.value))
        ]
    )

    #############

    ###the second page

    def create_textfields(a:int):
        textfield = ft.TextField(
            border=ft.InputBorder.UNDERLINE,
            width=a*35,
            text_size=40,
            on_change=onchange,
            on_focus=onfocus,
            on_blur=onblur,
            max_length=a,
            focused_border_color=ft.colors.BLUE,
            border_width = 3,
            focused_border_width= 4,
            text_style=ft.TextStyle(weight=ft.FontWeight.W_400)
        )
        return textfield
    
    def onchange(e):
        if e.control.value=="":return
        if not e.control.value.isalpha():
            e.control.value = e.control.value.replace(e.data[-1], "")
            e.control.update()
        else:
            asyncio.run(play_audio(audio1))
    
    def onfocus(e):
        nonlocal focused_text_field
        focused_text_field = e.control
        e.control.color = ft.colors.BLACK

    def onblur(e):
        nonlocal focused_text_field
        focused_text_field = None
    

    focused_text_field = None

    wh:str
    voices = []

    #a = ft.TextField(border_color=)

    def playit(ph:str):
        a = ft.Audio(
            src=ph,
            autoplay=True
        )
        page.overlay.append(a)
        page.update()
    

    def start():
        nonlocal current_index,current_sentencevo,wh,nowfilepath
        #enlines = [],cnlines = []
        entextcolumn.controls.clear()
        pb.value = 0
        voices.clear()
        print(Path(wh,"en"))
        with open(Path(wh,"en"), "r",encoding='utf-8') as f:
            enlines = f.readlines()
        with open(Path(wh,"cn"), "r",encoding='utf-8') as f:
            cnlines = f.readlines()
        for i in range(len(cnlines)+1):
            voices.append("")
        if(os.path.isfile(Path(wh,"voice"))):
            with open(Path(wh,"voice"), "r",encoding='utf-8') as f:
                getvoice = f.readlines()
                for i in range(len(getvoice)):
                    u = getvoice[i].split(",")
                    voices[int(u[0])]=u[1]
        sentencevos.clear()
        for i in range(len(enlines)):
            sentencevos.append(Sentencevo(enlines[i].strip(),cnlines[i].strip(),"None"))
        current_index = 0
        current_sentencevo = sentencevos[current_index]
        if is_hear.value==False: cn_text.value = current_sentencevo.cn
        buildtext(current_sentencevo.en)
        page.update()
        entextcolumn.controls[0].controls[0].focus()
        page.update()
        if(voices[current_index+1]!=""):
            voicesrc=voices[current_index+1]
            voicesrc = str(Path(nowfilepath,voicesrc))
            voicesrc = voicesrc.replace("\\","/")
            playit(voicesrc[:-1])


    # 定义一行布局
    cn_row = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=16,
    )

    
    current_index = 0
    current_sentencevo:Sentencevo = Sentencevo("it has some problem with this file","","")
    cn_text = ft.Text(current_sentencevo.cn, size=30, weight=ft.FontWeight.W_900,font_family="genyu")
    
    def handle_key_down(e: ft.KeyboardEvent):
        if page.route!="/challenge":return
        nonlocal current_index, current_sentencevo,focused_text_field
        print(e.key)
        if e.key == "Enter":
            print(getvalue())
            if getvalue() == current_sentencevo.en:
                asyncio.run(play_audio(audio2))
                current_index += 1
                if current_index < len(sentencevos):
                    current_sentencevo = sentencevos[current_index]
                    if is_hear.value==False:cn_text.value = current_sentencevo.cn
                    entextcolumn.controls.clear()
                    buildtext(current_sentencevo.en)
                    page.update()
                    entextcolumn.controls[0].controls[0].focus()
                    pb.value = current_index/len(sentencevos)
                    page.update()
                    if(voices[current_index+1]!=""):
                        voicesrc=voices[current_index+1]
                        voicesrc = str(Path(nowfilepath,voicesrc))
                        voicesrc = voicesrc.replace("\\","/")
                        playit(voicesrc[:-1])
                else :
                    gotomainpage()
            else:
                corretlist = current_sentencevo.en.split(' ')
                ans = 0
                for i in range(len(entextcolumn.controls)):
                    for j in range(len(entextcolumn.controls[i].controls)):
                        if(entextcolumn.controls[i].controls[j].value!=corretlist[ans]):
                            if entextcolumn.controls[i].controls[j].value!="": entextcolumn.controls[i].controls[j].color=ft.colors.RED
                            entextcolumn.controls[i].controls[j].update()
                            print(ans)
                        ans+=1
                    entextcolumn.controls[i].update()
                entextcolumn.update()
                page.update()
                asyncio.run(play_audio(audio3))
                page.update()
        elif e.key == " ":
            if focused_text_field is None:return
            for i in range(len(entextcolumn.controls)):
                if focused_text_field in entextcolumn.controls[i].controls:
                    index = entextcolumn.controls[i].controls.index(focused_text_field)
                    if(index==len(entextcolumn.controls[i].controls)-1):
                        if(i==len(entextcolumn.controls)-1):
                            return
                        else:
                            entextcolumn.controls[i+1].controls[0].focus()
                    else:
                        entextcolumn.controls[i].controls[index+1].focus()
                    page.update()
                    return
        elif e.key == ';':
            dlg = ft.AlertDialog(
                title=ft.Text(current_sentencevo.en)
            )
            page.open(dlg)
        elif e.key == "Backspace":
            if focused_text_field is None:return
            for i in range(len(entextcolumn.controls)):
                if focused_text_field in entextcolumn.controls[i].controls:
                    index = entextcolumn.controls[i].controls.index(focused_text_field)
                    if(entextcolumn.controls[i].controls[index].value!=""):return
                    if(index==0):
                        if(i==0):
                            return
                        else:
                            entextcolumn.controls[i-1].controls[-1].focus()
                    else:
                        entextcolumn.controls[i].controls[index-1].focus()
                    page.update()
                    return
        elif e.key == "/":
            if(voices[current_index+1]!=""):
                voicesrc=voices[current_index+1]
                voicesrc = str(Path(nowfilepath,voicesrc))
                voicesrc = voicesrc.replace("\\","/")
                playit(voicesrc[:-1])


    entextcolumn = ft.Column(
        controls=[],
        spacing=20
    )


    def buildtext(s:str):
        lines = s.split(' ')
        textfields = []
        lentotall = 0
        for i in range(len(lines)):
            lentotall += len(lines[i])*35+20
            if(lentotall<=page.width-100):
                textfields.append(create_textfields(len(lines[i])))
            else:
                row = ft.Row(
                    controls=[*textfields],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                )
                entextcolumn.controls.append(row)
                textfields.clear()
                textfields.append(create_textfields(len(lines[i])))
                lentotall = len(lines[i])*30+20
        if(len(textfields)!=0):
            row = ft.Row(
                controls=[*textfields],
                spacing=20,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            )
            entextcolumn.controls.append(row)
            textfields.clear()
            textfields.append(create_textfields(len(lines[i])))
        entextcolumn.update()

    def getvalue():
        a:str
        a=""
        for i in range(len(entextcolumn.controls)):
            for j in range(len(entextcolumn.controls[i].controls)):
                if(i==0 and j==0):
                    a+=entextcolumn.controls[i].controls[j].value
                else:
                    a+=" "
                    a+=entextcolumn.controls[i].controls[j].value
        return a

    pb = ft.ProgressBar(width=page.width-150,value=0,bar_height=8)
    bg_row = ft.Row(
        controls=[pb],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

        

    page.on_keyboard_event = handle_key_down

    cn_row.controls.append(cn_text),

    challenge = View(
        "/challenge",
        [
            button_row,
            bg_row,
            cn_row,
            entextcolumn
        ]
    )

    ###the third page

    global table
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("operate",width=200,color=ft.colors.BLACK,style=ft.TextStyle(weight=ft.FontWeight.BOLD,size=20))),
            ft.DataColumn(ft.Text("English",width=400,color=ft.colors.BLUE,style=ft.TextStyle(weight=ft.FontWeight.BOLD,size=20))),
            ft.DataColumn(ft.Text("Chinese",width=400,color=ft.colors.RED,style=ft.TextStyle(weight=ft.FontWeight.BOLD,size=20))),
        ],
        rows=[
        ],
        column_spacing=40,
        heading_row_color=ft.colors.BLUE_GREY_100,
        divider_thickness=2,
    )

    container = ft.Container(
        content=ft.Column(
            controls=[table],
            scroll=ft.ScrollMode.ALWAYS
        ),
        height=550
    )

    has:bool = False
    changerow:int=-1
    allnums:int = 0
    mp3s = []
    row_keys = {}

    def add_row(en:str,cn:str):
        global table
        nonlocal allnums
        allnums+=1
        row=ft.DataRow(
            cells=[
                ft.DataCell(
                    ft.Row(
                        [
                            ft.IconButton(icon=ft.icons.CHANGE_CIRCLE_OUTLINED,on_click=partial(change, allnums)),
                            ft.IconButton(icon=ft.icons.ADD,on_click=partial(add, allnums)),
                            ft.IconButton(icon=ft.icons.REMOVE,on_click=partial(delete, allnums)),
                            ft.IconButton(icon=ft.icons.FOLDER_OUTLINED,on_click=partial(addmp3,allnums))
                        ],
                        spacing=8
                    )
                ),
                ft.DataCell(ft.TextField(value=en,width=400)),
                ft.DataCell(ft.TextField(label=cn,width=400)),
            ]
        )
        table.rows.append(row)
        table.update()
        row_keys[row]=str(allnums)


    def search_key(key: str):
        nonlocal row_keys
        for row, row_key in row_keys.items():
            if row_key == key:
                return row
        return None

    def build():
        if(len(texts)!=0):
            for i in range(len(texts)):
                add_row(texts[i].replace(","," "),"Enter your chinese")

    def search_key_index(key: str):
        nonlocal row_keys
        for row, row_key in row_keys.items():
            if row_key == key:
                return table.rows.index(row)
        return None

    def add(a:int,_):
        nonlocal allnums
        if has : return
        get = search_key(str(a))
        en = get.cells[1].content.value
        cn = get.cells[2].content.value
        allnums+=1
        row=ft.DataRow(
            cells=[
                ft.DataCell(
                    ft.Row(
                        [
                            ft.IconButton(icon=ft.icons.CHANGE_CIRCLE_OUTLINED,on_click=partial(change, allnums)),
                            ft.IconButton(icon=ft.icons.ADD,on_click=partial(add, allnums)),
                            ft.IconButton(icon=ft.icons.REMOVE,on_click=partial(delete, allnums)),
                            ft.IconButton(icon=ft.icons.FOLDER_OUTLINED,on_click=partial(addmp3,allnums))
                        ],
                        spacing=8
                    )
                ),
                ft.DataCell(ft.TextField(value=en,width=400)),
                ft.DataCell(ft.TextField(value=cn,label="Enter your chinese",width=400)),
            ]
        )
        table.rows.append(row)
        table.update()
        page.update()
        row_keys[row]=str(allnums)

    def delete(a:int,_):
        if has : return
        for row, row_key in row_keys.items():
            if row_key == str(a):
                m = table.rows.index(row)
                if m in mp3s:
                    mp3s.pop(m)
                table.rows.remove(row)
                table.update()
                page.update()

    def change(a:int,_):
        nonlocal has,changerow
        if has:
            b = search_key_index(str(a))
            table.rows[changerow].cells[0].content.controls[0].icon=ft.icons.CHANGE_CIRCLE_OUTLINED
            has=False
            if b!=changerow:
                getrow = table.rows[changerow]
                table.rows.remove(getrow)
                table.rows.insert(b,getrow)
            table.update()
            page.update()

        else:
            changerow = search_key_index(str(a))
            has = True
            table.rows[changerow].cells[0].content.controls[0].icon=ft.icons.CHANGE_CIRCLE
            table.update()
            page.update()

    nowselect = -1

    def pick_files_result(e: ft.FilePickerResultEvent):
        nonlocal nowselect
        if nowselect==-1:return
        if e.files:
            print(e.files[0].path)
            b=search_key_index(str(nowselect))
            table.rows[b].cells[0].content.controls[3].icon=ft.icons.FOLDER
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"{e.name} has been add successfully"),
                show_close_icon = True
            )
            page.snack_bar.open = True
            if(is_relative.value) : mp3s.append(f"{nowselect},{os.path.relpath(e.files[0].path)}")
            else : mp3s.append(f"{nowselect},{e.files[0].path}")
            nowselect = -1
            page.update()


    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(pick_files_dialog)

    def addmp3(a:int,_):
        nonlocal nowselect
        nowselect = a
        pick_files_dialog.pick_files()



    def saveit():
        data = []
        for row in table.rows:
            row_data = []
            for cell in row.cells:
                text_field = cell.content
                if isinstance(text_field, ft.TextField):
                    row_data.append(text_field.value)
            data.append(row_data)
        with open(ph, "w",encoding='utf-8', newline='\n') as f:
            for i in range(len(data)):
                f.writelines(data[i][1]+"\n")
            f.close()
        with open(phe, "w",encoding='utf-8', newline='\n') as f:
            for i in range(len(data)):
                f.writelines(data[i][0]+"\n")
            f.close()
        if(len(mp3s)!=0):
            with open(phv, "w",encoding='utf-8', newline='\n') as f:
                for getit in mp3s:
                    index = search_key_index(getit.split(',')[0])
                    f.writelines(f"{index+1},{getit.split(',')[1]}"+"\n")
                f.close()
        page.snack_bar = ft.SnackBar(
            ft.Text("New articles has already saved.You can try it at the main page"),
            show_close_icon = True
        )
        page.show_snack_bar(page.snack_bar)
        gotomainpage()

    text = ft.Row(
        controls=[container],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    checkbt = ft.ElevatedButton(
        "Submit", on_click=lambda _: saveit()
    )


    modifications = View(
        "/modifications",
        horizontal_alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[button_row,text,checkbt]
    )

    ###choosepage

    deletewhich = -1

    articles = []

    buttons = ft.Column(
        controls=[],
        alignment=ft.MainAxisAlignment.CENTER
    )

    def deleteit(e):
        w1 = os.path.dirname(sys.argv[0])
        w2 = str(Path("articles",articles[deletewhich]))
        w=str(Path(w1,w2))
        print(w)
        shutil.rmtree(w)
        page.close(cupertino_alert_dialog)
        page.snack_bar = ft.SnackBar(
            ft.Text("Delete it successfully"),
            show_close_icon = True
        )
        page.show_snack_bar(page.snack_bar)
        page.update()
        buildlist()

    def useless(e):
        page.close(cupertino_alert_dialog)


    cupertino_alert_dialog = ft.CupertinoAlertDialog(
        title=ft.Text("Delete object",style=ft.TextStyle(size=15)),
        content=ft.Column(
            controls=[
                ft.Text("Do you want to delete this file?",style=ft.TextStyle(size=15)),
                ft.Text("If deleted, it cannot be retrieved",style=ft.TextStyle(italic=True, color=ft.colors.RED,size=12))
            ]
        ),
        actions=[
            ft.CupertinoDialogAction(
                text="Yes",
                is_destructive_action=True,
                on_click=deleteit,
            ),
            ft.CupertinoDialogAction(
                text="No", 
                is_default_action=True,
                on_click=useless,
            ),
        ],
    )

    def get_subdirectories(directory):
        subdirectory_names = []
        for entry in os.listdir(directory):
            entry_path = os.path.join(directory, entry)
            if os.path.isdir(entry_path):
                subdirectory_names.append(entry)
        return subdirectory_names
    
    def deletetoit(a,_):
        nonlocal deletewhich
        deletewhich = a
        page.open(cupertino_alert_dialog)

    fav_text = os.path.join(os.path.join(nowfilepath,"disposition"),"fav.txt")

    fav = []

    def fav_update():
        fav.clear()
        for c in buttons.controls:
            if(c.controls[0].icon == ft.icons.FAVORITE):
                fav.append(str(c.controls[2].text))
        with open(fav_text,"w",encoding="utf-8") as w:
            w.truncate(0)
            for a in fav:
                print(a)
                w.write(f"{a}\n")

    def favit(a,_):
        if buttons.controls[a].controls[0].icon == ft.icons.FAVORITE:
            buttons.controls[a].controls[0].icon = ft.icons.FAVORITE_BORDER_OUTLINED
        else:
            buttons.controls[a].controls[0].icon = ft.icons.FAVORITE
        page.update()
        fav_update()


    

    def buildlist():
        nonlocal articles,nowfilepath,fav,fav_text
        buttons.controls.clear()
        with open(fav_text,"r",encoding="utf-8") as f:
            fav = f.readlines()
            f.close()
        for i in range(len(fav)):
            if(fav[i]==""):fav.pop(i)
            else:
                fav[i] = fav[i][:-1]
        articles.clear()
        articles = get_subdirectories(os.path.join(os.path.dirname(sys.argv[0]), "articles"))
        for i in range(len(articles)):
            if(articles[i] in fav):
                buttons.controls.append(
                    ft.Row(
                        controls=[
                            ft.IconButton(icon=ft.icons.FAVORITE,icon_color=ft.colors.RED,icon_size=30,tooltip="collecte",on_click=partial(favit, i)),
                            ft.IconButton(icon=ft.icons.DELETE_FOREVER_ROUNDED,icon_color=ft.colors.RED,icon_size=30,tooltip="delete",on_click=partial(deletetoit, i)),
                            ft.ElevatedButton(text=articles[i],on_click=partial(click, i),width=300)
                        ]
                    )
                )
            else:
                buttons.controls.append(
                    ft.Row(
                        controls=[
                            ft.IconButton(icon=ft.icons.FAVORITE_BORDER_OUTLINED,icon_color=ft.colors.RED,icon_size=30,tooltip="collecte",on_click=partial(favit, i)),
                            ft.IconButton(icon=ft.icons.DELETE_FOREVER_ROUNDED,icon_color=ft.colors.RED,icon_size=30,tooltip="delete",on_click=partial(deletetoit, i)),
                            ft.ElevatedButton(text=articles[i],on_click=partial(click, i),width=300)
                        ]
                    )
                )
            buttons.update()


    def click(a,_):
        nonlocal wh
        wh1 = os.path.dirname(sys.argv[0])
        wh = str(Path("articles",articles[a]))
        wh = str(Path(wh1,wh))
        #wh = os.path.join(os.path.dirname(os.path.abspath(__file__)), "articles",articles[a])
        gotochallenge()

    ch_text = ft.Row(controls=[ft.Text("请选择你要挑战的关卡",font_family="oppo",size=30)],alignment=ft.MainAxisAlignment.CENTER)


    choosepage = View(
        "/choosepage",
        controls=[button_row,ch_text,buttons]
    )



    ###main page&controls

    def save_settings(e):
        with open(os.path.join(os.path.join(nowfilepath,"disposition"),"setting.txt"),"w",encoding="utf-8") as f:
            for s in setting.controls:
                f.writelines(f"{s.controls[0].value}\n")

    is_hear = ft.Switch(value=False,on_change=save_settings)
    hear =  ft.Row(controls=[is_hear,ft.Text("听写模式(无音频的文件不可使用)",size=15,font_family="oppo")],alignment=ft.MainAxisAlignment.CENTER,vertical_alignment=ft.CrossAxisAlignment.CENTER)
    is_relative = ft.Switch(value=False,on_change=save_settings)
    relative =  ft.Row(controls=[is_relative,ft.Text("新建文件时音频保存以相对路径保存(请将音频文件放在articles文件夹中)",size=15,font_family="oppo"),ft.Text("  慎用",style=ft.TextStyle(color=ft.colors.RED_200),font_family="fzkt")],alignment=ft.MainAxisAlignment.CENTER,vertical_alignment=ft.CrossAxisAlignment.CENTER)
    

    setting = ft.Column(
        controls=[hear,relative],
        alignment=ft.MainAxisAlignment.START,
        expand=True
    )

    verson = "1.0.0"
    verson_tf = ft.Text(f"verson:{verson}")
    
    vc = ft.Column(
        controls=[verson_tf],
        alignment=ft.MainAxisAlignment.END,
    )

    

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        # extended=True,
        min_width=100,
        min_extended_width=400,
        leading=ft.FloatingActionButton(icon=ft.icons.CREATE, text="Begin",on_click=lambda _:gotochoosepage()),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.HOME_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.HOME),
                label_content=ft.Text("Home"),
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SETTINGS_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.SETTINGS),
                label_content=ft.Text("Settings"),
            ),
        ],
        on_change=lambda e: gotoother(e),
    )

    def gotoother(e):
        if(e.control.selected_index==0):page.go("/")
        elif(e.control.selected_index==1):page.go("/settings")


    main_text1 = ft.Text(
        spans=[
            ft.TextSpan(
                "Welcome to ESR",
                ft.TextStyle(
                    size=80,
                    weight=ft.FontWeight.BOLD,
                    foreground=ft.Paint(
                        gradient=ft.PaintLinearGradient(
                            (0, 60), (150, 60), [ft.colors.BLUE, ft.colors.GREEN]
                        )
                    ),font_family="Typographica"
                ),
            ),
        ],
    )
    main_button1 = ft.CupertinoFilledButton(content=ft.Text("Challenge",font_family="oppo",size=15),on_click=lambda _:gotochoosepage(),padding=5)
    main_button2 = ft.CupertinoFilledButton(content=ft.Text("Custom article",font_family="oppo",size=15),on_click=lambda _:gotoCustomized(),padding=5)

    main_text = ft.Row(
        controls=[main_text1],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER
    )

    main_button = ft.Row(
        controls=[main_button1,main_button2],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER
    )

    mi = ft.Column(
        controls=[main_text,main_button],
        alignment=ft.MainAxisAlignment.START,
        expand=True
    )
    mainpage = View(
        "/",
        controls=[
            ft.Row(
                [
                    rail,
                    ft.VerticalDivider(width=1),
                    mi
                ],expand=True,
            )
        ]
    )

    settings = View(
        "/settings",
        controls=[
            ft.Row(
                [
                    rail,
                    ft.VerticalDivider(width=1),
                    setting
                ],expand=True,
            )
        ]
    )

    def setting_first():
        if os.path.exists(os.path.join(nowfilepath,"articles"))==False:
            os.makedirs(os.path.join(nowfilepath,"articles"), exist_ok=True)
        if os.path.exists(os.path.join(nowfilepath,"disposition"))==False:
            os.makedirs(os.path.join(nowfilepath,"disposition"), exist_ok=True)
        if os.path.isfile(os.path.join(os.path.join(nowfilepath,"disposition"),"setting.txt")):
            with open(os.path.join(os.path.join(nowfilepath,"disposition"),"setting.txt"),"r",encoding="utf-8") as f:
                setit = f.readlines()
                f.close()
            if len(setit)==2:
                if setit[0][:-1]=="True":is_hear.value = True
                else :is_hear.value = False
                if setit[1][:-1]=="True":is_relative.value = True
                else :is_relative.value = False
            else:
                with open(os.path.join(os.path.join(nowfilepath,"disposition"),"setting.txt"),"w",encoding="utf-8") as f:
                    f.writelines("False\n")
                    f.writelines("False\n")
        else:
            with open(os.path.join(os.path.join(nowfilepath,"disposition"),"setting.txt"),"w",encoding="utf-8") as f:
                f.writelines("False\n")
                f.writelines("False\n")
        if os.path.isfile(fav_text):
            pass
        else:
            with open(fav_text,"w",encoding="utf-8") as w:
                w.close()
                pass
            

    ###页面切换

    def route_change(e):
        nonlocal current_index, current_sentencevo
        page.views.clear()
        page.views.append(mainpage)
        if page.route=="/challenge":
            page.views.clear()
            page.views.append(challenge)
        elif page.route=="/modifications":
            page.views.clear()
            page.views.append(modifications)
        elif page.route=="/Customized":
            page.views.clear()
            page.views.append(begin)
        elif page.route=="/choosepage":
            page.views.clear()
            page.views.append(choosepage)
        elif page.route=="/settings":
            page.views.clear()
            page.views.append(settings)
        page.update()
        if page.route=="/modifications":
            build()
        elif page.route=="/challenge":
            page.update()
            start()
        elif page.route=="/choosepage":
            buildlist()

    def gotoCustomized():
        page.go("/Customized")

    def gotochallenge():
        page.go("/challenge")

    def gotomodifications():
        page.go("/modifications")


    def gotomainpage():
        page.go("/")

    def gotosettings():
        page.go("/settings")

    def gotochoosepage():
        page.go("/choosepage")
    

    def goany():
        page.go(lastroute)
        
    setting_first()
    page.on_route_change = route_change
    page.go(page.route)


ft.app(target=main)