package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"mime/multipart"
	"net/http"
)

func uploadHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Println("message received")

	if r.Method != http.MethodPost {
		http.Error(w, "Only POST allowed", http.StatusMethodNotAllowed)
		return
	}
	file, fileHeader, err := r.FormFile("file")
	if err != nil {
		http.Error(w, "Cant read image", http.StatusInternalServerError)
		return
	}
	defer file.Close()

	pr, pw := io.Pipe()
	wr := multipart.NewWriter(pw)
	go func() {
		p, _ := wr.CreateFormFile("file", fileHeader.Filename)
		io.Copy(p, file)
		wr.Close()
		pw.Close()
	}()
	//POST request
	req, err := http.NewRequest("POST", "http://localhost:5000/size", pr)
	req.Header.Set("Content-Type", wr.FormDataContentType())
	resp, _ := http.DefaultClient.Do(req)

	if err != nil || resp.StatusCode != http.StatusOK {
		http.Error(w, "Cant read image", http.StatusInternalServerError)
		return
	}
	defer resp.Body.Close()
	var result map[string]int
	err = json.NewDecoder(resp.Body).Decode(&result)
	if err != nil {
		http.Error(w, "Something went wrong", http.StatusInternalServerError)
		return
	}
	var width, height, menge int = result["width"], result["height"], result["menge"]
	fmt.Println("Width:", width, "Height:", height, "Menge:", menge)
	fmt.Fprintf(w, `{"width": %d, "height": %d, "menge": %d}`, width, height, menge)
}

func main() {
	fs := http.FileServer(http.Dir("static"))
	http.Handle("/", fs)
	http.HandleFunc("/upload", uploadHandler)

	log.Println("Server is running on :8080")
	log.Fatal(http.ListenAndServe("0.0.0.0:8080", nil))
}
