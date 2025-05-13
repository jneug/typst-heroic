/// [ppi: 96]
/// [max-delta: 20]
/// [max-deviations: 4]

#import "../../src/heroic.typ"

#set page(width: auto, height: auto, margin: 0%)

#for name in heroic.icon-names {
  heroic.icon(name, solid: false, height: 1cm)
  pagebreak(weak: true)
}
