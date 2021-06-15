library(tidyr)
library(dplyr)
library(ggplot2)
library(ggpubr)
setwd("C:/Users/CodeB/Documents/GitHub/XPF-soft-constraints/manner-harmony")

lang_codes <- read.csv("lang_codes.tsv", sep='\t', header=F)
colnames(lang_codes) <- c("code")

# vectors of percentiles
multiple_fricatives <- c()
multiple_same_fricatives <- c()
multiple_diff_fricatives <- c() 
multiple_sibilants <- c()
multiple_same_sibilants <- c()

# vectors of plots
multiple_fricatives_plots <- list()
multiple_same_fricatives_plots <- list()
multiple_diff_fricatives_plots <- list()
multiple_sibilants_plots <- list()
multiple_same_sibilants_plots <- list()

# For each lang code, get artificial distribution and natural value
for (i in 1:length(lang_codes$code)) {
  code <- lang_codes$code[i]
  artificial <- read.csv(paste("distributions/", code, "_artificial.csv", sep=""))
  artificial <- artificial %>% 
    mutate(multiple_same_fricatives = multiple_same_fricatives * 100, 
           multiple_diff_fricatives = multiple_diff_fricatives * 100,
           multiple_fricatives = multiple_fricatives * 100,
           multiple_sibilants = multiple_sibilants * 100,
           multiple_same_sibilants = multiple_same_sibilants * 100)
  natural <- read.csv(paste("distributions/", code, "_natural.csv", sep=""))
  natural <- natural %>% 
    mutate(multiple_same_fricatives = multiple_same_fricatives * 100, 
           multiple_diff_fricatives = multiple_diff_fricatives * 100,
           multiple_fricatives = multiple_fricatives * 100,
           multiple_sibilants = multiple_sibilants * 100,
           multiple_same_sibilants = multiple_same_sibilants * 100)
  # multiplication by 100 is so that it's in terms of percent (5% instead of 0.05)
  
  # Multiple of the same fricative
  same_fricatives_plot <- ggplot(data.frame(x=artificial$multiple_same_fricatives), aes(x, color="red")) +
    geom_density(aes(y=..scaled..)) + 
    theme_minimal() + 
    theme(legend.position = "none", text=element_text(family="serif")) +
    xlab("Violations (%)") +
    ylab("Density") + 
    ggtitle(paste(code, "same fricatives")) +
    geom_vline(xintercept=natural$multiple_same_fricatives)
  # ggsave(same_fricatives_plot, file=paste("visualizations/", code, "_same_fricatives.pdf", sep=""), height=4, width=8)
  multiple_same_fricatives_percentile <- ecdf(artificial$multiple_same_fricatives)(natural$multiple_same_fricatives)
  multiple_same_fricatives <- append(multiple_same_fricatives, multiple_same_fricatives_percentile)
  multiple_same_fricatives_plots[[i]] = same_fricatives_plot
  
 # Different fricatives in the same word
  diff_fricatives_plot <- ggplot(data.frame(x=artificial$multiple_diff_fricatives), aes(x, color="red")) +
    geom_density(aes(y=..scaled..)) + 
    theme_minimal() + 
    theme(legend.position = "none", text=element_text(family="serif")) +
    xlab("Violations (%)") +
    ylab("Density") + 
    ggtitle(paste(code, "same fricatives")) +
    geom_vline(xintercept=natural$multiple_diff_fricatives)
  # ggsave(same_fricatives_plot, file=paste("visualizations/", code, "_same_fricatives.pdf", sep=""), height=4, width=8)
  multiple_diff_fricatives_percentile <- ecdf(artificial$multiple_diff_fricatives)(natural$multiple_diff_fricatives)
  multiple_diff_fricatives <- append(multiple_diff_fricatives, multiple_diff_fricatives_percentile)
  multiple_diff_fricatives_plots[[i]] = diff_fricatives_plot

  # Multiple fricatives
  fricatives_plot <- ggplot(data.frame(x=artificial$multiple_fricatives), aes(x, color="red")) +
    geom_density(aes(y=..scaled..)) + 
    theme_minimal() + 
    theme(legend.position = "none", text=element_text(family="serif")) +
    xlab("Violations (%)") +
    ylab("Density") + 
    ggtitle(paste(code, "fricatives")) +
    geom_vline(xintercept=natural$multiple_fricatives)
  # ggsave(fricatives_plot, file=paste("visualizations/", code, "_fricatives.pdf", sep=""), height=4, width=8)
  multiple_fricatives_percentile <- ecdf(artificial$multiple_fricatives)(natural$multiple_fricatives)
  multiple_fricatives <- append(multiple_fricatives, multiple_fricatives_percentile)
  multiple_fricatives_plots[[i]] = fricatives_plot
  
  # Multiple of the same sibilant 
  same_sibilants_plot <- ggplot(data.frame(x=artificial$multiple_same_sibilants), aes(x, color='red')) +
    geom_density(aes(y=..scaled..)) + 
    theme_minimal() + 
    theme(legend.position = "none", text=element_text(family="serif")) +
    xlab("Violations (%)") +
    ylab("Density") + 
    ggtitle(paste(code, "same sibilants")) +
    geom_vline(xintercept=natural$multiple_same_sibilants)
  # ggsave(same_sibilants_plot, file=paste("visualizations/", code, "_same_sibilants.pdf", sep=""), height=4, width=8)
  multiple_same_sibilants_percentile <- ecdf(artificial$multiple_same_sibilants)(natural$multiple_same_sibilants)
  multiple_same_sibilants <- append(multiple_same_sibilants, multiple_same_sibilants_percentile)
  multiple_same_sibilants_plots[[i]] = same_sibilants_plot
  
  # Multiple sibilants
  sibilants_plot <- ggplot(data.frame(x=artificial$multiple_sibilants), aes(x, color='red')) +
    geom_density(aes(y=..scaled..)) + 
    theme_minimal() + 
    theme(legend.position = "none", text=element_text(family="serif")) +
    xlab("Violations (%)") +
    ylab("Density") + 
    ggtitle(paste(code, "sibilants")) +
    geom_vline(xintercept=natural$multiple_sibilants)
  # ggsave(sibilants_plot, file=paste("visualizations/", code, "_sibilants.pdf", sep=""), height=4, width=8)
  multiple_sibilants_percentile <- ecdf(artificial$multiple_sibilants)(natural$multiple_sibilants)
  multiple_sibilants <- append(multiple_sibilants, multiple_sibilants_percentile)
  multiple_sibilants_plots[[i]] = sibilants_plot
}

