import ctypes as C,sys
rs=C.CDLL('librsvg-2.so.2');ca=C.CDLL('libcairo.so.2')
rs.rsvg_handle_new_from_file.restype=C.c_void_p
rs.rsvg_handle_new_from_file.argtypes=[C.c_char_p,C.c_void_p]
ca.cairo_image_surface_create.restype=C.c_void_p
ca.cairo_create.restype=C.c_void_p;ca.cairo_create.argtypes=[C.c_void_p]
rs.rsvg_handle_render_cairo.argtypes=[C.c_void_p,C.c_void_p]
ca.cairo_surface_write_to_png.argtypes=[C.c_void_p,C.c_char_p]
h=rs.rsvg_handle_new_from_file(sys.argv[1].encode(),None)
s=ca.cairo_image_surface_create(0,1100,800);cr=ca.cairo_create(s)
rs.rsvg_handle_render_cairo(h,cr);ca.cairo_surface_write_to_png(s,sys.argv[2].encode())
