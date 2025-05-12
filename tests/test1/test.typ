#import "../../src/heroic.typ"

#heroic.icon("archive-box", height: 4em)

#heroic.icon("archive-box", height: 4em, color: red)

#heroic.icon("archive-box", height: 4em, solid: false)

#heroic.icon("archive-box", height: 4em, solid: false, color: red)

#heroic.hi("archive-box")

#set text(size: 2em, fill: green)
#lorem(8) #heroic.hi("archive-box") #lorem(8)

#set text(fill: red)
#lorem(8) #heroic.hi("archive-box", solid: false, baseline: 20%) #lorem(8)


// #assert-panic(() => heroic.icon("foo"))
