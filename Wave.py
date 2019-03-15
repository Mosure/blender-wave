import bpy
import numpy as np
from math import sin, cos, tan, pi


def func(n, x, y, t=0):
    step = (2 * pi / n)
    sx = step * x - pi
    sy = step * y - pi
    
    #return (sx, sy, sin(sx * 5 + t) * sin(sy * 5 + t) / 5)
    #return (sx, sy, sin(10 * (sx * sx * 0.25 + sy * sy * 0.25 + t)) / 8)
    return (sx, sy, cos(sy * sx * 2 + sy * sx * 2 + t) * sin(sx + t + pi) * sin(sy + t) / 8 + sin(sy + sx + t + pi) / 3 + cos(sy - sx + t + pi) / 3)

def generate_wave(n):
    name = 'wave'
    
    if name in bpy.data.meshes:
        bpy.data.meshes.remove(bpy.data.meshes[name])
    
    m = bpy.data.meshes.new(name)

    m.vertices.add(n * n)
    m.edges.add(3 * n * n - 4 * n + 1)
    #m.polygons.add(2 * (n - 1) * (n - 1))

    edge_index = 0
    polygon_index = 0

    for x in range(n):
        for y in range(n):
            m.vertices[x * n + y].co = func(n, x, y)
            
            if y < n - 1:
                m.edges[edge_index].vertices = (x * n + y, x * n + y + 1)
                edge_index += 1
                
                if x < n - 1:
                    m.edges[edge_index].vertices = (x * n + y, (x + 1) * n + y + 1)
                    edge_index += 1
                    
                    #m.polygons[polygon_index].vertices = [x * n + y, (x + 1) * n + y, x * n + y + 1]
                    #m.polygons[polygon_index].use_smooth = True
                    #polygon_index += 1
                    
                    #m.polygons[polygon_index].vertices = [(x + 1) * n + y + 1, x * n + y + 1, (x + 1) * n + y]
                    #m.polygons[polygon_index].use_smooth = True
                    #polygon_index += 1
            
            if x < n - 1:
                m.edges[edge_index].vertices = (x * n + y, (x + 1) * n + y)
                edge_index += 1
    
    o = bpy.data.objects.new(name, m)
    bpy.data.collections[0].objects.link(o)
    
    bpy.context.view_layer.objects.active = o

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.object.mode_set(mode='OBJECT')
    
    return o

def fill(o):
    bpy.context.view_layer.objects.active = o

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.fill_holes(sides=3)
    bpy.ops.mesh.select_all(action="DESELECT")
    bpy.ops.object.mode_set(mode='OBJECT')

    for f in o.data.polygons:
        f.use_smooth = True

def animate_v2(n, o, frames):
    def callback(scene):
        for v in o.data.vertices:
            x = v.index // n
            y = v.index - n * (v.index // n)
            t = scene.frame_current * 2 * pi / frames
            
            pos = func(n, x, y, t)
            
            v.co[2] = pos[2]
    
    bpy.app.handlers.frame_change_pre.clear()
    bpy.app.handlers.frame_change_pre.append(callback)
    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = frames


n = 100
frames = 240

#o = generate_wave(n)
#fill(o)
#animate_v2(n, o, frames)

animate_v2(n, bpy.data.objects['wave'], frames)
