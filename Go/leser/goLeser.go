package leser

import (
	"fmt"
	"log"

	"github.com/otiai10/gosseract/v2"
)

type goLeser struct {
}

func (g *goLeser) ReadKassenzettel(name string) (laden string, datum string, err error) {
	client := gosseract.NewClient()
	defer client.Close()

	// Optional: Sprache einstellen, z.B. Deutsch:
	// client.SetLanguage("deu")

	// Bilddatei setzen
	if err := client.SetImage("Aldi.jpeg"); err != nil {
		log.Fatalf("SetImage error: %v", err)
	}

	// Text auslesen
	text, err := client.Text()
	if err != nil {
		log.Fatalf("OCR error: %v", err)
	}

	fmt.Println("Erkannter Text:")
	fmt.Println(text)
}