ggsave(file="multiple_same_fricatives_1.pdf", gridExtra::arrangeGrob(grobs=multiple_same_fricatives_plots[1:33], labels=lang_codes$code), width=12, height=8)
ggsave(file="multiple_same_fricatives_2.pdf", gridExtra::arrangeGrob(grobs=multiple_same_fricatives_plots[34:75], labels=lang_codes$code), width=12, height=8)

ggsave(file="multiple_diff_fricatives_1.pdf", gridExtra::arrangeGrob(grobs=multiple_diff_fricatives_plots[1:33], labels=lang_codes$code), width=12, height=8)
ggsave(file="multiple_diff_fricatives_2.pdf", gridExtra::arrangeGrob(grobs=multiple_diff_fricatives_plots[34:75], labels=lang_codes$code), width=12, height=8)

ggsave(file="multiple_fricatives_1.pdf", gridExtra::arrangeGrob(grobs=multiple_fricatives_plots[1:33], labels=lang_codes$code), width=12, height=8)
ggsave(file="multiple_fricatives_2.pdf", gridExtra::arrangeGrob(grobs=multiple_fricatives_plots[34:75], labels=lang_codes$code), width=12, height=8)

ggsave(file="multiple_same_sibilants_1.pdf", gridExtra::arrangeGrob(grobs=multiple_same_sibilants_plots[1:33], labels=lang_codes$code), width=12, height=8)
ggsave(file="multiple_same_sibilants_2.pdf", gridExtra::arrangeGrob(grobs=multiple_same_sibilants_plots[34:75], labels=lang_codes$code), width=12, height=8)

ggsave(file="multiple_sibilants_1.pdf", gridExtra::arrangeGrob(grobs=multiple_sibilants_plots[1:33], labels=lang_codes$code), width=12, height=8)
ggsave(file="multiple_sibilants_2.pdf", gridExtra::arrangeGrob(grobs=multiple_sibilants_plots[34:75], labels=lang_codes$code), width=12, height=8)

percentiles <- data.frame(lang_codes, multiple_fricatives, multiple_same_fricatives, multiple_diff_fricatives, multiple_sibilants, multiple_same_sibilants)
write.csv(percentiles, "percentiles.csv")

