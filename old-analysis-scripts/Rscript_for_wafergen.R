#Library
library(reshape2)
library(ggplot2)
library(ggpubr)



#########################
# 1. Make data ready
########################

#read data 
dat <- read.table("~/Box Sync/2018/6June/NPB/Jin051518-96632/Jin061518.txt", sep="\t", header=T)[,c("Assay","Sample","Ct")]

#get sample info
meta <- read.csv("~/Box Sync/2018/6June/NPB/meta_fix.csv")

#convert 16S Ct into count
meta_std <- read.csv("~/Box Sync/2018/11November/NPB/meta_standard.csv")

#########################
# function
########################
add_to_meta <- function(merged_meta_chip, chip, target, meta, meta_std, name_target, sample_id){
	sub <- subset(chip, Assay %in% target)
	casted <- dcast(sub, Sample~Assay, fun=mean, value.var = "Ct")
	merged_meta <- merge(merged_meta_chip, casted, by.x = sample_id, by.y="Sample")
	meta_sub <- subset(meta_std, Assay %in% target)
	data_sub <- subset(sub, Sample %in% meta_sub$Sample)
	merged_std <- merge(data_sub, meta_sub, by.x = "Sample", by.y = "Sample", all.x=T)
	merged_std_no_NA <- subset(merged_std, Ct != "NA")
	
	ct <- merged_std_no_NA$Ct 
	count <-  log10(merged_std_no_NA$count+1)
	lm.r <- lm(ct ~ count)
	coef <- coef(lm.r)[2]
	eff <- 100*((10^(-1/coef))-1)
	inverse.lm <- lm(count ~ ct)
	
	if (length(target) > 1){
		merged_meta$mean_target<- rowMeans(merged_meta[,target], na.rm=T)
		val = merged_meta$"mean_target"
	}else{
		val = merged_meta[,target]
	}
	
	merged_meta$temp<- 10^predict(inverse.lm ,data.frame(ct = val), interval = "predict")[,1]
	names(merged_meta)[ncol(merged_meta)] <- paste0("cal_", name_target)
	names(merged_meta)[ncol(merged_meta)-1] <- paste0("mean_", name_target)
	return(merged_meta)
}

###############
# Add 16S rRNA count
###############
name_target = "16s"
sample_id = "sample"
target <- c("16sTom1","16sTom2","16sTom3")
merged_meta <- add_to_meta(meta, dat, target, meta, meta_std, name_target, sample_id)


#########################
# Add ermB count
########################
name_target = "ermb"
sample_id = "sample"
target <- c("ermbEdBob1","ermbEdBob2","ermbEdBob3")
merged_meta <- add_to_meta(merged_meta, dat, target, meta, meta_std, name_target, sample_id)

#########################
# Add ermF count
########################
name_target = "ermf"
sample_id = "sample"
target <- c("ermfEdBob1","ermfEdBob2","ermfEdBob3")
merged_meta <- add_to_meta(merged_meta, dat, target, meta, meta_std, name_target, sample_id)

#########################
# Add tetM count
########################
name_target = "tetm"
sample_id = "sample"
target <- c("tetmBob1","tetmBob2","tetmBob3")
merged_meta <- add_to_meta(merged_meta, dat, target, meta, meta_std, name_target, sample_id)


