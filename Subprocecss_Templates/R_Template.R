transcribe <- function(path) {
    transcript <- "Put your transcription function here."
    return(transcript)
}


main <- function() {
    path <- readLines(file("stdin", "r"), n=1)
    write(transcribe(path), stdout())    
}

main()