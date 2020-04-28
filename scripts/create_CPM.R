# Title     : TODO
# Objective : TODO
# Created by: ddhoogduin
# Created on: 23-04-20

# if (!requireNamespace("BiocManager", quietly = TRUE))
#     install.packages("BiocManager")
#
# BiocManager::install("edgeR")
args <- commandArgs(trailingOnly = TRUE)
create_CPM_file <- function (dataset, output){
  library(edgeR)
  table <- cpm(read.table(dataset, row.names=1, header=T, sep="\t"))
  write.table(table, output, sep="\t", col.names=NA, quote=F)
}
create_CPM_file(args[1], args[2])