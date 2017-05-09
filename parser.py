from display import *
from matrix import *
from draw import *

ARG_COMMANDS = [ 'line', 'scale', 'move', 'rotate', 'save', 'circle', 'bezier', 'hermite', 'box', 'sphere', 'torus' ]

def parse_file( fname, edges, transform, screen, color ):

    f = open(fname)
    lines = f.readlines()

    clear_screen(screen)
    t = new_matrix()
    ident(t)
    systems = [ t ]

    step = 0.1
    c = 0
    while c < len(lines):
        line = lines[c].strip()
        #print ':' + line + ':'

        if line in ARG_COMMANDS:            
            c+= 1
            args = lines[c].strip().split(' ')
            #print 'args\t' + str(args)
            
        if line == 'sphere':
            #print 'SPHERE\t' + str(args)
            add_sphere(edges,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step)
            matrix_mult( systems[-1], edges )
            draw_polygons(edges, screen, color)
            edges = []

        elif line == 'torus':
            #print 'TORUS\t' + str(args)
            add_torus(edges,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), step)
            matrix_mult( systems[-1], edges )
            draw_polygons(edges, screen, color)
            edges = []
            
        elif line == 'box':
            #print 'BOX\t' + str(args)
            add_box(edges,
                    float(args[0]), float(args[1]), float(args[2]),
                    float(args[3]), float(args[4]), float(args[5]))
            matrix_mult( systems[-1], edges )
            draw_polygons(edges, screen, color)
            edges = []
            
        elif line == 'circle':
            #print 'CIRCLE\t' + str(args)
            add_circle(edges,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step)

        elif line == 'hermite' or line == 'bezier':
            #print 'curve\t' + line + ": " + str(args)
            add_curve(edges,
                      float(args[0]), float(args[1]),
                      float(args[2]), float(args[3]),
                      float(args[4]), float(args[5]),
                      float(args[6]), float(args[7]),
                      step, line)                      
            
        elif line == 'line':            
            #print 'LINE\t' + str(args)

            add_edge( edges,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), float(args[5]) )

        elif line == 'scale':
            #print 'SCALE\t' + str(args)
            t = make_scale(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult( systems[-1], t )
            systems[-1] = [ x[:] for x in t]

        elif line == 'move':
            #print 'MOVE\t' + str(args)
            t = make_translate(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult( systems[-1], t )
            systems[-1] = [ x[:] for x in t]


        elif line == 'rotate':
            #print 'ROTATE\t' + str(args)
            theta = float(args[1]) * (math.pi / 180)
            
            if args[0] == 'x':
                t = make_rotX(theta)
            elif args[0] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult( systems[-1], t )
            systems[-1] = [ x[:] for x in t]
                
        elif line == 'clear':
            edges = []
            
        elif line == 'ident':
            ident(transform)

        elif line == 'apply':
            matrix_mult( transform, edges )

        elif line == 'push':
            systems.append( [x[:] for x in systems[-1]] )
            
        elif line == 'pop':
            systems.pop()
            
        elif line == 'display' or line == 'save':
            if line == 'display':
                display(screen)
            else:
                save_extension(screen, args[0])
            
        c+= 1