fricatives_percentile_density <- ggplot(data.frame(x=percentiles$multiple_fricatives), aes(x, fill="red")) + 
  geom_density(aes(y=..scaled..)) + 
  theme_minimal() + 
  theme(legend.position = "none", text=element_text(family="serif")) +
  ggtitle("Distribution of fricative co-occurrence percentiles") + 
  xlab("Percentile of natural language percent of violations compared to generated distribution") + 
  ylab("Density")
ggsave(fricatives_percentile_density, file="fricatives_percentile_density.png", height=4, width=8)

same_fricatives_percentile_density <- ggplot(data.frame(x=percentiles$multiple_same_fricatives), aes(x, fill="red")) + 
  geom_density(aes(y=..scaled..)) + 
  theme_minimal() + 
  theme(legend.position = "none", text=element_text(family="serif")) +
  ggtitle("Distribution of identical fricative co-occurrence percentiles") + 
  xlab("Percentile of natural language percent of violations compared to generated distribution") + 
  ylab("Density")
ggsave(same_fricatives_percentile_density, file="same_fricatives_percentile_density.png", height=4, width=8)

diff_fricatives_percentile_density <- ggplot(data.frame(x=percentiles$multiple_diff_fricatives), aes(x, fill="red")) + 
  geom_density(aes(y=..scaled..)) + 
  theme_minimal() + 
  theme(legend.position = "none", text=element_text(family="serif")) +
  ggtitle("Distribution of different fricative co-occurrence percentiles") + 
  xlab("Percentile of natural language percent of violations compared to generated distribution") + 
  ylab("Density")
ggsave(diff_fricatives_percentile_density, file="diff_fricatives_percentile_density.png", height=4, width=8)

sibilants_percentile_density <- ggplot(data.frame(x=percentiles$multiple_sibilants), aes(x, fill="red")) + 
  geom_density(aes(y=..scaled..)) + 
  theme_minimal() + 
  theme(legend.position = "none") + 
  ggtitle("Distribution of sibilant co-occurrence percentiles") + 
  xlab("Percentile of natural language percent of violations compared to generated distribution") + 
  ylab("Density")
ggsave(sibilants_percentile_density, file="sibilants_percentile_density.pdf", height=4, width=8)

same_sibilants_percentile_density <- ggplot(data.frame(x=percentiles$multiple_same_sibilants), aes(x, fill="red")) + 
  geom_density(aes(y=..scaled..)) + 
  theme_minimal() + 
  theme(legend.position = "none", text=element_text(family="serif")) +
  ggtitle("Distribution of identical sibilant co-occurrence percentiles") + 
  xlab("Percentile of natural language percent of violations compared to generated distribution") + 
  ylab("Density")
ggsave(fricatives_percentile_density, file="same_sibilants_percentile_density.pdf", height=4, width=8)

ggsave(file="percentile_density_plots.pdf", 
       gridExtra::arrangeGrob(grobs=list(fricatives_percentile_density,
                                         same_fricatives_percentile_density,
                                         diff_fricatives_percentile_density)),
                                        # sibilants_percentile_density,
                                        #  same_sibilants_percentile_density)),
       height=8, width=16)


### Finding significant individual languages
significant_general <- data.frame(lang_code = lang_codes$code[percentiles$multiple_fricatives > 0.975], percentiles = percentiles$multiple_fricatives[percentiles$multiple_fricatives > 0.975])
write.csv(significant_general, "fricatives_significant_indiv_langs.csv")

significant_same <- data.frame(lang_code = lang_codes$code[percentiles$multiple_same_fricatives > 0.975], percentiles = percentiles$multiple_same_fricatives[percentiles$multiple_same_fricatives > 0.975])
write.csv(significant_same, "same_fricatives_significant_indiv_langs.csv")

significant_diff <- data.frame(lang_code = lang_codes$code[percentiles$multiple_diff_fricatives > 0.975], percentiles = percentiles$multiple_diff_fricatives[percentiles$multiple_diff_fricatives > 0.975])
write.csv(significant_diff, "diff_fricatives_significant_indiv_langs.csv")

# This function can be used to find the mode of each artificial distribution
maxmode <- function(x){
  x <- x[!is.na(x)]
  d <- density(x)
  (d$x[d$y == max(d$y)])[1]
}

# The binom.test function can be used for binomial tests
