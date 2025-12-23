
#import "../../src/heroic.typ"

#set page(width: auto, height: auto, margin: 0%)

#for name in heroic.icon-names {
  image("../../assets/icons/solid/" + name + ".svg", height: 1em)
  pagebreak(weak: true)
}
