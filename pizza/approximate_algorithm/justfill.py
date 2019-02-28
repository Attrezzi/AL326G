from pizza.parser import datareader
import utilities


p = datareader.read_data("d_big.in")
p.fill_holes()
p.to_submission("justfill_big.txt")
utilities.showimage(p.occupied)