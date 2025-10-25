package main

import (
	"fmt"
	"kassenzettelleser/leser"
	"log"
	"net/http"
)

func getLeser() leser.KassenzettelLeser {
	return &leser.PythonLeser{}
}

func uploadHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Println("message received")

	if r.Method != http.MethodPost {
		fmt.Println("only POST allowed")
		http.Error(w, "Only POST allowed", http.StatusMethodNotAllowed)
		return
	}
	file, header, err := r.FormFile("file")
	if err != nil {
		fmt.Println("cant read file")
		http.Error(w, "Cant read image", http.StatusBadRequest)
		return
	}
	fmt.Printf("Got file: %v\n", header.Filename)
	defer file.Close()
	out, err := getLeser().ReadKassenzettel(file)
	if err != nil {
		fmt.Println("error reading kassenzettel:", err)
		http.Error(w, "Error reading kassenzettel", http.StatusBadRequest)
		return
	}
	fmt.Println(out)
	fmt.Fprintf(w, "%s", out)
}

func rescue(w http.ResponseWriter) {
	if r := recover(); r != nil {
		fmt.Println("Unexpected panic", r)
		http.Error(w, "Irgendwas ist kaputt gegangen, Sorry", http.StatusInternalServerError)
	}
}
func rescueDecorator(function func(http.ResponseWriter, *http.Request)) func(http.ResponseWriter, *http.Request) {
	return func(w http.ResponseWriter, r *http.Request) {
		defer func() { rescue(w) }()
		function(w, r)
	}
}

func main() {
	fs := http.FileServer(http.Dir("static"))
	http.Handle("/", fs)
	http.HandleFunc("/upload", rescueDecorator(uploadHandler))

	http.Handle("/favicon.ico", http.FileServer(http.Dir(".")))
	log.Println("Server is running on :8080")
	log.Fatal(http.ListenAndServe("0.0.0.0:8080", nil))
}
