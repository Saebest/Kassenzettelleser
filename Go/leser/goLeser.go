package leser

// "fmt"
// "mime/multipart"

// "github.com/otiai10/gosseract/v2"

// type GoLeser struct {
// }

// func (g *GoLeser) ReadKassenzettel(image multipart.File) (output string, err error) {
// 	client := gosseract.NewClient()
// 	client.SetLanguage("de")
// 	defer client.Close()

// 	// Read the file into memory
// 	imgBytes := make([]byte, 0)
// 	buf := make([]byte, 1024)
// 	for {
// 		n, err := image.Read(buf)
// 		if n > 0 {
// 			imgBytes = append(imgBytes, buf[:n]...)
// 		}
// 		if err != nil {
// 			break
// 		}
// 	}
// 	if err = client.SetImageFromBytes(imgBytes); err != nil {
// 		fmt.Printf("SetImage error: %v\n", err)
// 		return
// 	}

// 	// Text auslesen
// 	output, err = client.Text()
// 	if err != nil {
// 		fmt.Printf("Text Nicht lesbar: %v\n", err)
// 		return
// 	}

// 	fmt.Println("Erkannter Text:")
// 	fmt.Println(output)
// 	return
// }
