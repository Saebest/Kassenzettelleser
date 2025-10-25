package leser

import (
	"encoding/json"
	"fmt"
	"net/http"
)

type pytonLeser struct {
}

func (p *pytonLeser) Read() {
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
}
