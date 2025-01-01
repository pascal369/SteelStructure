import FreeCAD as App
import Draft


doc = App.newDocument()

place = App.Placement(FreeCAD.Vector(1000, 0, 0), App.Rotation())
polygon1 = Draft.make_polygon(3, 750)
polygon2 = Draft.make_polygon(5, 750, placement=place)

p1 = App.Vector(2000, -1000, 0)
p2 = App.Vector(2000, 1000, 0)

line1 = Draft.make_line(p1, p2)
mirrored1 = Draft.mirror(polygon1, p1, p2)

Line2 = Draft.make_line(-p1, -p2)
mirrored2 = Draft.mirror([polygon1, polygon2], -p1, -p2)
Part.show(mirrored1)

doc.recompute()