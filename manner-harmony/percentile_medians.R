library(tidyr)
library(dplyr)
library(ggplot2)
library(ggpubr)
setwd("C:/Users/CodeB/Documents/GitHub/XPF-soft-constraints/manner-harmony")

percentiles <- read.csv("percentiles.csv", header=T)

fricatives_median <- median(percentiles$multiple_fricatives)
same_fricatives_median <- median(percentiles$multiple_same_fricatives)
diff_fricatives_median <- median(percentiles$multiple_diff_fricatives)