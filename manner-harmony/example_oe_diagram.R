library(tidyr)
library(dplyr)
library(ggplot2)
library(ggpubr)
setwd("C:/Users/CodeB/Documents/GitHub/XPF-Daniela-Project/06-11-21-trigram_model")

artificial <- rbinom(1000, 5000, 2500/5000)

natural <- 2750

example_plot <- ggplot(data.frame(x=artificial), aes(x, color="red")) +
  geom_density(aes(y=..scaled..), fill = "red", alpha = 0.2) + 
  xlab("Number of words with final voiceless obstruents") +
  ylab("Density") + 
  ggtitle("Example observed vs expected plot for a single language") +
  theme_minimal() + 
  theme(legend.position = "none", text=element_text(family="serif")) + 
  geom_vline(xintercept=natural)
example_plot
ggsave(example_plot, file="example_oe_binom.png", height=4, width=8)