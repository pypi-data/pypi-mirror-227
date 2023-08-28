#!/usr/bin/env python3

import time
import plaques as plq

mpbase = plq.Window(h_abs_size = 40, v_abs_size = 14, 
    fill = plq.CharCell(char = ".", color = plq.BLUE),
    h_rel_pos = 0.5, v_rel_pos = 0.5, pivot = plq.BOTTOM_LEFT)
mpbase.title.text = "A title"

mpchild = plq.Plaque(h_rel_size = 0.5, v_rel_size = 0.6,
    fill = plq.CharCell(char = "+", color = plq.TRANSPARENT, bgcol = plq.RED))
mpbase.status.text = "MP Base status"
mpbase.status.align = plq.CENTER_RIGHT
mpbase.title.align = plq.TOP_LEFT
mpbase.frame = plq.OUTER_HALF
mpchild3 = plq.Text(h_abs_size = 10, v_abs_size = 5,  # XXX change here
    fill = plq.CharCell(bgcol = plq.CYAN, color = plq.BLACK, bold = True),
    align = plq.TOP_LEFT,
    text = "A quick -brown fox, jumped ~ over the lazy doaaaaag!!!")
mpchild2 = plq.Text(h_abs_size = 30, v_abs_size = 9,  # XXX change here
    #fill = plq.CharCell(bgcol = plq.CYAN, color = plq.BLACK, bold = True),
    v_rel_pos = 0.5, h_rel_pos = 0.5, align = plq.BOTTOM_CENTER)
mpchild2.text = "A quick -brown9999 ergrgerfox, jumped ~ over the lazy dog!!!"
#mpbase.content.append(mpchild)
mpbase.content.append(mpchild3)
mpbase.content.append(mpchild2)

with plq.Screen(title = "My Plaques Application") as myscreen:
    myscreen.content.append(mpbase)
    while True:
        myscreen.refresh()
        _key = myscreen.getkey()
        if _key:
            exit()
        time.sleep(.1)