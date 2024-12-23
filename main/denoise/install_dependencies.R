# When packaging in the shell, install the dependencies for R here
install_dependencies <- function() {
  library("devtools")
  library("dada2")
  library("foreach")
  library("doParallel")
}