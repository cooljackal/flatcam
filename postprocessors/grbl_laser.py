from FlatCAMPostProc import *

# This post processor is configured to output code that
# is compatible with almost any version of Grbl.


class grbl_laser(FlatCAMPostProc):

    coordinate_format = "%.*f"
    feedrate_format = '%.*f'

    def start_code(self, p):
        units = ' ' + str(p['units']).lower()
        gcode = ''

        gcode += '(Feedrate: ' + str(p['feedrate']) + units + '/min' + ')\n'
        gcode += '(Feedrate rapids ' + str(p['feedrate_rapid']) + units + '/min' + ')\n' + '\n'

        gcode += '(Steps per circle: ' + str(p['steps_per_circle']) + ')\n'

        if str(p['options']['type']) == 'Excellon' or str(p['options']['type']) == 'Excellon Geometry':
            gcode += '(Postprocessor Excellon: ' + str(p['pp_excellon_name']) + ')\n'
        else:
            gcode += '(Postprocessor Geometry: ' + str(p['pp_geometry_name']) + ')\n'
        gcode += ('G20' if p.units.upper() == 'IN' else 'G21') + "\n" + '\n'

        gcode += '(X min: ' + '%.*f' % (p.coords_decimals, p['options']['xmin']) + units + ')\n'
        gcode += '(Y min: ' + '%.*f' % (p.coords_decimals, p['options']['ymin']) + units + ')\n'
        gcode += '(X max: ' + '%.*f' % (p.coords_decimals, p['options']['xmax']) + units + ')\n'
        gcode += '(Y max: ' + '%.*f' % (p.coords_decimals, p['options']['ymax']) + units + ')\n\n'

        gcode += 'G90\n'
        gcode += 'G94\n'
        gcode += 'G17\n'

        return gcode

    def startz_code(self, p):
        return ''

    def lift_code(self, p):
        return 'M05'

    def down_code(self, p):
        if p.spindlespeed:
            return 'M03 S%d' % p.spindlespeed
        else:
            return 'M03'

    def toolchange_code(self, p):
        return ''

    def up_to_zero_code(self, p):
        return 'M05'

    def position_code(self, p):
        return ('X' + self.coordinate_format + ' Y' + self.coordinate_format) % \
               (p.coords_decimals, p.x, p.coords_decimals, p.y)

    def rapid_code(self, p):
        return ('G00 ' + self.position_code(p)).format(**p)

    def linear_code(self, p):
        return ('G01 ' + self.position_code(p)).format(**p) + \
               ' F' + str(self.feedrate_format %(p.fr_decimals, p.feedrate))

    def end_code(self, p):
        coords_xy = p['toolchange_xy']
        gcode = ('G00 Z' + self.feedrate_format %(p.fr_decimals, p.endz) + "\n")

        if coords_xy is not None:
            gcode += 'G00 X{x} Y{y}'.format(x=coords_xy[0], y=coords_xy[1]) + "\n"
        return gcode

    def feedrate_code(self, p):
        return 'G01 F' + str(self.feedrate_format %(p.fr_decimals, p.feedrate))

    def feedrate_z_code(self, p):
        return 'G01 F' + str(self.feedrate_format %(p.fr_decimals, p.feedrate_z))

    def spindle_code(self, p):
        return ''

    def dwell_code(self, p):
        return ''

    def spindle_stop_code(self,p):
        return 'M05'
