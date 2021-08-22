library(tidyverse)
options(stringAsFactors = FALSE)
library(tidyr)


phoible <- read_csv(file='Data/phoible-2020-04-06.csv')
phoible <- phoible[!duplicated(phoible$Phoneme),]

# account for missing phonemes in phoible ---------------------------
## affricates
phoible$Phoneme[phoible$Phoneme=='t̠ʃ']<-"tʃ"
phoible$Phoneme[phoible$Phoneme=='d̠ʒ'] <- "dʒ"
phoible$Phoneme[phoible$Phoneme=='t̠ʃʼ'] <- "tʃʼ"
phoible$Phoneme[phoible$Phoneme=='t̠ʃʰ'] <- "tʃʰ"

## pre-nasalized consonants
phoible$Phoneme[phoible$Phoneme=='mb'] <- "ᵐb"
phoible$Phoneme[phoible$Phoneme=='mp'] <- "ᵐp"
phoible$Phoneme[phoible$Phoneme=='ɱv'] <- "ᶬv"

phoible$Phoneme[phoible$Phoneme=='nd'] <- "ⁿd"
phoible$Phoneme[phoible$Phoneme=='nt'] <- "ⁿt"
phoible$Phoneme[phoible$Phoneme=='nd̪'] <- "ⁿd̪"
phoible$Phoneme[phoible$Phoneme=='nt̪'] <- "ⁿt̪"
phoible$Phoneme[phoible$Phoneme=='ndr'] <- "ⁿdʳ"
phoible$Phoneme[phoible$Phoneme=='n̠d̠ʒ'] <- "ⁿdʒ"
phoible$Phoneme[phoible$Phoneme=='n̠t̠ʃ'] <- "ⁿtʃ"
phoible$Phoneme[phoible$Phoneme=='ndz'] <- "ⁿdz"
phoible$Phoneme[phoible$Phoneme=='nts'] <- "ⁿts"
phoible$Phoneme[phoible$Phoneme=='ns'] <- "ⁿs"
phoible$Phoneme[phoible$Phoneme=='nz'] <- "ⁿz"

phoible$Phoneme[phoible$Phoneme=='ɳɖ'] <- "ⁿɖ"
phoible$Phoneme[phoible$Phoneme=='ɲɟ'] <- "ᶮɟ"

phoible$Phoneme[phoible$Phoneme=='ŋɡ'] <- "ᵑɡ"
phoible$Phoneme[phoible$Phoneme=='ŋɡʷ'] <- "ᵑɡʷ"
phoible$Phoneme[phoible$Phoneme=='ŋk'] <- "ᵑk"
phoible$Phoneme[phoible$Phoneme=='ŋkʲ'] <- "ᵑkʲ"

phoible$Phoneme[phoible$Phoneme=='ɳʈʂ'] <- "ᶯʈʂ"

phoible$Phoneme[phoible$Phoneme=='ɴɢ'] <- "ᶰɢ"

## nasalized vowels 
phoible$Phoneme[phoible$Phoneme=='ã'] <- "ã"
phoible$Phoneme[phoible$Phoneme=='õ'] <- "õ"
phoible$Phoneme[phoible$Phoneme=='ĩ'] <- "ĩ"
phoible$Phoneme[phoible$Phoneme=='ũ'] <- "ũ"

## palatalized vowels
phoible$Phoneme[phoible$Phoneme=='aʲ'] <- "aj"
phoible$Phoneme[phoible$Phoneme=='oʲ'] <- "oj"
phoible$Phoneme[phoible$Phoneme=='eʲ'] <- "ej"
phoible$Phoneme[phoible$Phoneme=='ʊʲ'] <- "ʊj"

## other 
phoible$Phoneme[phoible$Phoneme=='dr'] <- "dʳ"
phoible$Phoneme[phoible$Phoneme=='tr'] <- "tʳ"

write_csv(phoible,'Data/resolved-phoible.csv')