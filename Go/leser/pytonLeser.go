package leser

import (
	"encoding/json"
	"fmt"
	"io"
	"mime/multipart"
	"net/http"
)

type PythonLeser struct {
}

func (p *PythonLeser) ReadKassenzettel(image multipart.File) (output string, err error) {

	pr, pw := io.Pipe()
	wr := multipart.NewWriter(pw)
	go func() {
		p, _ := wr.CreateFormFile("file", "temp.jpg")
		io.Copy(p, image)
		wr.Close()
		pw.Close()
	}()
	req, err := http.NewRequest("POST", "http://localhost:5000/size", pr)
	req.Header.Set("Content-Type", wr.FormDataContentType())
	resp, _ := http.DefaultClient.Do(req)

	if err != nil || resp.StatusCode != http.StatusOK {
		fmt.Println("Python script can't read image")
		return
	}
	defer resp.Body.Close()
	output, err = readBody(resp.Body)
	if err != nil {
		return
	}
	fmt.Println("Received from Python service:", output)
	return
}

func readBody(body io.Reader) (out string, err error) {
	// 1. Read the body
	bodyBytes, err := io.ReadAll(body)
	if err != nil {
		return
	}

	// 2. Optional: Unmarshal into a generic map
	var data map[string]interface{}
	if err = json.Unmarshal(bodyBytes, &data); err != nil {
		return
	}

	// 3. Marshal back to pretty JSON string
	jsonStr, err := json.MarshalIndent(data, "", "  ")
	if err != nil {
		return
	}

	return string(jsonStr), nil
}
