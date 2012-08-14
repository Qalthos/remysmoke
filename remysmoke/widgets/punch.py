import tw2.core as twc
import tw2.protovis.core as twp
from tw2.protovis.core import pv

class js(twc.JSSymbol):
    def __init__(self, src):
        super(js, self).__init__(src=src)

class Punchcard(twp.PVWidget):
    def prepare(self):

        super(Punchcard, self).prepare()

        minx = min(map(lambda x: x['x'], self.p_data))
        maxx = max(map(lambda x: x['x'], self.p_data))
        miny = min(map(lambda x: x['y'], self.p_data))
        maxy = max(map(lambda x: x['y'], self.p_data))
        maxz = max(map(lambda x: x['z'], self.p_data))

        # Sizing and scales.
        self.init_js = js(
            """
            var weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday',
                            'Thursday', 'Friday', 'Saturday'];
            var data = %s,
                w = %i,
                h = %i,
                x = pv.Scale.linear(-0.25, 23.25).range(0, w),
                y = pv.Scale.ordinal(weekdays).split(0, h),
                c = pv.Scale.log(1, %f).range("orange", "brown");
            """ % (self.p_data, self.p_width-self.p_left, self.p_height, maxz))

        self.setupRootPanel()

        # Y-axis and ticks.
        self.add(pv.Rule) \
            .data(js('weekdays')) \
            .bottom(js('y')) \
            .strokeStyle(js('function(d) { return d ? "#eee" : "#000" }')) \
          .anchor("left").add(pv.Label) #\
            #.text(js('y.tickFormat'))

        # X-axis and ticks.
        self.add(pv.Rule) \
            .data(js('x.ticks()')) \
            .left(js('x')) \
            .strokeStyle(js('function(d) { return d ? "#eee" : "#000" }')) \
          .anchor("bottom").add(pv.Label) \
            .text(js('x.tickFormat'))

        # The dot plot!
        self.add(pv.Panel) \
            .data(js('data')) \
          .add(pv.Dot) \
            .left(js('function(d) { return x(d.x) }')) \
            .bottom(js('function(d) { return y(d.y) }')) \
            .strokeStyle(js('function(d) { return c(d.z) }'))  \
            .fillStyle(js('function() { return this.strokeStyle().alpha(.2) }'))  \
            .size(js('function(d) { return d.z / %f * 100 }' % (maxz))) \
            .title(js('function(d) { return d.z.toFixed(1) }'))
