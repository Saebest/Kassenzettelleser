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
		fmt.Println("only POST allowed")
		http.Error(w, "Only POST allowed", http.StatusMethodNotAllowed)
		return
	}
	file, fileHeader, err := r.FormFile("file")
	if err != nil {
		fmt.Println("cant read file")
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
		fmt.Println("Python script can't read image")
		http.Error(w, "Cant read image", http.StatusInternalServerError)
		return
	}
	defer resp.Body.Close()
	var result map[string]any
	err = json.NewDecoder(resp.Body).Decode(&result)
	fmt.Println(result)
	if err != nil {
		fmt.Println("Json decode error")
		http.Error(w, "Something went wrong", http.StatusInternalServerError)
		return
	}

	laden := result["laden"].(string)
	datum := result["datum"]
	fmt.Println(laden, datum)
	fmt.Fprintf(w, `{"laden": %q, "datum": %q}`, laden, datum)
}

func main() {
	fs := http.FileServer(http.Dir("static"))
	http.Handle("/", fs)
	http.HandleFunc("/upload", uploadHandler)

	http.Handle("/favicon.ico", http.FileServer(http.Dir(".")))
	log.Println("Server is running on :8080")
	log.Fatal(http.ListenAndServe("0.0.0.0:8080", nil))
}
